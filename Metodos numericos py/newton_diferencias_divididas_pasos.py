import sympy
from sympy import symbols, Rational, expand, simplify
from decimal import Decimal, getcontext
import io

# Configurar precisión decimal
getcontext().prec = 50

def to_decimal(val):
    """Convierte un valor (Rational, int, etc) a Decimal para impresión."""
    if hasattr(val, "p") and hasattr(val, "q"): # Caso Sympy Rational
        return Decimal(str(val.p)) / Decimal(str(val.q))
    if hasattr(val, "numerator"): # Caso fractions.Fraction
        return Decimal(str(val.numerator)) / Decimal(str(val.denominator))
    return Decimal(str(val))

def format_val(val):
    """Formatea el valor para visualización limpia: si es entero muestra entero, si no, decimal."""
    d = to_decimal(val)
    if d == d.to_integral_value():
        return str(d.to_integral_value())
    return str(d.normalize())

def leer_entradas():
    print("==================================================")
    print("INGRESO DE DATOS")
    print("==================================================")
    try:
        n = int(input("Ingrese la cantidad de puntos (n >= 2): "))
        if n < 2:
            print("Error: Se necesitan al menos 2 puntos.")
            return None
    except ValueError:
        print("Error: Ingrese un número entero válido.")
        return None

    x_points = []
    y_points = []
    for i in range(n):
        try:
            xi = Rational(input(f"Ingrese x{i+1}: ").replace(',', '.'))
            yi = Rational(input(f"Ingrese y{i+1}: ").replace(',', '.'))
            
            if xi in x_points:
                print("Error: Los valores de xi deben ser distintos.")
                return None
            
            x_points.append(xi)
            y_points.append(yi)
        except Exception as e:
            print(f"Error en la entrada: {e}")
            return None

    try:
        x_target = Rational(input("Ingrese el valor X a interpolar: ").replace(',', '.'))
    except Exception as e:
        print(f"Error en la entrada de X: {e}")
        return None

    return n, x_points, y_points, x_target

def construir_tabla_diferencias(n, x_points, y_points):
    # Tabla[col][row]
    # col 0: y_points
    # col 1: primera diferencia, etc.
    tabla = [[Rational(0)] * (n - i) for i in range(n)]
    
    # Inicializar primera columna con y
    for i in range(n):
        tabla[0][i] = y_points[i]

    pasos_calculo = []

    for col in range(1, n):
        for row in range(n - col):
            num = tabla[col-1][row+1] - tabla[col-1][row]
            den = x_points[row+col] - x_points[row]
            res = num / den
            tabla[col][row] = res
            
            # Detalle del paso en decimal para visualización
            y_next = format_val(tabla[col-1][row+1])
            y_prev = format_val(tabla[col-1][row])
            x_next = format_val(x_points[row+col])
            x_prev = format_val(x_points[row])
            res_disp = format_val(res)
            
            expresion = f"f[{', '.join([f'x{i+1}' for i in range(row, row+col+1)])}] = ({y_next} - ({y_prev})) / ({x_next} - {x_prev})"
            pasos_calculo.append(f"{expresion} = {res_disp}")

    return tabla, pasos_calculo

def imprimir_pasos(n, x_points, y_points, x_target, tabla, pasos_calculo):
    output = io.StringIO()
    
    def log(msg):
        print(msg)
        output.write(msg + "\n")

    log("="*50)
    log("MÉTODO DE NEWTON (Diferencias Divididas)")
    reference = ", ".join([f"(x{i+1}, y{i+1}) = ({format_val(x_points[i])}, {format_val(y_points[i])})" for i in range(n)])
    log(f"Referencia de entrada: {reference}")
    log(f"Valor a interpolar: X = {format_val(x_target)}")
    log("="*50)

    log("\nPASO 1: Tabla de diferencias divididas (mostrada en decimales)")
    
    # Mostrar detalle de cálculos de diferencias
    for paso in pasos_calculo:
        log(paso)

    log("\nTabla Resumen (D0=y, D1, D2, ...):")
    for i in range(n):
        row_str = f"x{i+1}={format_val(x_points[i]):<8} | "
        for j in range(n - i):
            row_str += f"D{j}={format_val(tabla[j][i]):<15} "
        log(row_str)

    log("\n" + "="*50)
    log("PASO 2: Construcción del polinomio de Newton")
    
    x = symbols('x')
    poly_terms = []
    current_term = Rational(1)
    
    poly_expr_str = "P(x) = "
    for i in range(n):
        coef = tabla[i][0]
        term = coef * current_term
        poly_terms.append(term)
        
        coef_disp = format_val(coef)
        # Construcción de la cadena visual
        if i == 0:
            poly_expr_str += f"{coef_disp}"
        else:
            factors = "".join([f"(x - {format_val(x_points[j])})" for j in range(i)])
            poly_expr_str += f" + ({coef_disp}){factors}"
        
        current_term *= (x - x_points[i])

    log(poly_expr_str)
    
    final_poly = sum(poly_terms)
    # Mostramos el simplificado también con decimales si es posible, pero simplify tiende a usar fracciones.
    # Para presentar el polinomio final expandido "decimalmente", sustituimos coeficientes.
    log(f"\nPolinomio simplificado (fracciones): P(x) = {simplify(final_poly)}")

    log("\n" + "="*50)
    log(f"PASO 3: Sustituyendo x = {format_val(x_target)}")
    
    sust_str = f"P({format_val(x_target)}) = "
    eval_current_term = Rational(1)
    total_eval = Rational(0)
    
    for i in range(n):
        coef = tabla[i][0]
        term_val = coef * eval_current_term
        total_eval += term_val
        
        coef_disp = format_val(coef)
        x_target_disp = format_val(x_target)
        if i == 0:
            sust_str += f"{coef_disp}"
        else:
            factors_val = "*".join([f"({x_target_disp} - {format_val(x_points[j])})" for j in range(i)])
            sust_str += f" + ({coef_disp})*({factors_val})"
        
        eval_current_term *= (x_target - x_points[i])

    log(sust_str)
    log(f"= {format_val(total_eval)}")

    log("\n" + "="*50)
    log("RESULTADO FINAL:")
    
    # Cálculo decimal final con alta precisión
    res_num, res_den = total_eval.as_numer_denom()
    res_decimal = Decimal(str(res_num)) / Decimal(str(res_den))
    
    log(f"Resultado exacto (fracción): {total_eval}")
    log(f"Resultado decimal (10 decimales): {res_decimal:.10f}")
    log("="*50)

    return output.getvalue()

def main():
    data = leer_entradas()
    if not data:
        return

    n, x_points, y_points, x_target = data
    tabla, pasos_calculo = construir_tabla_diferencias(n, x_points, y_points)
    
    full_log = imprimir_pasos(n, x_points, y_points, x_target, tabla, pasos_calculo)

    save = input("\n¿Desea guardar los pasos en 'pasos_newton.txt'? (s/n): ").lower()
    if save == 's':
        with open("pasos_newton.txt", "w", encoding="utf-8") as f:
            f.write(full_log)
        print("Archivo guardado con éxito.")

if __name__ == "__main__":
    main()

# Ejemplo de prueba sugerido:
# x = 7.3, 6.5, 6.1
# y = -0.28, -1.35, -1.82
# X = 7

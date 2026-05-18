import sympy
from sympy import symbols, Rational, simplify
from decimal import Decimal, getcontext

# Configurar la precisión decimal según los requisitos
getcontext().prec = 30

def format_equation_block(y_points, x_points, var_sym, substituted_val=None):
    """
    Construye la cadena de texto de la ecuación con valores sustituidos.
    Si substituted_val se proporciona, sustituye 'x' por ese valor.
    """
    n = len(y_points)
    blocks = []
    
    for i in range(n):
        numerator_factors = []
        denominator_factors = []
        
        for j in range(n):
            if i == j:
                continue
            
            # Convertir a float solo para visualización
            x_j = float(x_points[j])
            x_i = float(x_points[i])
            
            if substituted_val is not None:
                x_target_disp = float(substituted_val)
                numerator_factors.append(f"({x_target_disp} - {x_j})")
            else:
                numerator_factors.append(f"(x - {x_j})")
            
            denominator_factors.append(f"({x_i} - {x_j})")
        
        # y_i también como decimal para visualización
        y_i = float(y_points[i])
        block = f"{y_i}({''.join(numerator_factors)}) / ({''.join(denominator_factors)})"
        blocks.append(block)
    
    separator = "\n+ "
    return separator.join(blocks)

def lagrange_interpolation():
    print("\n---")
    print("MÉTODO DE INTERPOLACIÓN DE LAGRANGE")
    print("\nFórmula general:")
    print("g(x) = Σ yi * Π((x - xj)/(xi - xj))")
    print("---")

    # 1. Entrada de datos
    try:
        n_input = input("Ingrese la cantidad de puntos: ")
        if not n_input:
            return
        n = int(n_input)
        if n < 2:
            print("Se necesitan al menos 2 puntos.")
            return
    except ValueError:
        print("Error: Debe ingresar un número entero.")
        return

    x_points = []
    y_points = []

    for i in range(n):
        try:
            xi_raw = input(f"Ingrese x{i+1}: ").replace(',', '.')
            yi_raw = input(f"Ingrese y{i+1}: ").replace(',', '.')
            
            x_points.append(Rational(xi_raw))
            y_points.append(Rational(yi_raw))
        except Exception as e:
            print(f"Error al ingresar los puntos: {e}")
            return

    try:
        x_target_raw = input("Ingrese el valor X a interpolar: ").replace(',', '.')
        x_target = Rational(x_target_raw)
    except Exception as e:
        print(f"Error al ingresar X: {e}")
        return

    # Símbolo para g(x)
    x = symbols('x')

    # 2. Mostrar ecuación con valores sustituidos (simbólica)
    print("\nEcuación con valores sustituidos:")
    print("g(x) =")
    print(format_equation_block(y_points, x_points, x))
    print("---")

    # 3. Mostrar ecuación evaluada en X
    print(f"\nSustituyendo x = {x_target}:")
    print(f"g({x_target}) =")
    print(format_equation_block(y_points, x_points, x, substituted_val=x_target))
    print("---")

    # 4. Cálculo final (usando Rational para exactitud)
    poly = 0
    for i in range(n):
        li = 1
        for j in range(n):
            if i == j:
                continue
            li *= (x - x_points[j]) / (x_points[i] - x_points[j])
        poly += y_points[i] * li

    result_exact = poly.subs(x, x_target)
    
    # 5. Resultado decimal de alta precisión
    num, den = result_exact.as_numer_denom()
    res_decimal = Decimal(str(num)) / Decimal(str(den))

    print("\nResultado exacto:")
    print(result_exact)
    
    print("\nResultado decimal:")
    # Formato con 10 dígitos después del punto
    print(f"{res_decimal:.10f}")
    print("---\n")

if __name__ == "__main__":
    lagrange_interpolation()

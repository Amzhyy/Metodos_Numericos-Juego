import sympy as sp

def evaluar_con_sustitucion(expr, x_var, x_val):
    """
    Crea una cadena que muestra la sustitución de x_val en la expresión expr.
    """
    # Formatear el valor con 10 decimales
    val_str = f"({x_val:.10f})"
    
    # Crear un símbolo temporal con el nombre del valor formateado
    # Esto permite que sp.subs mantenga la estructura de la expresión
    val_sym = sp.Symbol(val_str)
    
    # Sustituir
    expr_sub = expr.subs(x_var, val_sym)
    
    # Convertir a cadena y limpiar posibles signos duplicados
    sub_str = str(expr_sub).replace("-+", "-").replace("+-", "-").replace("++", "+").replace("--", "+")
    return sub_str

def metodo_newton_raphson(f_str, x0, tol=1e-6, max_iter=100):
    """
    Implementa el método de Newton-Raphson con pasos detallados.
    """
    x = sp.symbols('x')
    try:
        f_expr = sp.sympify(f_str)
        df_expr = sp.diff(f_expr, x)
    except Exception as e:
        print(f"Error al procesar la función: {e}")
        return

    print(f"\n--- Método de Newton-Raphson ---")
    print(f"f(x)  = {f_expr}")
    print(f"f'(x) = {df_expr}")
    print(f"x0    = {x0:.10f}")
    print("-" * 40)

    xi = float(x0)
    resultados = []

    for i in range(1, max_iter + 1):
        print(f"\nIteración {i}")
        print(f"xi = {xi:.10f}")

        # Valores numéricos
        f_val = float(f_expr.subs(x, xi))
        df_val = float(df_expr.subs(x, xi))

        if df_val == 0:
            print("Error: La derivada es cero. El método no puede continuar.")
            break

        # Cadenas de sustitución para mostrar pasos
        f_sub_str = evaluar_con_sustitucion(f_expr, x, xi)
        df_sub_str = evaluar_con_sustitucion(df_expr, x, xi)

        print("\nSustitución en la fórmula:")
        print(f"xi+1 = xi - ( f(xi) / f'(xi) )")
        
        print("\nMostrando la sustitución real:")
        print(f"x{i} = {xi:.10f} - ( ({f_sub_str}) / ({df_sub_str}) )")

        # Cálculo de xi+1
        xi_next = xi - (f_val / df_val)
        error = abs(xi_next - xi)

        print("\nResultado:")
        print(f"x{i} = {xi_next:.10f}")

        print("\nError:")
        print(f"ε = |x{i} - x{i-1}|")
        print(f"ε = {error:.10f}")
        print("-" * 30)

        # Guardar para la tabla
        resultados.append((i, xi, xi_next, error))

        # Actualizar xi
        xi_prev = xi
        xi = xi_next

        # Criterio de paro
        if error < tol:
            break

    # Tabla resumida
    print("\nTabla Resumida:")
    print(f"{'i':<3} | {'xi':<15} | {'xi+1':<15} | {'ε':<15}")
    print("-" * 55)
    # Fila inicial opcional para mostrar x0, pero el requerimiento i | xi | xi+1 | ε 
    # suele empezar desde la primera iteración calculada.
    for res in resultados:
        idx, x_curr, x_nxt, err = res
        print(f"{idx:<3} | {x_curr:<15.10f} | {x_nxt:<15.10f} | {err:<15.10f}")
    
    print("-" * 55)
    print(f"\nResultado aproximado de la raíz: {xi:.10f}")
    print(f"Número de iteraciones: {len(resultados)}")
    print(f"Error final: {error:.10f}")

def main():
    print("--- Método de Newton-Raphson (Pasos Detallados) ---")
    try:
        f_input = input("Ingrese la función f(x) (ej. x**3 + 2*x**2 + 10*x - 20): ")
        x0_input = float(input("Ingrese el valor inicial x0: "))
        
        metodo_newton_raphson(f_input, x0_input)
        
    except ValueError:
        print("Error: Por favor ingrese un valor numérico válido para x0.")
    except Exception as e:
        print(f"Ocurrió un error inesperado: {e}")

if __name__ == "__main__":
    main()

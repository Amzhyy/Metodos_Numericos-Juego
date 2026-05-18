import sympy as sp

def evaluar_funcion(g_expr, x_var, x_val):
    """
    Evalua una expresión de sympy en un valor dado.
    """
    return float(g_expr.subs(x_var, x_val))

def metodo_punto_fijo(g_str, x0, tol=1e-6, max_iter=100):
    """
    Implementa el método de Punto Fijo y muestra una tabla de resultados.
    
    Argumentos:
    g_str -- La función g(x) como cadena (ej. 'exp(-x)')
    x0 -- Valor inicial para la iteración
    tol -- Tolerancia para el criterio de paro (default 1e-6)
    max_iter -- Número máximo de iteraciones (default 100)
    """
    # Definir la variable simbólica y parsear la expresión
    x = sp.symbols('x')
    try:
        g_expr = sp.sympify(g_str)
    except Exception as e:
        print(f"Error al procesar la función: {e}")
        return

    # Encabezado de la tabla
    print(f"\nIteraciones para g(x) = {g_str} con x0 = {x0:.10f}")
    print(f"{'i':<3} | {'g(xi)':<45} | {'xi':<15} | {'ε':<15}")
    print("-" * 85)

    xi = float(x0)
    
    # Iteración 0
    # En i=0: xi es x0, g(xi) no se muestra (-), ε no se muestra (-)
    print(f"{0:<3} | {'-':<45} | {xi:<15.10f} | {'-':<15}")

    for i in range(1, max_iter + 1):
        # Evaluación de g(xi_anterior)
        # Preparar la cadena de sustitución con 10 decimales y signos explícitos
        xi_str_formatted = f"{xi:+.10f}"
        val_sym = sp.Symbol(xi_str_formatted)
        sub_expr_raw = g_expr.subs(x, val_sym)
        
        # Limpiar signos duplicados (ej. -+ -> -)
        sub_str = str(sub_expr_raw).replace("-+", "-").replace("+-", "-").replace("++", "+").replace("--", "+")
        
        # Resultado numérico
        g_xi_prev = evaluar_funcion(g_expr, x, xi)
        
        # Formato de la columna g(xi): "sustitucion = resultado"
        g_xi_col = f"{sub_str} = {g_xi_prev:.10f}"
        
        # Fórmula iterativa: xi+1 = g(xi)
        xi_next = g_xi_prev
        
        # Cálculo del error: ε = |xi+1 - xi|
        error = abs(xi_next - xi)
        
        # Mostrar fila de la tabla
        print(f"{i:<3} | {g_xi_col:<45} | {xi_next:<15.10f} | {error:<15.10f}")
        
        # Actualizar xi para la siguiente iteración
        xi = xi_next

        # Criterio de paro: ε < tolerancia
        if error < tol:
            print("-" * 85)
            print(f"\nConvergió en {i} iteraciones.")
            print(f"Resultado aproximado de la raíz: {xi:.10f}")
            print(f"Número total de iteraciones: {i}")
            print(f"Error final: {error:.10f}")
            return xi, i, error

    print("-" * 85)
    print(f"\nSe alcanzó el máximo de {max_iter} iteraciones sin converger.")
    print(f"Último valor aproximado: {xi:.10f}")
    return xi, max_iter, error

def main():
    print("--- Método de Punto Fijo (Iteración Simple) ---")
    
    try:
        g_input = input("Ingrese la función g(x) (ej. exp(-x)): ")
        x0_input = float(input("Ingrese el valor inicial x0: "))
        
        metodo_punto_fijo(g_input, x0_input)
        
    except ValueError:
        print("Error: Por favor ingrese un valor numérico válido para x0.")
    except Exception as e:
        print(f"Ocurrió un error inesperado: {e}")

if __name__ == "__main__":
    main()

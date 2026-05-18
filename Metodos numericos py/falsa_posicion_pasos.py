import sympy as sp
import re

def preprocesar_funcion(f_str):
    """
    Convierte expresiones matemáticas naturales (ej. 3x) a formato Python (3*x).
    """
    # Agregar * entre números y letras (ej. 3x -> 3*x)
    f_str = re.sub(r'(\d)([a-zA-Z])', r'\1*\2', f_str)
    return f_str

def evaluar(f_expr, x_var, x_val):
    """
    Evalúa la expresión f_expr en x_val usando sympy.
    """
    return float(f_expr.subs(x_var, x_val))

def metodo_falsa_posicion():
    print("--- Método de Falsa Posición (Regula Falsi) ---")
    
    f_input = input("Ingrese la función f(x) (ej. 3x**3 - 2x - 3): ")
    f_str = preprocesar_funcion(f_input)
    
    try:
        a = float(input("Ingrese el extremo izquierdo a: "))
        b = float(input("Ingrese el extremo derecho b: "))
    except ValueError:
        print("Error: Ingrese valores numéricos para a y b.")
        return

    x_var = sp.symbols('x')
    try:
        f_expr = sp.sympify(f_str)
    except Exception as e:
        print(f"Error al procesar la función: {e}")
        return

    fa = evaluar(f_expr, x_var, a)
    fb = evaluar(f_expr, x_var, b)

    if fa * fb >= 0:
        print(f"\nError: f(a) y f(b) tienen el mismo signo.")
        print(f"f({a:.10f}) = {fa:.10f}")
        print(f"f({b:.10f}) = {fb:.10f}")
        return

    # Parámetros del método
    tol = 0.001
    max_iter = 100
    x_prev = None
    
    # Encabezado de la tabla
    header = f"{'i':<3} | {'b':<12} | {'f(b)':<12} | {'a':<12} | {'x':<12} | {'f(a)':<12} | {'ε':<12}"
    separator = "-" * len(header)
    
    print("\nTabla de Iteraciones:")
    print(header)
    print(separator)

    # Iteración 0 (Estado inicial)
    print(f"{0:<3} | {b:<12.10f} | {fb:<12.10f} | {a:<12.10f} | {'-':<12} | {fa:<12.10f} | {'-':<12}")

    for i in range(1, max_iter + 1):
        fa = evaluar(f_expr, x_var, a)
        fb = evaluar(f_expr, x_var, b)
        
        # Fórmula: x = a - fa*(b-a)/(fb-fa)
        x_curr = a - (fa * (b - a)) / (fb - fa)
        fx = evaluar(f_expr, x_var, x_curr)
        
        # Error: ε = |xi+1 - xi|
        if x_prev is None:
            err_display = "-"
            error = None
        else:
            error = abs(x_curr - x_prev)
            err_display = f"{error:.10f}"

        # Imprimir fila de la tabla
        print(f"{i:<3} | {b:<12.10f} | {fb:<12.10f} | {a:<12.10f} | {x_curr:<12.10f} | {fa:<12.10f} | {err_display:<12}")

        # Criterio de paro
        if error is not None and error <= tol:
            break

        # Actualizar intervalo y x_prev para la siguiente iteración
        x_prev = x_curr
        if fa * fx < 0:
            b = x_curr # Reemplaza b
        else:
            a = x_curr # Reemplaza a

    print(separator)
    print(f"\nRaíz aproximada: {x_curr:.10f}")
    print(f"Error final: {err_display}")
    print(f"Número de iteraciones: {i}")

if __name__ == "__main__":
    metodo_falsa_posicion()

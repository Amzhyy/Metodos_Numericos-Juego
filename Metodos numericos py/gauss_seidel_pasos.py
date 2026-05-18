def formatear_valor(val):
    """
    Formatea un valor numérico a 10 decimales.
    """
    return f"{val:.10f}"

def formatear_sustitucion(val):
    """
    Formatea un valor para sustitución en fórmulas, agregando paréntesis si es negativo.
    """
    res = f"{val:.10f}"
    if val < 0:
        return f"({res})"
    return res

def obtener_valor(label):
    """
    Pide un valor al usuario y lo convierte a float.
    """
    while True:
        try:
            return float(input(f"Ingrese {label}: "))
        except ValueError:
            print("Error: Ingrese un valor numérico válido.")

def formatear_termino(coef, var_name, is_first=False):
    """
    Formatea un término de una ecuación (ej. -0.1b).
    """
    if coef == 0:
        return ""
    
    signo = ""
    if is_first:
        if coef < 0:
            signo = "-"
    else:
        signo = "+" if coef > 0 else "-"
        
    abs_coef = abs(coef)
    if abs_coef == 1:
        return f" {signo} {var_name}"
    else:
        # Usar f"{abs_coef:g}" para evitar decimales innecesarios en la visualización del sistema
        return f" {signo} {abs_coef:g}{var_name}"

def metodo_gauss_seidel():
    print("--- Método de Gauss-Seidel (Pasos Detallados) ---")
    print("Sistema de ecuaciones 3x3:")
    print("a11*a + a12*b + a13*c = b1")
    print("a21*a + a22*b + a23*c = b2")
    print("a31*a + a32*b + a33*c = b3\n")
    
    # Lectura de datos
    a11 = obtener_valor("a11")
    a12 = obtener_valor("a12")
    a13 = obtener_valor("a13")
    b1  = obtener_valor("b1")
    print("")
    
    a21 = obtener_valor("a21")
    a22 = obtener_valor("a22")
    a23 = obtener_valor("a23")
    b2  = obtener_valor("b2")
    print("")
    
    a31 = obtener_valor("a31")
    a32 = obtener_valor("a32")
    a33 = obtener_valor("a33")
    b3  = obtener_valor("b3")
    
    # Mostrar sistema ingresado
    print("\nSistema original:")
    eq1 = f"{a11:g}a" + formatear_termino(a12, "b") + formatear_termino(a13, "c") + f" = {b1:g}"
    eq2 = f"{a21:g}a" + formatear_termino(a22, "b") + formatear_termino(a23, "c") + f" = {b2:g}"
    eq3 = f"{a31:g}a" + formatear_termino(a32, "b") + formatear_termino(a33, "c") + f" = {b3:g}"
    print(eq1)
    print(eq2)
    print(eq3)
    
    # Mostrar ecuaciones despejadas
    print("\nEcuaciones despejadas:")
    # a = (b1 - a12b - a13c) / a11
    # b = (b2 - a21a - a23c) / a22
    # c = (b3 - a31a - a32b) / a33
    
    def fmt_cleared(b_val, c1_val, var1, c2_val, var2, div_val):
        term1 = f"{-c1_val:g}{var1}" if c1_val != 0 else ""
        if term1 and term1[0] != '-': term1 = "+" + term1
        
        term2 = f"{-c2_val:g}{var2}" if c2_val != 0 else ""
        if term2 and term2[0] != '-': term2 = "+" + term2
        
        return f"({b_val:g} {term1} {term2}) / {div_val:g}"

    print(f"a = " + fmt_cleared(b1, a12, "b", a13, "c", a11))
    print(f"b = " + fmt_cleared(b2, a21, "a", a23, "c", a22))
    print(f"c = " + fmt_cleared(b3, a31, "a", a32, "b", a33))
    
    # Inicialización
    a = 0.0
    b = 0.0
    c = 0.0
    
    tol = 0.001
    max_iter = 100
    
    # Guardar resultados para la tabla
    tabla_resultados = [(0, a, b, c)]
    
    print("\nIteración 0")
    print(f"a0 = {a}")
    print(f"b0 = {b}")
    print(f"c0 = {c}")
    print("-" * 50)

    for i in range(1, max_iter + 1):
        a_old, b_old, c_old = a, b, c
        
        print(f"\nIteración {i}")
        
        def fmt_sub_term(coef):
            # Mostramos el término como "+ (-coef)" para que coincida con el estilo del usuario:
            # (b1 - a12(b)) -> (7.85 - (-0.1)(0)) -> (7.85 + 0.1(0))
            val = -coef
            signo = "+" if val >= 0 else "-"
            return f"{signo} {abs(val):g}"

        # Cálculo de a
        # a = (b1 - a12*b - a13*c) / a11
        b_s = formatear_sustitucion(b)
        c_s = formatear_sustitucion(c)
        if b >= 0: b_s = f"({b:.10f})"
        if c >= 0: c_s = f"({c:.10f})"
        
        print(f"a{i} = ({b1:g} {fmt_sub_term(a12)}{b_s} {fmt_sub_term(a13)}{c_s}) / {a11:g}")
        a = (b1 - a12 * b - a13 * c) / a11
        print(f"a{i} = {a:.10f}")
        
        # Cálculo de b
        # b = (b2 - a21*a - a23*c) / a22
        a_s = formatear_sustitucion(a)
        c_s = formatear_sustitucion(c)
        if a >= 0: a_s = f"({a:.10f})"
        if c >= 0: c_s = f"({c:.10f})"
        
        print(f"\nb{i} = ({b2:g} {fmt_sub_term(a21)}{a_s} {fmt_sub_term(a23)}{c_s}) / {a22:g}")
        b = (b2 - a21 * a - a23 * c) / a22
        print(f"b{i} = {b:.10f}")
        
        # Cálculo de c
        # c = (b3 - a31*a - a32*b) / a33
        a_s = formatear_sustitucion(a)
        b_s = formatear_sustitucion(b)
        if a >= 0: a_s = f"({a:.10f})"
        if b >= 0: b_s = f"({b:.10f})"
        
        print(f"\nc{i} = ({b3:g} {fmt_sub_term(a31)}{a_s} {fmt_sub_term(a32)}{b_s}) / {a33:g}")
        c = (b3 - a31 * a - a32 * b) / a33
        print(f"c{i} = {c:.10f}")
        
        # Cálculo de errores
        ea = abs(a - a_old)
        eb = abs(b - b_old)
        ec = abs(c - c_old)
        
        # Guardar en tabla
        tabla_resultados.append((i, a, b, c))
        
        print("-" * 50)
        
        # Criterio de paro
        if max(ea, eb, ec) <= tol:
            print(f"\nCriterio de paro alcanzado: max(εa, εb, εc) <= {tol}")
            break

    # Mostrar Tabla Resumen
    print("\nTabla Resumen:")
    print(f"{'i':<3} | {'a':<15} | {'b':<15} | {'c':<15}")
    print("-" * 55)
    for res in tabla_resultados:
        idx, va, vb, vc = res
        print(f"{idx:<3} | {va:<15.10f} | {vb:<15.10f} | {vc:<15.10f}")
    print("-" * 55)
    
    print(f"\nSolución aproximada:")
    print(f"a = {a:.10f}")
    print(f"b = {b:.10f}")
    print(f"c = {c:.10f}")
    print(f"\nNúmero de iteraciones: {i}")
    print(f"Errores finales:")
    print(f"εa = {ea:.10f}")
    print(f"εb = {eb:.10f}")
    print(f"εc = {ec:.10f}")

if __name__ == "__main__":
    metodo_gauss_seidel()

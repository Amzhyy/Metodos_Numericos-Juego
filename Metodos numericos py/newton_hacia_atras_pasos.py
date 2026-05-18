from fractions import Fraction
from decimal import Decimal, getcontext


def parse_fraction(prompt: str) -> Fraction:
    """
    Lee una entrada del usuario e intenta convertirla en Fraction
    aceptando formatos como:
    - 1.25
    - 3/4
    """
    while True:
        raw = input(prompt).strip()
        try:
            # Fraction maneja tanto 'a/b' como decimales en cadena
            value = Fraction(raw)
            return value
        except Exception:
            print("Entrada no válida. Intente de nuevo (use números como 1.25 o 3/4).")


def main() -> None:
    getcontext().prec = 50  # alta precisión para el resultado decimal

    pasos: list[str] = []

    def log(line: str = "") -> None:
        print(line)
        pasos.append(line)

    log("---")
    log("## MÉTODO DE NEWTON HACIA ATRÁS")
    log("---")

    # ========================
    # Entrada de datos
    # ========================
    while True:
        try:
            n_raw = input("Ingrese el número de puntos n (n >= 2): ").strip()
            n = int(n_raw)
            if n < 2:
                print("n debe ser al menos 2.")
                continue
            break
        except ValueError:
            print("Valor de n no válido. Intente de nuevo.")

    x_vals: list[Fraction] = []
    y_vals: list[Fraction] = []

    log("\nIngreso de puntos (xi, yi):")
    for i in range(n):
        idx = i + 1
        xi = parse_fraction(f"  Ingrese x{idx}: ")
        yi = parse_fraction(f"  Ingrese y{idx}: ")
        x_vals.append(xi)
        y_vals.append(yi)

    X = parse_fraction("\nIngrese el valor X a interpolar: ")

    # ========================
    # PASO 1: Verificación de h
    # ========================
    log("\nPASO 1: Verificación del intervalo uniforme h")
    log("Calculamos h = |x_{i+1} − x_i| para cada par consecutivo:")

    if n < 2:
        log("Se requieren al menos 2 puntos.")
        return

    diffs_h = []
    monotone_sign = None
    for i in range(n - 1):
        dx = x_vals[i + 1] - x_vals[i]
        if dx == 0:
            log(f"  Los puntos x{i+1} y x{i+2} son iguales; el método no es aplicable.")
            return
        sign = 1 if dx > 0 else -1
        if monotone_sign is None:
            monotone_sign = sign
        elif sign != monotone_sign:
            log("  Los valores xi no son monótonos. "
                "El método de Newton hacia atrás requiere puntos ordenados.")
            return

        h_i = abs(dx)
        diffs_h.append(h_i)
        log(
            f"  h{i+1} = |x{i+2} − x{i+1}| = |{x_vals[i+1]} − {x_vals[i]}| = {h_i}"
        )

    h = diffs_h[0]
    uniforme = all(d == h for d in diffs_h)

    if uniforme:
        log(f"\nTodos los intervalos son iguales: h = {h}")
    else:
        log("\nAl menos un intervalo es diferente:")
        for i, d in enumerate(diffs_h, start=1):
            log(f"  h{i} = {d}")
        log("\nEl método de Newton hacia atrás requiere intervalos uniformes.")
        return

    # ========================
    # PASO 2: Tabla de diferencias hacia atrás
    # ========================
    log("\nPASO 2: Tabla de diferencias hacia atrás (∇)")

    # diffs[k][i] = ∇^k f(x_i), con k=0 siendo los valores de y
    diffs: list[list[Fraction]] = []
    diffs.append(list(y_vals))  # orden 0

    # Cálculo y muestra de cada diferencia hacia atrás
    for k in range(1, n):
        prev = diffs[k - 1]
        current: list[Fraction] = [Fraction(0)] * n
        log(f"\nDiferencias de orden {k}:")
        for i in range(k, n):
            if k == 1:
                # ∇f(x_i) = y_i − y_{i-1}
                expr_name = f"∇f(x{i+1})"
                left_name_1 = f"y{i+1}"
                left_name_2 = f"y{i}"
            else:
                expr_name = f"∇^{k}f(x{i+1})"
                left_name_1 = f"∇^{k-1}f(x{i+1})"
                left_name_2 = f"∇^{k-1}f(x{i})"

            value = prev[i] - prev[i - 1]
            current[i] = value

            if k == 1:
                log(
                    f"  {expr_name} = {left_name_1} − {left_name_2} "
                    f"= {prev[i]} − {prev[i-1]} = {value}"
                )
            else:
                log(
                    f"  {expr_name} = {left_name_1} − {left_name_2} "
                    f"= {prev[i]} − {prev[i-1]} = {value}"
                )

        diffs.append(current)

    # Mostrar tabla completa
    log("\nTabla completa de diferencias hacia atrás:")
    # Encabezados
    headers = ["i", "xi", "yi"]
    for k in range(1, n):
        if k == 1:
            headers.append("∇y")
        else:
            headers.append(f"∇^{k}y")
    log("  ".join(f"{h:>12}" for h in headers))

    for i in range(n):
        row: list[str] = []
        row.append(f"{i+1}")
        row.append(str(x_vals[i]))
        row.append(str(diffs[0][i]))
        for k in range(1, n):
            val = diffs[k][i]
            if i >= k:
                row.append(str(val))
            else:
                row.append("")
        log("  ".join(f"{col:>12}" for col in row))

    # ========================
    # PASO 3: Cálculo del parámetro s
    # ========================
    log("\nPASO 3: Cálculo del parámetro s")
    x_n = x_vals[-1]
    y_n = diffs[0][-1]
    log(f"Tomamos como referencia el último punto: x_n = x{n} = {x_n}")
    log("Definición: s = (x − x_n) / h")
    log(f"Usando x = {X}, x_n = {x_n} y h = {h}:")
    s = (X - x_n) / h
    log(f"  s = ({X} − {x_n}) / {h} = {s}")

    # ========================
    # PASO 4: Construcción del polinomio
    # ========================
    log("\nPASO 4: Construcción del polinomio de Newton hacia atrás")

    log("Forma general del polinomio usando el último punto (x_n, y_n):")
    log("  g(x) = y_n")
    if n >= 2:
        log("         + s ∇f(x_n)")
    if n >= 3:
        log("         + s(s+1)/2! ∇²f(x_n)")
    for k in range(3, n):
        log(
            f"         + s(s+1)...(s+{k-1})/{k}! ∇^{k}f(x_n)"
        )

    log("\nSustituyendo los valores de la última fila de la tabla:")
    log(f"  y_n = y{n} = {y_n}")
    for k in range(1, n):
        delta_kn = diffs[k][n - 1]
        if k == 1:
            log(f"  ∇f(x_n)   = ∇f(x{n})   = {delta_kn}")
        else:
            log(f"  ∇^{k}f(x_n) = ∇^{k}f(x{n}) = {delta_kn}")

    log("\nPor lo tanto:")
    poly_str_parts = [f"{y_n}"]
    for k in range(1, n):
        delta_kn = diffs[k][n - 1]
        if k == 1:
            term_str = f"s·({delta_kn})"
        elif k == 2:
            term_str = f"s(s+1)/2!·({delta_kn})"
        else:
            term_str = f"s(s+1)...(s+{k-1})/{k}!·({delta_kn})"
        poly_str_parts.append(term_str)
    log("  g(x) = " + " + ".join(poly_str_parts))

    # ========================
    # PASO 5: Sustitución de x (s numérico)
    # ========================
    log("\nPASO 5: Sustitución del valor X en el polinomio")
    log(f"Usamos s = {s} obtenido para X = {X}:")

    # Evaluación numérica del polinomio en X
    valor = y_n
    log(f"  Término de orden 0: y_n = {y_n}")

    # term_factor contendrá el producto s(s+1)...(s+k-1)
    term_factor = Fraction(1, 1)
    from math import factorial

    for k in range(1, n):
        term_factor *= (s + (k - 1))  # producto incremental
        coef = term_factor / factorial(k)
        delta_kn = diffs[k][n - 1]
        termino = coef * delta_kn
        valor += termino

        # Construcción de la parte simbólica para mostrar
        if k == 1:
            simb_prod = f"s"
        elif k == 2:
            simb_prod = "s(s+1)"
        else:
            simb_prod = "s(s+1)...(s+{k-1})"

        log(f"\n  Término de orden {k}:")
        if k == 1:
            log(f"    s ∇f(x_n)")
        elif k == 2:
            log(f"    s(s+1)/2! ∇²f(x_n)")
        else:
            log(f"    {simb_prod}/{k}! ∇^{k}f(x_n)")

        log(f"    = ({term_factor})/{factorial(k)} · ({delta_kn})")
        log(f"    = {coef} · ({delta_kn}) = {termino}")
        log(f"    Suma parcial g({X}) = {valor}")

    # ========================
    # PASO 6: Resultado final
    # ========================
    log("\nPASO 6: Resultado final")
    log(f"Resultado exacto (fracción): g({X}) = {valor}")

    # Conversión a decimal de alta precisión
    decimal_val = Decimal(valor.numerator) / Decimal(valor.denominator)
    log(f"Resultado decimal con alta precisión (50 dígitos de contexto):")
    log(f"  g({X}) ≈ {decimal_val}")
    log(f"\nResultado decimal con 10 dígitos después del punto:")
    log(f"  g({X}) ≈ {decimal_val:.10f}")

    # ========================
    # Opción de guardar pasos
    # ========================
    choice = input("\n¿Desea guardar todos los pasos en 'pasos_newton_atras.txt'? (s/n): ").strip().lower()
    if choice == "s":
        filename = "pasos_newton_atras.txt"
        try:
            with open(filename, "w", encoding="utf-8") as f:
                f.write("\n".join(pasos))
            print(f"Pasos guardados correctamente en '{filename}'.")
        except OSError as e:
            print(f"No se pudieron guardar los pasos: {e}")


if __name__ == "__main__":
    main()


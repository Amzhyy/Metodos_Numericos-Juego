from decimal import Decimal, getcontext, InvalidOperation
import sys
from typing import Callable


def fmt_decimal(value: Decimal, ndigits: int | None = None) -> str:
    """
    Convierte un Decimal a cadena decimal para mostrar,
    sin usar float y con opción de fijar decimales.
    """
    if not isinstance(value, Decimal):
        value = Decimal(str(value))

    if ndigits is None:
        ndigits = 10
    return f"{value:.{ndigits}f}"

    s = format(value, "f")
    if "." in s:
        s = s.rstrip("0").rstrip(".")
    return s or "0"



def parse_decimal(prompt: str) -> Decimal:
    """
    Lee un número desde consola y lo convierte a Decimal.
    """
    while True:
        raw = input(prompt).strip()
        try:
            return Decimal(raw)
        except InvalidOperation:
            print("Entrada no válida. Intente de nuevo (use números como 1.25 o 3/4 o 1e-3).")


def build_function(expr: str) -> Callable[[Decimal], Decimal]:
    """
    Construye f(x) a partir de una cadena de expresión.
    Soporta, por ejemplo: exp(-x) - x
    usando Decimal con alta precisión.
    """

    def f(x: Decimal) -> Decimal:
        local_env = {
            "x": x,
            "exp": (lambda v: v.exp()),
            "Decimal": Decimal,
            # Constante e (por si el usuario la usa)
            "e": Decimal(1).exp(),
            "E": Decimal(1).exp(),
        }
        try:
            # Sin builtins para mayor seguridad
            val = eval(expr, {"__builtins__": {}}, local_env)
        except Exception as exc:  # noqa: BLE001
            raise ValueError(f"No se pudo evaluar f(x). Revise la expresión. Detalle: {exc}") from exc

        if not isinstance(val, Decimal):
            # Intentamos convertir el resultado a Decimal si no lo es ya
            try:
                val = Decimal(str(val))
            except InvalidOperation as exc:  # noqa: BLE001
                raise ValueError("La expresión no produce un valor numérico válido.") from exc
        return val

    return f


def main() -> None:
    # Evitar problemas de codificación en Windows
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:  # noqa: BLE001
        pass

    getcontext().prec = 50  # alta precisión

    pasos: list[str] = []

    def log(line: str = "") -> None:
        print(line)
        pasos.append(line)

    log("---")
    log("## MÉTODO DE LA SECANTE")
    log("---")

    # ========================
    # Entrada de datos
    # ========================
    expr = input("Ingrese la función f(x) (por ejemplo: exp(-x) - x): ").strip()

    x0 = parse_decimal("Ingrese el valor inicial x0: ")
    x1 = parse_decimal("Ingrese el valor inicial x1: ")
    eps = parse_decimal("Ingrese la tolerancia de error ε: ")

    while True:
        raw_nmax = input("Ingrese el número máximo de iteraciones: ").strip()
        try:
            nmax = int(raw_nmax)
            if nmax <= 0:
                print("El número máximo de iteraciones debe ser positivo.")
                continue
            break
        except ValueError:
            print("Valor no válido. Intente de nuevo.")

    f = build_function(expr)

    # ========================
    # PASO 1: Valores iniciales
    # ========================
    log("\nPASO 1: Valores iniciales")
    log(f"  f(x) = {expr}")
    log(f"  x0 = {fmt_decimal(x0)}")
    log(f"  x1 = {fmt_decimal(x1)}")
    log(f"  ε  = {fmt_decimal(eps)}")
    log(f"  Número máximo de iteraciones = {nmax}")

    # ========================
    # PASO 2: Evaluación de la función
    # ========================
    log("\nPASO 2: Evaluación de la función en los valores iniciales")

    try:
        f0 = f(x0)
        f1 = f(x1)
    except ValueError as exc:
        log(str(exc))
        return

    log(f"  f(x0) = f({fmt_decimal(x0)}) = {fmt_decimal(f0)}")
    log(f"  f(x1) = f({fmt_decimal(x1)}) = {fmt_decimal(f1)}")

    # ========================
    # PASO 3: Fórmula de la secante
    # ========================
    log("\nPASO 3: Aplicación de la fórmula de la Secante")
    log("Fórmula general:")
    log("  x_{i+1} = x_i − f(x_i)(x_i − x_{i−1}) / (f(x_i) − f(x_{i−1}))")

    # ========================
    # PASO 4: Iteraciones
    # ========================
    log("\nPASO 4: Iteraciones del método de la Secante")

    # Tabla para las iteraciones
    iter_rows: list[tuple[int, Decimal, Decimal, Decimal | None]] = []

    # Fila inicial para i = 0 y i = 1
    error01 = abs(x1 - x0)
    iter_rows.append((0, x0, f0, None))
    iter_rows.append((1, x1, f1, error01))

    # Iteraciones
    x_prev = x0
    x_curr = x1
    f_prev = f0
    f_curr = f1
    root: Decimal | None = None
    last_error: Decimal | None = None

    for it in range(1, nmax + 1):
        idx_new = it + 1
        idx_curr = it
        idx_prev = it - 1

        log(f"\nIteración {it}:")
        log(f"  x{idx_prev} = {fmt_decimal(x_prev)}")
        log(f"  x{idx_curr} = {fmt_decimal(x_curr)}")
        log(f"  f(x{idx_prev}) = {fmt_decimal(f_prev)}")
        log(f"  f(x{idx_curr}) = {fmt_decimal(f_curr)}")

        denom = f_curr - f_prev
        if denom == 0:
            log("  f(xi) − f(xi−1) = 0, no se puede continuar (división por cero).")
            break

        log("\n  Usando la fórmula de la Secante específica para esta iteración:")
        log(
            f"  x{idx_new} = x{idx_curr} − f(x{idx_curr})(x{idx_curr} − x{idx_prev}) / (f(x{idx_curr}) − f(x{idx_prev}))"
        )
        log(
            "  x{n} = {xc} − ({fc})({xc} − {xp}) / ({fc} − {fp})".format(
                n=idx_new,
                xc=fmt_decimal(x_curr),
                xp=fmt_decimal(x_prev),
                fc=fmt_decimal(f_curr),
                fp=fmt_decimal(f_prev),
            )
        )

        # Cálculo de x_{i+1}
        x_new = x_curr - f_curr * (x_curr - x_prev) / denom

        log(f"  x{idx_new} = {fmt_decimal(x_new)}")

        # Evaluar f(x_{i+1})
        try:
            f_new = f(x_new)
        except ValueError as exc:
            log(str(exc))
            break

        error = abs(x_new - x_curr)
        last_error = error
        root = x_new

        log(f"  f(x{idx_new}) = f({fmt_decimal(x_new)}) = {fmt_decimal(f_new)}")
        log(f"  error = |x{idx_new} − x{idx_curr}| = |{fmt_decimal(x_new)} − {fmt_decimal(x_curr)}| = {fmt_decimal(error)}")

        # Guardar en tabla de iteraciones
        iter_rows.append((idx_new, x_new, f_new, error))

        # Criterio de parada
        if error < eps:
            log(f"\n  Como el error {fmt_decimal(error)} < ε = {fmt_decimal(eps)}, se detiene el proceso iterativo.")
            break

        # Actualizar para la siguiente iteración
        x_prev, x_curr = x_curr, x_new
        f_prev, f_curr = f_curr, f_new

    # Mostrar tabla de iteraciones
    log("\nTabla de iteraciones:")
    headers = ["i", "xi", "f(xi)", "error"]
    log("  ".join(f"{h:>22}" for h in headers))
    for i, x_i, fx_i, err in iter_rows:
        err_str = fmt_decimal(err) if err is not None else "-"
        log(
            f"{i:>22}  {fmt_decimal(x_i):>22}  {fmt_decimal(fx_i):>22}  {err_str:>22}"
        )

    # ========================
    # PASO 5: Resultado final
    # ========================
    log("\nPASO 5: Resultado final")
    if root is None:
        log("El método no pudo encontrar una aproximación con los datos proporcionados.")
    else:
        log(f"Raíz aproximada (Decimal) x ≈ {fmt_decimal(root)}")
        log(f"Raíz aproximada con 10 decimales: {fmt_decimal(root, 10)}")
        if last_error is not None:
            log(f"Último error calculado: {fmt_decimal(last_error)}")

    # ========================
    # Opción de guardar pasos
    # ========================
    choice = input("\n¿Desea guardar todos los pasos en 'pasos_secante.txt'? (s/n): ").strip().lower()
    if choice == "s":
        filename = "pasos_secante.txt"
        try:
            with open(filename, "w", encoding="utf-8") as f:
                f.write("\n".join(pasos))
            print(f"Pasos guardados correctamente en '{filename}'.")
        except OSError as exc:  # noqa: BLE001
            print(f"No se pudieron guardar los pasos: {exc}")


if __name__ == "__main__":
    main()


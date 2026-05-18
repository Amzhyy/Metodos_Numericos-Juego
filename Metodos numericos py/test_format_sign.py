import sympy as sp

def test_substitution(g_str, x_val):
    x = sp.symbols('x')
    g_expr = sp.sympify(g_str)
    
    # Using explicit sign for the substitution
    xi_formatted = f"{x_val:+.10f}"
    
    val_sym = sp.Symbol(xi_formatted)
    sub_expr = g_expr.subs(x, val_sym)
    
    # result
    res = float(g_expr.subs(x, x_val))
    
    print(f"Original: {g_str}")
    print(f"Value: {x_val}")
    print(f"Substituted: {sub_expr} = {res:.10f}")
    print("-" * 20)

test_substitution("exp(-x)", 0.0)
test_substitution("exp(-x)", 0.3678794412)
test_substitution("x + 1", 0.5)
test_substitution("x - 1", -0.5)

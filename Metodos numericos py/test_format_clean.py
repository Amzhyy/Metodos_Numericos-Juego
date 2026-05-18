import sympy as sp

def test_substitution_clean(g_str, x_val):
    x = sp.symbols('x')
    g_expr = sp.sympify(g_str)
    
    # Format with sign
    xi_formatted = f"{x_val:+.10f}"
    
    # Substitute as a symbol to prevent immediate evaluation of the FUNCTION,
    # but we want the arithmetic around it to simplify if possible.
    val_sym = sp.Symbol(xi_formatted)
    sub_expr_raw = g_expr.subs(x, val_sym)
    
    # Now, if we sympify the string of sub_expr_raw, SymPy might simplify -+ to -.
    # But we want to keep the 10 decimals. Symbol names keep their exact string.
    # So if we have -+0.5000000000, and we want -0.5000000000.
    
    sub_str = str(sub_expr_raw)
    sub_str = sub_str.replace("-+", "-").replace("+-", "-").replace("++", "+").replace("--", "+")
    
    # Wait, what if there's no sign? We want to ensure at least one sign?
    # No, the rule says "mostrar explícitamente el signo". 
    # This usually means even for the first term.
    # SymPy's str() might omit '+' for the first term.
    
    print(f"Original: {g_str}, Val: {x_val}")
    print(f"Clean Sub: {sub_str}")
    print("-" * 20)

test_substitution_clean("exp(-x)", 0.3678794412)
test_substitution_clean("exp(-x)", -0.5)
test_substitution_clean("x + 1", 0.5)
test_substitution_clean("x + 1", -0.5)

import sympy as sp

def test_substitution(g_str, x_val):
    x = sp.symbols('x')
    g_expr = sp.sympify(g_str)
    
    # We want to show the expression with x replaced by (x_val)
    # But formatted to 10 decimals.
    
    # Method: Replace the symbol x with a SYMBOL that has the formatted string as its name.
    # This prevents SymPy from evaluating the outer function immediately but allows 
    # the internal representation of the substituted value to be what we want.
    
    # Let's see how it handles x_val = 0.5 and expr = exp(-x)
    xi_formatted = f"{x_val:.10f}"
    
    # Special case for "explicit sign" if requested.
    # The user example: exp(-0.0000000000). 
    # Here -x became -0.0000000000. 
    # If we substitute x with 0.0000000000, then -x becomes -0.0000000000.
    
    val_sym = sp.Symbol(xi_formatted)
    sub_expr = g_expr.subs(x, val_sym)
    
    # Note: SymPy might still simplify some things.
    # If g_expr = x + 1, sub_expr = 0.5000000000 + 1.
    
    print(f"Original: {g_str}")
    print(f"Value: {x_val}")
    print(f"Substituted Expression: {sub_expr}")
    print("-" * 20)

print("Testing substitution strings:")
test_substitution("exp(-x)", 0.0)
test_substitution("exp(-x)", 0.3678794412)
test_substitution("x**2 - 2", 1.4142)
test_substitution("sin(x)", 0.5)

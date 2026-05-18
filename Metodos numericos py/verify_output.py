import subprocess
import os

def run_test(g_func, x0):
    process = subprocess.Popen(
        ['python', 'punto_fijo_tabla.py'],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        cwd=os.getcwd()
    )
    
    # Input function and x0
    stdout, stderr = process.communicate(input=f"{g_func}\n{x0}\n")
    
    print(f"--- Output for g(x)={g_func}, x0={x0} ---")
    print(stdout)
    if stderr:
        print("--- Errors ---")
        print(stderr)
    print("-" * 40)

print("Verifying against user example:")
run_test("exp(-x)", 0)

print("Verifying with positive/negative signs:")
run_test("x/2 + 1", -0.5)

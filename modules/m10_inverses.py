# modules/m10_inverses.py  —  Inverses & Function Composition
from .utils import *
import math

def run():
    while True:
        clear(); header("INVERSES & FUNCTION COMPOSITION")
        print("  1  Find inverse of a linear function  y = mx + b")
        print("  2  Find inverse of a power/root function  y = axⁿ")
        print("  3  Find inverse of exponential / log")
        print("  4  Verify two functions are inverses  f(g(x)) = x")
        print("  5  Compose functions  (f∘g)(x)")
        print("  6  Evaluate composition at a point  f(g(a))")
        print("  0  Back")
        sep()
        ch = input("  Choose: ").strip()
        if ch == '1': inverse_linear()
        elif ch == '2': inverse_power()
        elif ch == '3': inverse_explog()
        elif ch == '4': verify_inverse()
        elif ch == '5': compose_symbolic()
        elif ch == '6': compose_numeric()
        elif ch == '0': break
        else: warn("Invalid."); pause()

# ── 1. Inverse of linear ──────────────────────────────────────────────────────

def inverse_linear():
    clear(); header("INVERSE OF LINEAR FUNCTION   y = mx + b")
    note("Swap x and y, then solve for y.\n")
    m = get_float("  Slope m: ")
    b = get_float("  y-intercept b [0]: ", fallback=0.0)

    if m == 0:
        warn("Slope = 0 — horizontal line has no inverse function."); pause(); return

    sep()
    step(1, "Write original function")
    print(f"     y = {m:g}x + {b:g}")

    step(2, "Swap x and y")
    print(f"     x = {m:g}y + {b:g}")

    step(3, "Isolate y")
    print(f"     {m:g}y = x − {b:g}")
    m_inv = 1 / m
    b_inv = -b / m
    print(f"     y  = (1/{m:g})x − {b:g}/{m:g}")

    result("f⁻¹(x)", f"{m_inv:g}x + ({b_inv:g})" if b_inv != 0 else f"{m_inv:g}x")
    note(f"The slopes are reciprocals: {m:g} × {m_inv:g} = 1 ✓")

    pause()

# ── 2. Inverse of power ───────────────────────────────────────────────────────

def inverse_power():
    clear(); header("INVERSE OF POWER FUNCTION   y = a · xⁿ")
    a = get_float("  Coefficient a [1]: ", fallback=1.0)
    n = get_float("  Exponent n: ")

    if a == 0 or n == 0:
        warn("a and n must be non-zero."); pause(); return

    sep()
    step(1, "Original function")
    print(f"     y = {a:g} · x^{n:g}")

    step(2, "Swap x and y")
    print(f"     x = {a:g} · y^{n:g}")

    step(3, "Isolate y")
    print(f"     y^{n:g} = x / {a:g}")
    print(f"     y     = (x / {a:g})^(1/{n:g})")
    print(f"            = (1/{a:g})^(1/{n:g}) · x^(1/{n:g})")

    a_inv = (1/a)**(1/n)
    n_inv = 1/n
    result("f⁻¹(x)", f"{a_inv:.5g} · x^{n_inv:g}  (or  {a_inv:.5g}·x^(1/{n:g}))")

    step(4, "Domain / Range swap")
    note("Domain of f  becomes Range of f⁻¹, and vice versa.")
    if n % 2 == 0:
        note(f"Since n={n:g} is even, original domain is x ≥ 0 → inverse domain is also x ≥ 0.")

    pause()

# ── 3. Inverse of exp / log ───────────────────────────────────────────────────

def inverse_explog():
    clear(); header("INVERSE OF EXPONENTIAL & LOGARITHMIC FUNCTIONS")
    fn_type = get_choice("  Function type", ["exponential", "log"])

    sep()
    if fn_type == "exponential":
        note("Form:  y = a · bˣ")
        a = get_float("  a [1]: ", fallback=1.0)
        b = get_float("  Base b: ")
        if b <= 0 or b == 1:
            warn("Base must be > 0 and ≠ 1."); pause(); return

        step(1, "Write original")
        print(f"     y = {a:g} · {b:g}^x")

        step(2, "Swap x and y")
        print(f"     x = {a:g} · {b:g}^y")

        step(3, "Isolate y using log")
        print(f"     {b:g}^y = x / {a:g}")
        print(f"     y·log({b:g}) = log(x/{a:g})")
        print(f"     y = log(x/{a:g}) / log({b:g})")
        print(f"     y = log_{b:g}(x/{a:g})")
        result("f⁻¹(x)", f"log_{b:g}(x / {a:g})")
        note(f"Domain of f⁻¹:  x > 0  (since x/{a:g} must be > 0)")

    else:
        note("Form:  y = log_b(x)  (general: y = a·log_b(x) + k)")
        a = get_float("  a [1]: ", fallback=1.0)
        b = get_float("  Base b: ")
        k = get_float("  Vertical shift k [0]: ", fallback=0.0)

        step(1, "Write original")
        print(f"     y = {a:g}·log_{b:g}(x) + {k:g}")

        step(2, "Swap x and y")
        print(f"     x = {a:g}·log_{b:g}(y) + {k:g}")

        step(3, "Isolate y")
        print(f"     x − {k:g} = {a:g}·log_{b:g}(y)")
        print(f"     log_{b:g}(y) = (x − {k:g}) / {a:g}")
        print(f"     y = {b:g}^((x − {k:g}) / {a:g})")
        result("f⁻¹(x)", f"{b:g}^((x − {k:g}) / {a:g})")
        note("Domain of f⁻¹: all real x  (exponentials defined everywhere)")

    pause()

# ── 4. Verify inverses numerically ────────────────────────────────────────────

def verify_inverse():
    clear(); header("VERIFY INVERSES   f(g(x)) = x  and  g(f(x)) = x")
    note("Enter both functions as Python expressions using variable 'x'.")
    note("Use math.sqrt, math.log, math.exp, x**n, etc.\n")
    note("Example f: 2*x + 3")
    note("Example g: (x - 3) / 2\n")

    f_str = input("  f(x) = ").strip()
    g_str = input("  g(x) = ").strip()

    test_vals = [1, 2, 5, 10, -3, 0.5, -7.2]
    safe_env = {"x": 0, "math": math, "__builtins__": {}}

    sep()
    step(1, "Test f(g(x)) = x")
    print(f"\n  {'x':>8}  {'g(x)':>12}  {'f(g(x))':>12}  {'= x?':>8}")
    sep('-', 46)
    fog_ok = True
    for xv in test_vals:
        try:
            safe_env["x"] = xv
            gx = eval(g_str, {"__builtins__": {}}, {"x": xv, "math": math})
            safe_env["x"] = gx
            fgx = eval(f_str, {"__builtins__": {}}, {"x": gx, "math": math})
            match = abs(fgx - xv) < 1e-7
            if not match: fog_ok = False
            mark = "✓" if match else "✗"
            print(f"  {xv:>8g}  {gx:>12.6f}  {fgx:>12.6f}  {mark:>8}")
        except Exception as e:
            print(f"  {xv:>8g}  {'error':>12}  {'–':>12}  {'–':>8}  ({e})")

    step(2, "Test g(f(x)) = x")
    print(f"\n  {'x':>8}  {'f(x)':>12}  {'g(f(x))':>12}  {'= x?':>8}")
    sep('-', 46)
    gof_ok = True
    for xv in test_vals:
        try:
            fx = eval(f_str, {"__builtins__": {}}, {"x": xv, "math": math})
            gfx = eval(g_str, {"__builtins__": {}}, {"x": fx, "math": math})
            match = abs(gfx - xv) < 1e-7
            if not match: gof_ok = False
            mark = "✓" if match else "✗"
            print(f"  {xv:>8g}  {fx:>12.6f}  {gfx:>12.6f}  {mark:>8}")
        except Exception as e:
            print(f"  {xv:>8g}  {'error':>12}  {'–':>12}  {'–':>8}  ({e})")

    sep()
    if fog_ok and gof_ok:
        ok("f and g appear to be INVERSES of each other ✓")
    else:
        warn("f and g do NOT appear to be inverses at all tested values.")

    pause()

# ── 5. Symbolic composition ───────────────────────────────────────────────────

def compose_symbolic():
    clear(); header("COMPOSE FUNCTIONS   (f∘g)(x) = f(g(x))")
    note("Enter functions as Python expressions using variable 'x'.")
    note("Examples:  2*x + 1    x**2 - 3    math.sqrt(x)\n")

    f_str = input("  f(x) = ").strip()
    g_str = input("  g(x) = ").strip()

    sep()
    step(1, "Write the composition")
    print(f"     f(x) = {f_str}")
    print(f"     g(x) = {g_str}")
    print(f"\n     (f∘g)(x) = f(g(x)) = f({g_str})")

    step(2, "Evaluate at sample points to show the pattern")
    print(f"\n  {'x':>6}  {'g(x)':>12}  {'f(g(x))':>14}")
    sep('-', 38)
    for xv in [-2, -1, 0, 1, 2, 3, 5]:
        try:
            gx  = eval(g_str, {"__builtins__": {}}, {"x": xv, "math": math})
            fgx = eval(f_str, {"__builtins__": {}}, {"x": gx,  "math": math})
            print(f"  {xv:>6g}  {gx:>12.4f}  {fgx:>14.4f}")
        except Exception as e:
            print(f"  {xv:>6g}  {'error':>12}  ({e})")

    pause()

# ── 6. Evaluate composition numerically ───────────────────────────────────────

def compose_numeric():
    clear(); header("EVALUATE COMPOSITION AT A POINT")
    note("Compute f(g(a)) step by step.\n")

    f_str = input("  f(x) = ").strip()
    g_str = input("  g(x) = ").strip()
    a = get_float("  Evaluate at x = a, a = ")

    sep()
    step(1, f"Compute g({a:g})")
    try:
        ga = eval(g_str, {"__builtins__": {}}, {"x": a, "math": math})
        print(f"     g({a:g}) = {ga:g}")
    except Exception as e:
        warn(f"Error computing g({a:g}): {e}"); pause(); return

    step(2, f"Compute f(g({a:g})) = f({ga:g})")
    try:
        fga = eval(f_str, {"__builtins__": {}}, {"x": ga, "math": math})
        print(f"     f({ga:g}) = {fga:g}")
    except Exception as e:
        warn(f"Error computing f({ga:g}): {e}"); pause(); return

    result(f"(f∘g)({a:g})", f"{fga:g}")
    pause()

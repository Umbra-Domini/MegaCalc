# modules/m04_explog.py  —  Exponential & Logarithmic Functions
from .utils import *
import math

def run():
    while True:
        clear(); header("EXPONENTIAL & LOGARITHMIC FUNCTIONS")
        print("  1  Laws of logarithms (simplify/expand)")
        print("  2  Solve exponential equation  a·bˣ = c")
        print("  3  Solve logarithmic equation  log_b(x) = c")
        print("  4  Change of base")
        print("  5  Exponential growth & decay")
        print("  6  Compound interest")
        print("  7  Graph exponential or log function")
        print("  0  Back")
        sep()
        ch = input("  Choose: ").strip()
        if ch == '1': log_laws()
        elif ch == '2': solve_exp()
        elif ch == '3': solve_log()
        elif ch == '4': change_of_base()
        elif ch == '5': growth_decay()
        elif ch == '6': compound_interest()
        elif ch == '7': graph_explog()
        elif ch == '0': break
        else: warn("Invalid."); pause()

# ── 1. Laws of logs ───────────────────────────────────────────────────────────

def log_laws():
    clear(); header("LAWS OF LOGARITHMS — REFERENCE & EVALUATOR")
    sep()
    print("""
  ┌─ Product Rule   ──────────────────────────────────┐
  │  log_b(M·N)  =  log_b(M) + log_b(N)              │
  ├─ Quotient Rule  ──────────────────────────────────┤
  │  log_b(M/N)  =  log_b(M) − log_b(N)              │
  ├─ Power Rule     ──────────────────────────────────┤
  │  log_b(Mⁿ)   =  n · log_b(M)                     │
  ├─ Change of Base ──────────────────────────────────┤
  │  log_b(M)    =  ln(M) / ln(b)                     │
  ├─ Special Values ──────────────────────────────────┤
  │  log_b(1)    =  0    (b^0 = 1)                    │
  │  log_b(b)    =  1    (b^1 = b)                    │
  │  log_b(bⁿ)   =  n                                 │
  │  b^(log_b x) =  x   (inverse property)           │
  └────────────────────────────────────────────────────┘
""")
    note("Now evaluate:  log_b(x)\n")
    b = get_float("  Base b (e.g. 10, 2, or 'e'→ 2.71828): ")
    if b <= 0 or b == 1:
        warn("Base must be > 0 and ≠ 1."); pause(); return
    x = get_float("  Argument x: ")
    if x <= 0:
        warn("Argument must be > 0."); pause(); return

    sep()
    step(1, "Apply change of base formula")
    print(f"     log_{b:g}({x:g})  =  ln({x:g}) / ln({b:g})")
    print(f"             =  {math.log(x):.6f} / {math.log(b):.6f}")
    val = math.log(x) / math.log(b)
    result(f"log_{b:g}({x:g})", fmt(val))
    pause()

# ── 2. Solve exponential equation ─────────────────────────────────────────────

def solve_exp():
    clear(); header("SOLVE EXPONENTIAL EQUATION")
    note("Form:  a · bˣ = c     (also handles  a · b^(mx+n) = c)\n")

    a = get_float("  Coefficient a [1]: ", fallback=1.0)
    b = get_float("  Base b: ")
    if b <= 0 or b == 1:
        warn("Base must be > 0 and ≠ 1."); pause(); return

    note("Exponent form: (m·x + n)  — simple x: m=1, n=0")
    m = get_float("  Exponent multiplier m [1]: ", fallback=1.0)
    n = get_float("  Exponent constant n [0]: ", fallback=0.0)
    c = get_float("  Right-hand side c: ")

    sep()
    step(1, "Isolate the exponential")
    rhs = c / a
    print(f"     {a:g} · {b:g}^({m:g}x + {n:g}) = {c:g}")
    print(f"     {b:g}^({m:g}x + {n:g}) = {c:g} / {a:g} = {rhs:g}")

    if rhs <= 0:
        warn("Right-hand side is ≤ 0 — no real solution (exponentials are always positive).")
        pause(); return

    step(2, "Take log of both sides")
    print(f"     log({b:g}^({m:g}x + {n:g})) = log({rhs:g})")
    print(f"     ({m:g}x + {n:g}) · log({b:g}) = log({rhs:g})")

    step(3, "Solve for x")
    log_b = math.log(b)
    log_r = math.log(rhs)
    print(f"     {m:g}x + {n:g} = log({rhs:g}) / log({b:g})")
    print(f"     {m:g}x + {n:g} = {log_r:.6f} / {log_b:.6f}")
    inner = log_r / log_b
    print(f"     {m:g}x + {n:g} = {inner:.6f}")
    x = (inner - n) / m
    print(f"     {m:g}x = {inner:.6f} − {n:g} = {inner - n:.6f}")
    print(f"     x = {inner - n:.6f} / {m:g}")
    result("x", fmt(x))

    # Verify
    check = a * b**(m * x + n)
    note(f"Verification: {a:g}·{b:g}^({m:g}·{x:.4f}+{n:g}) = {check:.4f}  (should be {c:g})")
    pause()

# ── 3. Solve logarithmic equation ─────────────────────────────────────────────

def solve_log():
    clear(); header("SOLVE LOGARITHMIC EQUATION")
    note("Form:  a · log_b(mx + n) = c\n")

    a = get_float("  Coefficient a [1]: ", fallback=1.0)
    b = get_float("  Base b [10]: ", fallback=10.0)
    if b <= 0 or b == 1:
        warn("Base must be > 0 and ≠ 1."); pause(); return
    m = get_float("  Inner multiplier m [1]: ", fallback=1.0)
    n = get_float("  Inner constant n [0]: ", fallback=0.0)
    c = get_float("  Right-hand side c: ")

    sep()
    step(1, "Isolate the logarithm")
    rhs = c / a
    print(f"     {a:g} · log_{b:g}({m:g}x + {n:g}) = {c:g}")
    print(f"     log_{b:g}({m:g}x + {n:g}) = {c:g} / {a:g} = {rhs:g}")

    step(2, "Convert to exponential form  (b^rhs = mx + n)")
    exp_val = b ** rhs
    print(f"     {b:g}^{rhs:g} = {m:g}x + {n:g}")
    print(f"     {exp_val:.6f} = {m:g}x + {n:g}")

    step(3, "Solve for x")
    x = (exp_val - n) / m
    print(f"     {m:g}x = {exp_val:.6f} − {n:g}")
    print(f"     x  = {exp_val - n:.6f} / {m:g}")
    result("x", fmt(x))

    step(4, "Check domain restriction  (mx + n > 0)")
    inner_val = m * x + n
    if inner_val > 0:
        ok(f"{m:g}·({x:.4f}) + {n:g} = {inner_val:.4f} > 0  ✓  Valid solution")
    else:
        warn(f"Argument = {inner_val:.4f} ≤ 0 — EXTRANEOUS solution (log undefined)")

    pause()

# ── 4. Change of base ─────────────────────────────────────────────────────────

def change_of_base():
    clear(); header("CHANGE OF BASE")
    note("log_b(x) = log_c(x) / log_c(b)  for any valid base c\n")

    b = get_float("  Original base b: ")
    x = get_float("  Argument x: ")
    c = get_float("  New base c [10]: ", fallback=10.0)

    if any(v <= 0 or v == 1 for v in [b, c]) or x <= 0:
        warn("All bases must be > 0, ≠ 1, and argument must be > 0."); pause(); return

    sep()
    step(1, "Apply change of base formula")
    print(f"     log_{b:g}({x:g})  =  log_{c:g}({x:g}) / log_{c:g}({b:g})")

    lx = math.log(x) / math.log(c)
    lb = math.log(b) / math.log(c)
    val = lx / lb
    print(f"              =  {lx:.6f} / {lb:.6f}")
    result(f"log_{b:g}({x:g})", fmt(val))
    pause()

# ── 5. Growth & decay ─────────────────────────────────────────────────────────

def growth_decay():
    clear(); header("EXPONENTIAL GROWTH & DECAY")
    note("Model:  A(t) = A₀ · b^t   OR   A(t) = A₀ · e^(kt)\n")

    model = get_choice("Model type", ["standard", "natural"])

    A0 = get_float("  Initial amount A₀: ")
    if model == "standard":
        b = get_float("  Base b (growth > 1, decay 0<b<1): ")
    else:
        k = get_float("  Growth constant k (negative = decay): ")

    sep()
    print("\n  TIME TABLE")
    print(f"  {'t':>8}  {'A(t)':>14}")
    sep('-', 28)
    for t in [0, 1, 2, 5, 10, 25, 50, 100]:
        if model == "standard":
            A = A0 * b**t
        else:
            A = A0 * math.exp(k * t)
        print(f"  {t:>8}  {A:>14.4f}")

    # Doubling / half-life
    sep()
    step(1, "Find doubling time / half-life")
    if model == "standard":
        if b > 1:
            t_double = math.log(2) / math.log(b)
            ok(f"Doubling time: t = log(2)/log({b:g}) = {t_double:.4f}")
        elif 0 < b < 1:
            t_half = math.log(0.5) / math.log(b)
            ok(f"Half-life: t = log(0.5)/log({b:g}) = {t_half:.4f}")
    else:
        if k > 0:
            t_double = math.log(2) / k
            ok(f"Doubling time: t = ln(2)/k = {t_double:.4f}")
        elif k < 0:
            t_half = math.log(0.5) / k
            ok(f"Half-life: t = ln(0.5)/k = {t_half:.4f}")

    # Find time for target amount
    sep()
    note("Find time to reach a target value:")
    target = get_float("  Target amount (blank to skip): ", fallback=None)
    if target is not None and target > 0:
        step(2, "Solve for t")
        if model == "standard":
            print(f"     A₀·b^t = target")
            print(f"     {A0:g}·{b:g}^t = {target:g}")
            ratio = target / A0
            t_sol = math.log(ratio) / math.log(b)
        else:
            ratio = target / A0
            t_sol = math.log(ratio) / k
        print(f"     t = {t_sol:.4f}")
        result("t", fmt(t_sol))

    pause()

# ── 6. Compound interest ──────────────────────────────────────────────────────

def compound_interest():
    clear(); header("COMPOUND INTEREST")
    note("A = P·(1 + r/n)^(nt)   or   A = P·e^(rt)  (continuous)\n")

    P = get_float("  Principal P: ")
    r = get_float("  Annual rate r (e.g. 0.05 for 5%): ")
    t = get_float("  Time in years t: ")
    mode = get_choice("  Compounding", ["annual", "semi", "quarterly", "monthly", "daily", "continuous"])

    n_map = {"annual": 1, "semi": 2, "quarterly": 4, "monthly": 12, "daily": 365, "continuous": None}
    n = n_map[mode]

    sep()
    step(1, "Apply formula")
    if n is not None:
        A = P * (1 + r/n)**(n*t)
        print(f"     A = {P:g}·(1 + {r:g}/{n})^({n}·{t:g})")
        print(f"       = {P:g}·({1 + r/n:.6f})^{n*t:g}")
    else:
        A = P * math.exp(r * t)
        print(f"     A = {P:g}·e^({r:g}·{t:g})")

    result("Final amount A", f"${A:,.4f}  ({fmt_plain(A)})")
    result("Interest earned", f"${A - P:,.4f}")
    pause()

# ── 7. Graph ──────────────────────────────────────────────────────────────────

def graph_explog():
    clear(); header("GRAPH EXPONENTIAL OR LOG FUNCTION")
    if not require_graph(): pause(); return

    import numpy as np
    import matplotlib.pyplot as plt

    fn_type = get_choice("Function type", ["exponential", "log"])
    a = get_float("  a [1]: ", fallback=1.0)
    b = get_float("  base b [2]: ", fallback=2.0)
    h = get_float("  h (horizontal shift) [0]: ", fallback=0.0)
    k = get_float("  k (vertical shift) [0]: ", fallback=0.0)

    x = np.linspace(-5, 5, 800)
    if fn_type == "exponential":
        y = a * b**(x - h) + k
        label = f'y = {a:g}·{b:g}^(x−{h:g}) + {k:g}'
    else:
        inner = x - h
        y = np.where(inner > 0, a * np.log(np.maximum(inner, 1e-10)) / math.log(b) + k, np.nan)
        label = f'y = {a:g}·log_{b:g}(x−{h:g}) + {k:g}'

    fig = make_plotly_fig(title=label)
    add_curve(fig, x, y, name=label, colour=PC['green'])
    show_plotly(fig, ymin=-10, ymax=10)
    pause()

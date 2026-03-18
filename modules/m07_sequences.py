# modules/m07_sequences.py  —  Sequences & Series
from .utils import *
import math

def run():
    while True:
        clear(); header("SEQUENCES & SERIES")
        print("  1  Arithmetic sequence / series")
        print("  2  Geometric sequence / series")
        print("  3  Infinite geometric series")
        print("  4  Sigma notation evaluator")
        print("  5  Find sequence type from terms")
        print("  0  Back")
        sep()
        ch = input("  Choose: ").strip()
        if ch == '1': arithmetic()
        elif ch == '2': geometric()
        elif ch == '3': infinite_geo()
        elif ch == '4': sigma()
        elif ch == '5': identify_sequence()
        elif ch == '0': break
        else: warn("Invalid."); pause()

# ── 1. Arithmetic ─────────────────────────────────────────────────────────────

def arithmetic():
    clear(); header("ARITHMETIC SEQUENCE & SERIES")
    note("Form:  aₙ = a₁ + (n−1)·d\n")

    print("  Provide at least 2 of: a₁, d, aₙ, n")
    a1 = get_float("  First term a₁ (blank to skip): ", fallback=None)
    d  = get_float("  Common difference d (blank to skip): ", fallback=None)
    an = get_float("  nth term aₙ (blank to skip): ", fallback=None)
    n  = get_float("  Term number n (blank to skip): ", fallback=None)

    # Solve for missing values
    if a1 is not None and d is not None and n is not None:
        an = a1 + (n - 1) * d
    elif a1 is not None and an is not None and n is not None:
        d = (an - a1) / (n - 1)
    elif d is not None and an is not None and n is not None:
        a1 = an - (n - 1) * d
    elif a1 is not None and d is not None and an is not None:
        n = (an - a1) / d + 1

    sep()
    if None in (a1, d, n, an):
        warn("Not enough info to solve. Need at least 3 of the 4 values."); pause(); return

    n = int(round(n))
    step(1, "Identify / confirm values")
    print(f"     a₁ = {a1:g}")
    print(f"     d  = {d:g}")
    print(f"     n  = {n}")
    print(f"     aₙ = a₁ + (n−1)·d = {a1:g} + ({n}−1)·{d:g} = {an:g}")

    step(2, "Partial sum Sₙ")
    Sn = n * (a1 + an) / 2
    print(f"     Sₙ = n·(a₁ + aₙ) / 2")
    print(f"       = {n}·({a1:g} + {an:g}) / 2")
    print(f"       = {n}·{a1+an:g} / 2")
    result(f"S_{n}", f"{Sn:g}")

    step(3, "First few terms")
    terms = [a1 + i*d for i in range(min(10, n))]
    print("     " + ",  ".join(f"{t:g}" for t in terms) + ("  ..." if n > 10 else ""))

    pause()

# ── 2. Geometric ──────────────────────────────────────────────────────────────

def geometric():
    clear(); header("GEOMETRIC SEQUENCE & SERIES")
    note("Form:  aₙ = a₁ · rⁿ⁻¹\n")

    a1 = get_float("  First term a₁: ")
    r  = get_float("  Common ratio r: ")
    n  = get_int("  Number of terms n: ")

    sep()
    step(1, "nth term")
    an = a1 * r**(n-1)
    print(f"     aₙ = {a1:g} · {r:g}^({n}−1)")
    print(f"       = {a1:g} · {r:g}^{n-1}")
    result(f"a_{n}", f"{an:g}")

    step(2, "Finite geometric sum Sₙ")
    if r == 1:
        Sn = a1 * n
        print(f"     r = 1, so Sₙ = n·a₁ = {n}·{a1:g} = {Sn:g}")
    else:
        Sn = a1 * (1 - r**n) / (1 - r)
        print(f"     Sₙ = a₁·(1 − rⁿ) / (1 − r)")
        print(f"       = {a1:g}·(1 − {r:g}^{n}) / (1 − {r:g})")
        print(f"       = {a1:g}·{1 - r**n:.6f} / {1 - r:.6f}")
    result(f"S_{n}", f"{Sn:g}")

    step(3, "First few terms")
    terms = [a1 * r**i for i in range(min(10, n))]
    print("     " + ",  ".join(f"{t:g}" for t in terms) + ("  ..." if n > 10 else ""))

    pause()

# ── 3. Infinite geometric series ─────────────────────────────────────────────

def infinite_geo():
    clear(); header("INFINITE GEOMETRIC SERIES")
    note("Converges only if |r| < 1.   S∞ = a₁ / (1 − r)\n")

    a1 = get_float("  First term a₁: ")
    r  = get_float("  Common ratio r: ")

    sep()
    step(1, "Check convergence condition |r| < 1")
    print(f"     |r| = |{r:g}| = {abs(r):g}")

    if abs(r) >= 1:
        warn(f"|r| = {abs(r):g} ≥ 1 — series DIVERGES (no finite sum).")
        pause(); return
    ok(f"|r| = {abs(r):g} < 1 — series CONVERGES.")

    step(2, "Apply formula S∞ = a₁ / (1 − r)")
    S = a1 / (1 - r)
    print(f"     S∞ = {a1:g} / (1 − {r:g})")
    print(f"       = {a1:g} / {1 - r:g}")
    result("S∞", f"{S:g}")

    step(3, "Partial sums approaching S∞")
    running = 0
    print(f"\n  {'n':>5}  {'Partial sum Sₙ':>18}  {'Diff from S∞':>16}")
    sep('-', 44)
    term = a1
    for i in range(1, 16):
        running += term
        term *= r
        print(f"  {i:>5}  {running:>18.8f}  {abs(running - S):>16.2e}")

    pause()

# ── 4. Sigma notation ─────────────────────────────────────────────────────────

def sigma():
    clear(); header("SIGMA NOTATION EVALUATOR")
    note("Evaluate  Σ f(i)  from i = start to i = end")
    note("Supported expressions use variable 'i'.")
    note("Examples:  i       i**2       3*i+1       2**i\n")

    expr = input("  Expression f(i): ").strip()
    start = get_int("  Start index: ")
    end   = get_int("  End index: ")

    if end < start:
        warn("End must be ≥ start."); pause(); return

    sep()
    step(1, "Evaluate term by term")
    total = 0
    terms = []
    for i in range(start, end + 1):
        try:
            val = eval(expr, {"__builtins__": {}}, {"i": i, "math": math})
            terms.append(val)
            total += val
        except Exception as e:
            warn(f"Error at i={i}: {e}"); pause(); return

    print(f"\n  {'i':>6}  {'f(i)':>14}  {'Running sum':>14}")
    sep('-', 40)
    running = 0
    for i, v in zip(range(start, end + 1), terms):
        running += v
        print(f"  {i:>6}  {v:>14.6g}  {running:>14.6g}")

    result(f"Σ f(i) from {start} to {end}", f"{total:g}")
    pause()

# ── 5. Identify sequence type ─────────────────────────────────────────────────

def identify_sequence():
    clear(); header("IDENTIFY SEQUENCE TYPE FROM TERMS")
    note("Enter at least 4 terms, space-separated.\n")

    raw = input("  Terms: ").strip()
    try:
        terms = [float(x) for x in raw.split()]
    except ValueError:
        warn("Invalid input."); pause(); return

    if len(terms) < 3:
        warn("Need at least 3 terms."); pause(); return

    sep()
    # Check arithmetic: constant difference
    diffs = [terms[i+1] - terms[i] for i in range(len(terms)-1)]
    is_arith = all(abs(d - diffs[0]) < 1e-9 for d in diffs)

    # Check geometric: constant ratio (handle zero carefully)
    is_geo = False
    if all(abs(t) > 1e-12 for t in terms):
        ratios = [terms[i+1] / terms[i] for i in range(len(terms)-1)]
        is_geo = all(abs(r - ratios[0]) < 1e-6 for r in ratios)

    step(1, "Check differences (arithmetic?)")
    print(f"     Differences: {[f'{d:g}' for d in diffs]}")
    if is_arith:
        ok(f"Constant difference d = {diffs[0]:g}  →  ARITHMETIC")
        step(2, "Arithmetic details")
        a1 = terms[0]; d = diffs[0]
        print(f"     a₁ = {a1:g},  d = {d:g}")
        n = 20
        an = a1 + (n-1)*d
        Sn = n*(a1+an)/2
        print(f"     a₂₀ = {an:g}")
        print(f"     S₂₀ = {Sn:g}")
    else:
        note("Differences not constant — not arithmetic.")

    step(2 if not is_arith else 3, "Check ratios (geometric?)")
    if all(abs(t) > 1e-12 for t in terms):
        print(f"     Ratios:      {[f'{r:g}' for r in ratios]}")
    if is_geo:
        ok(f"Constant ratio r = {ratios[0]:g}  →  GEOMETRIC")
        a1 = terms[0]; r = ratios[0]
        print(f"     a₁ = {a1:g},  r = {r:g}")
        print(f"     a₁₀ = {a1 * r**9:g}")
        if abs(r) < 1:
            ok(f"     S∞ = {a1/(1-r):g}")
    elif not is_arith:
        note("Ratios not constant — not geometric.")

    if not is_arith and not is_geo:
        note("Neither arithmetic nor geometric.")
        note("Try checking for quadratic pattern (2nd differences):")
        if len(diffs) >= 2:
            second_diffs = [diffs[i+1] - diffs[i] for i in range(len(diffs)-1)]
            print(f"     2nd differences: {[f'{d:g}' for d in second_diffs]}")
            if all(abs(d - second_diffs[0]) < 1e-9 for d in second_diffs):
                ok("Constant 2nd differences — QUADRATIC sequence!")

    pause()

# modules/m02_polynomials.py  —  Polynomial Functions
from .utils import *
import math

def run():
    while True:
        clear(); header("POLYNOMIAL FUNCTIONS")
        print("  1  End behaviour & degree analysis")
        print("  2  Evaluate polynomial at a point")
        print("  3  Find rational roots (Rational Root Theorem)")
        print("  4  Synthetic division")
        print("  5  Factor & find all roots")
        print("  6  Root multiplicity analysis")
        print("  7  Graph polynomial")
        print("  0  Back")
        sep()
        ch = input("  Choose: ").strip()
        if ch == '1': end_behaviour()
        elif ch == '2': evaluate()
        elif ch == '3': rational_roots()
        elif ch == '4': synthetic_division()
        elif ch == '5': factor_roots()
        elif ch == '6': multiplicity()
        elif ch == '7': graph_poly()
        elif ch == '0': break
        else: warn("Invalid."); pause()

def _get_poly():
    note("Enter coefficients from HIGHEST to LOWEST degree, space-separated.")
    note("Example: 2x³ − x + 5  →  2 0 -1 5\n")
    return get_poly()

def _factors_int(n):
    n = int(abs(n))
    return [i for i in range(1, n+1) if n % i == 0]

# ── 1. End behaviour ──────────────────────────────────────────────────────────

def end_behaviour():
    clear(); header("END BEHAVIOUR & DEGREE ANALYSIS")
    coeffs = _get_poly()
    degree = len(coeffs) - 1
    lead   = coeffs[0]

    step(1, "Identify degree and leading coefficient")
    working(f"Polynomial:  {poly_str(coeffs)}")
    val_line("Degree",  f"{degree}  ({'even' if degree%2==0 else 'odd'})")
    val_line("Leading coefficient", f"{lead:g}  ({'positive' if lead>0 else 'negative'})")

    step(2, "Apply end behaviour rules")
    note("As x → ±∞, the leading term dominates.")
    even = degree % 2 == 0
    pos  = lead > 0

    if even and pos:
        ok(c(C.YELLOW, "Degree EVEN, leading POSITIVE"))
        working("x → +∞ : y → +∞"); working("x → −∞ : y → +∞")
        result("End Behaviour", "↑  both ends rise  ↑")
    elif even and not pos:
        ok(c(C.YELLOW, "Degree EVEN, leading NEGATIVE"))
        working("x → +∞ : y → −∞"); working("x → −∞ : y → −∞")
        result("End Behaviour", "↓  both ends fall  ↓")
    elif not even and pos:
        ok(c(C.YELLOW, "Degree ODD, leading POSITIVE"))
        working("x → +∞ : y → +∞"); working("x → −∞ : y → −∞")
        result("End Behaviour", "↓ falls left,  rises right ↑")
    else:
        ok(c(C.YELLOW, "Degree ODD, leading NEGATIVE"))
        working("x → +∞ : y → −∞"); working("x → −∞ : y → +∞")
        result("End Behaviour", "↑ rises left,  falls right ↓")

    step(3, "Other properties")
    val_line("Max x-intercepts (roots)", str(degree))
    val_line("Max turning points",       str(degree - 1))
    val_line("y-intercept f(0)",         fmt(poly_eval(coeffs, 0)))
    pause()

# ── 2. Evaluate ───────────────────────────────────────────────────────────────

def evaluate():
    clear(); header("EVALUATE POLYNOMIAL")
    coeffs = _get_poly()
    x = get_float("\n  Evaluate at x = ")

    step(1, "Horner's method (synthetic evaluation)")
    working(f"P(x) = {poly_str(coeffs)}")
    working(f"x    = {x:g}\n")

    print(f"  {c(C.GREY, 'Coefficient'):20}  {c(C.GREY, 'Running total')}")
    sep('-', 40)
    val = 0
    for cv in coeffs:
        val = val * x + cv
        print(f"  {c(C.YELLOW, f'{cv:>12g}')}         {c(C.WHITE, f'{val:g}')}")

    result(f"P({x:g})", fmt(val))
    pause()

# ── 3. Rational Root Theorem ──────────────────────────────────────────────────

def rational_roots():
    clear(); header("RATIONAL ROOT THEOREM")
    coeffs = _get_poly()

    step(1, "Identify p (factors of constant) and q (factors of leading coeff)")
    const  = int(abs(coeffs[-1]))
    lead   = int(abs(coeffs[0]))
    p_list = _factors_int(const)
    q_list = _factors_int(lead)
    val_line("Constant term",       str(const))
    val_line("Leading coefficient", str(lead))
    working(f"p = ±{p_list}")
    working(f"q = ±{q_list}")

    step(2, "List all possible rational roots ±p/q")
    candidates = sorted({p/q for p in p_list for q in q_list} |
                        {-p/q for p in p_list for q in q_list})
    working(f"Candidates: {[f'{c_:g}' for c_ in candidates]}")

    step(3, "Test each candidate")
    actual_roots = []
    print(f"\n  {c(C.GREY,'Candidate x ='):20}  {c(C.GREY,'P(x)')}")
    sep('-', 42)
    for cand in candidates:
        val = poly_eval(coeffs, cand)
        is_root = abs(val) < 1e-9
        tag = c(C.GREEN, "  ← ROOT ✓") if is_root else ""
        colour = C.GREEN if is_root else C.DIM
        print(f"  {c(colour, f'x = {cand:>8g}'):30}  {c(colour, f'{val:g}')}{tag}")
        if is_root:
            actual_roots.append(cand)

    if actual_roots:
        results(*[(f"Rational root", f"x = {r:g}") for r in actual_roots])
    else:
        warn("No rational roots — polynomial may be irreducible over ℚ.")
    pause()

# ── 4. Synthetic Division ─────────────────────────────────────────────────────

def synthetic_division():
    clear(); header("SYNTHETIC DIVISION")
    note("Divide P(x) by (x − r).\n")
    coeffs = _get_poly()
    r = get_float("\n  Divide by (x − r), enter r = ")

    step(1, "Set up synthetic division table")
    working(f"Divisor: (x − {r:g})\n")

    row   = list(coeffs)
    bring = [row[0]]
    for i in range(1, len(row)):
        bring.append(row[i] + bring[-1] * r)

    w = 9
    print("  " + c(C.GREY,   "".join(f"{v:>{w}g}" for v in row)))
    print("  " + " "*w + c(C.CYAN, "".join(f"{bring[i-1]*r:>{w}g}" for i in range(1, len(row)))))
    print("  " + c(C.GREY, "─" * (w * len(row))))
    print("  " + c(C.WHITE, "".join(f"{v:>{w}g}" for v in bring)))

    step(2, "Read off quotient and remainder")
    remainder = bring[-1]
    q_coeffs  = bring[:-1]
    val_line("Quotient",  poly_str(q_coeffs))
    val_line("Remainder", fmt(remainder))

    if abs(remainder) < 1e-9:
        result("Factor check", f"(x − {r:g}) IS a factor ✓")
    else:
        note(f"Remainder ≠ 0 → (x − {r:g}) is NOT a factor")
        note(f"By Remainder Theorem: P({r:g}) = {remainder:g}")
    pause()

# ── 5. Factor & find all roots ────────────────────────────────────────────────

def factor_roots():
    clear(); header("FACTOR & FIND ALL ROOTS")
    note("Uses Rational Root Theorem + synthetic division iteratively.\n")
    coeffs = _get_poly()
    found  = _full_factor(list(coeffs))
    if found:
        results(*[(f"Root {i+1}", f"x = {fmt_plain(r)}") for i, r in enumerate(found)])
    pause()

def _full_factor(coeffs, depth=0, found=None):
    if found is None: found = []
    indent = "  " * (depth + 1)
    degree = len(coeffs) - 1
    if degree <= 0: return found

    if degree == 1:
        root = -coeffs[1] / coeffs[0]
        print(f"{indent}{c(C.GREEN,'→')} Linear root: x = {c(C.YELLOW, fmt_plain(root))}")
        found.append(root); return found

    if degree == 2:
        a, b, cv = coeffs
        disc = b**2 - 4*a*cv
        working(f"{indent}Quadratic {poly_str(coeffs)},  Δ = {disc:g}")
        if disc > 0:
            x1 = (-b + math.sqrt(disc)) / (2*a)
            x2 = (-b - math.sqrt(disc)) / (2*a)
            print(f"{indent}{c(C.GREEN,'→')} x = {c(C.YELLOW, fmt_plain(x1))},  x = {c(C.YELLOW, fmt_plain(x2))}")
            found += [x1, x2]
        elif disc == 0:
            x1 = -b / (2*a)
            print(f"{indent}{c(C.GREEN,'→')} x = {c(C.YELLOW, fmt_plain(x1))} (repeated)")
            found += [x1, x1]
        else:
            real = -b/(2*a); imag = math.sqrt(-disc)/(2*a)
            print(f"{indent}{c(C.GREY,'→')} Complex: {real:g} ± {imag:g}i")
        return found

    const = int(abs(coeffs[-1])) if coeffs[-1] != 0 else 1
    lead  = int(abs(coeffs[0]))
    cands = sorted({p/q for p in _factors_int(const) for q in _factors_int(lead)} |
                   {-p/q for p in _factors_int(const) for q in _factors_int(lead)})
    for cand in cands:
        if abs(poly_eval(coeffs, cand)) < 1e-8:
            print(f"{indent}{c(C.GREEN,'→')} Root x = {c(C.YELLOW,f'{cand:g}')} → factor (x − {cand:g})")
            found.append(cand)
            bring = [coeffs[0]]
            for i in range(1, len(coeffs)):
                bring.append(coeffs[i] + bring[-1] * cand)
            reduced = bring[:-1]
            working(f"{indent}Reduced:  {poly_str(reduced)}")
            return _full_factor(reduced, depth+1, found)
    print(f"{indent}{c(C.GREY,'No more rational roots for')} {poly_str(coeffs)}")
    return found

# ── 6. Multiplicity ───────────────────────────────────────────────────────────

def multiplicity():
    clear(); header("ROOT MULTIPLICITY ANALYSIS")
    coeffs = _get_poly()
    degree = len(coeffs) - 1
    note("Testing rational roots for multiplicity...\n")

    root_mult = {}
    const = int(abs(coeffs[-1])) if coeffs[-1] != 0 else 1
    lead  = int(abs(coeffs[0]))
    cands = sorted({p/q for p in _factors_int(const) for q in _factors_int(lead)} |
                   {-p/q for p in _factors_int(const) for q in _factors_int(lead)})

    working = list(coeffs)
    for cand in cands:
        mult = 0
        while len(working) > 1 and abs(poly_eval(working, cand)) < 1e-8:
            mult += 1
            bring = [working[0]]
            for i in range(1, len(working)):
                bring.append(working[i] + bring[-1] * cand)
            working = bring[:-1]
        if mult > 0:
            root_mult[cand] = mult

    if not root_mult:
        note("No rational roots found."); pause(); return

    step(1, "Root multiplicity table")
    print(f"\n  {c(C.GREY,'Root x ='):>16}  {c(C.GREY,'Mult'):>6}  {c(C.GREY,'Behaviour at root')}")
    sep('-', 52)
    for r, m in sorted(root_mult.items()):
        beh = c(C.CYAN,"touches & turns (even)") if m%2==0 else c(C.GREEN,"crosses x-axis (odd)")
        print(f"  {c(C.YELLOW,f'{r:>12g}')}      {c(C.WHITE,str(m)):>6}  {beh}")

    total = sum(root_mult.values())
    note(f"Sum of multiplicities: {total}  (degree = {degree})")
    if total < degree:
        note(f"Remaining degree {degree-total}: irrational or complex roots.")
    pause()

# ── 7. Graph ──────────────────────────────────────────────────────────────────

def graph_poly():
    clear(); header("GRAPH POLYNOMIAL")
    if not require_plotly(): pause(); return
    import numpy as np

    coeffs = _get_poly()
    degree = len(coeffs) - 1

    # Find rational roots
    const = int(abs(coeffs[-1])) if coeffs[-1] != 0 else 1
    lead  = int(abs(coeffs[0]))
    cands = sorted({p/q for p in _factors_int(const) for q in _factors_int(lead)} |
                   {-p/q for p in _factors_int(const) for q in _factors_int(lead)})
    roots = [r for r in cands if abs(poly_eval(coeffs, r)) < 1e-8]

    x = np.linspace(-10, 10, 1000)
    y = np.polyval(coeffs, x)
    y_clipped = np.where(np.abs(y) > 60, np.nan, y)

    title = f"P(x) = {poly_str(coeffs)}  (degree {degree})"
    fig = make_plotly_fig(title)
    add_curve(fig, x, y_clipped, name=f"P(x)", colour=PC['primary'])

    # y-intercept
    yi = poly_eval(coeffs, 0)
    add_scatter_point(fig, 0, yi, name=f"y-intercept", colour=PC['orange'])

    # Roots
    for r in roots:
        add_scatter_point(fig, r, 0, name=f"root x={fmt_plain(r)}", colour=PC['green'])

    finite_y = y_clipped[np.isfinite(y_clipped)]
    ylo = max(float(finite_y.min()) - 1, -60) if len(finite_y) else -12
    yhi = min(float(finite_y.max()) + 1,  60) if len(finite_y) else  12
    show_plotly(fig, ymin=ylo, ymax=yhi)
    pause()

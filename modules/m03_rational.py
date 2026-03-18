# modules/m03_rational.py  —  Rational Functions
from .utils import *
from .utils import _factors_of
import math

def run():
    while True:
        clear(); header("RATIONAL FUNCTIONS   f(x) = P(x) / Q(x)")
        print("  1  Find vertical asymptotes & holes")
        print("  2  Find horizontal / oblique asymptotes")
        print("  3  Find x- and y-intercepts")
        print("  4  Full analysis (all of the above)")
        print("  5  Solve rational equation  P(x)/Q(x) = c")
        print("  6  Graph rational function")
        print("  0  Back")
        sep()
        ch = input("  Choose: ").strip()
        if ch == '1': vert_asymptotes()
        elif ch == '2': horiz_asymptotes()
        elif ch == '3': intercepts()
        elif ch == '4': full_analysis()
        elif ch == '5': solve_rational()
        elif ch == '6': graph_rational()
        elif ch == '0': break
        else: warn("Invalid."); pause()

def _get_num_den():
    note("Enter numerator polynomial (highest → lowest degree).")
    num = get_poly("  Numerator coefficients: ")
    note("Enter denominator polynomial.")
    den = get_poly("  Denominator coefficients: ")
    return num, den

def _poly_roots_real(coeffs):
    degree = len(coeffs) - 1
    roots = []
    if degree == 1:
        a, b = coeffs
        if a != 0: roots.append(-b / a)
    elif degree == 2:
        a, b, cv = coeffs
        disc = b**2 - 4*a*cv
        if disc >= 0:
            roots.append((-b + math.sqrt(disc)) / (2*a))
            roots.append((-b - math.sqrt(disc)) / (2*a))
    else:
        const = int(abs(coeffs[-1])) if coeffs[-1] != 0 else 1
        lead  = int(abs(coeffs[0]))
        cands = {p/q for p in _factors_of(const) for q in _factors_of(lead)}
        cands |= {-v for v in cands}
        for cand in cands:
            if abs(poly_eval(coeffs, cand)) < 1e-8:
                roots.append(cand)
    return sorted(set(round(r, 8) for r in roots))

def _poly_gcd_roots(num, den):
    nr = set(round(r, 8) for r in _poly_roots_real(num))
    dr = set(round(r, 8) for r in _poly_roots_real(den))
    return sorted(nr & dr)

def _cancel_factor(coeffs, root):
    res = [coeffs[0]]
    for i in range(1, len(coeffs)):
        res.append(coeffs[i] + res[-1] * root)
    return res[:-1]

def _analyse_vert(num, den, verbose=True):
    if verbose:
        step(1, "Find zeros of denominator Q(x)")
    den_roots = _poly_roots_real(den)
    if verbose:
        working(f"Q(x) = {poly_str(den)}")
        working(f"Zeros: {[f'{r:g}' for r in den_roots] if den_roots else 'none'}")

    if verbose:
        step(2, "Check which are also zeros of numerator (→ holes)")
    holes = _poly_gcd_roots(num, den)
    vas   = [r for r in den_roots if r not in holes]

    if verbose:
        for h in holes:
            n2 = _cancel_factor(list(num), h)
            d2 = _cancel_factor(list(den), h)
            yh = poly_eval(n2, h) / poly_eval(d2, h) if poly_eval(d2, h) != 0 else float('nan')
            ok(f"{c(C.ORANGE,'Hole')} at  ({fmt(h)}, {fmt(yh)})  — factor (x − {fmt_plain(h)}) cancels")
        if not holes:
            note("No common factors — no holes.")
        for v in vas:
            ok(f"{c(C.RED,'Vertical asymptote')}:  x = {v:g}")
        if not vas:
            note("No vertical asymptotes.")
    return holes, vas

def _poly_long_div(num, den):
    num = list(num)
    den = list(den)
    if len(num) < len(den): return [0], num
    quot = []
    while len(num) >= len(den):
        coeff = num[0] / den[0]
        quot.append(coeff)
        for i in range(len(den)):
            num[i] -= coeff * den[i]
        num = num[1:]
    return quot, num

def _analyse_horiz(num, den, verbose=True):
    n = len(num) - 1
    m = len(den) - 1
    if verbose:
        step(1 if not verbose else 1, "Compare degrees")
        working(f"deg(P) = {n},   deg(Q) = {m}")
    if n < m:
        if verbose: ok(f"{c(C.CYAN,'Horizontal asymptote')}: y = 0  (deg P < deg Q)")
        return 0, None
    elif n == m:
        ha = num[0] / den[0]
        if verbose:
            working(f"y = leading ratio = {num[0]:g} / {den[0]:g} = {fmt(num[0]/den[0])}")
            ok(f"{c(C.CYAN,'Horizontal asymptote')}: y = {fmt(ha)}")
        return ha, None
    elif n == m + 1:
        quot, rem = _poly_long_div(num, den)
        if verbose:
            working(f"Quotient: {poly_str(quot)}")
            ok(f"{c(C.CYAN,'Oblique asymptote')}: y = {poly_str(quot)}")
        return None, quot
    else:
        if verbose: note("No horizontal or oblique asymptote.")
        return None, None

def vert_asymptotes():
    clear(); header("VERTICAL ASYMPTOTES & HOLES")
    num, den = _get_num_den()
    sep(); _analyse_vert(num, den, verbose=True); pause()

def horiz_asymptotes():
    clear(); header("HORIZONTAL & OBLIQUE ASYMPTOTES")
    num, den = _get_num_den()
    sep(); _analyse_horiz(num, den, verbose=True); pause()

def intercepts():
    clear(); header("INTERCEPTS OF RATIONAL FUNCTION")
    num, den = _get_num_den(); sep()

    step(1, "y-intercept: f(0) = P(0)/Q(0)")
    p0 = poly_eval(num, 0); q0 = poly_eval(den, 0)
    if abs(q0) < 1e-12:
        note("Q(0) = 0 — no y-intercept (or is a hole).")
    else:
        ok(f"{c(C.ORANGE,'y-intercept')}: (0, {fmt(p0/q0)})")

    step(2, "x-intercepts: zeros of P(x) not shared with Q(x)")
    num_roots = _poly_roots_real(num)
    holes = _poly_gcd_roots(num, den)
    xi = [r for r in num_roots if r not in holes]
    if xi:
        for x in xi:
            ok(f"{c(C.GREEN,'x-intercept')}: ({fmt(x)}, 0)")
    else:
        note("No x-intercepts.")
    pause()

def full_analysis():
    clear(); header("FULL RATIONAL FUNCTION ANALYSIS")
    num, den = _get_num_den()
    sep()
    print(f"\n  {c(C.WHITE,'f(x)')} = {c(C.YELLOW, f'[{poly_str(num)}]')} / {c(C.YELLOW, f'[{poly_str(den)}]')}\n")
    sep()

    print(f"\n  {c(C.BOLD+C.WHITE,'── HOLES & VERTICAL ASYMPTOTES ──')}")
    holes, vas = _analyse_vert(num, den, verbose=True)

    print(f"\n  {c(C.BOLD+C.WHITE,'── HORIZONTAL / OBLIQUE ASYMPTOTE ──')}")
    ha, oa = _analyse_horiz(num, den, verbose=True)

    print(f"\n  {c(C.BOLD+C.WHITE,'── INTERCEPTS ──')}")
    p0 = poly_eval(num, 0); q0 = poly_eval(den, 0)
    if abs(q0) > 1e-12:
        ok(f"{c(C.ORANGE,'y-intercept')}: (0, {fmt(p0/q0)})")
    else:
        note("No y-intercept.")
    xi = [r for r in _poly_roots_real(num) if r not in holes]
    for x in xi:
        ok(f"{c(C.GREEN,'x-intercept')}: ({fmt(x)}, 0)")

    print(f"\n  {c(C.BOLD+C.WHITE,'── DOMAIN ──')}")
    excluded = sorted(set(holes + vas))
    if excluded:
        parts = ",  ".join([f"x ≠ {v:g}" for v in excluded])
        ok(f"All reals,  {c(C.RED, parts)}")
    else:
        ok("All real numbers")

    sep()
    # Summary box
    summary_pairs = []
    if vas:   summary_pairs += [(f"VA", f"x = {v:g}") for v in vas]
    if holes: summary_pairs += [(f"Hole", f"({h:g}, ...)") for h in holes]
    if ha is not None: summary_pairs.append(("HA", f"y = {fmt_plain(ha)}"))
    if oa is not None: summary_pairs.append(("OA", f"y = {poly_str(oa)}"))
    if summary_pairs:
        results(*summary_pairs)
    pause()

def solve_rational():
    clear(); header("SOLVE RATIONAL EQUATION   P(x)/Q(x) = c")
    note("Cross-multiplies: P(x) − c·Q(x) = 0\n")
    num, den = _get_num_den()
    cv = get_float("\n  Right-hand side c = ")

    n, d = list(num), list(den)
    while len(n) < len(d): n.insert(0, 0)
    while len(d) < len(n): d.insert(0, 0)
    combined = [ni - cv * di for ni, di in zip(n, d)]

    step(1, "Cross-multiply and rearrange")
    working(f"{poly_str(num)} = {cv:g} · ({poly_str(den)})")
    working(f"{poly_str(combined)} = 0")

    step(2, "Find roots of combined polynomial")
    roots = _poly_roots_real(combined)

    step(3, "Check for extraneous solutions")
    valid = []
    for r in roots:
        qval = poly_eval(den, r)
        if abs(qval) > 1e-9:
            valid.append(r)
            ok(f"x = {c(C.YELLOW, fmt_plain(r))}  →  Q({fmt_plain(r)}) = {fmt_plain(qval)} ≠ 0  ✓")
        else:
            warn(f"x = {r:g}  →  EXTRANEOUS (causes division by zero)")

    if valid:
        results(*[("Solution", f"x = {fmt_plain(r)}") for r in valid])
    else:
        warn("No valid solutions.")
    pause()

def graph_rational():
    clear(); header("GRAPH RATIONAL FUNCTION")
    if not require_plotly(): pause(); return
    import numpy as np

    num, den = _get_num_den()
    holes, vas = _analyse_vert(num, den, verbose=False)
    ha, oa = _analyse_horiz(num, den, verbose=False)

    # Split curve at asymptotes so lines don't jump across them
    x_full = np.linspace(-10, 10, 4000)
    breakpoints = sorted(vas + [-10, 10])
    segments = []
    for i in range(len(breakpoints) - 1):
        lo = breakpoints[i] + 0.001
        hi = breakpoints[i+1] - 0.001
        if hi > lo:
            xseg = np.linspace(lo, hi, 800)
            segments.append(xseg)

    title = f"f(x) = ({poly_str(num)}) / ({poly_str(den)})"
    fig = make_plotly_fig(title)

    for i, xseg in enumerate(segments):
        with np.errstate(divide='ignore', invalid='ignore'):
            p = np.polyval(num, xseg)
            q = np.polyval(den, xseg)
            yseg = np.where(np.abs(q) > 1e-9, p / q, np.nan)
        yseg[np.abs(yseg) > 25] = np.nan
        show_legend = (i == 0)
        fig.add_trace(__import__('plotly.graph_objects', fromlist=['Scatter']).Scatter(
            x=xseg, y=yseg,
            mode='lines',
            name='f(x)' if show_legend else '',
            showlegend=show_legend,
            line=dict(color=PC['primary'], width=2.5),
            hovertemplate='x = %{x:.4f}<br>y = %{y:.4f}<extra>f(x)</extra>',
        ))

    # Asymptotes
    for v in vas:
        add_vasymptote(fig, v)
    if ha is not None:
        add_hasymptote(fig, ha)

    # x-intercepts
    xi = [r for r in _poly_roots_real(num) if r not in holes]
    for r in xi:
        add_scatter_point(fig, r, 0, name=f"x-int ({fmt_plain(r)}, 0)", colour=PC['green'])

    # y-intercept
    q0 = poly_eval(den, 0)
    if abs(q0) > 1e-12:
        yi = poly_eval(num, 0) / q0
        add_scatter_point(fig, 0, yi, name=f"y-int (0, {fmt_plain(yi)})", colour=PC['orange'])

    # Holes
    for h in holes:
        n2 = _cancel_factor(list(num), h)
        d2 = _cancel_factor(list(den), h)
        yh = poly_eval(n2, h) / poly_eval(d2, h) if poly_eval(d2, h) != 0 else 0
        add_hole_point(fig, h, yh)

    show_plotly(fig, ymin=-15, ymax=15)
    pause()

# modules/m01_transformations.py  —  Function Transformations
from .utils import *

# ── Sub-menu ──────────────────────────────────────────────────────────────────

def run():
    while True:
        clear(); header("FUNCTION TRANSFORMATIONS   y = a·f(b(x−h)) + k")
        print("  1  Describe transformations from parameters")
        print("  2  Map key points through a transformation")
        print("  3  Identify transformation from two points")
        print("  0  Back")
        sep()
        ch = input("  Choose: ").strip()
        if ch == '1': describe_transformations()
        elif ch == '2': map_points()
        elif ch == '3': identify_from_points()
        elif ch == '0': break
        else: warn("Invalid choice."); pause()

# ── 1. Describe transformations ───────────────────────────────────────────────

PARENT_FUNCTIONS = {
    'linear':      'y = x',
    'quadratic':   'y = x²',
    'cubic':       'y = x³',
    'sqrt':        'y = √x',
    'abs':         'y = |x|',
    'rational':    'y = 1/x',
    'exponential': 'y = bˣ (b>1)',
    'log':         'y = log(x)',
    'sin':         'y = sin(x)',
    'cos':         'y = cos(x)',
    'tan':         'y = tan(x)',
}

def describe_transformations():
    clear(); header("DESCRIBE TRANSFORMATIONS")
    print("  Parent function types:")
    for k, v in PARENT_FUNCTIONS.items():
        print(f"    {k:<14} {v}")
    print()
    fn = input("  Parent function: ").strip().lower()
    if fn not in PARENT_FUNCTIONS:
        warn("Unknown function type."); pause(); return

    print()
    note("Enter parameters for  y = a·f(b(x−h)) + k")
    note("Leave blank for default (a=1, b=1, h=0, k=0). Fractions OK (e.g. 1/2).\n")

    a = get_float("a (vertical stretch/reflect) [1]: ", fallback=1.0)
    b = get_float("b (horizontal stretch/reflect) [1]: ", fallback=1.0)
    h = get_float("h (horizontal shift) [0]: ", fallback=0.0)
    k = get_float("k (vertical shift) [0]: ", fallback=0.0)

    sep()
    print(f"\n  Function:  y = {a:g}·{fn}({b:g}·(x − {h:g})) + {k:g}")
    print(f"  Parent:    {PARENT_FUNCTIONS[fn]}\n")
    sep()

    steps = []

    # ── a ──
    step(1, "Analyze 'a' (vertical)")
    if a == 1:
        ok("a = 1 → No vertical stretch or reflection.")
    else:
        if a < 0:
            ok(f"a < 0 → Reflection over the x-axis.")
        if abs(a) > 1:
            ok(f"|a| = {abs(a):g} > 1 → Vertical STRETCH by factor {abs(a):g}.")
            ok(f"   Every y-value is multiplied by {abs(a):g}.")
        elif abs(a) < 1:
            ok(f"|a| = {abs(a):g} < 1 → Vertical COMPRESSION by factor {abs(a):g}.")
            ok(f"   Every y-value is multiplied by {abs(a):g}.")

    # ── b ──
    step(2, "Analyze 'b' (horizontal)")
    if b == 1:
        ok("b = 1 → No horizontal stretch or reflection.")
    else:
        if b < 0:
            ok(f"b < 0 → Reflection over the y-axis.")
        factor = 1 / abs(b)
        if abs(b) > 1:
            ok(f"|b| = {abs(b):g} > 1 → Horizontal COMPRESSION by factor {factor:g}.")
            ok(f"   Every x-value is multiplied by {factor:g}.")
        elif abs(b) < 1:
            ok(f"|b| = {abs(b):g} < 1 → Horizontal STRETCH by factor {factor:g}.")
            ok(f"   Every x-value is multiplied by {factor:g}.")

    # ── h ──
    step(3, "Analyze 'h' (horizontal shift)")
    if h == 0:
        ok("h = 0 → No horizontal translation.")
    elif h > 0:
        ok(f"h = {h:g} → Shift {h:g} units to the RIGHT.")
        note("   Inside the function: (x − h), positive h → right.")
    else:
        ok(f"h = {h:g} → Shift {abs(h):g} units to the LEFT.")

    # ── k ──
    step(4, "Analyze 'k' (vertical shift)")
    if k == 0:
        ok("k = 0 → No vertical translation.")
    elif k > 0:
        ok(f"k = {k:g} → Shift {k:g} units UP.")
    else:
        ok(f"k = {k:g} → Shift {abs(k):g} units DOWN.")

    # ── Domain / Range hints ──
    step(5, "Domain & Range notes")
    _domain_range_hint(fn, a, b, h, k)

    # ── Optional graph ──
    if require_graph():
        if get_choice("Show graph?", ["y", "n"]) == "y":
            _graph_transform(fn, a, b, h, k)

    pause()


def _domain_range_hint(fn, a, b, h, k):
    hints = {
        'sqrt':        (f"x ≥ {h:g}",           f"y ≥ {k:g}"),
        'log':         (f"x > {h:g}",            "all reals"),
        'rational':    (f"x ≠ {h:g}",            f"y ≠ {k:g}"),
        'exponential': ("all reals",             f"y > {k:g}"),
        'quadratic':   ("all reals",             f"y ≥ {k:g}" if a > 0 else f"y ≤ {k:g}"),
    }
    if fn in hints:
        d, r = hints[fn]
        note(f"Domain (approx): {d}")
        note(f"Range  (approx): {r}")
    else:
        note("Domain/Range: depends on parent function restrictions.")


def _graph_transform(fn, a, b, h, k):
    import numpy as np
    import matplotlib.pyplot as plt

    x = np.linspace(-10, 10, 800)
    # Parent
    xp, yp = _compute_fn(fn, x, 1, 1, 0, 0)
    xt, yt = _compute_fn(fn, x, a, b, h, k)

    fig = make_plotly_fig(title=f'Transformation of {fn}')
    if xp is not None:
        add_curve(fig, xp, yp, name='Parent', colour=PC['secondary'], dash='dash', width=1.5)
    if xt is not None:
        add_curve(fig, xt, yt, name=f'y={a:g}·{fn}({b:g}(x−{h:g}))+{k:g}', colour=PC['primary'])
    show_plotly(fig, ymin=-10, ymax=10)


def _compute_fn(fn, x, a, b, h, k):
    import numpy as np
    inner = b * (x - h)
    try:
        if fn == 'linear':      y = a * inner + k
        elif fn == 'quadratic': y = a * inner**2 + k
        elif fn == 'cubic':     y = a * inner**3 + k
        elif fn == 'sqrt':
            mask = inner >= 0
            y = np.where(mask, a * np.sqrt(np.maximum(inner, 0)) + k, np.nan)
        elif fn == 'abs':       y = a * np.abs(inner) + k
        elif fn == 'rational':
            with np.errstate(divide='ignore', invalid='ignore'):
                y = np.where(inner != 0, a / inner + k, np.nan)
        elif fn == 'exponential': y = a * np.exp(inner * 0.693) + k  # base 2
        elif fn == 'log':
            y = np.where(inner > 0, a * np.log(np.maximum(inner, 1e-10)) + k, np.nan)
        elif fn == 'sin':       y = a * np.sin(inner) + k
        elif fn == 'cos':       y = a * np.cos(inner) + k
        elif fn == 'tan':
            y = a * np.tan(inner) + k
            y[np.abs(y) > 15] = np.nan
        else: return None, None
        return x, y
    except Exception:
        return None, None

# ── 2. Map key points ─────────────────────────────────────────────────────────

def map_points():
    clear(); header("MAP KEY POINTS THROUGH TRANSFORMATION")
    note("Enter the parent key points, then the transformation parameters.")
    note("The tool will show the mapped (image) points step by step.\n")

    n = get_int("How many key points? ", fallback=3)
    points = []
    for i in range(n):
        print(f"\n  Point {i+1}:")
        px = get_float("  x: ")
        py = get_float("  y: ")
        points.append((px, py))

    print()
    a = get_float("a [1]: ", fallback=1.0)
    b = get_float("b [1]: ", fallback=1.0)
    h = get_float("h [0]: ", fallback=0.0)
    k = get_float("k [0]: ", fallback=0.0)

    sep()
    print(f"\n  Mapping rule:  (x, y) → (x/|b| + h,  a·y + k)\n")
    print(f"  {'Original':^18}  {'→':^4}  {'Image':^18}")
    sep()

    for px, py in points:
        nx = px * (1 / abs(b)) + h if b != 0 else px
        ny = a * py + k
        root_note = "  ← root" if round(ny, 8) == 0 else ""
        print(f"  ({px:>7g}, {py:>7g})       ({nx:>7g}, {ny:>7g}){root_note}")

    pause()

# ── 3. Identify from two points ───────────────────────────────────────────────

def identify_from_points():
    clear(); header("IDENTIFY VERTICAL STRETCH & SHIFT FROM POINTS")
    note("Given two image points on  y = a·f(x) + k, solve for a and k.")
    note("You provide f(x₁) and f(x₂) (parent values) and the image y-values.\n")

    print("  Parent point 1:")
    fx1 = get_float("  f(x₁) = ")
    y1  = get_float("  Image y₁ = ")

    print("\n  Parent point 2:")
    fx2 = get_float("  f(x₂) = ")
    y2  = get_float("  Image y₂ = ")

    sep()
    if fx1 == fx2:
        warn("f(x₁) and f(x₂) are equal — cannot solve unique system."); pause(); return

    step(1, "Set up the system")
    print(f"     y = a·f(x) + k")
    print(f"     {y1:g} = a·({fx1:g}) + k    ... (i)")
    print(f"     {y2:g} = a·({fx2:g}) + k    ... (ii)")

    step(2, "Subtract (i) from (ii) to eliminate k")
    diff_y  = y2 - y1
    diff_fx = fx2 - fx1
    print(f"     {y2:g} − {y1:g} = a·({fx2:g} − {fx1:g})")
    print(f"     {diff_y:g} = a·({diff_fx:g})")

    step(3, "Solve for a")
    a = diff_y / diff_fx
    print(f"     a = {diff_y:g} / {diff_fx:g} = {a:g}")

    step(4, "Substitute a back to find k")
    k = y1 - a * fx1
    print(f"     k = {y1:g} − ({a:g})·({fx1:g}) = {k:g}")

    result("Solution", f"a = {a:g},   k = {k:g}")
    note(f"Transformed function:  y = {a:g}·f(x) + {k:g}")

    pause()
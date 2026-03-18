# modules/m05_trig_functions.py  —  Trigonometric Functions
from .utils import *
import math

TRIG_FNS = {
    'sin': math.sin, 'cos': math.cos, 'tan': math.tan,
    'sec': lambda x: 1/math.cos(x), 'csc': lambda x: 1/math.sin(x),
    'cot': lambda x: math.cos(x)/math.sin(x),
}

def run():
    while True:
        clear(); header("TRIGONOMETRIC FUNCTIONS")
        print("  1  Evaluate trig function at an angle")
        print("  2  Describe graph parameters (amplitude, period, phase shift)")
        print("  3  Reciprocal trig functions reference")
        print("  4  Unit circle values (common angles)")
        print("  5  Graph sin / cos / tan (with transformations)")
        print("  6  Graph reciprocal functions (sec, csc, cot)")
        print("  0  Back")
        sep()
        ch = input("  Choose: ").strip()
        if ch == '1': evaluate_trig()
        elif ch == '2': graph_params()
        elif ch == '3': reciprocal_ref()
        elif ch == '4': unit_circle()
        elif ch == '5': graph_trig()
        elif ch == '6': graph_reciprocal()
        elif ch == '0': break
        else: warn("Invalid."); pause()

# ── 1. Evaluate ───────────────────────────────────────────────────────────────

def evaluate_trig():
    clear(); header("EVALUATE TRIG FUNCTION")

    fn_str = input("  Function (sin/cos/tan/sec/csc/cot): ").strip().lower()
    if fn_str not in TRIG_FNS:
        warn("Unknown function."); pause(); return

    angle_type = get_choice("  Angle in", ["degrees", "radians"])
    angle = get_float("  Angle value: ")

    rad = math.radians(angle) if angle_type == "degrees" else angle
    deg = angle if angle_type == "degrees" else math.degrees(angle)

    sep()
    step(1, "Convert angle if needed")
    print(f"     {deg:.4f}°  =  {rad:.6f} rad")

    step(2, f"Evaluate {fn_str}")
    try:
        val = TRIG_FNS[fn_str](rad)
        if abs(val) > 1e12:
            warn(f"{fn_str}({deg:.2f}°) is undefined at this angle (asymptote).")
        else:
            result(f"{fn_str}({deg:.4g}°)", f"{val:.6f}")
    except ZeroDivisionError:
        warn(f"{fn_str}({deg:.2f}°) is undefined (division by zero).")

    pause()

# ── 2. Graph parameters ───────────────────────────────────────────────────────

def graph_params():
    clear(); header("GRAPH PARAMETERS FROM  y = a·f(bx − c) + d")
    note("Enter the 4 parameters:\n")

    fn_str = get_choice("  Function", ["sin", "cos", "tan"])
    a = get_float("  a (amplitude factor) [1]: ", fallback=1.0)
    b = get_float("  b (period factor) [1]: ", fallback=1.0)
    c = get_float("  c (phase shift numerator) [0]: ", fallback=0.0)
    d = get_float("  d (vertical shift) [0]: ", fallback=0.0)

    sep()
    step(1, "Amplitude")
    amp = abs(a)
    if fn_str in ('sin', 'cos'):
        ok(f"Amplitude = |a| = |{a:g}| = {amp:g}")
        ok(f"Range: [{d - amp:g}, {d + amp:g}]")
    else:
        note("tan has no amplitude (unbounded).")

    step(2, "Period")
    if fn_str in ('sin', 'cos'):
        base_period = 2 * math.pi
    else:
        base_period = math.pi
    period = base_period / abs(b) if b != 0 else float('inf')
    print(f"     Base period of {fn_str}: {base_period:.4f} rad")
    print(f"     Period = base period / |b| = {base_period:.4f} / {abs(b):g} = {period:.4f} rad")
    ok(f"Period = {period:.4f} rad  ≈  {math.degrees(period):.2f}°")

    step(3, "Phase shift")
    if b != 0:
        ps = c / b
        direction = "right" if ps > 0 else "left"
        print(f"     Phase shift = c / b = {c:g} / {b:g} = {ps:g}")
        ok(f"Shift {abs(ps):g} rad to the {direction}")
    else:
        note("b = 0: undefined phase shift.")

    step(4, "Vertical shift")
    if d == 0:
        ok("No vertical shift.")
    else:
        ok(f"Vertical shift: {d:g} {'up' if d > 0 else 'down'}")

    step(5, "Key points summary")
    note(f"y = {a:g}·{fn_str}({b:g}x − {c:g}) + {d:g}")
    note(f"Midline: y = {d:g}")
    if fn_str in ('sin', 'cos'):
        note(f"Max: y = {d + amp:g},   Min: y = {d - amp:g}")

    pause()

# ── 3. Reciprocal reference ───────────────────────────────────────────────────

def reciprocal_ref():
    clear(); header("RECIPROCAL TRIG FUNCTIONS — REFERENCE")
    sep()
    print("""
  ┌──────────────────────────────────────────────────┐
  │  sec(x)  = 1/cos(x)    Domain: cos(x) ≠ 0       │
  │  csc(x)  = 1/sin(x)    Domain: sin(x) ≠ 0       │
  │  cot(x)  = cos(x)/sin(x) = 1/tan(x)             │
  │            Domain: sin(x) ≠ 0                    │
  ├──────────────────────────────────────────────────┤
  │  Pythagorean Identities:                         │
  │    sin²x + cos²x = 1                             │
  │    1 + tan²x     = sec²x                         │
  │    1 + cot²x     = csc²x                         │
  ├──────────────────────────────────────────────────┤
  │  Key: sec & csc have range (−∞,−1] ∪ [1,+∞)     │
  │       cot has period π (same as tan)             │
  └──────────────────────────────────────────────────┘
""")
    note("Evaluate a reciprocal function:")
    fn_str = get_choice("  Function", ["sec", "csc", "cot", "skip"])
    if fn_str == "skip": pause(); return

    angle_type = get_choice("  Angle in", ["degrees", "radians"])
    angle = get_float("  Angle: ")
    rad = math.radians(angle) if angle_type == "degrees" else angle
    try:
        val = TRIG_FNS[fn_str](rad)
        result(f"{fn_str}({angle:g}{'°' if angle_type == 'degrees' else ' rad'})", f"{val:.6f}")
    except ZeroDivisionError:
        warn("Undefined at this angle.")
    pause()

# ── 4. Unit circle ────────────────────────────────────────────────────────────

UNIT_CIRCLE = [
    (0,   "0",        1,       0),
    (30,  "π/6",      math.sqrt(3)/2, 1/2),
    (45,  "π/4",      math.sqrt(2)/2, math.sqrt(2)/2),
    (60,  "π/3",      1/2,     math.sqrt(3)/2),
    (90,  "π/2",      0,       1),
    (120, "2π/3",    -1/2,     math.sqrt(3)/2),
    (135, "3π/4",    -math.sqrt(2)/2, math.sqrt(2)/2),
    (150, "5π/6",    -math.sqrt(3)/2, 1/2),
    (180, "π",       -1,       0),
    (210, "7π/6",    -math.sqrt(3)/2, -1/2),
    (225, "5π/4",    -math.sqrt(2)/2, -math.sqrt(2)/2),
    (240, "4π/3",    -1/2,     -math.sqrt(3)/2),
    (270, "3π/2",     0,      -1),
    (300, "5π/3",     1/2,    -math.sqrt(3)/2),
    (315, "7π/4",     math.sqrt(2)/2, -math.sqrt(2)/2),
    (330, "11π/6",    math.sqrt(3)/2, -1/2),
    (360, "2π",       1,       0),
]

def unit_circle():
    clear(); header("UNIT CIRCLE — COMMON ANGLES")
    print(f"\n  {'Deg':>5}  {'Rad':>8}  {'cos':>12}  {'sin':>12}  {'tan':>14}")
    sep('-', 58)
    for deg, rad_str, c, s in UNIT_CIRCLE:
        if abs(c) < 1e-12:
            tan_str = "undefined"
        else:
            t = s / c
            tan_str = f"{t:.4f}"
        print(f"  {deg:>5}°  {rad_str:>8}  {c:>12.4f}  {s:>12.4f}  {tan_str:>14}")
    pause()

# ── 5 & 6. Graphs ─────────────────────────────────────────────────────────────

def _get_trig_params(reciprocal=False):
    if reciprocal:
        fn_str = get_choice("  Function", ["sec", "csc", "cot"])
    else:
        fn_str = get_choice("  Function", ["sin", "cos", "tan"])
    a = get_float("  a [1]: ", fallback=1.0)
    b = get_float("  b [1]: ", fallback=1.0)
    c = get_float("  c (phase, in radians) [0]: ", fallback=0.0)
    d = get_float("  d (vertical shift) [0]: ", fallback=0.0)
    return fn_str, a, b, c, d

def graph_trig():
    clear(); header("GRAPH TRIG FUNCTION   y = a·f(bx − c) + d")
    if not require_graph(): pause(); return
    fn_str, a, b, c, d = _get_trig_params()
    _draw_trig(fn_str, a, b, c, d)
    pause()

def graph_reciprocal():
    clear(); header("GRAPH RECIPROCAL TRIG FUNCTION")
    if not require_graph(): pause(); return
    fn_str, a, b, c, d = _get_trig_params(reciprocal=True)
    _draw_trig(fn_str, a, b, c, d)
    pause()

def _draw_trig(fn_str, a, b, c, d):
    import numpy as np
    import matplotlib.pyplot as plt

    x = np.linspace(-2*np.pi, 2*np.pi, 2000)
    inner = b * x - c

    with np.errstate(divide='ignore', invalid='ignore'):
        if fn_str == 'sin':   yr = np.sin(inner)
        elif fn_str == 'cos': yr = np.cos(inner)
        elif fn_str == 'tan': yr = np.tan(inner)
        elif fn_str == 'sec': yr = 1 / np.cos(inner)
        elif fn_str == 'csc': yr = 1 / np.sin(inner)
        elif fn_str == 'cot': yr = np.cos(inner) / np.sin(inner)

    y = a * yr + d
    y[np.abs(y) > 12] = np.nan

    # Parent curve (grey)
    if fn_str in ('sin', 'cos', 'tan'):
        yr_p = {'sin': np.sin(x), 'cos': np.cos(x), 'tan': np.tan(x)}[fn_str]
        yr_p[np.abs(yr_p) > 12] = np.nan
    else:
        yr_p = None

    # Midline
    period = (2*math.pi if fn_str in ('sin','cos','sec','csc') else math.pi) / abs(b) if b else 1
    amp = abs(a)

    title = f'y = {a:g}·{fn_str}({b:g}x − {c:g}) + {d:g}'
    fig = make_plotly_fig(title)

    if yr_p is not None:
        add_curve(fig, x, yr_p, name='Parent', colour=PC['secondary'], dash='dash', width=1.5)

    add_curve(fig, x, y, name=f'y={a:g}·{fn_str}({b:g}x−{c:g})+{d:g}', colour=PC['primary'])

    if fn_str in ('sin', 'cos'):
        add_hasymptote(fig, d, xmin=float(x[0]), xmax=float(x[-1]))

    # π-based x-axis tick labels
    import plotly.graph_objects as _go
    ticks = list(np.arange(-2*np.pi, 2*np.pi + 0.01, np.pi/2))
    tick_labels = [f'{v/np.pi:.2g}π' if abs(v) > 0.01 else '0' for v in ticks]
    fig.update_xaxes(tickvals=ticks, ticktext=tick_labels)

    show_plotly(fig, ymin=-10, ymax=10)

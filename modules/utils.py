# modules/utils.py  —  shared helpers for MegaCalc
import os
import math

# ══════════════════════════════════════════════════════════════════════════════
#  ANSI COLOUR CODES
# ══════════════════════════════════════════════════════════════════════════════

def _supports_colour():
    if os.name == 'nt':
        try:
            import ctypes
            kernel32 = ctypes.windll.kernel32
            kernel32.SetConsoleMode(kernel32.GetStdHandle(-11), 7)
            return True
        except Exception:
            return False
    return True

_USE_COLOUR = _supports_colour()

class C:
    RESET   = "\033[0m"  if _USE_COLOUR else ""
    BOLD    = "\033[1m"  if _USE_COLOUR else ""
    DIM     = "\033[2m"  if _USE_COLOUR else ""
    WHITE   = "\033[97m" if _USE_COLOUR else ""
    CYAN    = "\033[96m" if _USE_COLOUR else ""
    GREEN   = "\033[92m" if _USE_COLOUR else ""
    YELLOW  = "\033[93m" if _USE_COLOUR else ""
    RED     = "\033[91m" if _USE_COLOUR else ""
    ORANGE  = "\033[33m" if _USE_COLOUR else ""
    MAGENTA = "\033[95m" if _USE_COLOUR else ""
    BLUE    = "\033[94m" if _USE_COLOUR else ""
    GREY    = "\033[90m" if _USE_COLOUR else ""

def c(colour, text):
    return f"{colour}{text}{C.RESET}"

# ══════════════════════════════════════════════════════════════════════════════
#  TERMINAL LAYOUT
# ══════════════════════════════════════════════════════════════════════════════

WIDTH = 58

def clear():
    os.system('cls' if os.name == 'nt' else 'clear')

def sep(char='─', width=WIDTH):
    print(c(C.GREY, char * width))

def header(title):
    print()
    print(c(C.GREY, '═' * WIDTH))
    print(f"  {c(C.BOLD + C.WHITE, title)}")
    print(c(C.GREY, '═' * WIDTH))
    print()

def pause():
    print()
    input(c(C.GREY, "  Press Enter to continue..."))

_step_n = [0]

def reset_steps():
    _step_n[0] = 0

def step(n, text):
    if n is None:
        _step_n[0] += 1
        n = _step_n[0]
    else:
        _step_n[0] = n
    print()
    print(c(C.BOLD + C.CYAN, f"  ┌─ Step {n}:  {text}"))
    print(c(C.GREY,           f"  │"))

def result(label, value):
    """Big green answer box."""
    inner = f"  {label}:  {value}  "
    bar   = "─" * (len(inner) + 2)
    print()
    print(c(C.GREEN, f"  ╔{bar}╗"))
    print(c(C.GREEN, "  ║") + c(C.BOLD + C.WHITE, f"  {label}: ") + c(C.BOLD + C.GREEN, str(value)) + c(C.GREEN, "  ║"))
    print(c(C.GREEN, f"  ╚{bar}╝"))

def results(*pairs):
    """Multiple labelled results in one box."""
    if not pairs:
        return
    max_label = max(len(p[0]) for p in pairs)
    lines = [(lbl, val) for lbl, val in pairs]
    inner_w = max(len(f"  {lbl.rjust(max_label)}: {val}") for lbl, val in lines) + 4
    bar = "─" * inner_w
    print()
    print(c(C.GREEN, f"  ╔{bar}╗"))
    for lbl, val in lines:
        content = f"  {lbl.rjust(max_label)}: {val}"
        pad = " " * (inner_w - len(content))
        print(c(C.GREEN, "  ║") + c(C.BOLD + C.WHITE, f"  {lbl.rjust(max_label)}: ") + c(C.BOLD + C.GREEN, str(val)) + pad + c(C.GREEN, "║"))
    print(c(C.GREEN, f"  ╚{bar}╝"))

def note(text):
    print(c(C.GREY,  f"  ℹ  {text}"))

def warn(text):
    print(c(C.RED,   f"  ✗  {text}"))

def ok(text):
    print(c(C.GREEN, f"  ✓  ") + text)

def working(text):
    print(c(C.DIM, f"     {text}"))

def val_line(label, value, colour=None):
    colour = colour or C.YELLOW
    print(f"  {c(C.GREY, label + ':')}  {c(colour, str(value))}")

# ══════════════════════════════════════════════════════════════════════════════
#  INPUT HELPERS
# ══════════════════════════════════════════════════════════════════════════════

def get_float(prompt, fallback=None):
    while True:
        raw = input(f"  {c(C.CYAN, prompt)}").strip()
        if raw == "" and fallback is not None:
            return fallback
        try:
            if '/' in raw:
                n, d = raw.split('/', 1)
                return float(n) / float(d)
            return float(raw)
        except (ValueError, ZeroDivisionError):
            warn("Invalid — enter a number or fraction like 3/2.")

def get_int(prompt, fallback=None):
    while True:
        raw = input(f"  {c(C.CYAN, prompt)}").strip()
        if raw == "" and fallback is not None:
            return fallback
        try:
            return int(raw)
        except ValueError:
            warn("Invalid — enter a whole number.")

def get_choice(prompt, options):
    opts_display = " / ".join(c(C.YELLOW, o) for o in options)
    while True:
        raw = input(f"  {c(C.CYAN, prompt)} ({opts_display}): ").strip().lower()
        if raw in [o.lower() for o in options]:
            return raw
        warn(f"Choose one of: {' / '.join(options)}")

def get_poly(prompt="Enter coefficients highest→lowest (space-separated): "):
    while True:
        raw = input(f"  {c(C.CYAN, prompt)}").strip()
        try:
            coeffs = [float(x) for x in raw.split()]
            if coeffs:
                return coeffs
        except ValueError:
            pass
        warn("Invalid — enter space-separated numbers e.g. 1 -3 2")

# ══════════════════════════════════════════════════════════════════════════════
#  MATH HELPERS
# ══════════════════════════════════════════════════════════════════════════════

def poly_str(coeffs):
    degree = len(coeffs) - 1
    terms = []
    for i, cv in enumerate(coeffs):
        exp = degree - i
        if cv == 0:
            continue
        ca = abs(cv)
        sign = "+" if cv > 0 else "−"
        if exp == 0:   term = f"{ca:g}"
        elif exp == 1: term = f"{ca:g}x" if ca != 1 else "x"
        else:          term = f"{ca:g}x^{exp}" if ca != 1 else f"x^{exp}"
        terms.append((sign, term))
    if not terms:
        return "0"
    out = ("−" if terms[0][0] == "−" else "") + terms[0][1]
    for sign, term in terms[1:]:
        out += f" {sign} {term}"
    return out

def poly_eval(coeffs, x):
    val = 0
    for cv in coeffs:
        val = val * x + cv
    return val

def poly_derivative(coeffs):
    degree = len(coeffs) - 1
    if degree == 0:
        return [0]
    return [coeffs[i] * (degree - i) for i in range(degree)]

def gcd(a, b):
    a, b = int(abs(a)), int(abs(b))
    while b:
        a, b = b, a % b
    return a

def lcm(a, b):
    return abs(a * b) // gcd(a, b)

def factorial(n):
    if n < 0:
        raise ValueError("Factorial undefined for negatives")
    val = 1
    for i in range(2, n + 1):
        val *= i
    return val

def nCr(n, r):
    if r < 0 or r > n:
        return 0
    return factorial(n) // (factorial(r) * factorial(n - r))

def nPr(n, r):
    if r < 0 or r > n:
        return 0
    return factorial(n) // factorial(n - r)

def _factors_of(n):
    n = int(abs(n))
    return [i for i in range(1, n + 1) if n % i == 0]

# ══════════════════════════════════════════════════════════════════════════════
#  GRAPH HELPERS
# ══════════════════════════════════════════════════════════════════════════════

try:
    import numpy as np
    import matplotlib.pyplot as plt
    import matplotlib.ticker as ticker
    GRAPH_OK = True
except ImportError:
    GRAPH_OK = False

GCOL = {
    'bg_fig':   '#0d0d1a',
    'bg_ax':    '#12121f',
    'grid_maj': '#1e1e38',
    'grid_min': '#181828',
    'axis':     '#3a3a60',
    'tick':     '#5858a0',
    'label':    '#9090c0',
    'title':    '#e0e0ff',
    'primary':  '#7c6af7',
    'secondary':'#f7a26a',
    'green':    '#50e3a4',
    'red':      '#f76a6a',
    'orange':   '#f7d26a',
    'cyan':     '#6af7f7',
    'white':    '#e8e8ff',
    'bg_ax_c':  '#12121f',
}

def require_graph():
    if not GRAPH_OK:
        warn("numpy and matplotlib are required for graphs.")
        note("Run:  pip install numpy matplotlib")
        return False
    return True

def make_fig(title="", figsize=(10, 6)):
    """Create a polished dark figure. Returns (fig, ax)."""
    fig, ax = plt.subplots(figsize=figsize)
    fig.patch.set_facecolor(GCOL['bg_fig'])
    ax.set_facecolor(GCOL['bg_ax'])

    for spine in ax.spines.values():
        spine.set_edgecolor(GCOL['axis'])
        spine.set_linewidth(0.8)

    ax.tick_params(colors=GCOL['tick'], labelsize=9, length=4, which='both')
    ax.tick_params(length=2, which='minor')
    ax.xaxis.label.set_color(GCOL['label'])
    ax.yaxis.label.set_color(GCOL['label'])

    ax.grid(True, which='major', color=GCOL['grid_maj'], linewidth=0.7)
    ax.grid(True, which='minor', color=GCOL['grid_min'], linewidth=0.3)
    ax.minorticks_on()

    # Bold origin lines
    ax.axhline(0, color=GCOL['axis'], linewidth=1.2, zorder=2)
    ax.axvline(0, color=GCOL['axis'], linewidth=1.2, zorder=2)

    if title:
        ax.set_title(title, color=GCOL['title'], fontsize=11,
                     fontweight='bold', pad=14,
                     bbox=dict(boxstyle='round,pad=0.4', facecolor='#1a1a30',
                               edgecolor=GCOL['axis'], alpha=0.8))

    ax.set_xlabel("x", color=GCOL['label'], fontsize=10)
    ax.set_ylabel("y", color=GCOL['label'], fontsize=10, rotation=0, labelpad=12)

    return fig, ax

def add_legend(ax):
    handles, labels = ax.get_legend_handles_labels()
    if not labels:
        return
    leg = ax.legend(facecolor='#1a1a2e', edgecolor=GCOL['axis'],
                    labelcolor=GCOL['white'], fontsize=9,
                    framealpha=0.9, loc='best')
    for lh in leg.legend_handles:
        try:
            lh.set_linewidth(2.5)
        except Exception:
            pass

def mark_roots(ax, roots, y_fn=None):
    for r in roots:
        y = y_fn(r) if y_fn else 0
        ax.plot(r, y, 'o', color=GCOL['green'], markersize=9, zorder=6,
                markeredgecolor=GCOL['bg_ax'], markeredgewidth=1.5,
                label=f"root ({r:g}, {y:g})")
        ax.annotate(f" ({r:g}, {y:g})", xy=(r, y), fontsize=8,
                    color=GCOL['green'], xytext=(6, 8),
                    textcoords='offset points',
                    bbox=dict(boxstyle='round,pad=0.2', facecolor='#0d1a10',
                              edgecolor=GCOL['green'], alpha=0.7))

def mark_point(ax, x, y, label="", colour=None):
    colour = colour or GCOL['orange']
    ax.plot(x, y, 'o', color=colour, markersize=9, zorder=6,
            markeredgecolor=GCOL['bg_ax'], markeredgewidth=1.5)
    if label:
        ax.annotate(f" {label}", xy=(x, y), fontsize=8, color=colour,
                    xytext=(6, 6), textcoords='offset points',
                    bbox=dict(boxstyle='round,pad=0.2', facecolor=GCOL['bg_ax'],
                              edgecolor=colour, alpha=0.8))

def mark_hole(ax, x, y):
    ax.plot(x, y, 'o', color=GCOL['bg_ax'], markersize=11, zorder=6,
            markeredgecolor=GCOL['orange'], markeredgewidth=2.5)
    ax.annotate(f" hole ({x:g}, {y:g})", xy=(x, y), fontsize=8,
                color=GCOL['orange'], xytext=(8, 8), textcoords='offset points',
                bbox=dict(boxstyle='round,pad=0.2', facecolor='#1a1500',
                          edgecolor=GCOL['orange'], alpha=0.8))

def draw_vasymptote(ax, x, ymin=-12, ymax=12):
    ax.axvline(x, color=GCOL['red'], linewidth=1.2, linestyle='--',
               zorder=3, alpha=0.85, label=f"VA: x = {x:g}")
    ax.text(x + 0.12, ymax * 0.82, f"x = {x:g}",
            color=GCOL['red'], fontsize=8, va='top',
            bbox=dict(boxstyle='round,pad=0.2', facecolor='#1a0505',
                      edgecolor=GCOL['red'], alpha=0.8))

def draw_hasymptote(ax, y, xmin=-10, xmax=10):
    ax.axhline(y, color=GCOL['cyan'], linewidth=1.2, linestyle='--',
               zorder=3, alpha=0.85, label=f"HA: y = {y:g}")
    ax.text(xmax * 0.5, y + 0.25, f"y = {y:g}",
            color=GCOL['cyan'], fontsize=8,
            bbox=dict(boxstyle='round,pad=0.2', facecolor='#001a1a',
                      edgecolor=GCOL['cyan'], alpha=0.8))

def finalise(fig, ax, ymin=-12, ymax=12):
    ax.set_ylim(ymin, ymax)
    add_legend(ax)
    fig.tight_layout(pad=1.5)
    plt.show()

# Backward-compat alias
def style_axes(ax, fig):
    fig.patch.set_facecolor(GCOL['bg_fig'])
    ax.set_facecolor(GCOL['bg_ax'])
    ax.tick_params(colors=GCOL['tick'])
    ax.xaxis.label.set_color(GCOL['label'])
    ax.yaxis.label.set_color(GCOL['label'])
    ax.title.set_color(GCOL['title'])
    for spine in ax.spines.values():
        spine.set_edgecolor(GCOL['axis'])
    ax.axhline(0, color=GCOL['axis'], linewidth=0.8)
    ax.axvline(0, color=GCOL['axis'], linewidth=0.8)
    ax.grid(True, color=GCOL['grid_maj'], linewidth=0.5)

# ══════════════════════════════════════════════════════════════════════════════
#  FRACTION DISPLAY
# ══════════════════════════════════════════════════════════════════════════════

def _to_fraction(value, max_denom=1000):
    """
    Try to express a float as a simple fraction p/q.
    Returns (p, q) if found within tolerance, else None.
    """
    if not isinstance(value, float):
        return None
    # Already an integer
    if abs(value - round(value)) < 1e-9:
        return None
    # Search denominators 2..max_denom
    for q in range(2, max_denom + 1):
        p = round(value * q)
        if abs(p / q - value) < 1e-9:
            # Reduce by GCD
            g = gcd(abs(p), q)
            return (p // g, q // g)
    return None

def fmt(value, precision=6):
    """
    Format a number showing decimal + fraction if it's a 'nice' fraction.
    e.g.  0.666667  →  '0.666667  (= 2/3)'
          0.5       →  '0.5  (= 1/2)'
          2.0       →  '2'
          3.14159   →  '3.14159'   (no fraction — too complex)
    """
    if not isinstance(value, (int, float)):
        return str(value)
    # Integer — no decimal needed
    if isinstance(value, float) and abs(value - round(value)) < 1e-9:
        return f"{int(round(value))}"
    frac = _to_fraction(float(value))
    dec  = f"{value:.{precision}g}"
    if frac:
        p, q = frac
        return f"{dec}  {c(C.GREY, f'(= {p}/{q})')}"
    return dec

def fmt_plain(value, precision=6):
    """Like fmt() but returns plain string without ANSI codes (for labels/keys)."""
    if not isinstance(value, (int, float)):
        return str(value)
    if isinstance(value, float) and abs(value - round(value)) < 1e-9:
        return f"{int(round(value))}"
    frac = _to_fraction(float(value))
    dec  = f"{value:.{precision}g}"
    if frac:
        p, q = frac
        return f"{dec}  (= {p}/{q})"
    return dec

# ══════════════════════════════════════════════════════════════════════════════
#  PLOTLY GRAPH ENGINE
# ══════════════════════════════════════════════════════════════════════════════

try:
    import plotly.graph_objects as go
    import plotly.io as pio
    import numpy as np
    PLOTLY_OK = True
except ImportError:
    PLOTLY_OK = False

# Shared colour palette for Plotly graphs
PC = {
    'bg':        '#0d0d1a',
    'plot_bg':   '#12121f',
    'grid':      '#1e1e38',
    'axis':      '#3a3a60',
    'tick':      '#6060a0',
    'text':      '#c0c0e0',
    'title':     '#e0e0ff',
    'primary':   '#7c6af7',
    'secondary': '#f7a26a',
    'green':     '#50e3a4',
    'red':       '#f76a6a',
    'orange':    '#f7d26a',
    'cyan':      '#6af7f7',
    'white':     '#e8e8ff',
    'dim':       '#444466',
}

def require_plotly():
    if not PLOTLY_OK:
        warn("plotly and numpy are required for graphs.")
        note("Run:  pip install plotly numpy")
        return False
    return True

def _base_layout(title=""):
    """Return a dark Plotly layout dict."""
    return dict(
        title=dict(text=title, font=dict(color=PC['title'], size=14),
                   x=0.5, xanchor='center'),
        paper_bgcolor=PC['bg'],
        plot_bgcolor=PC['plot_bg'],
        font=dict(color=PC['text'], size=11),
        xaxis=dict(
            color=PC['tick'],
            gridcolor=PC['grid'],
            zerolinecolor=PC['axis'],
            zerolinewidth=1.5,
            showgrid=True,
            minor=dict(showgrid=True, gridcolor='#181828', gridwidth=0.4),
            title=dict(text='x', font=dict(color=PC['tick'])),
        ),
        yaxis=dict(
            color=PC['tick'],
            gridcolor=PC['grid'],
            zerolinecolor=PC['axis'],
            zerolinewidth=1.5,
            showgrid=True,
            minor=dict(showgrid=True, gridcolor='#181828', gridwidth=0.4),
            title=dict(text='y', font=dict(color=PC['tick'])),
        ),
        legend=dict(
            bgcolor='#1a1a2e',
            bordercolor=PC['axis'],
            borderwidth=1,
            font=dict(color=PC['white']),
        ),
        hovermode='x unified',
        hoverlabel=dict(
            bgcolor='#1a1a30',
            bordercolor=PC['primary'],
            font=dict(color=PC['white'], size=12),
        ),
        margin=dict(l=60, r=40, t=60, b=60),
    )

def make_plotly_fig(title=""):
    """Create a base Plotly Figure with dark theme."""
    fig = go.Figure()
    fig.update_layout(**_base_layout(title))
    return fig

def add_curve(fig, x, y, name, colour=None, dash='solid', width=2.5):
    colour = colour or PC['primary']
    fig.add_trace(go.Scatter(
        x=x, y=y,
        mode='lines',
        name=name,
        line=dict(color=colour, width=width, dash=dash),
        hovertemplate=f'<b>{name}</b><br>x = %{{x:.4f}}<br>y = %{{y:.4f}}<extra></extra>',
    ))

def add_scatter_point(fig, x, y, name, colour=None, symbol='circle', size=10):
    colour = colour or PC['green']
    fig.add_trace(go.Scatter(
        x=[x], y=[y],
        mode='markers+text',
        name=name,
        marker=dict(color=colour, size=size, symbol=symbol,
                    line=dict(color=PC['bg'], width=2)),
        text=[f'  ({fmt_plain(x)}, {fmt_plain(y)})'],
        textposition='middle right',
        textfont=dict(color=colour, size=10),
        hovertemplate=f'<b>{name}</b><br>({fmt_plain(x)}, {fmt_plain(y)})<extra></extra>',
    ))

def add_hole_point(fig, x, y):
    """Open circle for a hole in a rational function."""
    fig.add_trace(go.Scatter(
        x=[x], y=[y],
        mode='markers+text',
        name=f'Hole ({fmt_plain(x)}, {fmt_plain(y)})',
        marker=dict(color=PC['bg'], size=12, symbol='circle',
                    line=dict(color=PC['orange'], width=2.5)),
        text=[f'  hole ({fmt_plain(x)}, {fmt_plain(y)})'],
        textposition='middle right',
        textfont=dict(color=PC['orange'], size=10),
        hovertemplate=f'<b>Hole</b><br>({fmt_plain(x)}, {fmt_plain(y)})<extra></extra>',
    ))

def add_vasymptote(fig, x, ymin=-12, ymax=12):
    fig.add_shape(type='line',
        x0=x, x1=x, y0=ymin, y1=ymax,
        line=dict(color=PC['red'], width=1.5, dash='dash'))
    fig.add_annotation(x=x, y=ymax * 0.88,
        text=f'x = {fmt_plain(x)}',
        font=dict(color=PC['red'], size=10),
        showarrow=False, bgcolor='#1a0505',
        bordercolor=PC['red'], borderwidth=1)

def add_hasymptote(fig, y, xmin=-10, xmax=10):
    fig.add_shape(type='line',
        x0=xmin, x1=xmax, y0=y, y1=y,
        line=dict(color=PC['cyan'], width=1.5, dash='dash'))
    fig.add_annotation(x=xmax * 0.6, y=y,
        text=f'y = {fmt_plain(y)}',
        font=dict(color=PC['cyan'], size=10),
        showarrow=False, bgcolor='#001a1a', yshift=12,
        bordercolor=PC['cyan'], borderwidth=1)

def show_plotly(fig, ymin=-12, ymax=12):
    """Finalise axes range and open in browser."""
    fig.update_yaxes(range=[ymin, ymax])
    pio.show(fig, renderer='browser')
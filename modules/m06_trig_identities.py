# modules/m06_trig_identities.py  —  Trig Identities & Equations
from .utils import *
import math

def run():
    while True:
        clear(); header("TRIG IDENTITIES & EQUATIONS")
        print("  1  Identity reference sheet")
        print("  2  Verify an identity numerically")
        print("  3  Solve basic trig equation  a·f(bx+c) = d")
        print("  4  Solve using Pythagorean identity  (sin²x + cos²x = 1)")
        print("  5  Apply sum/difference identities")
        print("  6  Apply double-angle identities")
        print("  0  Back")
        sep()
        ch = input("  Choose: ").strip()
        if ch == '1': identity_ref()
        elif ch == '2': verify_identity()
        elif ch == '3': solve_trig_eq()
        elif ch == '4': pythagorean_solve()
        elif ch == '5': sum_difference()
        elif ch == '6': double_angle()
        elif ch == '0': break
        else: warn("Invalid."); pause()

# ── 1. Reference ──────────────────────────────────────────────────────────────

def identity_ref():
    clear(); header("TRIG IDENTITIES REFERENCE SHEET")
    print("""
  PYTHAGOREAN IDENTITIES
  ──────────────────────────────────────────────────
    sin²x + cos²x = 1
    1 + tan²x     = sec²x
    1 + cot²x     = csc²x

  RECIPROCAL IDENTITIES
  ──────────────────────────────────────────────────
    sin x = 1/csc x        csc x = 1/sin x
    cos x = 1/sec x        sec x = 1/cos x
    tan x = sin x/cos x    cot x = cos x/sin x

  QUOTIENT IDENTITIES
  ──────────────────────────────────────────────────
    tan x = sin x / cos x
    cot x = cos x / sin x

  SUM & DIFFERENCE IDENTITIES
  ──────────────────────────────────────────────────
    sin(A ± B) = sinA·cosB ± cosA·sinB
    cos(A ± B) = cosA·cosB ∓ sinA·sinB
    tan(A ± B) = (tanA ± tanB) / (1 ∓ tanA·tanB)

  DOUBLE-ANGLE IDENTITIES
  ──────────────────────────────────────────────────
    sin(2x) = 2·sinx·cosx
    cos(2x) = cos²x − sin²x
            = 2cos²x − 1
            = 1 − 2sin²x
    tan(2x) = 2·tanx / (1 − tan²x)

  HALF-ANGLE IDENTITIES
  ──────────────────────────────────────────────────
    sin²x = (1 − cos2x) / 2
    cos²x = (1 + cos2x) / 2

  EVEN / ODD IDENTITIES
  ──────────────────────────────────────────────────
    sin(−x) = −sin(x)    (odd)
    cos(−x) =  cos(x)    (even)
    tan(−x) = −tan(x)    (odd)

  CO-FUNCTION IDENTITIES  (x in radians)
  ──────────────────────────────────────────────────
    sin(π/2 − x) = cos(x)
    cos(π/2 − x) = sin(x)
    tan(π/2 − x) = cot(x)
""")
    pause()

# ── 2. Verify numerically ─────────────────────────────────────────────────────

IDENTITY_LHS = {
    'pyth_sin_cos': (lambda x: math.sin(x)**2 + math.cos(x)**2, "sin²x + cos²x"),
    'pyth_tan_sec': (lambda x: 1 + math.tan(x)**2,              "1 + tan²x"),
    'double_sin':   (lambda x: math.sin(2*x),                   "sin(2x)"),
    'double_cos':   (lambda x: math.cos(2*x),                   "cos(2x)"),
}
IDENTITY_RHS = {
    'pyth_sin_cos': (lambda x: 1.0,                             "1"),
    'pyth_tan_sec': (lambda x: (1/math.cos(x))**2,             "sec²x"),
    'double_sin':   (lambda x: 2*math.sin(x)*math.cos(x),      "2·sinx·cosx"),
    'double_cos':   (lambda x: math.cos(x)**2 - math.sin(x)**2,"cos²x − sin²x"),
}

def verify_identity():
    clear(); header("VERIFY IDENTITY NUMERICALLY")
    note("Choose an identity to verify at multiple test angles.\n")
    print("  Options:")
    for k in IDENTITY_LHS:
        lhs = IDENTITY_LHS[k][1]; rhs = IDENTITY_RHS[k][1]
        print(f"    {k:<18}  {lhs} = {rhs}")
    print()
    choice = input("  Choose identity: ").strip().lower()
    if choice not in IDENTITY_LHS:
        warn("Unknown identity."); pause(); return

    lhs_fn, lhs_str = IDENTITY_LHS[choice]
    rhs_fn, rhs_str = IDENTITY_RHS[choice]

    sep()
    print(f"\n  Verifying:  {lhs_str} = {rhs_str}\n")
    print(f"  {'Angle (°)':>12}  {'LHS':>14}  {'RHS':>14}  {'Match':>8}")
    sep('-', 56)

    test_angles = [0, 30, 45, 60, 90, 120, 150, 180, 270]
    all_match = True
    for deg in test_angles:
        rad = math.radians(deg)
        try:
            lv = lhs_fn(rad)
            rv = rhs_fn(rad)
            match = abs(lv - rv) < 1e-9
            if not match:
                all_match = False
            mark = "✓" if match else "✗"
            print(f"  {deg:>12}°  {lv:>14.6f}  {rv:>14.6f}  {mark:>8}")
        except ZeroDivisionError:
            print(f"  {deg:>12}°  {'undefined':>14}  {'undefined':>14}  {'–':>8}")

    sep()
    if all_match:
        ok("Identity VERIFIED at all tested angles ✓")
    else:
        warn("Identity FAILED at one or more angles.")

    pause()

# ── 3. Solve trig equation ────────────────────────────────────────────────────

def solve_trig_eq():
    clear(); header("SOLVE TRIG EQUATION   a·f(bx + c) = d")
    note("Finds all solutions in [0°, 360°] and gives general form.\n")

    fn_str = get_choice("  Function", ["sin", "cos", "tan"])
    a = get_float("  a [1]: ", fallback=1.0)
    b = get_float("  b [1]: ", fallback=1.0)
    c_deg = get_float("  c in degrees [0]: ", fallback=0.0)
    d = get_float("  RHS value d: ")

    sep()
    step(1, "Isolate the trig function")
    rhs = d / a
    print(f"     {a:g}·{fn_str}({b:g}x + {c_deg:g}°) = {d:g}")
    print(f"     {fn_str}({b:g}x + {c_deg:g}°) = {d:g} / {a:g} = {rhs:g}")

    if fn_str in ('sin', 'cos') and abs(rhs) > 1:
        warn(f"|{rhs:g}| > 1 — no real solution for {fn_str}.")
        pause(); return

    step(2, "Find reference angle (inverse trig)")
    if fn_str == 'sin':
        ref = math.degrees(math.asin(abs(rhs)))
    elif fn_str == 'cos':
        ref = math.degrees(math.acos(abs(rhs)))
    else:
        ref = math.degrees(math.atan(abs(rhs)))
    print(f"     Reference angle α = {ref:.4f}°")

    step(3, "Determine quadrants (CAST rule)")
    note("CAST: All positive in Q1, Sin in Q2, Tan in Q3, Cos in Q4")
    if fn_str == 'sin':
        angles = [ref, 180 - ref] if rhs >= 0 else [180 + ref, 360 - ref]
    elif fn_str == 'cos':
        angles = [ref, 360 - ref] if rhs >= 0 else [180 - ref, 180 + ref]
    else:  # tan
        angles = [ref, 180 + ref] if rhs >= 0 else [180 - ref, 360 - ref]
    # these are values of (bx + c)
    print(f"     {b:g}x + {c_deg:g}° ∈ {{ {', '.join(f'{a:.4f}°' for a in angles)} }}")

    step(4, "Solve for x from each angle")
    solutions = []
    for ang in angles:
        x_deg = (ang - c_deg) / b
        # Normalise to [0, 360)
        x_deg = x_deg % 360
        solutions.append(x_deg)
        print(f"     {b:g}x = {ang:.4f}° − {c_deg:g}° = {ang - c_deg:.4f}°")
        print(f"     x = {ang - c_deg:.4f}° / {b:g} = {x_deg:.4f}°")

    step(5, "General solution")
    period = 360 / abs(b)
    for s in solutions:
        print(f"     x = {s:.4f}° + n·{period:.4f}°, n ∈ ℤ")

    result("Solutions in [0°, 360°]", str([f'{s:.4f}°' for s in solutions]))
    pause()

# ── 4. Pythagorean solve ──────────────────────────────────────────────────────

def pythagorean_solve():
    clear(); header("SOLVE USING PYTHAGOREAN IDENTITY")
    note("Substitute sin²x = 1 − cos²x (or vice versa) to express in one function.\n")
    note("Example: 2sin²x + cosx − 1 = 0")
    note("         2(1−cos²x) + cosx − 1 = 0")
    note("         −2cos²x + cosx + 1 = 0")
    note("         Let u = cosx, solve −2u² + u + 1 = 0\n")

    note("Enter the REDUCED single-variable quadratic in u = sin(x) or cos(x):")
    print("  (i.e. after substitution, form: au² + bu + c = 0)\n")
    sub_var = get_choice("  Substitution variable u =", ["sin(x)", "cos(x)"])
    a_q = get_float("  a: ")
    b_q = get_float("  b: ")
    c_q = get_float("  c: ")

    sep()
    step(1, "Solve quadratic in u")
    disc = b_q**2 - 4*a_q*c_q
    print(f"     {a_q:g}u² + {b_q:g}u + {c_q:g} = 0")
    print(f"     Discriminant = {disc:g}")

    if disc < 0:
        warn("Discriminant < 0 — no real solutions."); pause(); return

    roots = []
    if disc >= 0:
        u1 = (-b_q + math.sqrt(disc)) / (2*a_q)
        u2 = (-b_q - math.sqrt(disc)) / (2*a_q)
        for u in {u1, u2}:
            print(f"     u = {u:.6f}")
            roots.append(u)

    step(2, f"Solve {sub_var} = u for x in [0°, 360°]")
    solutions = []
    for u in roots:
        if sub_var == "cos(x)":
            if abs(u) > 1:
                note(f"cos(x) = {u:.4f} — no real solution (|u|>1)")
                continue
            base = math.degrees(math.acos(u))
            cands = [base, 360 - base]
        else:
            if abs(u) > 1:
                note(f"sin(x) = {u:.4f} — no real solution (|u|>1)")
                continue
            base = math.degrees(math.asin(u))
            if u >= 0:
                cands = [base, 180 - base]
            else:
                cands = [180 - base, 360 + base]
        for x in cands:
            x = x % 360
            solutions.append(x)
            ok(f"{sub_var} = {u:.4f}  →  x = {x:.4f}°")

    result("Solutions in [0°, 360°]", str([f'{s:.4f}°' for s in sorted(set(round(s,4) for s in solutions))]))
    pause()

# ── 5. Sum/difference ─────────────────────────────────────────────────────────

def sum_difference():
    clear(); header("SUM / DIFFERENCE IDENTITIES")
    note("sin(A ± B) = sinA·cosB ± cosA·sinB")
    note("cos(A ± B) = cosA·cosB ∓ sinA·sinB\n")

    fn_str = get_choice("  Function", ["sin", "cos", "tan"])
    op     = get_choice("  Operation", ["+", "-"])
    angle_type = get_choice("  Angle type", ["degrees", "radians"])
    A = get_float("  Angle A: ")
    B = get_float("  Angle B: ")

    Ar = math.radians(A) if angle_type == "degrees" else A
    Br = math.radians(B) if angle_type == "degrees" else B

    sep()
    sA, cA, tA = math.sin(Ar), math.cos(Ar), math.tan(Ar)
    sB, cB, tB = math.sin(Br), math.cos(Br), math.tan(Br)
    sign = 1 if op == "+" else -1
    unit = "°" if angle_type == "degrees" else " rad"

    step(1, "State known values")
    print(f"     sin({A:g}{unit}) = {sA:.6f},   cos({A:g}{unit}) = {cA:.6f}")
    print(f"     sin({B:g}{unit}) = {sB:.6f},   cos({B:g}{unit}) = {cB:.6f}")

    step(2, "Apply identity")
    if fn_str == "sin":
        print(f"     sin({A:g} {op} {B:g}) = sin{A:g}·cos{B:g} {op} cos{A:g}·sin{B:g}")
        print(f"                  = ({sA:.6f})·({cB:.6f}) {op} ({cA:.6f})·({sB:.6f})")
        val = sA*cB + sign*cA*sB
    elif fn_str == "cos":
        print(f"     cos({A:g} {op} {B:g}) = cos{A:g}·cos{B:g} ∓ sin{A:g}·sin{B:g}")
        print(f"                  = ({cA:.6f})·({cB:.6f}) {'−' if op == '+' else '+'} ({sA:.6f})·({sB:.6f})")
        val = cA*cB - sign*sA*sB
    else:
        denom = 1 - sign*tA*tB
        if abs(denom) < 1e-10:
            warn("tan(A±B) is undefined here."); pause(); return
        print(f"     tan({A:g} {op} {B:g}) = (tan{A:g} {op} tan{B:g}) / (1 ∓ tan{A:g}·tan{B:g})")
        val = (tA + sign*tB) / denom

    result(f"{fn_str}({A:g} {op} {B:g})", f"{val:.6f}")
    # Verify directly
    direct = math.sin(Ar + sign*Br) if fn_str=="sin" else math.cos(Ar + sign*Br) if fn_str=="cos" else math.tan(Ar + sign*Br)
    note(f"Direct calculation: {direct:.6f}  (matches ✓)" if abs(val - direct) < 1e-9 else f"Direct: {direct:.6f}")
    pause()

# ── 6. Double angle ───────────────────────────────────────────────────────────

def double_angle():
    clear(); header("DOUBLE-ANGLE IDENTITIES")
    note("sin(2x) = 2·sinx·cosx")
    note("cos(2x) = cos²x − sin²x = 2cos²x − 1 = 1 − 2sin²x")
    note("tan(2x) = 2·tanx / (1 − tan²x)\n")

    angle_type = get_choice("  Angle type", ["degrees", "radians"])
    x = get_float("  Angle x: ")
    xr = math.radians(x) if angle_type == "degrees" else x
    unit = "°" if angle_type == "degrees" else " rad"

    sx, cx, tx = math.sin(xr), math.cos(xr), math.tan(xr)

    sep()
    step(1, "Known values")
    print(f"     sin({x:g}{unit}) = {sx:.6f}")
    print(f"     cos({x:g}{unit}) = {cx:.6f}")
    print(f"     tan({x:g}{unit}) = {tx:.6f}")

    step(2, "Apply double-angle formulas")
    sin2 = 2*sx*cx
    cos2a = cx**2 - sx**2
    cos2b = 2*cx**2 - 1
    cos2c = 1 - 2*sx**2
    denom = 1 - tx**2
    tan2  = 2*tx / denom if abs(denom) > 1e-10 else float('inf')

    print(f"\n     sin(2·{x:g}{unit}) = 2·sin·cos = 2·({sx:.4f})·({cx:.4f}) = {sin2:.6f}")
    print(f"\n     cos(2·{x:g}{unit}):")
    print(f"       Form 1: cos²x − sin²x = {cos2a:.6f}")
    print(f"       Form 2: 2cos²x − 1    = {cos2b:.6f}")
    print(f"       Form 3: 1 − 2sin²x    = {cos2c:.6f}")
    if math.isfinite(tan2):
        print(f"\n     tan(2·{x:g}{unit}) = 2tan / (1−tan²) = {tan2:.6f}")
    else:
        print(f"\n     tan(2·{x:g}{unit}) = undefined")

    # Verify
    two_x = 2 * xr
    note(f"Direct sin(2x) = {math.sin(two_x):.6f}  cos(2x) = {math.cos(two_x):.6f}")
    pause()

# modules/m09_binomial.py  —  Binomial Theorem
from .utils import *

def run():
    while True:
        clear(); header("BINOMIAL THEOREM   (a + b)ⁿ")
        print("  1  Expand (a + b)ⁿ  —  full expansion")
        print("  2  Find a specific term   T(k+1) = nCk · aⁿ⁻ᵏ · bᵏ")
        print("  3  Pascal's triangle (first N rows)")
        print("  0  Back")
        sep()
        ch = input("  Choose: ").strip()
        if ch == '1': expand()
        elif ch == '2': specific_term()
        elif ch == '3': pascal()
        elif ch == '0': break
        else: warn("Invalid."); pause()

def expand():
    clear(); header("EXPAND (a + b)ⁿ")
    note("Enter symbolic labels for a and b, or numeric values.\n")
    a_str = input("  Label/value for a (e.g. x, 2x, 3): ").strip() or "a"
    b_str = input("  Label/value for b (e.g. y, -1, 2): ").strip() or "b"
    n = get_int("  Exponent n (≥ 0): ")
    if n < 0 or n > 25:
        warn("n must be between 0 and 25."); pause(); return

    sep()
    step(1, "Apply Binomial Theorem")
    note(f"(a + b)ⁿ = Σ nCk · a^(n−k) · b^k  for k = 0 to n\n")
    print(f"  ({a_str} + {b_str})^{n}  =")

    terms = []
    for k in range(n + 1):
        coeff = nCr(n, k)
        a_exp = n - k
        b_exp = k
        parts = [str(coeff)] if coeff != 1 or (a_exp == 0 and b_exp == 0) else []
        if a_exp == 1: parts.append(a_str)
        elif a_exp > 1: parts.append(f"{a_str}^{a_exp}")
        if b_exp == 1: parts.append(b_str)
        elif b_exp > 1: parts.append(f"{b_str}^{b_exp}")
        term = "·".join(parts) if parts else "1"
        terms.append((coeff, a_exp, b_exp, term))

    # Print neatly in groups of 4
    line = "  "
    for i, (c, ae, be, t) in enumerate(terms):
        if i > 0:
            line += "  +  "
        line += t
        if (i + 1) % 4 == 0 and i < len(terms) - 1:
            print(line)
            line = "  "
    if line.strip():
        print(line)

    step(2, "Binomial coefficients (Pascal's row)")
    print("     " + "  ".join(str(nCr(n, k)) for k in range(n+1)))

    pause()

def specific_term():
    clear(); header("FIND SPECIFIC TERM   T(k+1) = nCk · aⁿ⁻ᵏ · bᵏ")
    note("Useful for finding the term containing a specific power.\n")
    n = get_int("  Exponent n: ")
    k = get_int("  Term index k (T₁ = k=0, T₂ = k=1, ...): ")
    if k > n or k < 0:
        warn("k must be 0 ≤ k ≤ n."); pause(); return

    a_val = get_float("  Value of a (numeric): ", fallback=1.0)
    b_val = get_float("  Value of b (numeric): ", fallback=1.0)

    sep()
    step(1, "Apply T(k+1) formula")
    coeff = nCr(n, k)
    a_part = a_val ** (n - k)
    b_part = b_val ** k
    term_val = coeff * a_part * b_part

    print(f"     T({k+1}) = {n}C{k} · a^{n-k} · b^{k}")
    print(f"           = {coeff} · ({a_val:g})^{n-k} · ({b_val:g})^{k}")
    print(f"           = {coeff} · {a_part:g} · {b_part:g}")
    result(f"T({k+1})", f"{term_val:g}")
    pause()

def pascal():
    clear(); header("PASCAL'S TRIANGLE")
    n_rows = get_int("  Number of rows to display (1–20): ", fallback=8)
    n_rows = max(1, min(n_rows, 20))
    sep()
    rows = [[nCr(r, k) for k in range(r+1)] for r in range(n_rows)]
    max_width = len(str(rows[-1][len(rows[-1])//2])) + 2
    for r, row in enumerate(rows):
        padding = " " * ((n_rows - r - 1) * (max_width // 2))
        print(padding + "  ".join(f"{v:^{max_width}}" for v in row))
    print()
    note("Each number = sum of two numbers directly above it.")
    note("Row n (0-indexed) gives coefficients of (a+b)ⁿ.")
    pause()

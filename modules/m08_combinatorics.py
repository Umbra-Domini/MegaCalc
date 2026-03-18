# modules/m08_combinatorics.py  —  Combinatorics / Counting
from .utils import *

def run():
    while True:
        clear(); header("COMBINATORICS & COUNTING METHODS")
        print("  1  Fundamental Counting Principle")
        print("  2  Permutations  nPr")
        print("  3  Combinations  nCr")
        print("  4  Permutations with repetition")
        print("  5  Arrangements with repeated elements  n! / (a!·b!...)")
        print("  0  Back")
        sep()
        ch = input("  Choose: ").strip()
        if ch == '1': fcp()
        elif ch == '2': permutations()
        elif ch == '3': combinations()
        elif ch == '4': perm_with_rep()
        elif ch == '5': arrangements_repeated()
        elif ch == '0': break
        else: warn("Invalid."); pause()

def fcp():
    clear(); header("FUNDAMENTAL COUNTING PRINCIPLE")
    note("If event 1 has m ways and event 2 has n ways, total = m × n × ...\n")
    k = get_int("  How many independent events/stages? ")
    counts = []
    for i in range(k):
        c = get_int(f"  Number of choices for event {i+1}: ")
        counts.append(c)
    sep()
    step(1, "Multiply all choices")
    print("     " + " × ".join(str(c) for c in counts))
    total = 1
    for c in counts:
        total *= c
    result("Total arrangements", f"{total:,}")
    pause()

def permutations():
    clear(); header("PERMUTATIONS   nPr = n! / (n−r)!")
    note("Order MATTERS. Selecting r items from n distinct items.\n")
    n = get_int("  n (total items): ")
    r = get_int("  r (items chosen): ")
    if r > n or r < 0:
        warn("r must be 0 ≤ r ≤ n."); pause(); return
    sep()
    step(1, "Apply formula")
    print(f"     nPr = {n}! / ({n}−{r})!")
    print(f"         = {n}! / {n-r}!")
    print(f"         = {factorial(n)} / {factorial(n-r)}")
    val = nPr(n, r)
    result(f"{n}P{r}", f"{val:,}")
    step(2, "What this means")
    note(f"There are {val:,} ways to arrange {r} items chosen from {n} (order matters).")
    pause()

def combinations():
    clear(); header("COMBINATIONS   nCr = n! / (r!·(n−r)!)")
    note("Order does NOT matter. Selecting r items from n distinct items.\n")
    n = get_int("  n (total items): ")
    r = get_int("  r (items chosen): ")
    if r > n or r < 0:
        warn("r must be 0 ≤ r ≤ n."); pause(); return
    sep()
    step(1, "Apply formula")
    print(f"     nCr = {n}! / ({r}! · ({n}−{r})!)")
    print(f"         = {factorial(n)} / ({factorial(r)} · {factorial(n-r)})")
    val = nCr(n, r)
    result(f"{n}C{r}", f"{val:,}")
    step(2, "Symmetry check")
    note(f"nC(n−r) = {n}C{n-r} = {nCr(n, n-r):,}  (should equal {val:,} ✓)")
    pause()

def perm_with_rep():
    clear(); header("PERMUTATIONS WITH REPETITION")
    note("Choosing r items from n where repetition is allowed:  nʳ\n")
    n = get_int("  n (distinct items available): ")
    r = get_int("  r (positions to fill): ")
    sep()
    step(1, "Apply formula")
    print(f"     n^r = {n}^{r} = {n**r:,}")
    result("Total", f"{n**r:,}")
    pause()

def arrangements_repeated():
    clear(); header("ARRANGEMENTS WITH REPEATED ELEMENTS   n! / (a!·b!·...)")
    note("Total arrangements of n items where some are identical.\n")
    n = get_int("  Total items n: ")
    k = get_int("  How many groups of identical items? ")
    groups = []
    for i in range(k):
        g = get_int(f"  Count of identical item group {i+1}: ")
        groups.append(g)
    sep()
    step(1, "Apply formula")
    num = factorial(n)
    den = 1
    for g in groups:
        den *= factorial(g)
    print(f"     {n}! / ({' · '.join(str(g)+'!' for g in groups)})")
    print(f"     = {num:,} / {den:,}")
    val = num // den
    result("Distinct arrangements", f"{val:,}")
    pause()

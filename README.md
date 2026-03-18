# MegaCalc — PreCalc 12 Toolkit

A terminal-based step-by-step math calculator covering all major PreCalc 12 topics.
Built in Python with optional graphing via Plotly.

---

## Getting Started

### Requirements

- Python 3.8+
- Optional (for graphs): `numpy` and `plotly`

### Install dependencies

```bash
pip install numpy plotly
```

### Run

```bash
python main.py
```

---

## Project Structure

```
megacalc/
├── main.py                   ← Entry point / main menu
└── modules/
    ├── utils.py              ← Shared helpers (formatting, input, graph engine)
    ├── m01_transformations.py
    ├── m02_polynomials.py
    ├── m03_rational.py
    ├── m04_explog.py
    ├── m05_trig_functions.py
    ├── m06_trig_identities.py
    ├── m07_sequences.py
    ├── m08_combinatorics.py
    ├── m09_binomial.py
    └── m10_inverses.py
```

---

## Modules

### 1 · Function Transformations
Analyse `y = a·f(b(x−h)) + k` for any parent function.
- Describe all 4 transformation parameters step by step
- Map key points from parent to transformed graph
- Identify stretch/reflection/translation from two points
- Supported parents: linear, quadratic, cubic, sqrt, abs, rational, exponential, log, sin, cos, tan
- **Graph**: transformed vs parent curve

### 2 · Polynomial Functions
- End behaviour from degree and leading coefficient
- Evaluate at a point using Horner's method
- Rational Root Theorem — lists and tests all ±p/q candidates
- Synthetic division with full table
- Full factoring (iterative rational roots + quadratic formula)
- Root multiplicity with crossing/touching behaviour
- **Graph**: labelled roots and y-intercept

### 3 · Rational Functions
- Vertical asymptotes and holes (with hole coordinates)
- Horizontal and oblique asymptotes (polynomial long division shown)
- x- and y-intercepts
- Full analysis combining all of the above
- Solve rational equations (cross-multiply + check extraneous solutions)
- **Graph**: asymptotes as dashed lines, holes as open circles, all points labelled

### 4 · Exponential & Logarithmic Functions
- Laws of logarithms reference + evaluator
- Solve `a·b^(mx+n) = c` step by step
- Solve `a·log_b(mx+n) = c` step by step
- Change of base
- Growth & decay table + doubling time / half-life
- Compound interest (annual, semi, quarterly, monthly, daily, continuous)
- **Graph**: exponential or log with transformation parameters

### 5 · Trigonometric Functions
- Evaluate sin, cos, tan, sec, csc, cot at any angle
- Describe graph parameters: amplitude, period, phase shift, vertical shift
- Reciprocal trig reference + evaluator
- Unit circle table (all 16 standard angles, degrees + radians)
- **Graph**: any trig or reciprocal function with full `a·f(bx−c)+d` transformations

### 6 · Trig Identities & Equations
- Full identity reference sheet (Pythagorean, reciprocal, sum/difference, double-angle, half-angle, co-function)
- Numerically verify identities at multiple test angles
- Solve `a·f(bx+c) = d` in [0°, 360°] with CAST rule
- Solve using Pythagorean substitution
- Apply sum/difference identities step by step
- Apply double-angle identities (all three forms for cos)

### 7 · Sequences & Series
- Arithmetic sequence: nth term, partial sum, first terms
- Geometric sequence: nth term, partial sum, first terms
- Infinite geometric series with convergence check
- Sigma notation evaluator (any Python expression)
- Identify sequence type from terms (arithmetic, geometric, quadratic)

### 8 · Combinatorics & Counting
- Fundamental Counting Principle (multi-stage events)
- Permutations nPr
- Combinations nCr
- Permutations with repetition (n^r)
- Arrangements with repeated elements (n! / a!b!...)

### 9 · Binomial Theorem
- Expand `(a+b)^n` symbolically for any n up to 25
- Find a specific term `T(k+1) = nCk · a^(n−k) · b^k`
- Pascal's triangle (up to 20 rows)

### 10 · Inverses & Function Composition
- Inverse of linear: `y = mx + b`
- Inverse of power: `y = axⁿ`
- Inverse of exponential and logarithmic functions
- Numerically verify two functions are inverses (`f(g(x)) = x`)
- Compose functions symbolically with sample point table
- Evaluate `f(g(a))` step by step

---

## Output Format

Every calculation follows the same pattern:

```
┌─ Step 1:  <what this step does>
│
   working lines (dimmed)
   key values highlighted

╔──────────────────╗
║  Answer:  value  ║
╚──────────────────╝
```

- **Steps** are colour-coded cyan headers — easy to skim
- **Working** is dimmed so it doesn't compete with results
- **Final answers** are in a green box — impossible to miss
- **Fractions**: decimal results show as `0.6667  (= 2/3)` where possible

---

## Graphs

Graphs open in your browser as interactive Plotly charts.

- Hover over any point to see exact `(x, y)` coordinates
- Scroll to zoom, click-drag to pan
- Roots, intercepts, asymptotes, and holes are all labelled
- Trig graphs use π-based x-axis labels

Graphs are optional — if `plotly` or `numpy` aren't installed, the rest of the calculator works fine without them.

---

## Notes

- Fraction input supported everywhere: type `3/4` instead of `0.75`
- All modules are independent — you can import any single module on its own
- Tested on Python 3.8+ on Linux, Windows, and macOS

---

*Originally started in Grade 12 as a set of Python CLI scripts to survive PreCalc 12.*

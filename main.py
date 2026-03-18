#!/usr/bin/env python3
# main.py  —  MegaCalc PreCalc 12 Toolkit
# Run with:  python main.py

import sys
import os

# Ensure the project root is on the path
sys.path.insert(0, os.path.dirname(__file__))

from modules.utils import clear, sep, pause

MENU = [
    ("Function Transformations",          "modules.m01_transformations"),
    ("Polynomial Functions",               "modules.m02_polynomials"),
    ("Rational Functions",                 "modules.m03_rational"),
    ("Exponential & Logarithmic",          "modules.m04_explog"),
    ("Trigonometric Functions",            "modules.m05_trig_functions"),
    ("Trig Identities & Equations",        "modules.m06_trig_identities"),
    ("Sequences & Series",                 "modules.m07_sequences"),
    ("Combinatorics & Counting",           "modules.m08_combinatorics"),
    ("Binomial Theorem",                   "modules.m09_binomial"),
    ("Inverses & Function Composition",    "modules.m10_inverses"),
]

def banner():
    print()
    print("  ╔══════════════════════════════════════════════════════╗")
    print("  ║          M E G A C A L C  —  PreCalc 12             ║")
    print("  ║                   by Manraaj Singh                  ║")
    print("  ╚══════════════════════════════════════════════════════╝")
    print()

def main():
    while True:
        clear()
        banner()
        print("  MODULES")
        sep()
        for i, (name, _) in enumerate(MENU, 1):
            print(f"  {i:>2}.  {name}")
        print()
        print("   0.  Quit")
        sep()

        choice = input("  Choose a module: ").strip()

        if choice == "0":
            print("\n  Bye!\n")
            break

        try:
            idx = int(choice) - 1
            if 0 <= idx < len(MENU):
                name, mod_path = MENU[idx]
                import importlib
                mod = importlib.import_module(mod_path)
                mod.run()
            else:
                print("  Invalid choice.")
                pause()
        except ValueError:
            print("  Enter a number.")
            pause()
        except ImportError as e:
            print(f"  Could not load module: {e}")
            pause()

if __name__ == "__main__":
    main()

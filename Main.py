from Problem import ProblemFormulation
from PreProcess import toCanonicalForm
from Simplex import simplexSolver

if __name__ == "__main__":
    p = ProblemFormulation()
    p.setTest_2()
    print("PROBLEM:")
    p.printProblem()

    print("\n\nCANONICAL:")
    p = toCanonicalForm(p)
    simplexSolver(p)

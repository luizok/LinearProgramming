from Problem import ProblemFormulation, printInfo
from PreProcess import toCanonicalForm
from Simplex import simplexSolver

if __name__ == "__main__":
    p = ProblemFormulation()
    p.setTest_2()
    printInfo(p, "PROBLEM")

    p = toCanonicalForm(p)
    p = simplexSolver(p)

    printInfo(p, "SOLVED PROBLEM")

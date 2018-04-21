from Problem import ProblemFormulation
from PreProccess import toCanonicalForm

if __name__ == "__main__":
    p = ProblemFormulation()
    p.setTest_2()
    print("PROBLEM:")
    p.printProblem()

    print("\n\nCANONICAL:")
    toCanonicalForm(p)

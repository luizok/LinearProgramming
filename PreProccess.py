from Problem import ProblemFormulation
from pprint import pprint


# def mapConstraints():

def toCanonicalForm(p: ProblemFormulation):
    n = len(p.c) # Number of variables
    m = len(p.b) # Number of constraints

    eqConsts = sum(1 for c in p.constraints if c == " =")

    canonical = ProblemFormulation()

    canonical.A = [[0 for _ in range(n+m+eqConsts)] for _ in range(m+eqConsts)]
    canonical.b = [0 for _ in range(m+eqConsts)]
    canonical.c = [0 for _ in range(n+m+eqConsts)]
    canonical.constraints = ["" for _ in range(m+eqConsts)]
    
    for j in range(n):
        canonical.c[j] = p.c[j] if p.max_min == "MIN" else -p.c[j]

    pprint(canonical.A)
    pprint(canonical.b)
    pprint(canonical.c)
    print("\n")

    k = 0
    mapConsts = {}
    for i in range(m):
        if p.constraints[i] != " =":
            mapConsts.update({i:k})
        else:
            mapConsts.update({i:(k,k+1)})
            k += 1
        k += 1

    pprint(mapConsts)

    for i in range(m):
        for j in range(n+m+eqConsts):
            if p.constraints[i] == " =":
                break


    canonical.printProblem()
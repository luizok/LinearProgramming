from Problem import ProblemFormulation
from pprint import pprint

# Substitute equals constraints for 2 cosntraints of type "<=" and ">="
def removeEqualsConstraints(mapConsts: dict, p: ProblemFormulation, oldProblem: ProblemFormulation):

    for i, ix in mapConsts.items():
        if oldProblem.constraints[i] == " =":
            p.constraints[ix[0]] = ">="
            p.constraints[ix[1]] = "<="

            p.b[ix[0]] = oldProblem.b[i]
            p.b[ix[1]] = oldProblem.b[i]
        else:
            p.constraints[ix[0]] = oldProblem.constraints[i]
            p.b[ix[0]] = oldProblem.b[i]

    return p


def toCanonicalForm(p: ProblemFormulation):
    n = len(p.c) # Number of variables
    m = len(p.b) # Number of constraints

    # Count number of constraints of type "="
    eqConsts = sum(1 for c in p.constraints if c == " =")

    canonical = ProblemFormulation()

    canonical.A = [[0 for _ in range(n+m+eqConsts)] for _ in range(m+eqConsts)]
    canonical.b = [0 for _ in range(m+eqConsts)]
    canonical.c = [0 for _ in range(n+m+eqConsts)]
    canonical.constraints = ["" for _ in range(m+eqConsts)]
    
    for j in range(n):
        canonical.c[j] = p.c[j] if p.max_min == "MIN" else -p.c[j]

    # The next step maps the old constraints to a new enumeration considering
    # "=" constraints as 2 constraints, for example:
    # Consider the constraints [<=, =, >=] mapConsts will give {0:(0,), 1:(1,2), 2:(3,)}
    # Note that "=" constraint represents 2, since "=" is equivalent to "<=" and ">="
    # at the same time
    k = 0
    mapConsts = {}
    for i in range(m):
        if p.constraints[i] != " =":
            mapConsts.update({i:(k,)})
        else:
            mapConsts.update({i:(k,k+1)})
            k += 1
        k += 1

    canonical = removeEqualsConstraints(mapConsts, canonical, p)

    for oldRow, row in mapConsts.items():
        for idx in row:
            for j in range(n+m+eqConsts):
                if j < n:
                    canonical.A[idx][j] = p.A[oldRow][j]
                elif j == n+idx:
                    canonical.A[idx][j] = 1 if canonical.constraints[idx] == "<=" else -1

    canonical.printProblem()
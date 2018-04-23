from Problem import ProblemFormulation, printInfo
from Simplex import simplexSolver
from copy import deepcopy

# Substitute equals constraints for 2 constraints of type "<=" and ">="
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

def generateBasicSolution(problem: ProblemFormulation, n, m):

    p = deepcopy(problem)
    artVars = [] # Set of Artificial Variables saving their indexes

    for j in range(m):
        if p.A[j][n+j] == -1:
            artVars.append(j)

            # Extends the matrix with aritificial vars columns
            for i in range(m):
                p.A[i] = p.A[i] + [1 if i == j else 0]

    p.max_min = "MIN"
    p.c = [1 if j >= n+m else 0 for j in range(n+m+len(artVars))] # Extends vector c
    printInfo(p, "ARITIFICIAL PROBLEM")
    # Set cost 0 to aritificial variables
    p.c = [c-sum(p.A[artVars[k]][j] for k in range(len(artVars))) for j, c in enumerate(p.c)]

    printInfo(p, "ZERO COST ARTIFICIAL VAR")
    p = simplexSolver(p)

    printInfo(p, "ARTIFICIAL SOLVED")

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
    # Note that "=" constraint represents 2 values, since "=" is equivalent to "<=" and ">="
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

    printInfo(canonical, "CANONICAL")

    basic = None
    if ">=" in canonical.constraints:
        basic = generateBasicSolution(canonical, n, m+eqConsts)

        #TODO VERIFY IF PROBLEM IS INFEASIBLE

        # Remove the artificial vars
        canonical.A = [[basic.A[i][j] for j in range(n+m+eqConsts)] for i in range(m+eqConsts)]
        canonical.b = basic.b

        # If the amount of 0's in j-th column of A is equals to the number of constraints-1
        # and the sum of j-th column of A is 1 then the j-th column is a basic column
        # Obs.: This is a specific case, not al32ways this is true 
        print()
        for j in range(n+m+eqConsts):
            if sum(1 for i in range(m+eqConsts) if canonical.A[i][j] == 0) == m+eqConsts-1 and \
                sum(canonical.A[i][j] for i in range(m+eqConsts)) == 1:

                    oneIndex = list(canonical.A[i][j] for i in range(m+eqConsts)).index(1)

                    value = canonical.c[j]
                    for jdx in range(n+m):
                        canonical.c[jdx] -= value * canonical.A[oneIndex][jdx]
    
    printInfo(canonical, "NEW PROBLEM")

    return canonical
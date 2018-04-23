from Problem import ProblemFormulation

def simplexSolver(problem: ProblemFormulation):

    p = problem

    n = len(p.c)
    m = len(p.b)

    iteration = 1
    c_min = min(p.c)

    while c_min < 0:   
        k = p.c.index(c_min)
        print("\n\n"+3*"\t"+" ITER %d ".center(100, "*") % iteration)
        print("min(%s) = %5.2f in col=%d" % (str(p.c), c_min, k))
        iteration += 1

        fractions = [(i, p.b[i]/p.A[i][k]) for i in range(m) if p.A[i][k] > 0]

        if fractions == []:
            print("The problem is unlimited")
            return 

        idx, fract = list(zip(*fractions))

        r = idx[fract.index(min(fract))]
        print("min(%s) = %5.2f in row=%d" % (str(fract), min(fract), r))

        p.b[r] = p.b[r]/p.A[r][k]
        p.A[r] = [p.A[r][j]/p.A[r][k] for j in range(n)]

        print()
        for i in range(m):
            if i != r:
                p.b[i] -= p.A[i][k]*p.b[r]
                p.A[i] = [p.A[i][j]-p.A[i][k]*p.A[r][j] for j in range(n)]

        p.c = [p.c[j]-p.A[r][j]*p.c[k] for j in range(n)]  

        p.printProblem()

        c_min = min(p.c)

    return p
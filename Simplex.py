from Problem import ProblemFormulation

def simplexSolver(problem: ProblemFormulation):

    p = problem
    p.printProblem()

    n = len(p.c)
    m = len(p.b)

    iteration = 1
    c_min = min(p.c)


    while c_min < 0:   
        k = p.c.index(c_min)
        print("\n\n"+"ITER %d".center(50, "-") % iteration)
        print("min(%s) = %5.2f in col=%d" % (str(p.c), c_min, k))
        iteration += 1

        rations = [(i, p.b[i]/p.A[i][k]) for i in range(m) if p.A[i][k] > 0]

        if rations == []:
            print("The problem is unlimited")
            break

        idx, rat = list(zip(*rations))

        print(str(rat))
        print(str(idx))

        r = idx[rat.index(min(rat))]
        print("min(%s) = %5.2f in rol=%d" % (str(rat), min(rat), r))

        p.b[r] = p.b[r]/p.A[r][k]
        p.A[r] = [p.A[r][j]/p.A[r][k] for j in range(n)]

        print()
        for i in range(m):
            if i != r:
                p.b[i] = p.b[i]-p.A[i][k]*p.b[r]
                p.A[i] = [p.A[i][j]-p.A[i][k]*p.A[r][j] for j in range(n)]

        p.c = [p.c[j]-p.A[r][j]*p.c[k] for j in range(n)]  

        p.printProblem()
        print("z = %5.2f")

        c_min = min(p.c)
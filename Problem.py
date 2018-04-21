class ProblemFormulation():
    def __init__(self, A=[], constraints=[], b=[], c=[], max_min="MIN"):
        self.A = A
        self.b = b
        self.c = c
        self.constraints = constraints
        self.max_min = max_min

    def setTest_1(self):
        #Optimial = (x1=3, x2=12)
        self.A = [
            [2, 1],
            [2, 3],
            [3, 1]
        ]

        self.constraints = [
            "<=",
            "<=",
            "<="
        ]

        self.b = [
            18,
            42,
            24
        ]

        self.c = [3, 2]

        self.max_min = "MAX"

    def setTest_2(self):
        #Optimal = (x1=1.0891, x2=2, x3=1.3069) e Z=2.0594
        self.A = [
            [2, 3, 0],
            [-3, 4, 2.5],
            [3.1, 2.9, -.9],
            [0, 1, 0]
        ]

        self.constraints = [
            " =",
            "<=",
            " =",
            " ="
        ]

        self.b = [
            10,
            8,
            8,
            2
        ]

        self.c = [5, -3, 2]
        self.max_min = "MAX"

    def printProblem(self):
        sign = lambda x: "+" if x > 0 else ""

        # Generates a list from i-th line of matrix A
        # output be like: ["+Ai0.x1", "+Ai1.x2", "+... , "+Ain-1.xn"]
        generateString = lambda Ai: [
            sign(Ai[j]) + "{:4.2f}".format(float(Ai[j]))+" x"+str(j+1) if Ai[j] != 0 \
            else 8*" "
            for j in range(len(Ai))     
        ]
        
        print("%s\t%s" % (self.max_min, " ".join(generateString(self.c))))
        print("S.a.")

        for i, row in enumerate(self.A):
            print("    \t%s %s %5.2f" \
                % (" ".join(generateString(row)), self.constraints[i], float(self.b[i])))
            

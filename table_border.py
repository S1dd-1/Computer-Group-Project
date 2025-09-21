def print_table(L):
    def print_border():
        print("+", end = "")
        for i in lens:
            print("-"*(i+2)+"+", end = "")
        print()

    L = list(L)

    lens = []
    for i in L[0]:
        lens.append([])

    for i in range(len(L)):
        L[i] = list(L[i])
        for j in range(len(L[i])):
            L[i][j] = str(L[i][j])
            lens[j].append(len(L[i][j]))

    for i in range(len(lens)):
        lens[i] = max(lens[i])

    for i in range(len(L)):
        for j in range(len(L[i])):
            while len(L[i][j]) < lens[j]:
                L[i][j] += " "

    print_border()
    for i in range(len(L)):
        print("|", end = "")
        for j in range(len(L[i])):
            print(" "+L[i][j]+" ", end = "|")
        print()
    print_border()

# example
L1 = ((123,"abc",45),(233,"xxcyz",200))
print_table(L1)


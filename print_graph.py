def print_graph(Values):

    for i in range(len(Values)):
        Values[i][1] = round(Values[i][1]/50)*50

    qx = [x for x, y in Values]
    qy = [y for x, y in Values]

    L = []

    xx = "     "
    for x in range(max(qx)+2):
        xx += str(x) + " "
    L.append(xx)

    L.append("   0 +-" + '--'*(max(qx)+2))

    yy = list(range(50, max(qy) + 50, 50))

    for y in yy:
        str1 = ' '*abs(len(str(y))-4) + str(y) + ' | '
        for x in range(1,max(qx)+2):
            if [x, y] in Values:
                str1 += 'x '
            else:
                str1 += 'o '
        L.append(str1)

    L.reverse()
    for line in L:
        print(line)

#test
Values = [[1, 234], [2, 60], [6, 150]]
print_graph(Values)

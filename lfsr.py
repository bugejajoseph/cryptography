state = 0b100
for i in range(9):
        print("{} {:03b}".format(i, state))
        newbit = (state ^ (state >> 1)) & 1
        state = (state >> 1) | (newbit << 2)

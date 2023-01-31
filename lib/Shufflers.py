from random import randint


#-*-------------- 3x3 shuffler -----------------*-#
#                                                 #
#   This shuffler work in: 2x2 and 3x3 puzzles    #
#   the arguments are in lib/__init__.py file     #
#                                                 #
#-*---------------------------------------------*-#
def s3x3_shuffler(cube):
    '''
    Internal function to generate valid and secure 2x2x2 Rubik's cube scrambles instead of only
    "shuflle" strings.
    Warning: the scrambles generated here are not in random state, they only satisfies
    the conditions of how a scramble should looks like.
    '''
    def gen2x2():
        moves = ["R", "U", "F"]
        directions = [" ", "' ", "2 "]

        moveA = ""
        scramble = []

        for i in range(0, 10 + randint(0, 3)):
            while True:
                moveB = moves[randint(0, len(moves) - 1)]
                if moveB != moveA: break
            
            moveA = moveB
            scramble.append(moveB + directions[randint(0, len(directions) - 1)])

        return scramble

    '''
    Internal function to generate valid and secure 3x3x3 Rubik's cube scrambles instead of only
    "shuflle" strings.
    Warning: the scrambles generated here are not in random state, they only satisfies
    the conditions of how a scramble should looks like.
    '''
    def gen3x3():
        moves = ["Rx", "Uy", "Fz", "Lx", "Dy", "Bz"]
        directions = [" ", "' ", "2 "]

        """
        Internal function to check if a group of 3 movements
        are from the same axis.
        A sequence of 3 moves in the same aixis is not valid.
        Ex.: R L R, F B F, U D U, L R L, etc.
        """
        def sameAxis(moveA, moveB, moveC):
            concatened = moveA[1] + moveB[1] + moveC[1]
            return concatened == "xxx" or concatened == "yyy" or concatened == "zzz"
        
        moveA = "  "
        moveB = "  "
        scramble = []

        for i in range(0, 21 + randint(0, 5)):
            while True:
                moveC = moves[randint(0, len(moves) - 1)]
                if (not sameAxis(moveA, moveB, moveC)) and (moveC != moveB): break
            moveA = moveB
            moveB = moveC
            scramble.append(moveC[0] + directions[randint(0, len(directions) - 1)])

        return scramble

    # checks if param is "2x2" or "3x3" ad returns based on it
    if cube == "2x2": return gen2x2()
    else: return gen3x3()


#-*--------------- pyranminx shuffler ----------*-#
#                                                 #
#   This shuffler work in: pyranmix and skewb     #
#   The arguments are in lib/__init__.py file     #
#                                                 #
#-*---------------------------------------------*-#
def pyra_shuffler(cube):
    def genpyra():
        moves = ['r', 'l', 'u', 'b']
        directions = [" ", "' "]

        moveA = ''
        scramble = genskewb()

        for m in range(0, 1 + randint(0, 2)):
            while True:
                moveB = moves[randint(0, len(moves) - 1)]
                if moveB != moveA: break

            moveA = moveB
            scramble.append(moveB + directions[randint(0, len(directions) -1)])

        return scramble

    def genskewb():
        moves = ['R', 'L', 'U', 'B']
        directions = [" ", "' "]

        moveA = ''
        scramble = []

        for m in range(0, 8 + randint(0, 1)):
            while True:
                moveB = moves[randint(0, len(moves) - 1)]
                if moveB != moveA: break

            moveA = moveB
            scramble.append(moveB + directions[randint(0, len(directions) - 1)])

        return scramble

    # checks if param is "pyra" or "skewb" ad returns based on it
    if cube == 'pyra': return genpyra()
    else: return genskewb()

#-*---------------- 4x4 shuffler -----------------*-#
#                                                   #
#     This shuffler work in: 4x4 and 5x5 puzzles.   #
#     The arguments are in lib/__init__.py file     #
#                                                   #
#-*-----------------------------------------------*-#
def s4x4_shuffler(cube):
    def gen4x4():
        moves = ['Rx', 'Uy', 'Fz', 'Lx', 'Dy', 'Bz']
        directions = [" ", "' ", "2 ", "w ", "w' ", "w2 "]

        moveA = "  "
        moveB = "  "
        scramble = []

        def sameAxis(moveA, moveB, moveC):
            concatened = moveA[1] + moveB[1] + moveC[1]
            return concatened == "xxx" or concatened == "yyy" or concatened == "zzz"

        for i in range(0, 41 + randint(0, 5)):
            while True:
                moveC = moves[randint(0, len(moves) - 1)]
                if (not sameAxis(moveA, moveB, moveC)) and (moveC != moveB): break
            moveA = moveB
            moveB = moveC
            scramble.append(moveC[0] + directions[randint(0, len(directions) - 1)])

        return scramble

    def gen5x5():
        moves = ['Rx', 'Uy', 'Fz', 'Lx', 'Dy', 'Bz']
        directions = [" ", "' ", "2 ", "w ", "w' ", "w2 "]

        moveA = "  "
        moveB = "  "
        scramble = []

        def sameAxis(moveA, moveB, moveC):
            concatened = moveA[1] + moveB[1] + moveC[1]
            return concatened == "xxx" or concatened == "yyy" or concatened == "zzz"

        for i in range(0, 58 + randint(0, 5)):
            while True:
                moveC = moves[randint(0, len(moves) - 1)]
                if (not sameAxis(moveA, moveB, moveC)) and (moveC != moveB): break
            moveA = moveB
            moveB = moveC
            scramble.append(moveC[0] + directions[randint(0, len(directions) - 1)])

        return scramble


    if cube == '4x4': return gen4x4()
    else: return gen5x5()

#-*-------------- 6x6 shuffler ----------------*-#
#                                                #
#   This shuffler work in: 6x6 and 7x7 puzzles   #
#   the arguments are in lib/__init__.py file    #
#                                                #
#-*--------------------------------------------*-#
def s6x6_shuffler(cube):
    moves = []
    old = 0
    if cube == '6x6': size = 80
    else: size = 100

    for move in range(1, size):
        while True:
            m = randint(1, 6)

            if not m == old:
                if m == 1:
                    old = m
                    moves.append('U')
                    break
                if m == 2:
                    old = m
                    moves.append('R')
                    break
                if m == 3:
                    old = m
                    moves.append('L')
                    break
                if m == 4:
                    old = m
                    moves.append('D')
                    break
                if m == 5:
                    old = m
                    moves.append('F')
                    break
                if m == 6:
                    old = m
                    moves.append('B')
                    break
    for letter in range(0, size-1):
        x = randint(1, 3)
        if cube == '6x6':
            if moves[letter] in 'RFU':
                if x == 1: moves[letter] = f'{moves[letter]}w' # add 'w'
                if x == 2: moves[letter] = f'3{moves[letter]}w'
        else:
            if x == 1: moves[letter] = f'{moves[letter]}w'
            if x == 2: moves[letter] = f'3{moves[letter]}w'

        x = randint(1, 3)
        if x == 1: moves[letter] = f'{moves[letter]}\'' # add apostrophe
        if x == 2: moves[letter] = f'{moves[letter]}2' # add two

    return moves


#-*------------- Square-1 shuffler -----------*-#
#                                               #
#   This shuffler work in: square-1 puzzle      #
#   the arguments are in lib/__init__.py file   #
#                                               #
#-*-------------------------------------------*-#
def sq1_shuffler():
    moves = []
    for move in range(1, 15):
        w = ()
        x = randint(-5, 6)
        y = randint(-5, 6)
        moves.append((x, y))
        if not move == 14: moves.append('/')
        else:
            x = randint(0, 1)
            if x == 1: moves.append('/')

    return moves

if __name__ == "__main__": print("Run, the Main.py file to start program")

#-*----- import area -----*-#
from random import randint  #
#-*-----------------------*-#

#-*-------------- Salete shuffler --------------*-#
#                                                 #
#   This shuffler work in: 2x2 and 3x3 puzzles    #
#   the arguments are in lib/__init__.py file     #
#   Version of salete: 1.1                        #
#                                                 #
#-*---------------------------------------------*-#
def Salete(cube):
    moves = [] # Letters enter here
    old = 0 # variable to not repeat letter
    if cube == '2x2':
        size = 10
        w = 3
    else:
        size = 21
        w = 6

    for move in range(1, size):
        while True:
            m = randint(1, w) # the cube have 6 moves these are:

            if not m == old:
                if m == 1:
                    old = m
                    moves.append('U') # Up
                    break
                if m == 2:
                    old = m
                    moves.append('R') # Right
                    break
                if m == 3:
                    old = m
                    moves.append('F') # Front
                    break
                if m == 4:
                    old = m
                    moves.append('D') # Down
                    break
                if m == 5:
                    old = m
                    moves.append('L') # Left
                    break
                if m == 6:
                    old = m
                    moves.append('B') # Back
                    break

    # Here is to add apostruphe('), two(2) to the letters randomly
    for letter in range(0, size - 1):
        x = randint(1, 3)
        if x == 1: moves[letter] = f'{moves[letter]}\'' # add apostrophe
        if x == 2: moves[letter] = f'{moves[letter]}2' # add two
        if x == 3: pass # do nothing "\_(シ)_/"
    return moves

#-*--------------- Cida shuffler ---------------*-#
#                                                 #
#   This shuffler work in: pyranmix and skewb     #
#   The arguments are in lib/__init__.py file     #
#   Version of Cida: 1.1                          #
#                                                 #
#-*---------------------------------------------*-#
def Cida(cube):
    moves = [] # Letters enter here
    old = 0 # variable to not repeat letter

    if cube == 'pyra': w = 11
    else: w = 9
    for move in range(1, 10):
        while True:
            m = randint(1, 4) # the pyranmix and skewb have 4 initial moves these are:

            if not m == old:
                if m == 1:
                    old = m
                    moves.append('U') # Up
                    break
                if m == 2:
                    old = m
                    moves.append('R') # Right
                    break
                if m == 3:
                    old = m
                    moves.append('L') # Left
                    break
                if m == 4:
                    old = m
                    moves.append('B') # Back
                    break

    if cube == 'pyra':
        for move in range(1, 4):
            while True:
                m = randint(1, 5) # the pyranmix have 4 cap moves these are:

                if not m == old:
                    if m == 1:
                        old = m
                        moves.append('u') # Up Cap
                        break
                    if m == 2:
                        old = m
                        moves.append('r') # Right
                        break
                    if m == 3:
                        old = m
                        moves.append('l') # Left
                        break
                    if m == 4:
                        old = m
                        moves.append('b') # Back
                        break

    # Here is to add apostruphe(') to the letters randomly
    for letter in range(0, w):
        x = randint(1, 2)
        if x == 1: moves[letter] = f'{moves[letter]}\'' # add apostrophe
        if x == 2: pass # do nothing "\_(シ)_/"
    return moves

#-*---------------- Lucia shuffler ---------------*-#
#                                                   #
#     This shuffler work in: 4x4 and 5x5 puzzles.   #
#     The arguments are in lib/__init__.py file     #
#     Version of Lucia: 1.0                         #
#                                                   #
#-*-----------------------------------------------*-#

def Lucia(cube):
    moves = []
    old = 0
    if cube == '4x4': size = 41
    else: size = 61

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
        x = randint(1, 2)
        if cube == '4x4':
            if moves[letter] in 'RFU':
                if x == 1: moves[letter] = f'{moves[letter]}w' # add 'w'
                if x == 2: pass # do nothing "\_(シ)_/"
        else:
            if x == 1: moves[letter] = f'{moves[letter]}w'
            if x == 2: pass # do nothing "\_(シ)_/"

        x = randint(1, 3)
        if x == 1: moves[letter] = f'{moves[letter]}\'' # add apostrophe
        if x == 2: moves[letter] = f'{moves[letter]}2' # add two
        if x == 3: pass # do nothing "\_(シ)_/"

    return moves

def Naldo(cube):
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
                if x == 3: pass # do nothing "\_(シ)_/"
        else:
            if x == 1: moves[letter] = f'{moves[letter]}w'
            if x == 2: moves[letter] = f'3{moves[letter]}w'
            if x == 3: pass # do nothing "\_(シ)_/"

        x = randint(1, 3)
        if x == 1: moves[letter] = f'{moves[letter]}\'' # add apostrophe
        if x == 2: moves[letter] = f'{moves[letter]}2' # add two
        if x == 3: pass # do nothing "\_(シ)_/"

    return moves

def Marcos():
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

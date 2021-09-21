#-*----- import area -----*-#
from random import randint  #
#-*-----------------------*-#

#-*-------------- Salete shuffler --------------*-#
#                                                 #
#   This shuffler work in: 2x2 and 3x3 puzzles    #
#   to use in 3x3 then size=20                    #
#   to 2x2 then size=9                            #
#   this arguments are in lib.py file             #
#   Version of salete: 1.0                        #
#                                                 #
#-*---------------------------------------------*-#
def Salete(size):
    moves = [] # Letters enter here
    old = 0 # variable to not repeat letter
    for move in range(1, 1+size):
        while True:
            m = randint(1, 6) # the cube have 6 moves these are:

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
                    moves.append('D') # Down
                    break
                if m == 5:
                    old = m
                    moves.append('F') # Front
                    break
                if m == 6:
                    old = m
                    moves.append('B') # Back
                    break

    # Here is to add apostruphe('), two(2) to the letters randomly
    for letter in range(0, size):
        x = randint(1, 3)
        if x == 1: moves[letter] = f'{moves[letter]}\'' # add apostrophe
        if x == 2: moves[letter] = f'{moves[letter]}2' # add two
        if x == 3: pass # do nothing "\_(シ)_/"

    return moves

#-*-------------- Cida shuffler --------------*-#
#                                               #
#   This shuffler work in: pyranmix             #
#   To use then size=4                          #
#   this arguments are in lib/__init__ file     #
#   Version of Cida: 1.0                        #
#                                               #
#-*-------------------------------------------*-#
def Cida(size, corner):
    moves = [] # Letters enter here
    old = 0 # variable to not repeat letter
    for move in range(1, 1+size):
        while True:
            m = randint(1, 4) # the pyranmix have 4 initial moves these are:

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

    for move in range(1, 1+corner):
        while True:
            m = randint(1, 4) # the pyranmix have 4 final moves these are:

            if not m == old:
                if m == 1:
                    old = m
                    moves.append('u') # Up tip
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
    for letter in range(0, size + corner):
        x = randint(1, 2)
        if x == 1: moves[letter] = f'{moves[letter]}\'' # add apostrophe
        if x == 2: pass # do nothing "\_(シ)_/"

    return moves

def Lucia(size):
    moves = []
    old = 0
    for moves in range(1, 1+size):
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
    return moves
    

import sys
import copy
import time
from collections import defaultdict
from collections import deque

start = []
states = deque()
utils = deque()
tree = defaultdict(list)
end_states = []
b_h = 4 #x limit
b_w = 5 #y limit
end = False
util = {}
col = -1

def getState():
    path = 'board.txt'
    for x in range (1, len(sys.argv)): #collect full path (including possible spaces)
        path = path + sys.argv[x] + ' '
    file = open(path, 'r')
    for line in file:
        start.append([str(s) for s in line.lower()])
    file.close()
    tree[getStr(start)].append("Start")
    states.append(start)
    #heapq.heappush(h,start)

def getStr(s): #returns state as string
    list = sum(s, [])
    str = ''.join(list)
    return str

def printState(s):
    for x in range (0, b_h):
        print()
        for y in range(0, b_w):
            #print(y)
            print (s[x][y], end='')
            if len(s[x][y]) ==1:
                print("  ", end='')
            else:
                print(" ",end ='')

    print()

# list of possible [col,row] placements (note board array is [row,col])
def valMoves(s):
    p_state = copy.deepcopy(s)
    val_moves = []
    new_states = []
    turn = getTurn(s)
    if turn != "Tie":
        for col in range (0,b_w):
            if(s[0][col]=="."):
                val_moves.append([col,-1])
        for v in  range(0,len(val_moves)):
            c = val_moves[v][0]
            for x in range (b_h-1,-1,-1):
                if s[x][c] == ".":
                    val_moves[v][1] = x
                    break
        for move in val_moves: #create list of new states from moves
            new = copy.deepcopy(p_state)
            new[move[1]][move[0]] = turn
            new_states.append(new)
        return new_states
    else:
        end_states.append(p_state)

def logMoves(s, new_states):
    global end
    #print("Number of new: " + str(len(new_states)))
    if(len(new_states)>5):
        print("IMPOSSIBLE")
    for state in new_states:
        winner = isWin(state)
        move_str = getStr(state)
        if move_str not in tree:
            tree[move_str].append(s)
        if(winner == "x" or winner == "o"):
            #printState(state)
            #end_states.append([new, s])
            end_states.append(state)
            #printState(state)
            #print(winner + " Wins!")
            #print("End states: " + str(len(end_states)))
            #if len(end_states)==10:
               # end = True
            return
    for state in new_states: #if group does not contain winning move
        if getTurn(state) == "Tie":
            end_states.append(state)
        else:
            states.append(state)






        #testing
       # for move in val_moves:
           # print(str(move),end ='')

def getTurn(s):
    x_count = 0
    o_count = 0
    s_count = 0
    for x in range (0, b_h):
        for y in range(0, b_w):
            if s[x][y]=="x":
                x_count += 1
            if s[x][y]=="o":
                o_count += 1
            if s[x][y]==".":
                s_count +=1
    if s_count == 0:
        return "Tie"
    elif x_count == o_count:
        return "x"
    elif x_count == o_count +1:
        return "o"
    else:
        return "Invalid"

#check for 3-in-a-row
def isWin(s):

    for x in range (0, b_h):
        for y in range(0, b_w):
            if(s[x][y]) != ".":
                str = s[x][y]
                group = 1

               #vertical
                if(x<=b_h-3):
                    for tx in range (x+1,b_h):
                        if (s[tx][y]== str):
                            group +=1
                        else:
                            group = 1
                            break
                        if group == 3:
                            #print("vert")
                            return str

                #horizontal
                if(y<=b_w-3):
                    for ty in range(y+1,b_w):
                        if (s[x][ty] == str):
                            group +=1
                        else:
                            group = 1
                            break
                        if group == 3:
                            #print("horz")
                            return str

                tx = x+1
                ty = y+1
                #diagonal right
                if(x<=b_h-3 and y<=b_w-3):
                    while tx<b_h and ty<b_w:
                        if s[tx][ty] == str:
                            group +=1
                            tx+=1
                            ty+=1
                        else:
                            group = 1
                            break
                        if group == 3:
                            #print("DR")
                            return str

                tx = x+1
                ty = y-1
                #diagonal left
                if(x<=b_h-3 and y>=b_w-3):
                    while tx<b_h and ty>-1:
                        if s[tx][ty] == str:
                            group +=1
                            tx+=1
                            ty-=1
                        else:
                            group =1
                            break
                        if group == 3:
                            #print("DL")
                            return str

    return "none"  # no winner

def calcUtil(s):
    #printState(s)
    minmax = []
    turn = getTurn(s)
    #print(len(tree))
    parents = tree[getStr(s)]  # state can have multiple parents
    #print(len(parents))
    if getStr(s) not in util: #end state
        winner = isWin(s)
        for parent in parents:
            if parent != "Start":
                p_string = getStr(parent)
                if winner == "x":
                    util[p_string] = 1
                    util[getStr(s)] = 1
                elif winner == "o":
                    util[p_string] = -1
                    util[getStr(s)] = -1
                elif turn == "Tie":
                    util[p_string] = 0
                    util[getStr(s)] = 0

                utils.append(parent)
    else: #parent of a node with util
        for parent in parents:
            if parent != "Start":
                p_string = getStr(parent)
                for val_move in valMoves(parent):
                    if getStr(val_move) in util:
                        minmax.append(util[getStr(val_move)])
                if turn == "x": #turn of current state (opposite parent)
                    util[p_string] = min(minmax)
                elif turn == "o":
                    util[p_string] = max(minmax)
                utils.append(parent)
                if getStr(parent) == getStr(start):
                    continue
            else:
                continue

def getCol(s,m):
    for x in range (0, b_h):
            for y in range(0, b_w):
                if s[x][y] != m[x][y]:
                    return y

getState()
if isWin(start) != "none":
    print(isWin(start) + " already won!")
    end = True
if getTurn(start) == "Invalid":
    print("Invalid state")
    end = True
#printState(start)
#print(str(getTurn(start)) + " Moves")
#print("\n" + isWin(start) + " Wins!")
#print(getStr(start))

if end == False:

    while len(states)!= 0 and end == False:
        #print(len(states))
        next_state = states.popleft()
        logMoves(next_state,valMoves(next_state))

    #print("We made it!")
    counter = 0
    for state in end_states:
        calcUtil(state)
        counter+=1
        #print("End_State: " + str(counter))
    while len(utils)!=0:
        next_util = utils.popleft()
        calcUtil(next_util)
    """minmax = []
    turn = getTurn(start)
    for move in valMoves(start):
        if getStr(move) in util:
            minmax.append(util[getStr(move)])
            #print("Util of moves: " + str(util[getStr(move)]))
    if turn == "x":  # turn of current state (opposite parent)
        util[getStr(start)] = max(minmax)
    elif turn == "o":
        util[getStr(start)] = max(minmax)"""
    for move in valMoves(start):
        if getStr(move) in util:
            if util[getStr(move)] == util[getStr(start)]:
                best_move = move
                #printState(best_move)
                col = getCol(start,best_move)
    #print(len(util))
    #print(util[getStr(start)])
    print(str(util[getStr(start)]) + " " + getTurn(start).upper() + str(col))

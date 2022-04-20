from pyswip import Prolog, call, Functor
import random
import copy

rmidx = 0

prolog = Prolog()
prolog.consult("agent.pl")
reborn=Functor("reborn",0)
move = Functor("move",2)
reposition= Functor("reposition",1)

COIN_COUNT=1
PORTAL_COUNT=3
def printMap(mazeMap):
    for maplist in mazeMap:
        row0=[]
        row1=[]
        row2=[]
        for cube in maplist:
            row0+=cube[0]+[' ']
            row1+=cube[1]+[' ']
            row2+=cube[2]+[' ']
            
        for el in row0:
            print(el,end=' ')
        print()
        for el in row1:
            print(el,end=' ')
        print()
        for el in row2:
            print(el,end=' ')
        print()
        print()

def generateFixedMap():
    mazeMap = []
    for i in range(7):
        maplist=[]
        for j in range(6):
            if i == 0 or i == 6 or j == 0 or j == 5:
                maplist.append([['#','#','#'],['#','#','#'],['#','#','#']])
            else:
                maplist.append([['.','.','.'],[' ','?',' '],['.','.','.']])
        mazeMap.append(maplist)
    
    # portal positions
    portalPos = [[2,2],[4,3],[3,1]]
    for x,y in portalPos:
        mazeMap[6-y][x][1][0] = '-'
        mazeMap[6-y][x][1][1] = 'O'
        mazeMap[6-y][x][1][2] = '-'
        for ychange in [-1,0,1]:
            for xchange in [-1,0,1]:
                if (xchange==0 or ychange==0) and not(xchange==0 and ychange==0):
                    if 6-y+ychange!=0 and 6-y+ychange!=6 and x+xchange!=0 and x+xchange!=5:
                        mazeMap[6-y+ychange][x+xchange][0][2]='T'
    
    # wumpus position                    
    x,y=[1,1]
    mazeMap[6-y][x][1][0] = '-'
    mazeMap[6-y][x][1][1] = 'W'
    mazeMap[6-y][x][1][2] = '-'
    for ychange in [-1,0,1]:
        for xchange in [-1,0,1]:
            if (xchange==0 or ychange==0) and not(xchange==0 and ychange==0):
                if 6-y+ychange!=0 and 6-y+ychange!=6 and x+xchange!=0 and x+xchange!=5:
                    mazeMap[6-y+ychange][x+xchange][0][1]='='

    # coin position
    x,y=[3,3]             
    mazeMap[6-y][x][2][0] = '*'

    # agent position
    x,y = [3,5]
    mazeMap[6-y][x][1][0] = '-'
    mazeMap[6-y][x][1][1] = '^'
    mazeMap[6-y][x][1][2] = '-'

    return [x,y], mazeMap


def generateMap():
    mazeMap = []
    for i in range(7):
        maplist=[]
        for j in range(6):
            if i == 0 or i == 6 or j == 0 or j == 5:
                maplist.append([['#','#','#'],['#','#','#'],['#','#','#']])
            else:
                maplist.append([['.','.','.'],[' ','?',' '],['.','.','.']])
        mazeMap.append(maplist)
    usedPos = []
    coinPos = []
    coins=0
    while(coins < COIN_COUNT):
        temp = [random.randint(1,4),random.randint(1,5)]
        if temp not in usedPos:
            coins+=1
            coinPos.append(temp)
            usedPos.append(temp)

    wumpusPos = []
    while(True):
        temp = [random.randint(1,4),random.randint(1,5)]
        if temp not in usedPos:
            wumpusPos = temp
            usedPos.append(wumpusPos)
            break

    portalPos = []
    portals=0
    while(portals < PORTAL_COUNT):
        temp = [random.randint(1,4),random.randint(1,5)]
        if temp not in usedPos:
            portals+=1
            portalPos.append(temp)
            usedPos.append(temp)

    agentPos=[]
    while(True):
        temp = [random.randint(1,4),random.randint(1,5)]
        if temp not in portalPos and temp != wumpusPos:
            agentPos = temp
            break

    for x,y in coinPos:
        mazeMap[6-y][x][2][0] = '*'

    x,y=wumpusPos
    mazeMap[6-y][x][1][0] = '-'
    mazeMap[6-y][x][1][1] = 'W'
    mazeMap[6-y][x][1][2] = '-'
    for ychange in [-1,0,1]:
        for xchange in [-1,0,1]:
            if (xchange==0 or ychange==0) and not(xchange==0 and ychange==0):
                if 6-y+ychange!=0 and 6-y+ychange!=6 and x+xchange!=0 and x+xchange!=5:
                    mazeMap[6-y+ychange][x+xchange][0][1]='='

    for x,y in portalPos:
        mazeMap[6-y][x][1][0] = '-'
        mazeMap[6-y][x][1][1] = 'O'
        mazeMap[6-y][x][1][2] = '-'
        for ychange in [-1,0,1]:
            for xchange in [-1,0,1]:
                if (xchange==0 or ychange==0) and not(xchange==0 and ychange==0):
                    if 6-y+ychange!=0 and 6-y+ychange!=6 and x+xchange!=0 and x+xchange!=5:
                        mazeMap[6-y+ychange][x+xchange][0][2]='T'

    x,y=agentPos
    mazeMap[6-y][x][1][0] = '-'
    mazeMap[6-y][x][1][1] = random.choice(['^','>','<','v'])
    mazeMap[6-y][x][1][2] = '-'

    return agentPos,mazeMap


def getStenchTingleGlitter(x,y,absoluteMap):
    res=[]
    if absoluteMap[6-y][x][0][1]=='=':
        res.append("on")
    else:
        res.append("off")
    if absoluteMap[6-y][x][0][2]=='T':
        res.append("on")
    else:
        res.append("off")
    if absoluteMap[6-y][x][2][0]=='*':
        res.append("on")
    else:
        res.append("off")
    return res

def isWall(x,y,absoluteMap):
    if absoluteMap[6-y][x][1][1] == '#':
        return True
    else:
        return False

def isWumpus(x,y,absoluteMap):
    if absoluteMap[6-y][x][1][1] == 'W':
        return True
    else:
        return False

def isPortal(x,y,absoluteMap):
    if absoluteMap[6-y][x][1][1] == 'O':
        return True
    else:
        return False

def moveforward(agentPos, absoluteMap, numCoins,hasArrow):
    x,y=agentPos
    d = absoluteMap[6-y][x][1][1]
    newx,newy=agentPos
    if d == '^':
        newy=y+1
    elif d == '<':
        newx=x-1
    elif d == 'v':
        newy=y-1
    elif d == '>':
        newx=x+1
    L=[]
    if isWall(newx,newy,absoluteMap):
        L=["off"]+getStenchTingleGlitter(x,y,absoluteMap)+["on","off"]
        call(move("moveforward", L))
        
    elif isWumpus(newx,newy,absoluteMap):
        agentPos,absoluteMap = generateMap()
        numCoins=0
        newx,newy=agentPos
        hasArrow=True
        L=["on"]+getStenchTingleGlitter(newx,newy,absoluteMap)+["off","off"]
        call(reborn())
        call(reposition(L))
    
    elif isPortal(newx,newy,absoluteMap):
        agentPos=[]
        while(True):
            temp = [random.randint(1,4),random.randint(1,5)]
            if absoluteMap[6-temp[1]][temp[0]][1][1] != "W" and absoluteMap[6-temp[1]][temp[0]][1][1] != "O":
                agentPos = temp
                break
        newx,newy=agentPos
        absoluteMap[6-y][x][1][1] = "?"
        absoluteMap[6-y][x][1][0] = " "
        absoluteMap[6-y][x][1][2] = " "    
        absoluteMap[6-newy][newx][1][0] = "-"    
        absoluteMap[6-newy][newx][1][1] = random.choice(['^','>','<','v'])    
        absoluteMap[6-newy][newx][1][2] = "-"
        for row in absoluteMap:
            for cube in row:
                if cube[1][1]=='S':
                    cube[1][1]='?'
        L=["on"]+getStenchTingleGlitter(newx,newy,absoluteMap)+["off","off"]
        call(reposition(L))
    
    else:
        absoluteMap[6-y][x][1][1] = "S"
        absoluteMap[6-y][x][1][0] = " "
        absoluteMap[6-y][x][1][2] = " "    
        absoluteMap[6-newy][newx][1][0] = "-"    
        absoluteMap[6-newy][newx][1][1] = d    
        absoluteMap[6-newy][newx][1][2] = "-"
        agentPos=[newx,newy]
        L=["off"]+getStenchTingleGlitter(newx,newy,absoluteMap)+["off","off"]
        call(move("moveforward", L))

    return agentPos, absoluteMap, numCoins, hasArrow, L

def turnleft(agentPos, absoluteMap):
    x,y=agentPos    
    d = absoluteMap[6-y][x][1][1]
    if d == '^':
        absoluteMap[6-y][x][1][1] = '<'
    elif d == '<':
        absoluteMap[6-y][x][1][1] = 'v'
    elif d == 'v':
        absoluteMap[6-y][x][1][1] = '>'
    elif d == '>':
        absoluteMap[6-y][x][1][1] = '^'
    L=["off"]+getStenchTingleGlitter(x,y,absoluteMap)+["off","off"]
    call(move("turnleft", L))
    return absoluteMap, L
        
def turnright(agentPos, absoluteMap):
    x,y = agentPos
    d = absoluteMap[6-y][x][1][1]
    if d == '^':
        absoluteMap[6-y][x][1][1] = '>'
    elif d == '<':
        absoluteMap[6-y][x][1][1] = '^'
    elif d == 'v':
        absoluteMap[6-y][x][1][1] = '<'
    elif d == '>':
        absoluteMap[6-y][x][1][1] = 'v'

    L=["off"]+getStenchTingleGlitter(x,y,absoluteMap)+["off","off"]
    call(move("turnright", L))

    return absoluteMap, L

def pickup(agentPos, absoluteMap, numCoins):
    x,y = agentPos
    if absoluteMap[6-y][x][2][0]=='*':
        absoluteMap[6-y][x][2][0] = '.'
        numCoins += 1

    L=["off"]+getStenchTingleGlitter(x,y,absoluteMap)+["off","off"]
    call(move("pickup", L))
    return absoluteMap,numCoins, L

def killWumpus(x,y,absoluteMap):
    absoluteMap[6-y][x][1][1] = "?"
    absoluteMap[6-y][x][1][0] = " "
    absoluteMap[6-y][x][1][2] = " "
    for ychange in [-1,0,1]:
        for xchange in [-1,0,1]:
            if (xchange==0 or ychange==0) and not(xchange==0 and ychange==0):
                if 6-y+ychange!=0 and 6-y+ychange!=6 and x+xchange!=0 and x+xchange!=5:
                    absoluteMap[6-y+ychange][x+xchange][0][1]='.'
    return absoluteMap

def shoot(agentPos, absoluteMap, hasArrow):
    x,y=agentPos
    scream='off'
    
    if hasArrow:
        d = absoluteMap[6-y][x][1][1]
        
        if d == '^':
            while(y<=6):
                y+=1
                if absoluteMap[6-y][x][1][1] == 'W':
                    absoluteMap = killWumpus(x,y,absoluteMap)
                    scream='on'
                    break
        elif d == 'v':
            while(y>=0):
                y-=1
                if absoluteMap[6-y][x][1][1] == 'W':
                    absoluteMap = killWumpus(x,y,absoluteMap)
                    scream='on'
                    break
        elif d == '<':
            while(x>=0):
                x-=1
                if absoluteMap[6-y][x][1][1] == 'W':
                    absoluteMap = killWumpus(x,y,absoluteMap)
                    scream='on'
                    break
        elif d == '>':
            while(x<=5):
                x+=1
                if absoluteMap[6-y][x][1][1] == 'W':
                    absoluteMap = killWumpus(x,y,absoluteMap)
                    scream='on'
                    break
        
        hasArrow = False
    L=["off"]+getStenchTingleGlitter(agentPos[0],agentPos[1],absoluteMap)+["off"]
    L.append(scream)
    call(move("shoot",L))
    return absoluteMap, hasArrow, L

def generateRelativeMap(L):
    visited=list(prolog.query("visited(X,Y)"))
    safe=list(prolog.query("safe(X,Y)"))
    stench=list(prolog.query("stench(X,Y)"))
    tingle=list(prolog.query("tingle(X,Y)"))
    glitter=list(prolog.query("glitter(X,Y)"))
    wumpus=list(prolog.query("wumpus(X,Y)"))
    confundus=list(prolog.query("confundus(X,Y)"))
    wall=list(prolog.query("wall(X,Y)"))
    current=list(prolog.query("current(X,Y,D)"))
    current=current[0]
    currentPos={'X':current['X'], 'Y':current['Y']}
    currentD=current['D']
    furthestX=0
    furthestY=0
    for coords in visited:
        x=coords['X']
        y=coords['Y']
        if abs(x)>furthestX:
            furthestX=abs(x)
        if abs(y)>furthestY:
            furthestY=abs(y)
    furthestX+=1
    furthestY+=1
    relmap=[]
    row=[]
    for i in range(furthestX*2+1):
        row.append([[0,0,0],[0,0,0],[0,0,0]])
    for i in range(furthestY*2+1):
        newrow=row[:]
        relmap.append(newrow)
    
    for y in range(-furthestY,furthestY+1):
        for x in range(-furthestX,furthestX+1):
            newtile=[[0,0,0],[0,0,0],[0,0,0]]
            coordToTest={'X':x,'Y':y}
            newtile[0][0]='.'
            newtile[2][1]='.'       
            newtile[2][2]='.'
            if coordToTest in stench:
                newtile[0][1]='='
            else:
                newtile[0][1]='.'
            if coordToTest in tingle:
                newtile[0][2]='T'
            else:
                newtile[0][2]='.'
            newtile[1][0]=' '
            newtile[1][1]='?'
            newtile[1][2]=' '
            if coordToTest in safe:
                newtile[1][1]='s'
            if coordToTest in visited:
                newtile[1][1]='S'
            if coordToTest in wumpus:
                newtile[1][0]='-'
                newtile[1][1]='W'
                newtile[1][2]='-'
            if coordToTest in confundus:
                newtile[1][0]='-'
                newtile[1][1]='O'
                newtile[1][2]='-'
            if (coordToTest in confundus) and (coordToTest in wumpus):
                newtile[1][0]='-'
                newtile[1][1]='U'
                newtile[1][2]='-'
            if coordToTest==currentPos:
                newtile[1][0]='-'
                if currentD=='rnorth':
                    newtile[1][1]='^'
                if currentD=='rsouth':
                    newtile[1][1]='v'
                if currentD=='reast':
                    newtile[1][1]='>'
                if currentD=='rwest':
                    newtile[1][1]='<'
                newtile[1][2]='-'
                if L[0]=="on":
                    newtile[0][0]='%'
                if L[4]=="on":
                    newtile[2][1]='B'
                if L[5]=="on":
                    newtile[2][2]='@'
            if coordToTest in glitter:
                newtile[2][0]='*'
            else:
                newtile[2][0]='.'
            if coordToTest in wall:
                newtile=[['#','#','#'],['#','#','#'],['#','#','#']]
            relmap[-y+furthestY][x+furthestX]=newtile
    return relmap 
            
def TranslateSensoryInputs(L):
    sinputs = []
    if L[0] == 'on':
        sinputs.append('Confounded')
    else:
        sinputs.append('C')
    if L[1] == 'on':
        sinputs.append('Stench')
    else:
        sinputs.append('S')
    if L[2] == 'on':
        sinputs.append('Tingle')
    else:
        sinputs.append('C')
    if L[3] == 'on':
        sinputs.append('Glitter')
    else:
            sinputs.append('G')
    if L[4] == 'on':
        sinputs.append('Bump')
    else:
            sinputs.append('B')
    if L[5] == 'on':
        sinputs.append('Scream')
    else:
        sinputs.append('S')
    
    return '-'.join(sinputs)

def incrementIdx():
    global rmidx
    rmidx += 1

def TestCorrectness(testSequence):

    agentPos,absoluteMap = generateFixedMap()
    numCoins = 0
    hasArrow = True
    L=["on"]+getStenchTingleGlitter(agentPos[0],agentPos[1],absoluteMap)+["off","off"]
    call(reborn())
    call(reposition(L))
            
    print("############# TEST CORRECTNESS START #############\n")
    print("Absolute Map:")
    printMap(absoluteMap)
    print("-----------------------------------------------------\n")

    print("Percepts:", TranslateSensoryInputs(L))
    print("Number of coins:", numCoins)
    print("Driver Has Arrow?", hasArrow)
    print("Agent Has Arrow?", bool(list(prolog.query("hasarrow()"))))
    relativePos = list(prolog.query("current(X,Y,D)"))
    print("Agent Current Position:", "("+str(relativePos[0]['X'])+","+str(relativePos[0]['Y'])+"), "+str(relativePos[0]['D']))
    
    incrementIdx()
    print("Initial Relative Map: (RM"+str(rmidx)+")")
    printMap(generateRelativeMap(L))

    print("Test Sequence:")
    print(", ".join(testSequence))
    print("")
    
    for action in testSequence:
        
        if action=='moveforward':
            agentPos,absoluteMap,numCoins,hasArrow,L=moveforward(agentPos,absoluteMap,numCoins,hasArrow)
        elif action=='turnleft':
            absoluteMap,L=turnleft(agentPos,absoluteMap)
        elif action=='turnright':
            absoluteMap,L=turnright(agentPos,absoluteMap)
        elif action=='pickup':
            absoluteMap,numCoins,L=pickup(agentPos,absoluteMap,numCoins)
        elif action=='shoot':
            absoluteMap,hasArrow,L=shoot(agentPos,absoluteMap,hasArrow)
        
        print("-----------------------------------------------------\n")

        print("Action:", action)

        print("Percepts:", TranslateSensoryInputs(L))
        print("Number of coins:", numCoins)
        print("Driver Has Arrow?", hasArrow)
        print("Agent Has Arrow?", bool(list(prolog.query("hasarrow()"))))
        relativePos = list(prolog.query("current(X,Y,D)"))
        print("Agent Current Position:", "("+str(relativePos[0]['X'])+","+str(relativePos[0]['Y'])+"), "+str(relativePos[0]['D']))

        incrementIdx()
        print("\nRelative Map: (RM"+str(rmidx)+")")
        printMap(generateRelativeMap(L))

    print("\n############# TEST CORRECTNESS END #############\n")

#Test correctness 
# print("Test: Localisation and mapping abilities, sensory inference and memory management after stepping into confundus portal\n")  
# TestCorrectness(["moveforward","turnright","turnright","moveforward","moveforward","pickup","turnright","moveforward","moveforward","turnleft","moveforward","shoot","turnleft","moveforward"])

# Test end game reset correctness
# print("Test: End game reset due to stepping into Wumpus\n")
# TestCorrectness(["shoot","turnleft","moveforward","moveforward","turnleft","moveforward","moveforward","moveforward","moveforward"])

def getSequence():
    path=list(prolog.query("explore(L)",maxresult=1))
    return path[0]['L']

def TestExplore():
    print("############# TEST EXPLORE START #############\n")
    agentPos,absoluteMap = generateMap()
    origin=agentPos[:]
    numCoins = 0
    hasArrow = True
    L=["on"]+getStenchTingleGlitter(agentPos[0],agentPos[1],absoluteMap)+["off","off"]
    call(reborn())
    call(reposition(L))

    print("Absolute Map:")
    printMap(absoluteMap)
    print("-----------------------------------------------------\n")

    print("Percepts:", TranslateSensoryInputs(L))
    print("Number of coins:", numCoins)
    print("Driver Has Arrow?", hasArrow)
    print("Agent Has Arrow?", bool(list(prolog.query("hasarrow()"))))
    relativePos = list(prolog.query("current(X,Y,D)"))
    print("Agent Current Position:", "("+str(relativePos[0]['X'])+","+str(relativePos[0]['Y'])+"), "+str(relativePos[0]['D']))
    
    incrementIdx()
    print("\nInitial Relative Map: (RM"+str(rmidx)+")")
    printMap(generateRelativeMap(L))

    if L[3] == 'on':
        absoluteMap,numCoins,L=pickup(agentPos,absoluteMap,numCoins)

    path = getSequence()
    oldMap=copy.deepcopy(absoluteMap)
    while len(path) != 0:
        print("====================================================\n")
        print("Path generated by agent:")
        print(", ".join(path))

        print("Percepts:", TranslateSensoryInputs(L))
        print("Number of coins:", numCoins)
        print("Driver Has Arrow?", hasArrow)
        print("Agent Has Arrow?", bool(list(prolog.query("hasarrow()"))))
        relativePos = list(prolog.query("current(X,Y,D)"))
        print("Agent Current Position:", "("+str(relativePos[0]['X'])+","+str(relativePos[0]['Y'])+"), "+str(relativePos[0]['D']))
        
        incrementIdx()
        print("\nBefore Execute Path Relative Map: (RM"+str(rmidx)+")")
        printMap(generateRelativeMap(L))
        print("-----------------------------------------------------\n")

        for action in path:
            
            if action=='moveforward':
                agentPos,absoluteMap,numCoins,hasArrow,L=moveforward(agentPos,absoluteMap,numCoins,hasArrow)
            elif action=='turnleft':
                absoluteMap,L=turnleft(agentPos,absoluteMap)
            elif action=='turnright':
                absoluteMap,L=turnright(agentPos,absoluteMap)
            elif action=='pickup':
                absoluteMap,numCoins,L=pickup(agentPos,absoluteMap,numCoins)
            elif action=='shoot':
                absoluteMap,hasArrow,L=shoot(agentPos,absoluteMap,hasArrow)
                    
            if L[0] == 'on':
                print('Unsafe spot')
                break

            if L[3] == 'on':
                absoluteMap,numCoins,L=pickup(agentPos,absoluteMap,numCoins)

            print("Action:",action)
            print("Percepts:", TranslateSensoryInputs(L))
            print("Number of coins:", numCoins)
            print("Driver Has Arrow?", hasArrow)
            print("Agent Has Arrow?", bool(list(prolog.query("hasarrow()"))))
            relativePos = list(prolog.query("current(X,Y,D)"))
            print("Agent Current Position:", "("+str(relativePos[0]['X'])+","+str(relativePos[0]['Y'])+"), "+str(relativePos[0]['D']))

            incrementIdx()
            print("\nAfter Action Relative Map: (RM"+str(rmidx)+")")
            printMap(generateRelativeMap(L))
            print("-----------------------------------------------------\n")

        x,y=agentPos
        if oldMap[6-y][x][1][1]=='S' and L[4] == 'off':
            print('Cell has been visited')
            break

        path = getSequence()
        oldMap=copy.deepcopy(absoluteMap)

    if agentPos!=origin:
        print("Agent did not return to origin")
    else: 
        print("Agent returned to origin")

    for row in absoluteMap:
        for cube in row:
            if cube[1][1]== 'S' and cube[2][0] == '*':
                print('Discovered coin uncollected')
                
    visited=list(prolog.query("visited(X,Y)"))
    safe=list(prolog.query("safe(X,Y)"))
    wall=list(prolog.query("wall(X,Y)"))

    for s in safe:
        if s not in visited and s not in wall:
            print(s)
            print('Unvisited safe location')
    
    print("Number of coins:", numCoins)
    print("\n############# TEST EXPLORE END #############\n")

# Test Agent’s exploration capabilities
print("Test: Agent exploration capabilities\n")
TestExplore()
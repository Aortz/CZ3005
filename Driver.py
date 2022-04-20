from pyswip import Prolog, call, Functor
import random
import copy

relativeMapIndex = 0

prolog = Prolog()
prolog.consult("Agent.pl")
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
        for cell in maplist:
            row0+=cell[0]+[' ']
            row1+=cell[1]+[' ']
            row2+=cell[2]+[' ']
            
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

#Fixed Map Generation
def generateFixedPortal(mazeMap):
    PORTAL_POSITION = [[2,4],[4,4],[5,2]]
    for x,y in PORTAL_POSITION:
        yoffset = 5-y
        mazeMap[yoffset][x][1][0] = '-'
        mazeMap[yoffset][x][1][1] = 'O'
        mazeMap[yoffset][x][1][2] = '-'
        for ychange in [-1,0,1]:
            for xchange in [-1,0,1]:
                if (xchange==0 or ychange==0) and not(xchange==0 and ychange==0):
                    if yoffset+ychange!=0 and yoffset+ychange!=5 and x+xchange!=0 and x+xchange!=6:
                         yposition = yoffset+ychange
                         xposition = x+xchange
                         if yposition!=0 and yposition!=5 and xposition!=0 and xposition!=6:
                            if mazeMap[yposition][xposition][0][2] != '#':
                                mazeMap[yposition][xposition][0][2]='T'
    return mazeMap

def generateFixedWumpus(mazeMap):
    x,y=[3,2]
    yoffset = 5-y
    mazeMap[yoffset][x][1][0] = '-'
    mazeMap[yoffset][x][1][1] = 'W'
    mazeMap[yoffset][x][1][2] = '-'
    for ychange in [-1,0,1]:
        for xchange in [-1,0,1]:
            if (xchange==0 or ychange==0) and not(xchange==0 and ychange==0):
                yposition = yoffset+ychange
                xposition = x+xchange
                if yposition!=0 and yposition!=5 and xposition!=0 and xposition!=6:
                    if mazeMap[yposition][xposition][0][1] != '#':
                        mazeMap[yposition][xposition][0][1]='='
    return mazeMap

def generateFixedMap():
    mazeMap = []
    for i in range(6):
        maplist=[]
        for j in range(7):
            if i == 0 or i == 5 or j == 0 or j == 6:
                wallSymbol = [['#','#','#'],['#','#','#'],['#','#','#']]
                maplist.append(wallSymbol)
            else:
                maplist.append([['.','.','.'],[' ','?',' '],['.','.','.']])
        mazeMap.append(maplist)
    
    # portal positions
    mazeMap = generateFixedPortal(mazeMap)

    # wumpus position
    mazeMap = generateFixedWumpus(mazeMap)                    

    # coin position
    x,y=[4,1]             
    mazeMap[5-y][x][2][0] = '*'

    # agent position
    x,y = [1,1]
    mazeMap[5-y][x][1][0] = '-'
    mazeMap[5-y][x][1][1] = '^'
    mazeMap[5-y][x][1][2] = '-'

    return [x,y], mazeMap


def checkSTG(x,y,AMap):
    indicator=[]
    yoffset = 5-y
    if AMap[yoffset][x][0][1]=='=':
        indicator.append("on")
    else:
        indicator.append("off")
    if AMap[yoffset][x][0][2]=='T':
        indicator.append("on")
    else:
        indicator.append("off")
    if AMap[yoffset][x][2][0]=='*':
        indicator.append("on")
    else:
        indicator.append("off")
    return indicator

def isWall(x,y,AMap):
    if AMap[5-y][x][1][1] == '#':
        return True
    else:
        return False

def isWumpus(x,y,AMap):
    if AMap[5-y][x][1][1] == 'W':
        return True
    else:
        return False

def isPortal(x,y,AMap):
    if AMap[5-y][x][1][1] == 'O':
        return True
    else:
        return False

def moveforward(agentPos, AMap, coinCount,hasArrow):
    x,y=agentPos
    d = AMap[5-y][x][1][1]
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
    if isWall(newx,newy,AMap):
        L=["off"]+checkSTG(x,y,AMap)+["on","off"]
        call(move("moveforward", L))
        
    elif isWumpus(newx,newy,AMap):
        agentPos,AMap = generateFixedMap()
        coinCount=0
        newx,newy=agentPos
        hasArrow=True
        L=["on"]+checkSTG(newx,newy,AMap)+["off","off"]
        call(reborn())
        call(reposition(L))
    
    elif isPortal(newx,newy,AMap):
        agentPos=[]
        while(True):
            temp = [random.randint(1,4),random.randint(1,5)]
            if AMap[5-temp[1]][temp[0]][1][1] != "W" and AMap[5-temp[1]][temp[0]][1][1] != "O":
                agentPos = temp
                break
        newx,newy=agentPos
        AMap[5-y][x][1][1] = "?"
        AMap[5-y][x][1][0] = " "
        AMap[5-y][x][1][2] = " "    
        AMap[5-newy][newx][1][0] = "-"    
        AMap[5-newy][newx][1][1] = random.choice(['^','>','<','v'])    
        AMap[5-newy][newx][1][2] = "-"
        for row in AMap:
            for cell in row:
                if cell[1][1]=='S':
                    cell[1][1]='?'
        L=["on"]+checkSTG(newx,newy,AMap)+["off","off"]
        call(reposition(L))
    
    else:
        AMap[5-y][x][1][1] = "S"
        AMap[5-y][x][1][0] = " "
        AMap[5-y][x][1][2] = " "    
        AMap[5-newy][newx][1][0] = "-"    
        AMap[5-newy][newx][1][1] = d    
        AMap[5-newy][newx][1][2] = "-"
        agentPos=[newx,newy]
        L=["off"]+checkSTG(newx,newy,AMap)+["off","off"]
        call(move("moveforward", L))

    return agentPos, AMap, coinCount, hasArrow, L

def turnleft(agentPos, AMap):
    x,y=agentPos
    yoffset = 5-y    
    d = AMap[yoffset][x][1][1]
    if d == '^':
        AMap[yoffset][x][1][1] = '<'
    elif d == '<':
        AMap[yoffset][x][1][1] = 'v'
    elif d == 'v':
        AMap[yoffset][x][1][1] = '>'
    elif d == '>':
        AMap[yoffset][x][1][1] = '^'
    L=["off"]+checkSTG(x,y,AMap)+["off","off"]
    call(move("turnleft", L))
    return AMap, L
        
def turnright(agentPos, AMap):
    x,y = agentPos
    yoffset = 5-y
    d = AMap[yoffset][x][1][1]
    if d == '^':
        AMap[yoffset][x][1][1] = '>'
    elif d == '<':
        AMap[yoffset][x][1][1] = '^'
    elif d == 'v':
        AMap[yoffset][x][1][1] = '<'
    elif d == '>':
        AMap[yoffset][x][1][1] = 'v'

    L=["off"]+checkSTG(x,y,AMap)+["off","off"]
    call(move("turnright", L))

    return AMap, L

def pickup(agentPos, AMap, coinCount):
    x,y = agentPos
    if AMap[5-y][x][2][0]=='*':
        AMap[5-y][x][2][0] = '.'
        coinCount += 1

    L=["off"]+checkSTG(x,y,AMap)+["off","off"]
    call(move("pickup", L))
    return AMap,coinCount, L

def killWumpus(x,y,AMap):
    yoffset = 5-y
    AMap[yoffset][x][1][1] = "?"
    AMap[yoffset][x][1][0] = " "
    AMap[yoffset][x][1][2] = " "
    for ychange in [-1,0,1]:
        for xchange in [-1,0,1]:
            if (xchange==0 or ychange==0) and not(xchange==0 and ychange==0):
                if yoffset+ychange!=0 and yoffset+ychange!=6 and x+xchange!=0 and x+xchange!=5:
                    AMap[yoffset+ychange][x+xchange][0][1]='.'
    return AMap

def shoot(agentPos, AMap, hasArrow):
    x,y=agentPos
    scream='off'
    yoffset=5-y
    if hasArrow:
        d = AMap[yoffset][x][1][1]
        if d == '^':
            while(y<=5):
                y+=1
                
                if AMap[5-y][x][1][1] == 'W':
                    AMap = killWumpus(x,y,AMap)
                    scream='on'
                    break
        elif d == 'v':
            while(y>=0):
                y-=1
                if AMap[5-y][x][1][1] == 'W':
                    AMap = killWumpus(x,y,AMap)
                    scream='on'
                    break
        elif d == '<':
            while(x>=0):
                x-=1
                if AMap[yoffset][x][1][1] == 'W':
                    AMap = killWumpus(x,y,AMap)
                    scream='on'
                    break
        elif d == '>':
            while(x<=6):
                x+=1
                if AMap[yoffset][x][1][1] == 'W':
                    AMap = killWumpus(x,y,AMap)
                    scream='on'
                    break
        
        hasArrow = False

    L=["off"]+checkSTG(agentPos[0],agentPos[1],AMap)+["off"]
    L.append(scream)
    call(move("shoot",L))
    return AMap, hasArrow, L

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
            trialCoord={'X':x,'Y':y}
            newtile[0][0]='.'
            newtile[2][1]='.'       
            newtile[2][2]='.'
            if trialCoord in stench:
                newtile[0][1]='='
            else:
                newtile[0][1]='.'
            if trialCoord in tingle:
                newtile[0][2]='T'
            else:
                newtile[0][2]='.'
            newtile[1][0]=' '
            newtile[1][1]='?'
            newtile[1][2]=' '
            if trialCoord in safe:
                newtile[1][1]='s'
            if trialCoord in visited:
                newtile[1][1]='S'
            if trialCoord in wumpus:
                newtile[1][0]='-'
                newtile[1][1]='W'
                newtile[1][2]='-'
            if trialCoord in confundus:
                newtile[1][0]='-'
                newtile[1][1]='O'
                newtile[1][2]='-'
            if (trialCoord in confundus) and (trialCoord in wumpus):
                newtile[1][0]='-'
                newtile[1][1]='U'
                newtile[1][2]='-'
            if trialCoord==currentPos:
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
            if trialCoord in glitter:
                newtile[2][0]='*'
            else:
                newtile[2][0]='.'
            if trialCoord in wall:
                newtile=[['#','#','#'],['#','#','#'],['#','#','#']]
            relmap[-y+furthestY][x+furthestX]=newtile
    return relmap 
            
def PerceptsTranslation(L):
    sinputs = []
    for i in range(6):
        if L[i] == 'on':
            if i == 0:
                sinputs.append('Confounded')
            if i == 1:
                sinputs.append('Stench(=)')
            if i == 2:
                sinputs.append('Tingle(T)')
            if i == 3:
                sinputs.append('Glitter(*)')
            if i == 4:
                sinputs.append('Bump(B)')
            if i == 5:
                sinputs.append('Scream')
        else:
            if i == 0:
                sinputs.append('C')
            if i == 1:
                sinputs.append('S')
            if i == 2:
                sinputs.append('T')
            if i == 3:
                sinputs.append('G')
            if i == 4:
                sinputs.append('B')
            if i == 5:
                sinputs.append('S')
    
    return '-'.join(sinputs)

def plusMapCounter():
    global relativeMapIndex
    relativeMapIndex += 1

def printStatus(hasArrow,coinCount):
    print("----------------------------------------------")
    print("| Arrow :", hasArrow, "                              |")
    print("| Coins collected :", coinCount, "                       |")
    relativePos = list(prolog.query("current(X,Y,D)"))
    print("| Current Position :", "X="+str(relativePos[0]['X'])+", Y="+str(relativePos[0]['Y'])+", D="+str(relativePos[0]['D']), "      |")
    print("----------------------------------------------")

def TestCorrectness(testSequence):
    agentPos,AMap = generateFixedMap()
    coinCount = 0
    hasArrow = True
    L=["on"]+checkSTG(agentPos[0],agentPos[1],AMap)+["off","off"]
    call(reborn())

    print("Percepts:", PerceptsTranslation(L))
    
    print("------------- TEST CORRECTNESS START -------------\n")
    print("Absolute Map:")
    printMap(AMap)
    print("-----------------------------------------------------\n")

    printStatus(hasArrow,coinCount)
    
    plusMapCounter()
    print("\nInitial Map: ("+str(relativeMapIndex)+")")
    printMap(generateRelativeMap(L))

    print("Test Sequence:")
    print(", ".join(testSequence))
    print("")
    
    for action in testSequence:
        
        if action=='moveforward':
            agentPos,AMap,coinCount,hasArrow,L=moveforward(agentPos,AMap,coinCount,hasArrow)
        elif action=='turnleft':
            AMap,L=turnleft(agentPos,AMap)
        elif action=='turnright':
            AMap,L=turnright(agentPos,AMap)
        elif action=='pickup':
            AMap,coinCount,L=pickup(agentPos,AMap,coinCount)
        elif action=='shoot':
            AMap,hasArrow,L=shoot(agentPos,AMap,hasArrow)
        
        print("-----------------------------------------------------\n")

        print("Percepts:", PerceptsTranslation(L))

        plusMapCounter()
        print("\nRelative Map: ("+str(relativeMapIndex)+")")
        print("----------------------------------------------")
        print("             Action:", action)

        printStatus(hasArrow,coinCount)

        printMap(generateRelativeMap(L))

    print("\n------------- TEST CORRECTNESS END -------------\n")

# Test correctness 
# print("Test: Localisation and mapping abilities, sensory inference and memory management after stepping into confundus portal\n")  
# TestCorrectness(["turnright","moveforward","moveforward","turnleft","shoot","turnright","moveforward","pickup","moveforward","turnleft","moveforward","moveforward"])

# Test end game reset correctness
# print("Test: End game reset due to stepping into Wumpus\n")
# TestCorrectness(["moveforward","turnright","moveforward","turnleft","shoot","turnright","moveforward","moveforward"])

def exploreSequence():
    path=list(prolog.query("explore(L)",maxresult=1))
    return (path[0]['L'])

def TestAgentExploration():
    print("------------- TEST EXPLORE START -------------\n")
    agentPos,AMap = generateFixedMap()
    origin=agentPos[:]
    coinCount = 0
    hasArrow = True
    L=["on"]+checkSTG(agentPos[0],agentPos[1],AMap)+["off","off"]
    call(reborn())

    print("Absolute Map:")
    printMap(AMap)
    print("-----------------------------------------------------\n")
    
    print("Percepts:", PerceptsTranslation(L))
    plusMapCounter()
    print("\nInitial Map: ("+str(relativeMapIndex)+")")
    printMap(generateRelativeMap(L))
    printStatus(hasArrow,coinCount)

    if L[3] == 'on':
        AMap,coinCount,L=pickup(agentPos,AMap,coinCount)

    path = exploreSequence()
    oldMap=copy.deepcopy(AMap)
    while len(path) != 0:
        print("====================================================\n")
        print("Path generated by agent:")
        print(", ".join(path))

        print("Percepts:", PerceptsTranslation(L))
        
        plusMapCounter()
        print("\nMap before Execution: ("+str(relativeMapIndex)+")")
        printMap(generateRelativeMap(L))
        printStatus(hasArrow,coinCount)
        print("-----------------------------------------------------\n")
        for action in path:
            if action=='moveforward':
                agentPos,AMap,coinCount,hasArrow,L=moveforward(agentPos,AMap,coinCount,hasArrow)
            elif action=='turnleft':
                AMap,L=turnleft(agentPos,AMap)
            elif action=='turnright':
                AMap,L=turnright(agentPos,AMap)
            elif action=='pickup':
                AMap,coinCount,L=pickup(agentPos,AMap,coinCount)
            elif action=='shoot':
                AMap,hasArrow,L=shoot(agentPos,AMap,hasArrow)
                    
            if L[0] == 'on':
                print('Unsafe spot')
                break

            if L[3] == 'on':
                AMap,coinCount,L=pickup(agentPos,AMap,coinCount)
                
            print("Percepts:", PerceptsTranslation(L))

            plusMapCounter()
            print("\nMap after Execution: ("+str(relativeMapIndex)+")")
            printMap(generateRelativeMap(L))
            print("----------------------------------------------")
            print("             Action:", action)
            printStatus(hasArrow,coinCount)
            print("-----------------------------------------------------\n")

        x,y=agentPos
        if oldMap[5-y][x][1][1]=='S' and L[4] == 'off':
            print('Cell visited')
            break

        path = exploreSequence()
        oldMap=copy.deepcopy(AMap)

    if agentPos!=origin:
        print("Agent did not return to origin")
    else: 
        print("Agent returned to origin")

    for row in AMap:
        for cell in row:
            if cell[1][1]== 'S' and cell[2][0] == '*':
                print('Discovered coin uncollected')
                
    visited=list(prolog.query("visited(X,Y)"))
    safe=list(prolog.query("safe(X,Y)"))
    wall=list(prolog.query("wall(X,Y)"))

    scount = 0
    for s in safe:
        if s not in visited and s not in wall:
            scount+=1
    print('Number of Unvisited safe location:', scount)
    
    print("Number of coins:", coinCount)
    print("\n------------- TEST EXPLORE END -------------\n")

# Test Agent’s exploration capabilities
print("Test: Agent exploration capabilities\n")
TestAgentExploration()
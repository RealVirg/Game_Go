import pygame
import mapgo
import math
import random
import sys
from queue import Queue
pygame.init()

run = True

f = open('log.txt', 'w')
f.close()
f = open('temp.txt', 'w')
f.close()

global size

size = 19
sizeFlag = 361
givingName = False
namePlayer = ''
players = {1: 'black', 2: 'white'}
dictNames = {'first': '', 'second': ''}
screen = pygame.display.set_mode((525, 525))
bg = pygame.image.load('mapgo19.png')
field = mapgo.corsMap19
sizeDraw = 10
corsScore = ((10, 10), (505, 10))
sizeFont = 30
giveScoreCors = ((175, 200), (175, 250), (175, 300))
currentPlayerCors = (225, 20)
dictLog = {1: 'A', 2: 'B', 3: 'C', 4: 'D', 5: 'E', 6: 'F', 7: 'G', 8: 'H',
           9: 'J', 10: 'K', 11: 'L', 12: 'M', 13: 'N', 14: 'O', 15: 'P',
           16: 'Q', 17: 'R', 18: 'S', 19: 'T'}
dictSave = {'A': 1, 'B': 2, 'C': 3, 'D': 4, 'E': 5, 'F': 6, 'G': 7, 'H': 8,
            'J': 9, 'K': 10, 'L': 11, 'M': 12, 'N': 13, 'O': 14, 'P': 15,
            'Q': 16, 'R': 17, 'S': 18, 'T': 19}
if len(sys.argv) == 2:
    if sys.argv[1] == '9':
        size = 9
        sizeFlag = 81
        screen = pygame.display.set_mode((691, 690))
        bg = pygame.image.load('mapgo.jpg')
        field = mapgo.corsMap
        sizeDraw = 20
        corsScore = ((50, 40), (640, 40))
        giveScoreCors = ((175, 300), (175, 400), (175, 500))
        sizeFont = 50
        currentPlayerCors = (640, 650)
    else:
        run = False
        print('WRONG SIZE')
if len(sys.argv) > 2:
    run = False
    print('WRONG SIZE')

pygame.display.set_caption("Go game")
player = 1
prevDictScore = {1: 0, 2: 0}
dictPlayer = {1: 'black', 2: 'white'}
dictScore = {1: 0, 2: 0}
endFlag = 0
black = (0, 0, 0)
white = (255, 255, 255)
dictSize = {1: sizeDraw, 2: sizeDraw, 0: 0,
            3: sizeDraw, 4: sizeDraw}
dictColor = {1: black, 2: white, 0: black,
             3: (80, 80, 80), 4: (200, 200, 200)}
screen.blit(bg, (0, 0))
pygame.display.update()
gameEnd = False
killingDead = False
gettingScore = False
stoneBlack = 0
stoneWhite = 0
KOMI = 5.5
blackTerritory = 0
whiteTerritory = 0
winner = ''
scoreBlack = ''
scoreWhite = ''
repeatDef = False
playWithBot = False
pause = False
botColor = 0
saveColor = False
complexity = 0
dictComplexity = {1: 'very easy', 2: 'easy'}


def emptyMap():
    return [[0] * size for i in range(size)]
gameMap = emptyMap()
prevMap = emptyMap()
prevPrevMap = emptyMap()


def bot1(botColor, gameMap):
    randX = random.randint(0, size - 1)
    randY = random.randint(0, size - 1)
    while True:
        if gameMap[randX][randY] != 0:
            randX = random.randint(0, size - 1)
            randY = random.randint(0, size - 1)
        else:
            break
    a = (randX, randY)
    return a


def load(gameMap, dictScore, stoneWhite, stoneBlack, endFlag,
         gameEnd, gettingScore, killingDead, repeatDef, saveColor, complexity,
         playWithBot, pause, player):
    f = open('save.txt')
    r = f.read().split('\n')
    r.pop()
    gameMapLoad = emptyMap()
    dictScore[1] = 0
    dictScore[2] = 0
    stoneWhite = 0
    stoneBlack = 0
    endFlag = 0
    gameEnd = False
    gettingScore = False
    killingDead = False
    repeatDef = False
    pause = False
    playWithBot = False
    saveColor = False
    complexity = 0
    playerLog = 0
    for line in r:
        i = int(dictSave[line.split(' ')[1]]) - 1
        j = int(line.split(' ')[0]) - 1
        playerLog = int(line.split(' ')[2])
        gameMapLoad[i][j] = playerLog
        checkForKill(dictScore, gameMapLoad, i, j)
    f.close()
    for i in range(size):
        for j in range(size):
            gameMap[i][j] = gameMapLoad[i][j]


def leaderBoard():
    pass


def save(log, save):
    f = open(log)
    ft = open(save, 'w')
    r = f.read()
    rr = r.split('\n')
    rr.pop()
    temp = ''
    for i in range(len(rr)):
        temp = temp + rr[i] + '\n'
    if save == 'log.txt':
        ft.write(temp)
    else:
        ft.write(r + str(size))
    f.close()
    ft.close()


def bot2(botColor, gameMap):
    botColorMap = emptyMap()
    humanMap = emptyMap()
    for i in range(size):
        for j in range(size):
            if gameMap[i][j] == botColor:
                botColorMap[i][j] = botColor
    iterator = 0
    listStep = []
    for i in range(size):
        for j in range(size):
            if gameMap[i][j] == botColor % 2 + 1:
                listStep.append([i + 1, j])
                listStep.append([i, j + 1])
                listStep.append([i - 1, j])
                listStep.append([i, j - 1])
    point = [0, 0]
    iterator = 0
    while iterator < 100000:
        if len(listStep) != 0:
            randomPoint = random.randint(0, len(listStep) - 1)
            if 0 <= listStep[randomPoint][0] < size and 0 <= listStep[
                            randomPoint][1] < size:
                if gameMap[listStep[randomPoint][0]][listStep[
                          randomPoint][1]] == 0:
                    point[0] = listStep[randomPoint][0]
                    point[1] = listStep[randomPoint][1]
                    break
        iterator += 1
        if iterator == 99999:
            point[0] = -1
    if point[0] != -1:
        return point
    else:
        return bot1(botColor, gameMap)


def undo(gameMap, dictScore, stoneWhite, stoneBlack, endFlag,
         gameEnd, gettingScore, killingDead, repeatDef, saveColor, complexity,
         playWithBot, pause, player):
    f = open('log.txt')
    r = f.read().split('\n')
    r.pop()
    f.close()
    if len(r) < 1:
        return
    t = r.pop()
    ff = open('temp.txt', 'a')
    ff.write(t + '\n')
    ff.close()
    temp = ''
    for i in range(len(r)):
        temp = temp + r[i] + '\n'
    f = open('log.txt', 'w')
    f.write(temp)
    f.close()
    gameMapLoad = emptyMap()
    dictScore[1] = 0
    dictScore[2] = 0
    stoneWhite = 0
    stoneBlack = 0
    endFlag = 0
    gameEnd = False
    gettingScore = False
    killingDead = False
    repeatDef = False
    pause = False
    playWithBot = False
    saveColor = False
    complexity = 0
    playerLog = 0
    for line in r:
        i = int(dictSave[line.split(' ')[1]]) - 1
        j = int(line.split(' ')[0]) - 1
        playerLog = int(line.split(' ')[2])
        gameMapLoad[i][j] = playerLog
        checkForKill(dictScore, gameMapLoad, i, j)
    for i in range(size):
        for j in range(size):
            gameMap[i][j] = gameMapLoad[i][j]


def redo(gameMap, dictScore, stoneWhite, stoneBlack, endFlag, gameEnd,
         gettingScore, killingDead, repeatDef, saveColor, complexity,
         playWithBot, pause, player):
    f = open('temp.txt')
    ff = open('log.txt')
    r = f.read().split('\n')
    rr = ff.read().split('\n')
    ff.close()
    f.close()
    if len(r) <= 1:
        f = open('temp.txt', 'w')
        f.close()
        return
    if len(r) == 2:
        i = int(dictSave[r[0].split(' ')[1]]) - 1
        j = int(r[0].split(' ')[0]) - 1
        playerLog = int(r[0].split(' ')[2])
        gameMap[i][j] = playerLog
        checkForKill(dictScore, gameMap, i, j)
        temp = ''
        rr[len(rr) - 1] = r[len(r) - 2]
        for i in range(len(rr)):
            temp = temp + rr[i] + '\n'
        f = open('log.txt', 'w')
        f.write(temp)
        f.close()
        f = open('temp.txt', 'w')
        f.close()
        return
    rr[len(rr) - 1] = r[len(r) - 2]
    rr.append(r[len(r) - 3])
    r.pop()
    r.pop()
    r.pop()
    temp = ''
    for i in range(len(rr)):
        temp = temp + rr[i] + '\n'
    f = open('log.txt', 'w')
    f.write(temp)
    f.close()
    temp = ''
    for i in range(len(r)):
        temp = temp + r[i] + '\n'
    f = open('temp.txt', 'w')
    f.write(temp)
    f.close()
    undo(gameMap, dictScore, stoneWhite, stoneBlack, endFlag, gameEnd,
         gettingScore, killingDead, repeatDef, saveColor, complexity,
         playWithBot, pause, player)


def drawWindow(dictScore, dictPlayer):
    screen.blit(bg, (0, 0))
    font = pygame.font.Font(None, 24)
    end = pygame.font.Font(None, sizeFont)
    screen.blit(font.render(str(dictScore[1]), False, dictColor[1]),
                corsScore[0])
    screen.blit(font.render(str(dictScore[2]), False, dictColor[2]),
                corsScore[1])
    for i in range(size):
        for j in range(size):
            pygame.draw.circle(screen, dictColor[gameMap[i][j]],
                               field[i][j], dictSize[gameMap[i][j]])
    if killingDead:
        screen.blit(end.render('Choose dead stone', False, (125, 125, 125)),
                    (175, 300))
    if givingName:
        screen.blit(end.render('First player: ' + dictNames['first'], False,
                    (125, 125, 125)), giveScoreCors[0])
    if givingName and not playWithBot:
        screen.blit(end.render('Second player: ' + dictNames['second'], False,
                    (125, 125, 125)), giveScoreCors[1])
    if gettingScore:
        screen.blit(end.render(scoreBlack, False, (125, 125, 125)),
                    giveScoreCors[0])
        screen.blit(end.render(scoreWhite, False, (125, 125, 125)),
                    giveScoreCors[1])
        screen.blit(end.render(winner, False, (125, 125, 125)),
                    giveScoreCors[2])
    if pause and complexity == 0:
        screen.blit(end.render('Choose: 1(very easy), 2(easy)', False,
                    (125, 125, 125)), (175, 300))
    if pause and complexity != 0:
        screen.blit(end.render('Choose: 1(black), 2(white)', False,
                               (125, 125, 125)), (175, 300))
    if gameEnd:
        screen.blit(end.render('Game over', False, (125, 125, 125)),
                    (225, 40))
    screen.blit(font.render(dictPlayer[player],
                False, dictColor[player]), currentPlayerCors)
    pygame.display.update()


def checkForKill(dictScore, gameMap,  a, b):
    visited = []
    currentStepStruct = emptyMap()
    removeFlag = False
    removeCurrent = False
    for i in range(size):
        for j in range(size):
            if visited.count((i, j)) != 0:
                continue
            struct = emptyMap()
            if gameMap[i][j] == 0:
                continue
            colorStart = gameMap[i][j]
            q = Queue()
            q.put([i, j])
            while not q.empty():
                p = q.get()
                if p[0] < 0 or p[0] > size - 1 or p[1] < 0 or p[1] > size - 1:
                    continue
                if gameMap[p[0]][p[1]] != colorStart:
                    continue
                if visited.count((p[0], p[1])) != 0:
                    continue
                struct[p[0]][p[1]] = colorStart
                visited.append((p[0], p[1]))
                q.put([p[0] - 1, p[1]])
                q.put([p[0] + 1, p[1]])
                q.put([p[0], p[1] + 1])
                q.put([p[0], p[1] - 1])
            flag = False
            for x in range(size):
                for y in range(size):
                    if struct[x][y] == colorStart:
                        if 0 < x < size - 1 and 0 < y < size - 1:
                            if gameMap[x - 1][y] == 0 or gameMap[
                                       x + 1][y] == 0 or gameMap[
                                       x][y - 1] == 0 or gameMap[
                                       x][y + 1] == 0:
                                flag = True
                        elif x == size - 1 and y == size - 1:
                            if gameMap[x - 1][y] == 0 or gameMap[
                                       x][y - 1] == 0:
                                flag = True
                        elif x == size - 1 and y == 0:
                            if gameMap[x - 1][y] == 0 or gameMap[
                                       x][y + 1] == 0:
                                flag = True
                        elif x == 0 and y == 0:
                            if gameMap[x + 1][y] == 0 or gameMap[
                                       x][y + 1] == 0:
                                flag = True
                        elif x == 0 and y == size - 1:
                            if gameMap[x + 1][y] == 0 or gameMap[
                                       x][y - 1] == 0:
                                flag = True
                        elif x == size - 1:
                            if gameMap[x - 1][y] == 0 or gameMap[
                                       x][y - 1] == 0 or gameMap[
                                       x][y + 1] == 0:
                                flag = True
                        elif x == 0:
                            if gameMap[x + 1][y] == 0 or gameMap[
                                       x][y - 1] == 0 or gameMap[
                                       x][y + 1] == 0:
                                flag = True
                        elif y == size - 1:
                            if gameMap[x - 1][y] == 0 or gameMap[
                                       x + 1][y] == 0 or gameMap[
                                       x][y - 1] == 0:
                                flag = True
                        elif y == 0:
                            if gameMap[x - 1][y] == 0 or gameMap[
                                       x + 1][y] == 0 or gameMap[
                                       x][y + 1] == 0:
                                flag = True
            if not flag and struct[a][b] != 0:
                for x in range(size):
                    for y in range(size):
                        currentStepStruct[x][y] = struct[x][y]
                removeCurrent = True
            elif not flag:
                removeFlag = True
                for x in range(size):
                    for y in range(size):
                        if struct[x][y] == colorStart:
                            if colorStart == 2:
                                dictScore[1] += 1
                            else:
                                dictScore[2] += 1
                            gameMap[x][y] = 0
    if not removeFlag and removeCurrent:
        gameMap[a][b] = 0


def getTerritory(gameMap, player):
    l = emptyMap()
    territory = 0
    for i in range(size):
        for j in range(size):
            if gameMap[i][j] == player:
                l[i][j] = player
    visited = []
    for i in range(size):
        for j in range(size):
            if visited.count((i, j)) != 0:
                continue
            struct = emptyMap()
            if l[i][j] != 0:
                continue
            q = Queue()
            q.put([i, j])
            while not q.empty():
                p = q.get()
                if p[0] < 0 or p[0] > size - 1 or p[1] < 0 or p[1] > size - 1:
                    continue
                if l[p[0]][p[1]] != 0:
                    continue
                if visited.count((p[0], p[1])) != 0:
                    continue
                struct[p[0]][p[1]] = player
                visited.append((p[0], p[1]))
                q.put([p[0] - 1, p[1]])
                q.put([p[0] + 1, p[1]])
                q.put([p[0], p[1] + 1])
                q.put([p[0], p[1] - 1])
            flag = False
            for x in range(size):
                for y in range(size):
                    if struct[x][y] == player and gameMap[
                            x][y] == player % 2 + 1:
                        flag = True
            if not flag:
                for x in range(size):
                    for y in range(size):
                        if struct[x][y] == player:
                            gameMap[x][y] = player + 2
                            territory += 1
    return territory


def ruleCo(gameMap, prevMap, prevPrevMap, dictScore, prevDictScore):
    flag = 0
    for x in range(size):
        for y in range(size):
            if gameMap[x][y] == prevPrevMap[x][y]:
                flag += 1
    if flag == sizeFlag:
        for x in range(size):
            for y in range(size):
                gameMap[x][y] = prevMap[x][y]
        dictScore[1] = prevDictScore[1]
        dictScore[2] = prevDictScore[2]
        return False
    return True


def returnSuicideStep(gameMap, i, j):
    if gameMap[i][j] == 0:
        return False
    return True


def changePreviosMap(changePrevMapFlag, prevMap, prevPrevMap, prevDictScore,
                     dictScore):
    if changePrevMapFlag:
        for x in range(size):
            for y in range(size):
                prevPrevMap[x][y] = prevMap[x][y]
        for x in range(size):
            for y in range(size):
                prevMap[x][y] = gameMap[x][y]
        prevDictScore[1] = dictScore[1]
        prevDictScore[2] = dictScore[2]


def changePlayer(changeFlag, changePrevMapFlag, player, i, j):
    if changeFlag and changePrevMapFlag:
        f = open('log.txt', 'a')
        f.write(str(j + 1) + ' ' + dictLog[i + 1] + ' ' + str(player) + '\n')
        f.close()
        f = open('temp.txt', 'w')
        f.close()
        return player % 2 + 1
    return player


while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
    keys = pygame.key.get_pressed()
    if keys[pygame.K_RETURN] and not gameEnd and givingName and not pause:
        if namePlayer == 'second' or playWithBot:
            givingName = False
            drawWindow(dictScore, dictPlayer)
        else:
            namePlayer = 'second'
        pygame.time.delay(200)
        continue
    if givingName:
        if event.type == pygame.KEYDOWN and not gameEnd and not pause:
            if keys[pygame.K_BACKSPACE] and len(dictNames[namePlayer]) != 0:
                dictNames[namePlayer] = dictNames[namePlayer][:-1]
                drawWindow(dictScore, dictPlayer)
                pygame.time.delay(100)
                continue
            dictNames[namePlayer] = dictNames[namePlayer] + event.unicode
            drawWindow(dictScore, dictPlayer)
            pygame.time.delay(100)
        continue
    if keys[pygame.K_h] and not gameEnd and not pause:
        namePlayer = 'first'
        givingName = True
        dictNames['first'] = ''
        dictNames['second'] = ''
        drawWindow(dictScore, dictPlayer)
        pygame.time.delay(100)
        continue
    if keys[pygame.K_r] and not gameEnd and not pause:
        f = open('temp.txt')
        r = f.read().split('\n')
        f.close()
        if len(r) != 1:
            redo(gameMap, dictScore, stoneWhite, stoneBlack, endFlag, gameEnd,
                 gettingScore, killingDead, repeatDef, saveColor, complexity,
                 playWithBot, pause, player)
            ff = open('temp.txt')
            rr = ff.read().split('\n')
            ff.close()
            f = open('log.txt')
            r = f.read().split('\n')
            r.pop()
            if len(r) >= 1:
                player = int(r[len(r) - 1].split(' ')[2]) % 2 + 1
                f.close()
            else:
                player = 1
            drawWindow(dictScore, dictPlayer)
            pygame.time.delay(100)
        if playWithBot:
            f = open('temp.txt')
            r = f.read().split('\n')
            f.close()
            if len(r) != 1:
                redo(gameMap, dictScore, stoneWhite, stoneBlack,
                     endFlag, gameEnd,
                     gettingScore, killingDead, repeatDef,
                     saveColor, complexity,
                     playWithBot, pause, player)
                ff = open('temp.txt')
                rr = ff.read().split('\n')
                ff.close()
                f = open('log.txt')
                r = f.read().split('\n')
                r.pop()
                if len(r) >= 1:
                    player = int(r[len(r) - 1].split(' ')[2]) % 2 + 1
                    f.close()
                else:
                    player = 1
                drawWindow(dictScore, dictPlayer)
                pygame.time.delay(100)
    if keys[pygame.K_u] and not gameEnd and not pause:
        undo(gameMap, dictScore, stoneWhite, stoneBlack, endFlag, gameEnd,
             gettingScore, killingDead, repeatDef, saveColor, complexity,
             playWithBot, pause, player)
        f = open('log.txt')
        r = f.read().split('\n')
        r.pop()
        if len(r) >= 1:
            player = int(r[len(r) - 1].split(' ')[2]) % 2 + 1
            f.close()
        else:
            player = 1
        if playWithBot:
            undo(gameMap, dictScore, stoneWhite, stoneBlack, endFlag, gameEnd,
                 gettingScore, killingDead, repeatDef, saveColor, complexity,
                 playWithBot, pause, player)
            f = open('log.txt')
            r = f.read().split('\n')
            r.pop()
            if len(r) >= 1:
                player = int(r[len(r) - 1].split(' ')[2]) % 2 + 1
                f.close()
            else:
                player = 1
        drawWindow(dictScore, dictPlayer)
        pygame.time.delay(100)
    if keys[pygame.K_n]:
        f = open('log.txt', 'w')
        f.close()
        f = open('temp.txt', 'w')
        f.close()
        gameMap = emptyMap()
        dictScore[1] = 0
        dictScore[2] = 0
        stoneWhite = 0
        stoneBlack = 0
        player = 1
        endFlag = 0
        gameEnd = False
        gettingScore = False
        killingDead = False
        repeatDef = False
        pause = False
        playWithBot = False
        saveColor = False
        complexity = 0
        drawWindow(dictScore, dictPlayer)
    if keys[pygame.K_s] and not gameEnd and not pause:
        save('log.txt', 'save.txt')
        pygame.time.delay(100)
    if keys[pygame.K_l] and not gameEnd and not pause:
        f = open('save.txt')
        r = f.read().split('\n')
        rtoo = r.pop()
        f.close()
        if int(rtoo) == size:
            save('save.txt', 'log.txt')
            load(gameMap, dictScore, stoneWhite, stoneBlack,
                 endFlag, gameEnd, gettingScore, killingDead,
                 repeatDef, saveColor, complexity, playWithBot, pause, player)
            f = open('save.txt')
            r = f.read().split('\n')
            if len(r) == 1:
                player = 1
                drawWindow(dictScore, dictPlayer)
                continue
            r.pop()
            player = int(r[len(r) - 1].split(' ')[2]) % 2 + 1
            f.close()
            pygame.time.delay(100)
            drawWindow(dictScore, dictPlayer)
        else:
            end = pygame.font.Font(None, sizeFont)
            screen.blit(end.render('Save for another size',
                        False, (125, 125, 125)),
                        (175, 300))
            pygame.display.update()
            pygame.time.delay(100)
    if keys[pygame.K_b] and not gameEnd:
        playWithBot = True
        if not saveColor:
            pause = True
    if pause:
        if complexity == 0:
            if keys[pygame.K_1]:
                complexity = 1
                pygame.time.delay(300)
            if keys[pygame.K_2]:
                complexity = 2
                pygame.time.delay(300)
            drawWindow(dictScore, dictPlayer)
        else:
            if keys[pygame.K_1]:
                botColor = 2
                pause = False
                saveColor = True
            if keys[pygame.K_2]:
                botColor = 1
                pause = False
                saveColor = True
            drawWindow(dictScore, dictPlayer)
    if not gameEnd and not pause:
        if playWithBot and player == botColor:
            if complexity == 1:
                botStep = bot1(botColor, gameMap)
            elif complexity == 2:
                botStep = bot2(botColor, gameMap)
            gameMap[botStep[0]][botStep[1]] = botColor
            checkForKill(dictScore, gameMap, botStep[0], botStep[1])
            changeFlag = returnSuicideStep(gameMap, botStep[0], botStep[1])
            changePrevMapFlag = ruleCo(gameMap, prevMap,
                                       prevPrevMap, dictScore, prevDictScore)
            player = changePlayer(changeFlag,
                                  changePrevMapFlag, player,
                                  botStep[0], botStep[1])
            drawWindow(dictScore, dictPlayer)
            changePreviosMap(changePrevMapFlag, prevMap,
                             prevPrevMap, prevDictScore, dictScore)
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                for i in range(size):
                    for j in range(size):
                        posXGood = math.fabs(event.pos[0] -
                                             field[i][j][0]) <= sizeDraw
                        posYGood = math.fabs(event.pos[1] -
                                             field[i][j][1]) <= sizeDraw
                        if posXGood and posYGood and gameMap[i][j] == 0:
                            endFlag = 0
                            gameMap[i][j] = player
                            checkForKill(dictScore, gameMap, i, j)
                            changeFlag = returnSuicideStep(gameMap, i, j)
                            changePrevMapFlag = ruleCo(gameMap, prevMap,
                                                       prevPrevMap, dictScore,
                                                       prevDictScore)
                            player = changePlayer(changeFlag,
                                                  changePrevMapFlag,
                                                  player, i, j)
                            drawWindow(dictScore, dictPlayer)
                            changePreviosMap(changePrevMapFlag, prevMap,
                                             prevPrevMap, prevDictScore,
                                             dictScore)
        if keys[pygame.K_p]:
            player = player % 2 + 1
            endFlag += 1
            pygame.time.delay(300)
            drawWindow(dictScore, dictPlayer)
        if endFlag == 2:
            gameEnd = True
        if endFlag == 1 and playWithBot:
            gameEnd = True
    elif not pause:
        if not gettingScore:
            killingDead = True
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    for i in range(size):
                        for j in range(size):
                            posXGood = math.fabs(event.pos[0] -
                                                 field[i][j][0]) <= sizeDraw
                            posYGood = math.fabs(event.pos[1] -
                                                 field[i][j][1]) <= sizeDraw
                            if posXGood and posYGood and gameMap[i][j] != 0:
                                dictScore[gameMap[i][j] % 2 + 1] += 1
                                gameMap[i][j] = 0
        drawWindow(dictScore, dictPlayer)
        if keys[pygame.K_p] and not repeatDef:
            killingDead = False
            gettingScore = True
            pygame.time.delay(100)
            repeatDef = True
            for i in range(size):
                for j in range(size):
                    if gameMap[i][j] == 1:
                        stoneBlack += 1
                    elif gameMap[i][j] == 2:
                        stoneWhite += 1
            blackTerritory = getTerritory(gameMap, 1)
            whiteTerritory = getTerritory(gameMap, 2)
            scoreBlack = 'Black: ' + str(dictScore[1]) + ' + ' + str(
                stoneBlack) + ' + ' + str(blackTerritory)
            scoreWhite = 'White: ' + str(dictScore[2]) + ' + ' + str(
                stoneWhite) + ' + ' + str(whiteTerritory) + ' + ' + str(KOMI)
            dictFinalScore = {1: 0, 2: 0}
            dictFinalScore[1] = dictScore[1] + stoneBlack + blackTerritory
            dictFinalScore[2] = (dictScore[2] + stoneWhite +
                                 whiteTerritory + KOMI)
            if dictFinalScore[1] > dictFinalScore[2]:
                winner = 'Black win' + "(" + str(dictFinalScore[1] -
                                                 dictFinalScore[2]) + ")"
            else:
                winner = 'White win' + "(" + str(dictFinalScore[2] -
                                                 dictFinalScore[1]) + ")"
            drawWindow(dictScore, dictPlayer)
            if dictNames['first'] != '':
                if playWithBot:
                    writeEnd = ''
                    winOrLose = (dictFinalScore[botColor % 2 + 1] -
                                 dictFinalScore[botColor])
                    if winOrLose < 0:
                        writeEnd = ' Lose' + ' ' + str(winOrLose * (-1))
                    else:
                        writeEnd = ' Win' + ' ' + str(winOrLose)
                    f = open('board.txt', 'a')
                    f.write('Player vs bot' + '(' +
                            dictComplexity[complexity] + '): ' +
                            dictNames['first'] + '(' +
                            players[botColor % 2 + 1] + ')' + writeEnd + '\n')
                    f.close()
                else:
                    f = open('board.txt', 'a')
                    f.write('Player vs Player: ' + dictNames['first'] +
                            '(' + str(dictFinalScore[1]) + ')' +
                            ' ' + dictNames['second'] + '(' +
                            str(dictFinalScore[2]) + ')' + '\n')
                    f.close()
pygame.quit()

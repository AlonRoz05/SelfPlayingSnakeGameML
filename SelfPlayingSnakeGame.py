import numpy as np
import random
import pygame
import math
import time
import os


class cube(object):
    rows = 20
    w = 500

    def __init__(self, start, dirnx=1, dirny=0, color=(255, 100, 100)):
        self.pos = start
        self.dirnx = 1
        self.dirny = 0
        self.color = color

    def move(self, dirnx, dirny):
        self.dirnx = dirnx
        self.dirny = dirny
        self.pos = (self.pos[0] + self.dirnx, self.pos[1] + self.dirny)

    def draw(self, surface):
        dis = self.w // self.rows
        i = self.pos[0]
        j = self.pos[1]

        pygame.draw.rect(surface, self.color,
                         (i * dis + 1, j * dis + 1, dis - 2, dis - 2))


class snake(object):
    body = []
    turns = {}

    def __init__(self, color, pos):
        self.color = color
        self.head = cube(pos)
        self.body.append(self.head)
        self.score = 1
        self.snakeIsAlive = True
        self.dirnx = 0
        self.dirny = 1

    def move(self, isPlaying):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

            keys = pygame.key.get_pressed()
            if isPlaying:
                for key in keys:
                    if keys[pygame.K_LEFT]:
                        s.moveLeft()
                    elif keys[pygame.K_RIGHT]:
                        s.moveRight()
                    elif keys[pygame.K_DOWN]:
                        s.moveDown()
                    elif keys[pygame.K_UP]:
                        s.moveUp()

        for i, c in enumerate(self.body):
            p = c.pos[:]
            if p in self.turns:
                turn = self.turns[p]
                c.move(turn[0], turn[1])
                if i == len(self.body)-1:
                    self.turns.pop(p)

            else:
                if c.dirnx == -1 and c.pos[0] <= 0:
                    c.pos = (c.rows-1, c.pos[1])

                elif c.dirnx == 1 and c.pos[0] >= c.rows-1:
                    c.pos = (0, c.pos[1])

                elif c.dirny == 1 and c.pos[1] >= c.rows-1:
                    c.pos = (c.pos[0], 0)

                elif c.dirny == -1 and c.pos[1] <= 0:
                    c.pos = (c.pos[0], c.rows-1)

                else:
                    c.move(c.dirnx, c.dirny)

    def moveRight(self):
        self.dirnx = 1
        self.dirny = 0
        self.turns[self.head.pos[:]] = [self.dirnx, self.dirny]

    def moveLeft(self):
        self.dirnx = -1
        self.dirny = 0
        self.turns[self.head.pos[:]] = [self.dirnx, self.dirny]

    def moveDown(self):
        self.dirnx = 0
        self.dirny = 1
        self.turns[self.head.pos[:]] = [self.dirnx, self.dirny]

    def moveUp(self):
        self.dirnx = 0
        self.dirny = -1
        self.turns[self.head.pos[:]] = [self.dirnx, self.dirny]

    def reset(self, pos):
        self.head = cube(pos)
        self.body = []
        self.body.append(self.head)
        self.score = 1
        self.snakeIsAlive = True
        self.turns = {}
        self.dirnx = 0
        self.dirny = 1

    def addCube(self):
        tail = self.body[-1]
        dx, dy = tail.dirnx, tail.dirny

        if dx == 1 and dy == 0:
            self.body.append(cube((tail.pos[0]-1, tail.pos[1])))

        elif dx == -1 and dy == 0:
            self.body.append(cube((tail.pos[0]+1, tail.pos[1])))

        elif dx == 0 and dy == 1:
            self.body.append(cube((tail.pos[0], tail.pos[1]-1)))

        elif dx == 0 and dy == -1:
            self.body.append(cube((tail.pos[0], tail.pos[1]+1)))

        self.score = len(self.body)

        self.body[-1].dirnx = dx
        self.body[-1].dirny = dy

    def draw(self, surface):
        for i, c in enumerate(self.body):
            c.draw(surface)


def drawGrid(w, rows, surface):
    sizeBetween = w // rows

    x = 0
    y = 0
    for l in range(rows):
        x = x + sizeBetween
        y = y + sizeBetween

        pygame.draw.line(surface, (0, 0, 0), (x, 0), (x, w))
        pygame.draw.line(surface, (0, 0, 0), (0, y), (w, y))


def redrawWindow(surface):
    global rows, width, s, snack
    surface.fill((0, 0, 0))
    s.draw(surface)
    snack.draw(surface)
    drawGrid(width, rows, surface)
    pygame.display.update()


def randomSnack(item, rows):
    positions = item.body

    while True:
        x = random.randrange(rows)
        y = random.randrange(rows)
        if len(list(filter(lambda z: z.pos == (x, y), positions))) > 0:
            continue
        else:
            break

    return (x, y)


def selfPlayingAI(snakePos, snakeBody, isSnakeAlive, snackPos):
    global currentMove

    cubesBeforeTheX = False
    cubesInTheSameY = False

    cubesInTheSameX = False
    cubesBeforeTheY = False

    if snakePos[0] < snackPos[0] and currentMove != "Left":
        for cube in snakeBody:
            if snakePos[0] < cube.pos[0] and cube.pos[0] < snackPos[0]:
                cubesBeforeTheX = True

                if snakePos[1] == cube.pos[1] and snakePos[1] == snackPos[1]:
                    cubesInTheSameY = True
                else:
                    cubesInTheSameY = False
                    s.moveRight()
                    currentMove = "Right"

            else:
                cubesBeforeTheX = False
                s.moveRight()
                currentMove = "Right"

            if cubesBeforeTheX and cubesInTheSameY:
                print("A")

    elif snakePos[0] > snackPos[0] and currentMove != "Right":
        for cube in snakeBody:
            if snakePos[0] > cube.pos[0] and cube.pos[0] > snackPos[0]:
                cubesBeforeTheX = True

                if snakePos[1] == cube.pos[1] and snakePos[1] == snackPos[1]:
                    cubesInTheSameY = True
                else:
                    cubesInTheSameY = False
                    s.moveLeft()
                    currentMove = "Left"

            else:
                cubesBeforeTheX = False
                s.moveLeft()
                currentMove = "Left"

            if cubesBeforeTheX and cubesInTheSameY:
                print("B")

    elif snakePos[1] > snackPos[1] and currentMove != "Down":
        for cube in snakeBody:
            if snakePos[1] > cube.pos[1] and cube.pos[1] > snackPos[1]:
                cubesBeforeTheY = True

                if snakePos[0] == cube.pos[0] and snakePos[0] == snackPos[0]:
                    cubesInTheSameX = True
                else:
                    cubesInTheSameX = False
                    s.moveUp()
                    currentMove = "Up"

            else:
                cubesBeforeTheY = False
                s.moveUp()
                currentMove = "Up"

            if cubesInTheSameX and cubesBeforeTheY:
                print("C")

    elif snakePos[1] < snackPos[1] and currentMove != "Up":
        for cube in snakeBody:
            if snakePos[1] < cube.pos[1] and cube.pos[1] < snackPos[1]:
                cubesBeforeTheY = True

                if snakePos[0] == cube.pos[0] and snakePos[0] == snackPos[0]:
                    cubesInTheSameX = True
                else:
                    cubesBeforeTheX = False
                    s.moveDown()
                    currentMove = "Down"

            else:
                cubesBeforeTheY = False
                s.moveDown()
                currentMove = "Down"

            if cubesInTheSameX and cubesBeforeTheY:
                print("D")


def main():
    global width, rows, s, snack, currentMove

    currentMove = ""
    flag = True
    width = 500
    height = 500
    rows = 20
    win = pygame.display.set_mode((width, height))

    s = snake((255, 100, 100), (10, 10))
    snack = cube(randomSnack(s, rows), color=(100, 255, 100))

    clock = pygame.time.Clock()

    while flag:
        pygame.time.delay(60)
        clock.tick(8)

        if s.body[0].pos == snack.pos:
            snack = cube(randomSnack(s, rows), color=(100, 255, 100))
            s.addCube()

        for x in range(len(s.body)):
            if s.body[x].pos in list(map(lambda z: z.pos, s.body[x+1:])):
                print("Score:", s.score)
                s.reset((10, 10))
                break

        s.move(False)
        selfPlayingAI(s.body[0].pos, s.body, s.snakeIsAlive, snack.pos)
        redrawWindow(win)


if __name__ == "__main__":
    main()

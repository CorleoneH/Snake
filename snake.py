'''
1. 使用空格键SPACE暂停游戏
2. 使用回车键RETURN开启游戏，开启时游戏处于暂停状态
3. 根据分数区间，设置不同的游戏速度和单个食物的得分
4. 由于按键延迟，为了降低game over。随机生成的新食物，不会在边界
'''

import random
import sys
import time
import pygame
from pygame.locals import *
#from collections import deque
from settings import Settings

class Snack:
    def __init__(self):
        self.settings = Settings()
        pygame.init()
        pygame.display.set_caption("贪吃蛇")
        self.screen = pygame.display.set_mode((self.settings.width, self.settings.height))
        self.clock = pygame.time.Clock()
        self.totalScore = 0
        self.isPause = True

        # 初始化食物
        self.food = [(random.randint(self.settings.gridX[0], self.settings.gridX[1] - 1), random.randint(self.settings.gridY[0], self.settings.gridY[1] - 1))]
        
        # 初始化蛇，长度1，并且避免与实物重叠
        self.snakes = [((self.settings.gridX[1] - self.settings.gridX[0]) // 2, (self.settings.gridY[1] - self.settings.gridY[0]) // 2)]
        if self.snakes[0] == self.food[0]:
            self.snakes = [(self.snakes[0][0] + 1, self.snakes[0][1])]
        
        # 初始化蛇的方向，向下
        self.dir = (0, 1)

    def drawRects(self, color, rects):
        for rect in rects:
            pygame.draw.rect(self.screen, color, (rect[0] * self.settings.unit, rect[1] * self.settings.unit, self.settings.unit, self.settings.unit), 0)

    def fillBackgournd(self):
        self.screen.fill(self.settings.bg)
        # 绘制网格竖线
        for x in range (self.settings.gameAreaX[0], self.settings.gameAreaX[1], self.settings.unit):
            pygame.draw.line(self.screen, self.settings.BLACK, (x, self.settings.gameAreaY[0]), (x, self.settings.gameAreaY[1]), self.settings.lineWidth)
        # 绘制网格横线
        for y in range (self.settings.gameAreaY[0], self.settings.gameAreaY[1], self.settings.unit):
            pygame.draw.line(self.screen, self.settings.BLACK, (self.settings.gameAreaX[0], y), (self.settings.gameAreaX[1], y), self.settings.lineWidth)

        font = pygame.font.SysFont(self.settings.fontSimHei, 24, bold=True)
        self.screen.blit(font.render(f"Score: {self.totalScore}", True, self.settings.LIGHT, self.settings.BLACK), (self.settings.unit * 2, self.settings.unit // 2))
        self.screen.blit(font.render(f"Speed: {self.settings.speed}fps", True, self.settings.LIGHT, self.settings.BLACK), (self.settings.width - self.settings.unit * 8, self.settings.unit // 2))

        # 绘制初始化的食物
        self.drawRects(self.settings.RED, self.food)

        # 绘制初始化的蛇
        self.drawRects(self.settings.BLUE, self.snakes)
    
    def isGameOver(self):
        if (
            self.snakes[0][0] < self.settings.gridX[0] or
           self.snakes[0][0] >= self.settings.gridX[1] or
            self.snakes[0][1] < self.settings.gridY[0] or
            self.snakes[0][1] >= self.settings.gridY[1] or
            self.snakes[0] in self.snakes[1:]
        ):      
            return True

    def runGame(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                pygame.event.pump()
                keys = pygame.key.get_pressed()
                if keys[K_UP] and self.dir != (0, 1):
                    self.dir = (0, -1)
                if keys[K_DOWN] and self.dir != (0, -1):
                    self.dir = (0, 1)
                if keys[K_LEFT] and self.dir != (1, 0):
                    self.dir = (-1, 0)
                if keys[K_RIGHT] and self.dir != (-1, 0):
                    self.dir = (1, 0)
                if keys[K_SPACE]:
                    self.isPause = True
                if keys[K_RETURN]:
                    self.isPause = False

            if not self.isPause:
                # 移动蛇
                newHead = (self.snakes[0][0] + self.dir[0], self.snakes[0][1] + self.dir[1])
                self.snakes.insert(0, newHead)


                # 如果蛇头碰到了食物，则加分，且再随机生成一个食物
                if self.snakes[0] == self.food[0]:
                    self.totalScore += self.settings.score
                    self.food = [(random.randint(self.settings.gridX[0] + 1, self.settings.gridX[1] - 2), random.randint(self.settings.gridY[0] + 1, self.settings.gridY[1] - 2))]
                # 如果舌头没有碰到食物，且没有Game Over,则pop列表尾部，以获取蛇前进一步的效果
                else:
                    self.snakes.pop()
                
            if self.isGameOver():
                # 在屏幕中央显示Game Over!!!
                font = pygame.font.SysFont(self.settings.fontComicsansms, 72, bold=True)
                fontWidth, fontHeight = font.size("Game Over!!!")
                gameOverX = (self.settings.gameAreaX[1] - self.settings.gameAreaX[0] - fontWidth) // 2
                gameOverY = (self.settings.gameAreaY[1] - self.settings.gameAreaY[0] - fontHeight) // 2
                self.screen.blit(font.render("Game Over!!!", True, self.settings.RED, self.settings.BLACK), (gameOverX, gameOverY))
                pygame.display.flip()
                
                # 暂停1s后退出
                time.sleep(1)
                pygame.quit()
                sys.exit()
            self.fillBackgournd()
                
            pygame.display.flip()
            if self.totalScore >= 40 and self.totalScore < 100:
                self.settings.speed = 6
                self.settings.score = 15
            elif self.totalScore >= 100 and self.totalScore < 200:
                self.settings.speed = 8
                self.settings.score = 20
            elif self.totalScore >= 200 and self.totalScore < 400:
                self.settings.speed = 10
                self.settings.score = 25
            elif self.totalScore >= 400 and self.totalScore < 700:
                self.settings.speed = 12
                self.settings.score = 30
            elif self.totalScore >= 700 and self.totalScore < 1100:
                self.settings.speed = 15
                self.settings.score = 40
            elif self.totalScore >= 1100 and self.totalScore < 1500:
                self.settings.speed = 20
                self.settings.score = 50
            self.clock.tick(self.settings.speed)
 
def main():
    snack = Snack()
    snack.fillBackgournd()
    snack.runGame()

if __name__=='__main__':
    main()


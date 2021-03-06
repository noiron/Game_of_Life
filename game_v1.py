# -*- coding:utf8 -*-

''' -----------------------------------------------------------------------
Each cell has eight neighbours, except the ones reside on the borders.
Rules:
1. Any live cell with fewer than two live neighbours dies,
    as if caused by under-population
2. Any live cell with two or three live neighbours lives on 
    to the next generation.
3. Any live cell with more than three live neighbours dies,
    as if by overcrowding.
4. Any dead cell with exactly three live neighbours becomes
    a live cell, as if by reproduction.
--------------------------------------------------------------------------
'''

import sys, pygame
from pygame.locals import *
import random

class Game(object):
    def __init__(self):
        self.width = 1000
        self.height = 800
        self.offset_x = 30
        self.offset_y = 50
        self.gridSize = 9   # 格子的大小取为9，加上边界的一个像素，能保证格子是整数
        self.colorFill = (0, 0, 0)
        self.colorUnfill = (255, 255, 255)
        
        self.matrix =[]
        self.next_matrix = []
        
        self.row = (self.height - self.offset_x - self.offset_y) / \
            (self.gridSize + 1)
        self.col = (self.width - self.offset_x * 2) / \
            (self.gridSize + 1)
          
        self.initMatrix()
        pygame.init()
        self.screen = pygame.display.set_mode((self.width, self.height))
        self.screen.fill(self.colorUnfill, (0, 0, self.width, self.height))
        pygame.display.flip()
        self.drawGrid(self.offset_x, self.offset_y)
        
        self.clock = pygame.time.Clock()
    
    
    def initMatrix(self):
        col = (self.width - self.offset_x * 2) / (self.gridSize + 1)
        row = (self.height - self.offset_x - self.offset_y) /(self.gridSize + 1)
        for y in xrange(self.row):
            self.matrix.append([])
            self.next_matrix.append([])
            for x in xrange(self.col):
                self.matrix[y].append(False)
                self.next_matrix[y].append(False)
    
    
    def drawGrid(self, offset_x, offset_y):
        width = self.width - offset_x * 2
        height = self.height - offset_x - offset_y
        sz = self.gridSize + 1
        
        grey = (200, 200, 200)
        dark = (50, 50, 50)
        
        # 先画出内部的细线，如果不能整除，会有几个像素的微调
        # 画出垂直线
        for x in xrange(offset_x , offset_x + width + sz, sz):
            pygame.draw.line(self.screen, grey, (x, offset_y),
                (x, offset_y + height), 1)
        # 画出水平线
        for y in xrange(offset_y, offset_y + height + sz, sz):
            pygame.draw.line(self.screen, grey, (offset_x, y),
                (offset_x + width , y), 1) 
                
        # 画出四周较粗的边界线，上，下，左，右
        # pygame.draw.line(self.screen, dark, (offset_x - 2, offset_y - 2),
            # (offset_x + width , offset_y - 2), 3)
        # pygame.draw.line(self.screen, dark, (offset_x-2, offset_y + height+2),
            # (offset_x + width, offset_y + height+2), 3+2)
        # pygame.draw.line(self.screen, dark, (offset_x-2, offset_y-2),
            # (offset_x-2 , offset_y + height+2), 3)
        # pygame.draw.line(self.screen, dark, (offset_x + width, offset_y-2),
            # (offset_x + width, offset_y + height+2), 3)
        
        
        pygame.display.flip()
        
        
    def handle_keyboard(self, event):
        if event.key == pygame.K_q or event.key == pygame.K_ESCAPE:
            print u"游戏结束，已退出。"
            pygame.quit()
        elif event.key == pygame.K_SPACE:
            print u"已按下空格键，游戏启动。"
            # print self.clock.tick()
            self.conway()
        elif event.key == pygame.K_r:
            print u"屏幕已清空。"
            self.reset_grid()
        # 设置随机概率
        elif event.key == pygame.K_d:
            self.random_state(0)
            self.print_state()
        # 按相应数字键，选择给定概率值
        elif event.key >= pygame.K_1 and event.key <= K_9:
            self.random_state(int(event.key - K_1 + 1))
            self.print_state()
        
            
                       
    def run(self):
        sz = self.gridSize + 1
        mouse_down = False
        mouse_up = True
        last_rect = pygame.Rect(0, 0, 0, 0) # 这个对象用于判断鼠标是否移出了当前细胞的范围
        
        # 循环检测输入的事件，进行相应的处理
        while True:
            self.clock.tick(30)
            for event in pygame.event.get():
                # 退出程序
                if event.type == pygame.QUIT:
                    pygame.quit()
                # 键盘有键按下，则转去子程序handle_keyboard执行
                elif event.type == pygame.KEYDOWN:
                    self.handle_keyboard(event)
                elif event.type == pygame.MOUSEBUTTONUP:
                    mouse_down = False
                    mouse_up = True     
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_down = True
                    
            if mouse_down == True:
                ## just for fun here
                # print "test"
                # pygame.draw.line(self.screen, 
                    # (random.random()*256, random.random()*256, random.random()*256), 
                    # (self.width/2, self.height/2), 
                    # (random.random()*1024,random.random()*768),1)
                # pygame.display.flip() 
                
                x, y = pygame.mouse.get_pos()
                
                if (x > self.width - self.offset_x 
                    or y > self.height - self.offset_x
                    or x < self.offset_x or y < self.offset_y):
                    continue
				# 判断鼠标是否移出当前细胞
                if not mouse_up and last_rect.collidepoint(x, y):
                    continue
                mouse_up = False
                
                # 判断目前鼠标所在位置在第几格内
                # 这里x要减2是因为鼠标点在格子右侧部分时，会错误地标记到右边的格子上。
                # Bug，未修复。
                # 将细胞大小从12修改为9后，Bug自动修复了！？
                idx_x = (x - self.offset_x) / sz    
                idx_y = (y - self.offset_y) / sz
                # 所在格子的左上角的坐标
                off_x = x / sz * sz
                off_y = y / sz * sz
               
                rect = (off_x + 1, off_y + 1, self.gridSize, self.gridSize)
                last_rect = pygame.Rect(off_x, off_y, sz, sz)
                
                if self.matrix[idx_y][idx_x] == True:
                    pygame.draw.rect(self.screen, self.colorUnfill, rect)
                    self.matrix[idx_y][idx_x] = False     
                else:
                    pygame.draw.rect(self.screen, self.colorFill, rect)
                    self.matrix[idx_y][idx_x] = True    
                pygame.display.flip()
                
                
    # 按下空格键后，游戏开始运行，程序转到此处运行            
    def conway(self):
        running = True
        pause = False
        
        while running:
            self.clock.tick(10)
            x, y = pygame.mouse.get_pos()
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        pygame.quit()
                    elif event.key == pygame.K_SPACE:
                        pause = not pause
                    elif event.key == pygame.K_r:
                        running = False
                        self.reset_grid()
            
            if pause == True:
                continue
                
            self.next_gen()
            self.print_state()
    
    
    def reset_grid(self):
        for y in xrange(self.row):
            for x in xrange(self.col):
                self.matrix[y][x] = False
                self.next_matrix[y][x] = False
        self.print_state()
    
    
    def print_state(self):
        for r in xrange(self.row):
            for c in xrange(self.col):
                rect = (c * (self.gridSize + 1) + self.offset_x + 1,
                    r * (self.gridSize + 1) + self.offset_y + 1,
                    self.gridSize, self.gridSize)
                if self.matrix[r][c] == True:
                    pygame.draw.rect(self.screen, self.colorFill, rect)
                elif self.matrix[r][c] == False:
                    pygame.draw.rect(self.screen, self.colorUnfill, rect)
        pygame.display.flip()
        
                
    def next_gen(self):
        for row in xrange(self.row):
            for col in xrange(self.col):
                neighbours = self.getNeighbours(row, col)
                if self.matrix[row][col] == True: 
                    if  neighbours < 2 or neighbours >3:
                        self.next_matrix[row][col] = False
                    else:
                        self.next_matrix[row][col] = True
                else:
                    if  neighbours == 3:
                        self.next_matrix[row][col] = True 
                    else:
                        self.next_matrix[row][col] = False
                
        for row in xrange(self.row):
            for col in xrange(self.col):
                self.matrix[row][col] = self.next_matrix[row][col]
                self.next_matrix[row][col] = False
        
        
    def getNeighbours(self, r, c):
        dr = [-1, -1, -1, 0, 1, 1, 1, 0]
        dc = [-1, 0, 1, 1, 1, 0, -1, -1]
        neighbours = 0
        
        for i in xrange(8):
            row = r + dr[i]
            col = c + dc[i]
            if row >= 0 and col >= 0 and row < self.row and col < self.col:
                if self.matrix[row][col] == True:
                    neighbours += 1
                    
        return neighbours            
        
    
    def random_state(self, mode):
        probablity = [0.05, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9]
        idx = 0
        if mode == 0:
            idx = int(random.random() * 10)
        elif mode >= 0 and mode <= 9:
            idx = mode
        
        for r in xrange(self.row):
            for c in xrange(self.col):
                if probablity[idx] > random.random():
                    self.matrix[r][c] = True
                else:
                    self.matrix[r][c] = False

    
def main():
    game = Game()
    game.run()
    

if __name__ == "__main__":
    main()





    
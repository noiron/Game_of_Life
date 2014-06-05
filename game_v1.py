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
        # pygame.display.init()
        self.screen = pygame.display.set_mode((self.width, self.height))
        self.screen.fill(self.colorUnfill, (0, 0, self.width, self.height))
        # self.screen.fill((100, 100, 255))
        pygame.display.flip()
        # pygame.time.wait(2000)
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
        # pygame.time.wait(10000)
        
        
    def handle_keyboard(self, event):
        if event.key == pygame.K_q or event.key == pygame.K_ESCAPE:
            pygame.quit()
        elif event.key == pygame.K_SPACE:
            print u"已按下空格键，游戏启动。"
            print self.clock.tick()
            self.conway()
            
                
        
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
                ## just for fun
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
                
                
    def conway(self):
        running = True
        
                
                
                
                
                
                    
                    
                    
        
        
        

        
def main():
    game = Game()
    game.run()
    

if __name__ == "__main__":
    main()





    
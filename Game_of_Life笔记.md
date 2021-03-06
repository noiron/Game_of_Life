## 实现目标：
Conway 生命游戏用Pygame实现


## 界面：
1280*720分辨率的画面


## 调用的函数：
1. 
    self.initMatrix(self)
    将存储数据的矩阵初始化,设置两个矩阵matrix、next_matrix的维数，以及细胞的初始状态

2. 
    self.drawGrid(self.offset_x, self.offset_y)

    ## 定义的变量：

    self.width     # 屏幕的宽度
    self.height    # 屏幕的高度
    self.offset_x  # 水平方向上，内部显示区域与边界的距离
    self.offset_y  # 垂直方向上，内部显示区域与边界的距离
    self.gridSize  # 每个细胞的大小
    self.colorFill    # 细胞存活时，填充的颜色
    self.colorUnfill  # 细胞死亡时，填充的颜色
    
    self.matrix       # 保存当前细胞的状态
    self.next_matrix  # 保存下一个时刻的细胞状态
    self.row       # 显示的行数，即矩阵的行
    self.col       # 显示的列数，即矩阵的列
    
    grey = (200, 200, 200)    # 灰色，用于画细线
    dark = (120, 120, 120)    # 深色，用于画粗线


## 调用的Python或Pygame中的函数：

1.
    array.append(x)
    Append a new item with value x to the end of the array.
    在数组的末尾添加一个值为x的元素

2. 
    pygame.draw.line()
    draw a straight line segment
    line(Surface, color, start_pos, end_pos, width=1) -> Rect

    Draw a straight line segment on a Surface. There are no endcaps, the ends are squared off for thick lines.
    在Surface上画出一段直线


3. 
    pygame.display.flip()
    Update the full display Surface to the screen
    flip() -> None
    将更新后的Surface对象全部显示在屏幕上

4. 
    class pygame.Rect
    pygame object for storing rectangular coordinates
    Rect(left, top, width, height) -> Rect
    Rect((left, top), (width, height)) -> Rect
    Rect(object) -> Rect
    pygame.Rect类，用于存储矩形的坐标，有三种调用方式   
  
   
5. 
    time.clock()
    返回一个浮点数，代表当前的处理器时间（秒）


6.  
    class pygame.time.Clock
    create an object to help track time
    Clock() -> Clock
    pygame.time.Clock.tick  —   update the clock
    pygame.time.Clock 创建一个对象用于记录时间

    tick()
    update the clock
    tick(framerate=0) -> milliseconds
    This method should be called once per frame. It will compute how many milliseconds have passed since the previous call.
    tick（）每一帧都需要调用一次，用于计算从上一次调用到现在已经过去了多少毫秒


7. 
    pygame.event.get()
    get events from the queue
    get() -> Eventlist
    从队列中取出一个事件


8. 
    pygame.init()
    initialize all imported pygame modules
    init() -> (numpass, numfail)
    将所有import的pygame模组均初始化。与之对应的是：
    pygame.quit()
    uninitialize all pygame modules
    quit() -> None
    Uninitialize all pygame modules that have previously been initialized. 
    
    
9.  
    pygame.display.set_mode()
    Initialize a window or screen for display
    set_mode(resolution=(0,0), flags=0, depth=0) -> Surface
    初始化一个窗口或screen用于显示，该函数会创建一个Surface对象。
    This function will create a display Surface. 
 
 
10. 
    pygame.Surface.fill()   
    fill Surface with a solid color
    fill(color, rect=None, special_flags=0) -> Rect
    将Surface对象上色
    

11. 
    pygame.mouse.get_pos()


12. 
    pygame.draw.rect()


13. 
    pygame.Rect.collidepoint()
    test if a point is inside a rectangle
    collidepoint(x, y) -> bool
    collidepoint((x,y)) -> bool
    Returns true if the given point is inside the rectangle. 
    A point along the right or bottom edge is not considered to be inside the rectangle.
   
   


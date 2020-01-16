import pygame as pg
import time, random

black = (0,0,0)
white = (255,255,255)
# color -------------- #
red = (255,0,0)
green = (0,255,0)
blue = (0,0,255)
yellow = (255,255,0)
pink = (255,0,255)
cyan = (0,255,255)
orange = (255,165,0)
brown = (165,42,42)
magenta = (139,0,139)
silver = (192,192,192)
silvera = (255,255,192)

pg.display.set_caption("tetris")
# tetris blocks -----------------#
BLOCKS = {
    "_Z":{"color":red,
    "shape":[
        [None,True,True],
        [True,True,None]]},
    "Z":{"color":green,
        "shape":[
        [True,True,None],
        [None,True,True]
    ]},
    "rectangle":{"color":blue,
        "shape":[
        [True,True,True,True,True]
    ]},
    "cube":{"color":yellow,
        "shape":[
            [True,True],
            [True,True]
        ]},
    "L":{"color":pink,
        "shape":[
            [None,None,True],
            [True,True,True]
        ]},
    "_R":{"color":cyan,
        "shape":[
            [True,True],
            [None,True],
            [None,True]
        ]},
    "I":{"color":orange,
        "shape":[
            [True,None],
            [True,True],
            [True,None]
        ]},
    "_Z_":{"color":brown,
        "shape":[
            [None,True,True],
            [None,True,None],
            [True,True,None]
        ]},
    "i":{"color":magenta,
        "shape":[
            [True],
            [True]
        ]}
    }
# window --------------------- #
WIN_WIDTH, WIN_HEIGHT = 600,900
win = pg.display.set_mode((WIN_WIDTH,WIN_HEIGHT))
# font ---------------- #
pg.font.init()
FONT = pg.font.SysFont('comicsans',60)

clock = pg.time.Clock()

Grid= [
    [(black) for _ in range(WIN_WIDTH//50)] for _ in range(WIN_HEIGHT//50)
]

class Figure():
    def __init__(self,x,y,shape):
        self.color = BLOCKS[shape]["color"]
        self.coords = [] # [y, x], [col,row] #
        self.shape = BLOCKS[shape]["shape"]
        self.get_coords(x,y)

    def get_coords(self,x,y): # get coords of every "existing" cube in figure #
        self.copy = self.coords.copy()
        self.coords = []
        for i,row in enumerate(self.shape):
            arow = []
            for j,block in enumerate(row):
                if block:
                    arow.append([i+y,j+x])
                else:
                    arow.append([None])
            self.coords.append(arow)

    def fall(self): # move the block vertically down #
        for i, row in enumerate(self.coords):
            for j in range(len(row)):
                if row[j][0] != None:
                    self.coords[i][j][0] += 1

    def move(self,dire): # move the block horizontally (left or right) #
        fill = 1 if dire == "right" else -1
        for i,row in enumerate(self.coords):
            for j in range(len(row)):
                if row[j][0] != None:
                    self.coords[i][j][1] += fill


    def draw(self,win):
        for row in self.coords:
            for j,cube in enumerate(row):
                if cube[0] != None: # draw every part of the block #
                    pg.draw.rect(win,self.color,(cube[1]*50,cube[0]*50,50,50))
                    pg.draw.rect(win,white,(cube[1]*50,cube[0]*50,50,50),2)

    def update_grid(self): # if block finished moving, update the grid of its coordinates #
        for i, row in enumerate(self.coords):
            for j, cube in enumerate(row):
                if cube[0] != None:
                    Grid[cube[0]][cube[1]] = self.color

    def get_pos(self): 
        '''   
        :param: coords
        :returns: coords of the left up corner of tile '''
        for i in range(len(self.coords[0])):
            if self.coords[0][i][0] != None:
                return [self.coords[0][i][0],self.coords[0][i][1]-i]

    def rotate(self,dire): # rotate the block #
        n_shape = []
        pos = self.get_pos()
        for i in reversed(range(len(self.shape[0]))):
            n_row = []
            for row in self.shape:
                n_row.append(row[i])
            if dire == "right":
                n_row.reverse()
            n_shape.append(n_row)
        if dire == "right":
            n_shape.reverse()
        self.shapeCopy = self.shape.copy()
        self.shape = n_shape
        self.get_coords(pos[1],pos[0])
        self.check()
    
    def check(self,mode=0): # check if the rotated block is valid, and if its not, restore its prevorious shape #
        for i,row in enumerate(self.coords):
            for j,cube in enumerate(row):
                if cube[0] != None: # V check if the shape is outside the grid or shape is in another block # 
                    if 0 > cube[0] > len(Grid)-1 or 0 > cube[1] > len(Grid[0])-1 or Grid[cube[0]][cube[1]] != black:
                        if mode == 0:
                            self.coords = self.copy
                            self.shape = self.shapeCopy
                        return True
        return False

def draw_grid(): # draw the game grid #
    win.fill(black)
    for i,row in enumerate(Grid): # 18 rows total #
        for j, cube in enumerate(Grid[i]): # 12 columns total #
            pg.draw.rect(win,cube,(j*50,i*50,50,50))
            if i == 17:
                pg.draw.line(win,white,(j*50,0),(j*50,WIN_HEIGHT),1)
        pg.draw.line(win,white,(0,i*50),(WIN_WIDTH,i*50),1)
        
def check_move(coords): # check whether the block can move vertically down #
    move = True
    for i, row in enumerate(coords):
        if not move:
            break
        for j, cube in enumerate(row):
            if cube[0] != None: #cube[1] - x; cube[0] - y
                if cube[0] < (len(Grid)-1):
                    next_on_y = Grid[cube[0]+1][cube[1]]
                else:
                    next_on_y = white
                if next_on_y == black: #fall
                    move = True
                else:
                    move = False
                    break
        if not move:
            break
    return move

def run():
    av = [i for i in BLOCKS.keys()]
    shapes = []
    for i in range(200): # get the 200 random blocks #
        #r = random.randint(0,len(av)-1)
        key = random.choice(av)
        shape = BLOCKS[key]["shape"]
        width = len(shape[0])
        shapes.append(Figure(6-width//2,0,key))
    draw_grid()
    pg.display.update()
    n = 0
    abreak = False
    notdelay = False
    delay = False
    while True:
        shape = shapes[n]
        moved = False
        for i in range(len(Grid[0])):
            if Grid[0][i] != black:
                abreak = True
                break
        if shape.check(mode=1): # if the shape doesnt have enought space to spawn, break #
            abreak = True
        if abreak:
            s = FONT.render(f"You Lost! Ur score was: {n}",1,silvera) #(220,20,60)
            win.blit(s,(WIN_WIDTH//2-(s.get_width()//2),30))
            pg.display.flip()
            time.sleep(5)
            break
        
        move = check_move(shape.coords)

        for event in pg.event.get():
            if event.type == pg.QUIT:
                time.sleep(2)
                pg.quit()
                break
          
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE: # if player clicked esc, quit #
                    time.sleep(2)
                    break
                    pg.quit()
                if event.key == pg.K_DOWN: # if player holds the down arrow, speed up the time #
                    notdelay = True
                elif event.key == pg.K_UP: # if player holds the up arrow, slow down the time #
                    delay = True

                if event.key == pg.K_RCTRL and move: # rotate #
                    shape.rotate("left")
                    move = check_move(shape.coords)
                elif event.key == pg.K_KP0 and move:
                    shape.rotate("right")
                    move = check_move(shape.coords)

                left = True
                right = True
                if event.key == pg.K_LEFT and not moved:
                    for i, row in enumerate(shape.coords): # check if the block can move to left #
                        if not left or not move:
                            break
                        for j, cube in enumerate(row):
                            if cube[0] != None: #cube[1] - x; cube[0] - y
                                if cube[1] >= 1:
                                    prev_on_x = Grid[cube[0]][cube[1]-1]
                                else:
                                    prev_on_x = white
                                if prev_on_x == black:
                                    left = True
                                else:
                                    left = False
                                    break
                        if not left or not move: # if it cant move left or down, break #
                            break
                    if left and move and not moved: # if it can move, and in this frame it didnt moved horizontally, move it to the left #
                        shape.move("left")
                        left = False
                        moved = True

                if event.key == pg.K_RIGHT and not moved:
                    for i, row in enumerate(shape.coords): # check if the block can move to the right #
                        if not right or not move:
                            break
                        for j, cube in enumerate(row):
                            if cube[0] != None: #cube[1] - x; cube[0] - y
                                if cube[1] < (len(Grid[0]))-1:
                                    next_on_x = Grid[cube[0]][cube[1]+1]
                                else:
                                    next_on_x = white
                                if next_on_x == black:
                                    right = True
                                else:
                                    right = False
                                    break
                        if not right or not move: # if it cant move left or down, break #
                            break
                    if right and move and not moved: # if it can move, and in this frame it didnt moved horizontally, move it to the right#
                        shape.move("right")
                        right = False
                        moved = True
            
            if event.type == pg.KEYUP: # if player stops holding the up arrow, stop slow down the time #
                if event.key == pg.K_UP:
                    delay = False
                elif event.key == pg.K_DOWN: # if player stops holding the down arrow, stop speed up the time #
                    notdelay = False

        if moved: # if the block moved horizontally , check again if it can move vertically down #
            move = check_move(shape.coords)

        draw_grid()

        if move:
            shape.fall()
            shape.draw(win)

        else: #save shape on grid, and switch shape to next one
            shape.update_grid()
            draw_grid()
            n += 1
        
        if not notdelay:
            clock.tick(4)
        else:
            clock.tick(20)

        if delay:
            clock.tick(2) 

        pg.display.update()

if __name__ == "__main__":
    run()

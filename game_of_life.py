from graphics import *

import random

    

BLOCK_SIZE = 40
BLOCK_OUTLINE_WIDTH = 2
BOARD_WIDTH = 25
BOARD_HEIGHT = 25



neighbor_test_blocklist = [(0,0), (1,1)]
toad_blocklist = [(4,4), (3,5), (3,6), (5,7), (6,5), (6,6)]
beacon_blocklist = [(2,3), (2,4), (3,3), (3,4), (4,5), (4,6), (5,5), (5,6)]
glider_blocklist = [(1,2), (2,3), (3,1), (3,2), (3,3)]
pulsar_blocklist = [(2,4), (2,5), (2,6), (4,2), (4,7), (5,2), (5,7),
                    (6,2), (6,7), (7,4), (7,5), (7,6), ]
diehard_blocklist = [(5,7), (6,7), (6,8), (10,8), (11,8), (12,8), (11,6)]


class Block(Rectangle):
    ''' Block class:
        Implement a block for a tetris piece
        Attributes: x - type: int
                    y - type: int
        specify the position on the board
        in terms of the square grid
    '''
    
    def __init__(self, pos, color):
        '''
        pos: a Point object specifing the (x, y) square of the Block (NOT in pixels!)
        color: a string specifing the color of the block (eg 'blue' or 'purple')
        '''
        self.x = pos.x
        self.y = pos.y

        p1 = Point(pos.x*BLOCK_SIZE,
                   pos.y*BLOCK_SIZE)
        p2 = Point(p1.x + BLOCK_SIZE, p1.y + BLOCK_SIZE)

        Rectangle.__init__(self, p1, p2)
        self.setWidth(BLOCK_OUTLINE_WIDTH)
        self.setFill(color)
        self.status = 'dead'
        self.new_status = 'None'

    def get_coords(self):
        return (self.x, self.y)

    def set_live(self, canvas):
        '''
        Sets the block status to 'live' and draws it on the grid.
        Be sure to do this on the canvas!
        '''
        if self.status=='dead':
          self.status = 'live'
          self.draw(canvas)

    def set_dead(self):
        '''
        Sets the block status to 'dead' and undraws it from the grid.
        '''
        if self.status=='live':
          self.status = 'dead'
          self.undraw()

    def is_live(self):
        '''
        Returns True if the block is currently 'live'. Returns False otherwise.
        '''
        if self.status == 'live':
            return True
        return False

    def reset_status(self, canvas):
        '''
        Sets the new_status to be the current status
        '''
        if self.new_status=='dead':
            self.set_dead()
        elif self.new_status=='live':
            self.set_live(canvas)
            

class Board(object):
    ''' Board class: it represents the Game of Life board
        Attributes: width - type:int - width of the board in squares
                    height - type:int - height of the board in squares
                    canvas - type:CanvasFrame - where the blocks will be drawn
                    block_list - type:Dictionary - stores the blocks for a given position
    '''

    def __init__(self, win, width, height):
        self.width = width
        self.height = height
        self.win = win
        # self.delay is the number of ms between each simulation.
        self.delay = 1000
        # create a canvas to draw the blocks on
        self.canvas = CanvasFrame(win, self.width * BLOCK_SIZE,
                                       self.height * BLOCK_SIZE)
        self.canvas.setBackground('white')

        # initialize grid lines
        for x in range(1,self.width):
            self.draw_gridline(Point(x, 0), Point(x, self.height))

        for y in range(1,self.height):
            self.draw_gridline(Point(0, y), Point(self.width, y))

        # For each square on the board, a block is initialized
        # and stored in a dictionary (self.block_list) that has 
        # key:value pairs of (x,y):Block
        self.block_list = {}
        y = 0
        while y < BOARD_HEIGHT:  
            for x in range(BOARD_WIDTH):  
                self.block_list[(x,y)] = Block(Point(x,y),'blue')
            y += 1            



    def draw_gridline(self, startp, endp):

        ''' Parameters: startp - a Point of where to start the gridline

                        endp - a Point of where to end the gridline

            Draws two straight 1 pixel lines next to each other, to create

            a nice looking grid on the canvas.

        '''

        line = Line(Point(startp.x*BLOCK_SIZE, startp.y*BLOCK_SIZE), \

                    Point(endp.x*BLOCK_SIZE, endp.y*BLOCK_SIZE))

        line.draw(self.canvas)

        

        line = Line(Point(startp.x*BLOCK_SIZE-1, startp.y*BLOCK_SIZE-1), \

                    Point(endp.x*BLOCK_SIZE-1, endp.y*BLOCK_SIZE-1))

        line.draw(self.canvas)



    def random_seed(self, percentage):

        ''' Parameters: percentage - a number between 0 and 1 representing the

                                     percentage of the board to be filled with

                                     blocks

            This method activates the specified percentage of blocks randomly.

        '''

        for block in self.block_list.values():

            if random.random() < percentage:

                block.set_live(self.canvas)



    def seed(self, block_coords):

        '''

        Seeds the board with a certain configuration.

        Takes in a list of (x, y) tuples representing block coordinates,

        and activates the blocks corresponding to those coordinates.

        '''

        

        for coord in block_coords:

            if coord in self.block_list.keys():

                self.block_list[coord].set_live(self.canvas)



    def get_block_neighbors(self, block):

        '''

        Given a Block object, returns a list of neighboring blocks.

        Should not return itself in the list.

        '''
        

        neighbors = []

        coords = block.get_coords()

        y = -1

        while y < 2:            

            for x in range(-1,2):

                if 0 <= (coords[0] + x) <= BOARD_WIDTH - 1 and 0 <= (coords[1] + y) <= BOARD_HEIGHT - 1:

                    neighbors.append(self.block_list[coords[0] + x, coords[1] + y])

            y += 1

        neighbors.remove(self.block_list[coords[0], coords[1]])           

        return neighbors

       

    def simulate(self):

        '''
        Executes one turn of Conways Game of Life 
        '''

        for block in self.block_list.values():
            neighbors = self.get_block_neighbors(block)
            alive = 0
            for neighbor in neighbors:
                if neighbor.is_live() == True:
                    alive += 1
            if alive < 2:
                block.new_status = 'dead'
            elif alive == 2 and block.status == 'live':
                block.new_status = 'live'
            elif alive == 3:
                block.new_status = 'live'
            elif alive > 3:
                block.new_status = 'dead'
                
        for block in self.block_list.values():
            block.reset_status(self.canvas)


    def animate(self):
        '''
        Animates the Game of Life, calling "simulate"
        once every second
        '''
        self.simulate()
        self.win.after(self.delay, self.animate)

################################################################

# RUNNING THE SIMULATION

################################################################

if __name__ == '__main__':    
    # Initalize board
    win = Window("Conway's Game of Life")
    board = Board(win, BOARD_WIDTH, BOARD_HEIGHT)
    board.seed(diehard_blocklist)
    win.after(2000, board.animate)
    win.mainloop()

                


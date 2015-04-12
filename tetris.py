from graphics import *
import random

############################################################
# BLOCK CLASS
############################################################


class Block(Rectangle):
    ''' Block class:
        Implement a block for a tetris piece
        Attributes: x - type: int
                    y - type: int
        specify the position on the tetris board
        in terms of the square grid
    '''

    BLOCK_SIZE = 30
    OUTLINE_WIDTH = 3

    def __init__(self, pos, color):
        self.x = pos.x
        self.y = pos.y

        p1 = Point(pos.x * Block.BLOCK_SIZE + Block.OUTLINE_WIDTH,
                   pos.y * Block.BLOCK_SIZE + Block.OUTLINE_WIDTH)
        p2 = Point(p1.x + Block.BLOCK_SIZE, p1.y + Block.BLOCK_SIZE)

        Rectangle.__init__(self, p1, p2)
        self.setWidth(Block.OUTLINE_WIDTH)
        self.setFill(color)

    def can_move(self, board, dx, dy):
        ''' Parameters: dx - type: int
                        dy - type: int

            Return value: type: bool

            checks if the block can move dx squares in the x direction
            and dy squares in the y direction
            Returns True if it can, and False otherwise
            HINT: use the can_move method on the Board object
        '''

        if Board.can_move(board, dx + self.x, dy + self.y):
            return True
        else:
            return False

    def move(self, dx, dy):
        ''' Parameters: dx - type: int
                        dy - type: int

            moves the block dx squares in the x direction
            and dy squares in the y direction
        '''

        self.x += dx
        self.y += dy

        Rectangle.move(self, dx * Block.BLOCK_SIZE, dy * Block.BLOCK_SIZE)

############################################################
# SHAPE CLASS
############################################################


class Shape():
    ''' Shape class:
        Base class for all the tetris shapes
        Attributes: blocks - type: list - the list of blocks making up the shape
                    rotation_dir - type: int - the current rotation direction
                    of the shape shift_rotation_dir - type: Boolean - whether
                    or not the shape rotates
    '''

    def __init__(self, coords, color):
        self.blocks = []
        self.rotation_dir = 1
        ### A boolean to indicate if a shape shifts rotation direction or not.
        ### Defaults to false since only 3 shapes shift rotation directions
        ###(I, S and Z)
        self.shift_rotation_dir = False

        for pos in coords:
            self.blocks.append(Block(pos, color))

    def get_blocks(self):
        '''returns the list of blocks
        '''

        return self.blocks

    def draw(self, win):
        ''' Parameter: win - type: CanvasFrame

            Draws the shape:
            i.e. draws each block
        '''
        for block in self.blocks:
            block.draw(win)

    def undraw(self):
        ''' Parameter: win - type: CanvasFrame

            unDraws the shape:
            i.e. draws each block
        '''
        for block in self.blocks:
            block.undraw()

    def move(self, dx, dy):
        ''' Parameters: dx - type: int
                        dy - type: int

            moves the shape dx squares in the x direction
            and dy squares in the y direction, i.e.
            moves each of the blocks
        '''
        for block in self.blocks:
            block.move(dx, dy)

    def can_move(self, board, dx, dy):
        ''' Parameters: dx - type: int
                        dy - type: int

            Return value: type: bool

            checks if the shape can move dx squares in the x direction
            and dy squares in the y direction, i.e.
            check if each of the blocks can move
            Returns True if all of them can, and False otherwise

        '''

        for block in self.blocks:
            if not Block.can_move(block, board, dx, dy):
                return False

        return True

    def get_rotation_dir(self):
        ''' Return value: type: int

            returns the current rotation direction
        '''
        return self.rotation_dir

    def can_rotate(self, board):
        ''' Parameters: board - type: Board object
            Return value: type : bool

            Checks if the shape can be rotated.

            1. Get the rotation direction using the get_rotation_dir method
            2. Compute the position of each block after rotation and check if
            the new position is valid
            3. If any of the blocks cannot be moved to their new position,
            return False

            otherwise all is good, return True
        '''

        rot = self.get_rotation_dir()
        center = self.blocks[1]
        for block in self.blocks:
            x = center.x - rot * center.y + rot * block.y
            y = center.y + rot * center.x - rot * block.x
            if not Block.can_move(block, board, x - block.x, y - block.y):
                return False
        return True

    def rotate(self, board):
        ''' Parameters: board - type: Board object

            rotates the shape:
            1. Get the rotation direction using the get_rotation_dir method
            2. Compute the position of each block after rotation
            3. Move the block to the new position

        '''

        rot = self.get_rotation_dir()
        center = self.blocks[1]
        for block in self.blocks:
            x = center.x - rot * center.y + rot * block.y
            y = center.y + rot * center.x - rot * block.x
            block.move(x - block.x, y - block.y)

        ### This ensures that pieces which switch rotations definitely
        ### remain within their accepted rotation positions.
        if self.shift_rotation_dir:
            self.rotation_dir *= -1

############################################################
# ALL SHAPE CLASSES
############################################################


class I_shape(Shape):
    def __init__(self, center):
        coords = [Point(center.x - 2, center.y),
                  Point(center.x - 1, center.y),
                  Point(center.x, center.y),
                  Point(center.x + 1, center.y)]
        Shape.__init__(self, coords, 'blue')
        self.shift_rotation_dir = True
        self.center_block = self.blocks[2]


class J_shape(Shape):
    def __init__(self, center):
        coords = [Point(center.x - 1, center.y),
                  Point(center.x, center.y),
                  Point(center.x + 1, center.y),
                  Point(center.x + 1, center.y + 1)]
        Shape.__init__(self, coords, 'orange')
        self.center_block = self.blocks[1]


class L_shape(Shape):
    def __init__(self, center):
        coords = [Point(center.x - 1, center.y),
                  Point(center.x, center.y),
                  Point(center.x + 1, center.y),
                  Point(center.x - 1, center.y + 1)]
        Shape.__init__(self, coords, 'cyan')
        self.center_block = self.blocks[1]


class O_shape(Shape):
    def __init__(self, center):
        coords = [Point(center.x, center.y),
                  Point(center.x - 1, center.y),
                  Point(center.x, center.y + 1),
                  Point(center.x - 1, center.y + 1)]
        Shape.__init__(self, coords, 'red')
        self.center_block = self.blocks[0]

    def rotate(self, board):
        # Override Shape's rotate method since O_Shape does not rotate
        return


class S_shape(Shape):
    def __init__(self, center):
        coords = [Point(center.x, center.y),
                  Point(center.x, center.y + 1),
                  Point(center.x + 1, center.y),
                  Point(center.x - 1, center.y + 1)]
        Shape.__init__(self, coords, 'green')
        self.center_block = self.blocks[0]
        self.shift_rotation_dir = True
        self.rotation_dir = -1


class T_shape(Shape):
    def __init__(self, center):
        coords = [Point(center.x - 1, center.y),
                  Point(center.x, center.y),
                  Point(center.x + 1, center.y),
                  Point(center.x, center.y + 1)]
        Shape.__init__(self, coords, 'yellow')
        self.center_block = self.blocks[1]


class Z_shape(Shape):
    def __init__(self, center):
        coords = [Point(center.x - 1, center.y),
                  Point(center.x, center.y),
                  Point(center.x, center.y + 1),
                  Point(center.x + 1, center.y + 1)]
        Shape.__init__(self, coords, 'magenta')
        self.center_block = self.blocks[1]
        self.shift_rotation_dir = True
        self.rotation_dir = -1

############################################################
# BOARD CLASS
############################################################


class Board():
    ''' Board class: it represents the Tetris board

        Attributes: width - type:int - width of the board in squares
                    height - type:int - height of the board in squares
                    canvas - type:CanvasFrame - where the pieces will be drawn
                    grid - type:Dictionary - keeps track of the current state of
                    the board; stores the blocks for a given position
    '''

    def __init__(self, win, width, height):
        self.width = width
        self.height = height

        # create a canvas to draw the tetris shapes on
        self.canvas = CanvasFrame(win, self.width * Block.BLOCK_SIZE,
                                        self.height * Block.BLOCK_SIZE)
        self.canvas.setBackground('light gray')

        # create an empty dictionary to hold shapes on the board
        self.grid = {}

    def draw_shape(self, shape):
        ''' Parameters: shape - type: Shape
            Return value: type: bool

            draws the shape on the board if there is space for it
            and returns True, otherwise it returns False
        '''
        if shape.can_move(self, 0, 0):
            shape.draw(self.canvas)
            return True

        self.game_over()
        return False

    def can_move(self, x, y):
        ''' Parameters: x - type:int
                        y - type:int
            Return value: type: bool

            1. checks if it is ok to move to square x,y
            if the position is outside of the board boundaries, can't move there
            return False
            2. If there is already a block at that postion, can't move there
            return False
            3. Returns True in all other cases
        '''

        if x not in range(Tetris.BOARD_WIDTH) or y not in range(Tetris.BOARD_HEIGHT):
            return False
        elif (x, y) in self.grid.keys():
            return False
        else:
            return True

    def add_shape(self, shape):
        ''' Parameter: shape - type:Shape

            add a shape to the grid, i.e.
            add each block to the grid using its
            (x, y) coordinates as a dictionary key

            Hint: use the get_blocks method on Shape to
            get the list of blocks

        '''
        blocks = Shape.get_blocks(shape)
        for block in blocks:
            self.grid[(block.x, block.y)] = block

    def delete_row(self, y):
        ''' Parameters: y - type:int

            remove all the blocks in row y
            to remove a block you must remove it from the grid
            and erase it from the screen.
            If you dont remember how to erase a graphics object
            from the screen, take a look at the Graphics Library
            handout

        '''
        for x in range(10):
            self.grid[(x, y)].undraw()
            del self.grid[(x, y)]

    def is_row_complete(self, y):
        ''' Parameter: y - type: int
            Return value: type: bool

            for each block in row y
            check if there is a block in the grid (use the in operator)
            if there is one square that is not occupied, return False
            otherwise return True

        '''
        for x in range(10):
            if (x, y) not in self.grid.keys():
                return False

        return True

    def move_down_rows(self, y_start):
        ''' Parameters: y_start - type:int

            for each row from y_start to the top
                for each column
                    check if there is a block in the grid
                    if there is, remove it from the grid
                    and move the block object down on the screen
                    and then place it back in the grid in the new position

        '''
        while y_start > 0:
            for x in range(10):
                if (x, y_start) in self.grid.keys():
                    block = self.grid[(x, y_start)]
                    del self.grid[(x, y_start)]
                    block.move(0, 1)
                    self.grid[(block.x, block.y)] = block

            y_start -= 1

    def remove_complete_rows(self):
        ''' removes all the complete rows
            1. for each row, y,
            2. check if the row is complete
                if it is,
                    delete the row
                    move all rows down starting at row y - 1

        '''
        for y in range(Tetris.BOARD_HEIGHT):
            if self.is_row_complete(y):
                self.delete_row(y)
                self.move_down_rows(y)

    def game_over(self):
        ''' display "Game Over !!!" message in the center of the board
            HINT: use the Text class from the graphics library
        '''
        game = Text(Point(self.width / 2 * Block.BLOCK_SIZE, self.height / 2.5 *
                                            Block.BLOCK_SIZE), "Game Over !!!")
        game.setSize(30)
        game.setStyle('bold')
        game.draw(self.canvas)
        return True

############################################################
# SCOREBOARD CLASS
############################################################


class ScoreBoard():
    ''' ScoreBoard class: Scores the game, keeps track of the level

        Attributes: width - type:int - width of the board in squares
                    height - type:int - height of the board in squares
                    canvas - type:CanvasFrame - where the pieces will be drawn

    '''
    Level = 1
    Level2 = 1
    Display = 0

    def __init__(self, win, width, height):
        self.width = width
        self.height = height
        self.canvas = CanvasFrame(win, self.width * Block.BLOCK_SIZE,
                                        self.height * Block.BLOCK_SIZE)
        self.canvas.setBackground('light gray')
        self.current_score = Text(Point(8 * Block.BLOCK_SIZE, self.height / 2 *
                                                Block.BLOCK_SIZE), self.Display)
        self.current_score.setSize(25)
        self.current_score.draw(self.canvas)
        self.current_level = Text(Point(self.width / 4 * Block.BLOCK_SIZE,
                                        self.height / 2 * Block.BLOCK_SIZE),
                                        "Level " + str(self.Level))
        self.current_level.setSize(25)
        self.current_level.draw(self.canvas)

    def update(self, score):

        self.Display += score

        self.current_score.setText(self.Display)
        if 0 <= self.Display < 1000:
            self.Level = 1
        elif 1000 <= self.Display < 2000:
            self.Level = 2
        elif 2000 <= self.Display < 4000:
            self.Level = 3
        elif 4000 <= self.Display < 8000:
            self.Level = 4
        elif 8000 <= self.Display < 16000:
            self.Level = 5
        else:
            self.Level = 6
        self.current_level.setText("Level " + str(self.Level))

    def level_up(self):
        if self.Level == self.Level2:
            return False
        else:
            self.Level2 += 1
            return True

############################################################
# SPIECE PREVIEW CLASS
############################################################


class PiecePreview():
    ''' piece preview class: Shows the upcoming piece

        Attributes: width - type:int - width of the board in squares
                    height - type:int - height of the board in squares
                    canvas - type:CanvasFrame - where the pieces will be drawn
                    grid - type:Dictionary - keeps track of the current state of
                    the board; stores the blocks for a given position
    '''

    def __init__(self, win, width, height):
        self.width = width
        self.height = height
        self.canvas = CanvasFrame(win, self.width * Block.BLOCK_SIZE,
                                        self.height * Block.BLOCK_SIZE)
        self.canvas.setBackground('light gray')

    def draw_shape(self, n):
        ''' Parameters: shape - type: Shape
            draws the preview piece on the board
        '''
        self.preview = Tetris.SHAPES[n](Point(int(Tetris.BOARD_WIDTH / 2), 0.5))
        self.preview.draw(self.canvas)

    def remove_shape(self):
        ''' Removes the current piece preview

        '''
        Shape.undraw(self.preview)


############################################################
# TETRIS CLASS
############################################################

class Tetris(object):
    ''' Tetris class: Controls the game play
        Attributes:
            SHAPES - type: list (list of Shape classes)
            DIRECTION - type: dictionary - converts string direction to (dx, dy)
            BOARD_WIDTH - type:int - the width of the board
            BOARD_HEIGHT - type:int - the height of the board
            board - type:Board - the tetris board
            win - type:Window - the window for the tetris game
            delay - type:int - the speed in milliseconds for moving the shapes
            current_shape - type: Shape - the current moving shape on the board
    '''

    SHAPES = [I_shape, J_shape, L_shape, O_shape, S_shape, T_shape, Z_shape]
    DIRECTION = {'Left': (-1, 0), 'Right': (1, 0), 'Down': (0, 1)}
    BOARD_WIDTH = 10
    BOARD_HEIGHT = 20

    def __init__(self, win):

        self.score = ScoreBoard(win, self.BOARD_WIDTH, 2)
        self.piece = PiecePreview(win, self.BOARD_WIDTH, 3)
        self.board = Board(win, self.BOARD_WIDTH, self.BOARD_HEIGHT)

        self.win = win
        self.delay = 1000  # ms
        self.key = 0
        # sets up the keyboard events
        # when a key is called the method key_pressed will be called
        self.win.bind_all('<Key>', self.key_pressed)

        # set the current shape to a random new shape
        self.current_shape = self.create_new_shape()

        # Draw the current_shape on the board (take a look at the
        # draw_shape method in the Board class)
        self.board.draw_shape(self.current_shape)
        self.new = self.create_new_shape()
        PiecePreview.draw_shape(self.piece, self.random_number)
        #  animate the shape!
        self.animate_shape()

    def create_new_shape(self):
        ''' Return value: type: Shape

            Create a random new shape that is centered
             at y = 0 and x = int(self.BOARD_WIDTH/2)
            return the shape
        '''
        self.random_number = random.randint(0, 6)
        self.new_shape = self.SHAPES[self.random_number](Point(int
                                        (self.BOARD_WIDTH / 2), 0))
        return self.new_shape

    def animate_shape(self):
        ''' animate the shape - move down at equal intervals
            specified by the delay attribute
        '''
        if (self.key == 'p' or self.key == 'P') and self.timestop != self.delay:
            return
        if self.current_shape.can_move(self.board, 0, 0):
            self.do_move('Down')
            self.win.after(self.delay, self.animate_shape)

    def do_move(self, direction):
        ''' Parameters: direction - type: string
            Return value: type: bool

            Move the current shape in the direction specified by the parameter:
            First check if the shape can move. If it can, move it and return
            True Otherwise if the direction we tried to move was 'Down',
            add the current shape to the board, scores completed rows
            checks if level up, remove the completed rows if any,
            create a new random shape and sets current_shape attribute
            3. If the shape cannot be drawn on the board, displays a
               game over message

        '''

        (dx, dy) = self.DIRECTION[direction]

        if self.current_shape.can_move(self.board, dx, dy):
            self.current_shape.move(dx, dy)
            return True

        if self.current_shape.can_move(self.board, dx,
                     dy) == False and (dx, dy) == (0, 1):
            Board.add_shape(self.board, self.current_shape)
            PiecePreview.remove_shape(self.piece)
            scored1 = 5 * ScoreBoard.Level
            ScoreBoard.update(self.score, scored1)
            mult = 0
            for y in range(self.BOARD_HEIGHT):
                if Board.is_row_complete(self.board, y) == True:
                    mult += 2
            if mult > 0:
                scored = 10 * mult * ScoreBoard.Level * mult
            elif mult >= 8:
                scored = 1000 * ScoreBoard.Level
            else:
                scored = 0
            ScoreBoard.update(self.score, scored)
            if ScoreBoard.level_up(self.score) == True:
                self.delay -= 120
            Board.remove_complete_rows(self.board)
            self.current_shape = self.new
            self.board.draw_shape(self.current_shape)
            self.new = self.create_new_shape()
            PiecePreview.draw_shape(self.piece, self.random_number)
            return True
        return False

    def do_rotate(self):
        ''' Checks if the current_shape can be rotated and
            rotates if it can
        '''
        if self.delay == 100000:
            return
        if self.current_shape.can_rotate(self.board):
            self.current_shape.rotate(self.board)

    def key_pressed(self, event):
        ''' when a key is pressed on the keyboard the current_shape will move in
            the appropriate direction
            if the user presses the space bar 'space', the shape will move
            down until it can no longer move and is added to the board
            if the user presses the 'Up' arrow key
                the shape rotates.
        '''

        self.key = event.keysym
        if self.key in self.DIRECTION:
            if self.delay == 100000:
                return
            return self.do_move(self.key)
        elif self.key == 'space':
            if self.delay == 100000:
                return
            while self.current_shape.can_move(self.board, 0, 1):
                self.do_move('Down')
        elif self.key == 'Up':
            self.do_rotate()
        elif self.key == 'p' or self.key == 'P':
            if self.delay == 100000 and (self.key == 'p' or self.key == 'P'):
                self.delay = self.timestop
                self.animate_shape()

            else:
                self.timestop = self.delay
                self.delay = 100000

################################################################
# Start the game
################################################################

win = Window("Tetris")
game = Tetris(win)
win.mainloop()

from tkinter import Frame, Label, CENTER

import Game2048
import Game2048_constant as c

class Game(Frame): # Frame class to make a frame
    
    def __init__(self):
        Frame.__init__(self) # Frame inherited as super class
    
        self.grid() # inbuilt grid manager in tkinter so frame is visualised as a grid
        self.master.title('2048')
        self.master.bind("<Key>",self.key_down) # if any key event happens in the master 
                                                # boundary/frame, it'll be represented by key down
        self.commands = {c.KEY_UP: Game2048.move_up,c.KEY_DOWN: Game2048.move_down,
                         c.KEY_LEFT: Game2048.move_left,c.KEY_RIGHT: Game2048.move_right}
        
        self.grid_cells = []
        self.init_grid() # to initialize widgets like background/grid cells
        self.init_matrix() # to initialize the matrix
        self.update_grid_cells() # to change UI like color etc
        
        self.mainloop() # to run the program when the frame is ready
    
    def init_grid(self):
        # creating a frame inside a frame
        background = Frame(self, bg = c.BACKGROUND_COLOR_GAME,
                           width = c.SIZE, height = c.SIZE)
        background.grid()
        
        for i in range(c.GRID_LEN):
            grid_row = []
            for j in range(c.GRID_LEN):
                # create a frame for cell of size (size/length)
                cell = Frame(background, bg = c.BACKGROUND_COLOR_CELL_EMPTY,
                             width = c.SIZE / c.GRID_LEN,
                             height = c.SIZE / c.GRID_LEN)
                # add cell inside grid
                # padding is for gap between cells
                cell.grid(row = i,column = j,padx = c.GRID_PADDING,
                          pady = c.GRID_PADDING)
                # add label inside a cell
                t = Label(master = cell,text = '',
                          bg = c.BACKGROUND_COLOR_CELL_EMPTY,
                          justify = CENTER, font = c.FONT, width = 5, height = 2)
                t.grid() # initialize label as a grid
                grid_row.append(t)
                
            self.grid_cells.append(grid_row)
    
    def init_matrix(self): # to initialize matrix and add 2 random 2s
        self.matrix = Game2048.start()
        Game2048.add_new(self.matrix)
        Game2048.add_new(self.matrix)
        
    def update_grid_cells(self):
        for i in range(c.GRID_LEN):
            for j in range(c.GRID_LEN):
                new_number = self.matrix[i][j]
                if new_number == 0: # if cell is empty, set text to none and background empty
                    self.grid_cells[i][j].configure(
                        text ="",bg = c.BACKGROUND_COLOR_CELL_EMPTY)
                else: # if number is present, sell background accordingly
                    self.grid_cells[i][j].configure(text=str(
                        new_number), bg = c.BACKGROUND_COLOR_DICT[new_number],
                        fg = c.CELL_COLOR_DICT[new_number])
        self.update_idletasks() # waits till all updates are done
        
    def key_down(self,event):
        key = repr(event.char) # for correct mapping
        if key in self.commands:
            self.matrix, changed = self.commands[repr(event.char)](self.matrix)
            if changed:
                Game2048.add_new(self.matrix)
                self.update_grid_cells()
                changed = False
                if Game2048.state(self.matrix)=='WON':
                    self.grid_cells[1][1].configure(
                        text = 'You',bg = c.BACKGROUND_COLOR_CELL_EMPTY)
                    self.grid_cells[1][2].configure(
                        text = 'Win!',bg = c.BACKGROUND_COLOR_CELL_EMPTY)
                if Game2048.state(self.matrix)=='LOST':
                    self.grid_cells[1][1].configure(
                        text = 'You',bg = c.BACKGROUND_COLOR_CELL_EMPTY)
                    self.grid_cells[1][2].configure(
                        text = 'Lose!',bg = c.BACKGROUND_COLOR_CELL_EMPTY)
                
    
game = Game()
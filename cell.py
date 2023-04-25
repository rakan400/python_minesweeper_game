from tkinter import Button, Label
import random
import settings
import sys, os
import ctypes

class Cell():
    all = []
    cell_count_label_object = None
    mine_count_label_object = None
    cell_count = settings.CELLS_COUNT - settings.MINES_COUNT
    mines_count = settings.MINES_COUNT

    def __init__(self, x, y, is_mine=False):
        self.is_mine = is_mine
        self.is_opened = False
        self.is_mine_candidate = False
        self.cell_btn_object = None
        self.x = x
        self.y = y
        Cell.all.append(self)

    def create_btn_object(self, location):
        btn = Button(
            location,
            width = 10,
            height = 3,
        )
        btn.bind('<Button-1>', self.left_click_actions)            # <button-1> is left click in tkinter
        btn.bind('<Button-3>', self.right_click_actions)            # <button-3> is right click in tkinter
        self.cell_btn_object = btn

    def left_click_actions(self,event):     # the event does nothing, but it's essential for tkinter events
        if self.is_mine:
            self.show_mine()
        else:
            if self.surrounded_cells_mines_length == 0:
                for cell in self.surrounded_cells:
                    cell.show_cell()
            self.show_cell()

            if Cell.cell_count == 0 and Cell.mines_count==0:
                value = ctypes.windll.user32.MessageBoxW(0, "Congratulations, You win! Retry?", "Game Over", 4) # display a message box
                if value == 6:
                    python = sys.executable
                    os.execl(python, python, * sys.argv)
                else:
                    sys.exit()

        self.cell_btn_object.unbind('<Button-1>')
        self.cell_btn_object.unbind('<Button-3>')
        self.cell_btn_object["state"] = "disabled"

    def get_cell_by_axis(self, x, y):       # get cell based on x and y
        for cell in Cell.all:
            if cell.x == x and cell.y == y:
                return cell
            
    @property
    def surrounded_cells(self):
        cells = []
        for i in range (-1, 2):
            for j in range(-1, 2):
                if i == 0 and j == 0:
                    continue
                elif self.get_cell_by_axis(self.x+i,self.y+j) == None:
                    continue
                else:
                    cells.append(self.get_cell_by_axis(self.x+i,self.y+j))
        return cells
    
    @property
    def surrounded_cells_mines_length(self):        # get number of mines in surrounding cells
        mines = [cell.is_mine for cell in self.surrounded_cells]
        return mines.count(True)

    def show_cell(self):        # show the number of mines surrounding a cell
        if not self.is_opened:
            self.cell_btn_object.configure(bg='SystemButtonFace') 
            Cell.cell_count -=1
            self.cell_btn_object.configure(text=f'{self.surrounded_cells_mines_length}')
            if Cell.cell_count_label_object:
                Cell.cell_count_label_object.configure(text=f'Cells Left: {Cell.cell_count}')

        if self.is_mine_candidate:
            Cell.mines_count += 1
            Cell.mine_count_label_object.configure(text=f'Mines Left: {Cell.mines_count}')

        self.cell_btn_object.configure(bg='SystemButtonFace') 
        self.is_opened = True

    def show_mine(self):
        self.cell_btn_object.configure(bg='red')
        value = ctypes.windll.user32.MessageBoxW(0, "You lost! Retry?", "game over", 4) # display a message box
        if value == 6:
            python = sys.executable
            os.execl(python, python, * sys.argv)
        else:
            sys.exit()

    def right_click_actions(self,event):     # the event does nothing, but it's essential for tkinter events
        if not self.is_mine_candidate and not self.is_opened:
            if Cell.mines_count == 0:
                ctypes.windll.user32.MessageBoxW(0, "You reached the maximum number of mines", "", 0) # display a message box
            else:
                Cell.mines_count -=1
                self.cell_btn_object.configure(bg='orange')
                Cell.mine_count_label_object.configure(text=f'Mines Left: {Cell.mines_count}')
                self.is_mine_candidate = True
        elif not self.is_opened:
            Cell.mines_count +=1
            Cell.mine_count_label_object.configure(text=f'Miness Left: {Cell.mines_count}')
            self.cell_btn_object.configure(bg='SystemButtonFace')   # SystemButtonFace is default color of buttons
            self.is_mine_candidate = False

        if Cell.cell_count == 0 and Cell.mines_count==0:
                value = ctypes.windll.user32.MessageBoxW(0, "Congratulations, You win! Retry?", "Game Over", 4) # display a message box
                if value == 6:
                    python = sys.executable
                    os.execl(python, python, * sys.argv)
                else:
                    sys.exit()
     
    @staticmethod
    def randomize_mines():
        picked_cells = random.sample(Cell.all, settings.MINES_COUNT)
        for cell in picked_cells:
            cell.is_mine = True

    @staticmethod                           # static method is just for usecase of class not the instance
    def create_cell_count_label(location):
        lbl = Label(location, 
                    text=f'Cells Left: {Cell.cell_count}',
                    bg='grey', 
                    fg='white',
                    font=("Times New Roman", 25)
                    )
        Cell.cell_count_label_object = lbl

    @staticmethod                           # static method is just for usecase of class not the instance
    def create_mine_count_label(location):
        lbl = Label(location, 
                    text=f'Mines Left: {settings.MINES_COUNT}', 
                    bg='grey', 
                    fg='white',
                    font=("Times New Roman", 25)
                    )
        Cell.mine_count_label_object = lbl

    def __repr__(self):
        return f"Cell({self.x}, {self.y})"
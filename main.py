from tkinter import *
import settings
import utilities
from cell import Cell

root = Tk()

screen_width = root.winfo_screenwidth()  # Width of the screen
screen_height = root.winfo_screenheight() # Height of the screen

x = int((screen_width/2) - (settings.WIDTH/2))
y = int((screen_height/2) - (settings.HEIGHT/2))

root.configure(bg="grey")      # background color = black
root.geometry(f'{settings.WIDTH}x{settings.HEIGHT}+{x}+{y}')   # change size of window
root.title("Minesweeper Game")
root.resizable(False, False)    #disable resizing the window

top_frame = Frame(
    root,
    bg='grey',       # background color
    width = settings.WIDTH,
    height = utilities.height_percentage(25),
)
top_frame.place(x = 0, y = 0)        # placement of frame

game_title = Label(
    top_frame,
    bg='grey',
    font=("Times New Roman", 45),
    fg='white',
    text='Minesweeper:'
)
game_title.place(x=utilities.width_percentage(25), y=25)

left_frame = Frame(
    root,
    bg='grey',
    width = utilities.width_percentage(25),
    height = utilities.height_percentage(75)
)
left_frame.place(x = 0, y = 130)

center_frame = Frame(
    root,
    bg='grey',
    width = utilities.width_percentage(75),
    height = utilities.height_percentage(75),
)
center_frame.place(x = utilities.width_percentage(25), y = utilities.height_percentage(25))

for x in range(settings.GRID_SIZE):         # initialize the buttons using the cell class
    for y in range(settings.GRID_SIZE):
        c = Cell(x, y)
        c.create_btn_object(center_frame)
        c.cell_btn_object.grid(column=x, row=y)

Cell.randomize_mines()          # change some cells in board to mines

Cell.create_cell_count_label(left_frame)
Cell.cell_count_label_object.place(x=30,y=0)

Cell.create_mine_count_label(left_frame)
Cell.mine_count_label_object.place(x=30,y=60)


 
# Calculate Starting X and Y coordinates for Window

 

root.mainloop()        # run window until we hit x button
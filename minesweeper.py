from tkinter import *
import settings
import utility
from cell import Cell

root = Tk()

#Settings of the window
root.configure(bg="black")
root.geometry(f"{settings.WIDTH}x{settings.HEIGHT}")
root.title('Minesweeper Game')
root.resizable(False, False)

top_frame = Frame(
    root, 
    bg = "#000000",
    width = settings.WIDTH,
    height = utility.height_perc(20)
)
top_frame.place(x=0, y=0)

left_frame = Frame(
    root,
    bg = "#000000",
    width = utility.width_perc(20),
    height = utility.height_perc(80),
)
left_frame.place(x = 0, y=utility.height_perc(20))

centre_frame = Frame(
    root,
    bg="#000000",
    width = utility.width_perc(80),
    height = utility.height_perc(80),
)
centre_frame.place(x= utility.width_perc(20), y= utility.height_perc(20))

for i in range(settings.GRID_SIZE):
    for j in range(settings.GRID_SIZE):
        c = Cell(i+1, j+1)
        c.create_button(centre_frame)
        c.cell_button.grid(
            column=i, row=j
        )

Cell.random_mine()
Cell.cell_count_label(left_frame)
Cell.cell_count.place(x=0 , y = 0)

game_title=Label(
    bg = 'black',
    fg = 'white',
    text = "MINESWEEPER",
    font = ("", 48)
)

game_title.place(
    x = utility.width_perc(37),
    y = utility.height_perc(5)
)
#Start of mainloop
root.mainloop()
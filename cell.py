from tkinter import Button, Label
import random
import settings
import sys
import subprocess

losescript = """
display dialog "You clicked on a mine!" ¬
with title "GAME OVER" ¬
with icon caution ¬
buttons {"OK"}
"""
winscript = """
display dialog "You have won the game!" ¬
with title "CONGRATULATIONS" ¬
with icon caution ¬
buttons {"OK"}
"""

class Cell:

    all = []
    cell_count = None
    cellCount = settings.CELL_COUNT

    def __init__(self, x, y, is_mine = False) -> None:
        self.is_mine = is_mine
        self.is_open = False
        self.mine_candidate = False
        self.cell_button = None
        self.x = x
        self.y = y
        Cell.all.append(self)

    def create_button(self, location):
        btn = Button(
            location,
            width = 12,
            height = 4,
            highlightbackground='white'
        )
        btn.bind('<Button-1>', self.left_click)
        btn.bind('<Button-2>', self.right_click)
        self.cell_button = btn

    @staticmethod
    def cell_count_label(location):
        lbl = Label(
            location,
            text = f"Cells left = {(Cell.cellCount)}",
            bg = "black",
            fg = "white",
            font = ("", 30)
        )
        Cell.cell_count = lbl
    
    def show_mine(self):
        subprocess.call("osascript -e '{}'".format(losescript), shell=True)
        sys.exit()

    def get_cell(self, x, y):
        for cell in Cell.all:
            if cell.x == x and cell.y == y:
                return cell

    @property
    def surround_cells(self):
        surrounding_cells = []
        for i in range(self.x-1, self.x+2):
            for j in range(self.y-1, self.y+2):
                cell = self.get_cell(i, j)
                surrounding_cells.append(cell)
        cell = self.get_cell(self.x, self.y)
        surrounding_cells.remove(cell)
        surrounding_cells = [cell for cell in surrounding_cells if cell is not None]
        return surrounding_cells

    @property
    def get_mine_number(self):
        cells = self.surround_cells
        count = 0
        for cell in cells:
            if cell.is_mine == True:
                count = count+1
        return count

    def show_cell(self):
        if not self.is_open:
            Cell.cellCount -= 1
        self.cell_button.configure(text = self.get_mine_number)
        #change cells left label value
        Cell.cell_count.configure(text = f"Cells left= {Cell.cellCount}")
        self.is_open = True

    def left_click(self, event):
        if self.is_mine:
            self.show_mine()
        else:
            self.cell_button.configure(
                highlightbackground='white'
            )
            self.mine_candidate = False
            if self.get_mine_number == 0:
                for cell_obj in self.surround_cells:
                    cell_obj.show_cell()
            self.show_cell()
            if Cell.cellCount == settings.CELL_COUNT:
                subprocess.call("osascript -e '{}'".format(losescript), shell=True)
                sys.exit()

        #Cancel events for open cell
        self.cell_button.unbind('<Button-1>')
        self.cell_button.unbind('<Button-2>')

    def right_click(self, event):
        if not self.mine_candidate:
            self.cell_button.configure(
                highlightbackground='orange'
            )
            self.mine_candidate = True
        else:
            self.cell_button.configure(
                highlightbackground='white'
            )
            self.mine_candidate = False

    @staticmethod
    def random_mine():
        mines = random.sample(
            Cell.all, settings.MINES_COUNT
        )
        for i in mines:
            i.is_mine = True

    def __repr__(self) -> str:
        return f"Cell({self.x},{self.y})"
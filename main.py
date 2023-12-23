# %%

import numpy as np
import numpy.typing as npt

import matplotlib.pyplot as plt

from typing import (
    Literal
)
# %%

class board(object):

    def __init__(self):
        self.modifier_grid: npt.NDArray[modifier] = make_standard_grid()
        self.grid: npt.NDArray[str | None] = np.full((15, 15), None)

    def draw(self):
        plt.figure()
        for i, row in enumerate(self.modifier_grid):
            for j, point in enumerate(row):
                plt.scatter(i, j, color = point.colour)
        plt.show()
    
    def _check_empty(self, positions: list[tuple[int, int]])-> bool:
        for position in positions:
            if self.grid[position] is not None:
                return False
        return True
    
    def play_word(self, letters: list[str], positions = list[tuple[int, int]])->int:
        self._check_empty(positions)


class modifier(object):

    def __init__(self, mult: Literal[2, 3, 1], type: Literal["letter", "word"]):
        self.type: Literal["letter" , "word"] = type
        self.mult: Literal[2 , 3] = mult

        self.colour = self._colour()

    def _colour(self):
        if self.mult == 1:
            colour = 'g'
        elif self.mult == 3 and self.type == "word":
            colour = 'r'
        elif self.mult == 2 and self.type == "word":
            colour = 'orange'
        elif self.mult == 3 and self.type == "letter":
            colour = 'b'
        elif self.mult == 2 and self.type == "letter":
            colour = "c"
        return colour
        
MODIFIER_TRIPLE_WORD = modifier(3, "word")
MODIFIER_DOUBLE_WORD = modifier(2, "word")
MODIFIER_TRIPLE_LETTER = modifier(3, "letter")
MODIFIER_DOUBLE_LETTER = modifier(2, "letter")

def make_standard_grid()->npt.NDArray[modifier]:
    grid = np.full((15, 15), modifier(1, "letter"))

    triple_word_coords = [
        (0, 0), (0, 7), (0, 14), (7, 0), (14, 0), (14, 7), (7, 14), (14, 14),
    ]
    double_word_coords = [
        (7, 7),
        (1, 1), (2, 2), (3, 3), (4, 4),
        (13, 1), (12, 2), (11, 3), (10, 4),
        (1, 13), (2, 12), (3, 11), (4, 10),
        (13, 13), (12, 12), (11, 11), (10, 10)
    ]
    
    triple_letter_coords = [
        (1, 5), (5, 1), (5, 5),
        (13, 5), (9, 1), (9, 5),
        (1, 9), (5, 13), (5, 9),
        (9, 13), (13, 9), (9, 9),
    ]
    double_letter_coords = [
        (0, 3), (3, 0), (6, 2), (2, 6), (6, 6),
        (14, 3), (11, 0), (8, 2), (12, 6), (8, 6),
        (0, 11), (3, 14), (6, 12), (2, 8), (6, 8),
        (14, 11), (11, 14), (8, 12), (12, 8), (8, 8),
        (3, 7), (7, 3), (11, 7), (7, 11),
    ]

    for coord in triple_word_coords:
        grid[coord] = MODIFIER_TRIPLE_WORD

    for coord in double_word_coords:
        grid[coord] = MODIFIER_DOUBLE_WORD

    for coord in triple_letter_coords:
        grid[coord] = MODIFIER_TRIPLE_LETTER

    for coord in double_letter_coords:
        grid[coord] = MODIFIER_DOUBLE_LETTER

    return grid 


class letter(object):

    def __init__(self):
        self.value = 1

letter_values = {
    "A": 1,
    "B": 3,
    "C": 3,
    "D": 2,
    "E": 1,
    "F": 4,
    "G": 2,
    "H": 4,
    "I": 1,
    "J": 8,
    "K": 5,
    "L": 1,
    "M": 3,
    "N": 1,
    "O": 1,
    "P": 3,
    "Q": 10,
    "R": 1,
    "S": 1,
    "T": 1,
    "U": 1,
    "V": 4,
    "W": 4,
    "X": 8,
    "Y": 4,
    "Z": 10,
    " ": 0,
}
# %%

test_board = board()

test_board.draw()
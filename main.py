# %%

import numpy as np
import numpy.typing as npt

import matplotlib.pyplot as plt

from typing import (
    Literal
)
# %%

class Letter(object):

    def __init__(self, letter:str, blank_override:str = None):
        
        self.char: str = letter
        self.value = LETTER_VALUES[letter]
        self.blank_override: str | None = blank_override


def Word(object):

    def __init__(self):
        self.letters: list[Letter]
        self.positions: 

class Board(object):

    def __init__(self):
        self.modifier_grid: npt.NDArray[modifier] = make_standard_grid()
        self.grid: npt.NDArray[Letter | None] = np.full((15, 15), None)

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
    
    def _in_line(self, positions: list[tuple[int, int]])->bool:
        if len(positions) == 0:
            raise ValueError("empty list of positions to check if in line")
        row = positions[0][0]
        col = positions[0][1]
        for position in positions:
            if position[0]!=row:
                row = None
            if position[1]!=col:
                col = None
        if row is not None or col is not None:
            return True
        else:
            return False
    
    def _place_letters(self, letters: list[Letter], positions = list[tuple[int, int]])->None:
        for letter, position in zip(letters, positions):
            if self.grid[position] is not None:
                raise ValueError("Position in grid is not empty to place a letter")
            self.grid[position] = letter

    def _get_words_played(self, positions = list[tuple[int, int]])->set[Word]:
        words = {}
        for position in positions:
            LR_word = self._get_LR_word(position)
            words.add(LR_word)
            UD_word = self._get_UD_word(position)
            words.add(UD_word)
        return words

    def play_word(self, letters: list[Letter], positions = list[tuple[int, int]])->int:
        if not self._check_empty(positions):
            raise ValueError("Position on Board wasn't empty")
        if not self._in_line(positions):
            raise ValueError("Positions for word is not a stright line")

        self._place_letters(letters, positions)

        words_played = self._get_words_played(positions)



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

LETTER_VALUES = {
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

test_Board = Board()

test_Board.draw()
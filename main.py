# %%

import numpy as np
import numpy.typing as npt

import matplotlib.pyplot as plt
from matplotlib.collections import PatchCollection
from matplotlib.patches import Rectangle

from typing import Literal

# %%


class Letter(object):
    def __init__(self, letter: str, blank_override: str = None):
        self.char: str = letter
        self.value = LETTER_VALUES[letter]
        self.blank_override: str | None = blank_override

    def __repr__(self):
        return self.char


class Word(object):
    def __init__(self, letters: list[Letter], positions: tuple[int, int]):
        self.letters: list[Letter] = letters
        self.positions: list[tuple[int, int]] = positions

    def __repr__(self):
        return "".join([x.__repr__() for x in self.letters])

    def __eq__(self, other):
        return self.positions == other.positions

    def __hash__(self):
        return hash(tuple(self.positions))

    def __iter__(self):
        return iter(zip(self.letters, self.positions))
    
    @classmethod
    def init_dummy(cls, string)->'Word':
        letter_list = [Letter(x.upper()) for x in string]
        positions = [(np.random.randint(0,14), np.random.randint(0, 14)) for x in letter_list]

        return cls(letter_list, positions)



class Board(object):
    def __init__(self):
        self.modifier_grid: npt.NDArray[modifier] = make_standard_grid()
        self.grid: npt.NDArray[Letter | None] = np.full((15, 15), None)

    def draw(self):
        fig, ax = plt.subplots()
        for i, row in enumerate(self.modifier_grid):
            for j, point in enumerate(row):
                patch = Rectangle((i, j), 1, 1, facecolor=point.colour, alpha=0.3)
                ax.add_patch(patch)
                if self.grid[i, j] is not None:
                    plt.text(i + 0.25, j + 0.75, self.grid[i, j].char)
        plt.ylim(0, 15)
        plt.xlim(0, 15)
        plt.gca().invert_yaxis()
        plt.show()

    def _check_empty(self, positions: list[tuple[int, int]]) -> bool:
        for position in positions:
            if self.grid[position] is not None:
                return False
        return True

    def _in_line(self, positions: list[tuple[int, int]]) -> bool:
        if len(positions) == 0:
            raise ValueError("empty list of positions to check if in line")
        row = positions[0][0]
        col = positions[0][1]
        for position in positions:
            if position[0] != row:
                row = None
            if position[1] != col:
                col = None
        if row is not None or col is not None:
            return True
        else:
            return False

    def _place_letters(
        self, letters: list[Letter], positions=list[tuple[int, int]]
    ) -> None:
        for letter, position in zip(letters, positions):
            if self.grid[position] is not None:
                raise ValueError("Position in grid is not empty to place a letter")
            self.grid[position] = letter

    def _get_LR_word(self, position: tuple[int, int]) -> Word:
        lhs = position[0]
        can_move_left = False
        if lhs > 0 and self.grid[(lhs - 1, position[1])] is not None:
            can_move_left = True
        while can_move_left:
            lhs -= 1
            if lhs <= 0 or self.grid[(lhs - 1, position[1])] is None:
                can_move_left = False

        rhs = position[0]
        can_move_right = False
        if rhs < 14 and self.grid[(rhs + 1, position[1])] is not None:
            can_move_right = True
        while can_move_right:
            rhs += 1
            if rhs >= 14 or self.grid[(rhs + 1, position[1])] is None:
                can_move_right = False

        x_range = list(range(lhs, rhs + 1))

        positions = [(x, position[1]) for x in x_range]
        letters = [self.grid[position] for position in positions]

        word = Word(letters, positions)

        return word

    def _get_UD_word(self, position: tuple[int, int]) -> Word:
        "left = up, right = down"
        lhs = position[1]
        can_move_left = False
        if lhs > 0 and self.grid[(position[0], lhs - 1)] is not None:
            can_move_left = True
        while can_move_left:
            lhs -= 1
            if lhs <= 0 or self.grid[(position[0], lhs - 1)] is None:
                can_move_left = False

        rhs = position[1]
        can_move_right = False
        if rhs < 14 and self.grid[(position[0], rhs + 1)] is not None:
            can_move_right = True
        while can_move_right:
            rhs += 1
            if rhs >= 14 or self.grid[(position[0], rhs + 1)] is None:
                can_move_right = False

        x_range = list(range(lhs, rhs + 1))  #
        positions = [(position[0], x) for x in x_range]
        letters = [self.grid[position] for position in positions]

        word = Word(letters, positions)

        return word

    def _get_words_played(self, positions=list[tuple[int, int]]) -> set[Word]:
        words = set()
        for position in positions:
            LR_word = self._get_LR_word(position)
            if len(LR_word.letters) > 1:
                words.add(LR_word)
            UD_word = self._get_UD_word(position)
            if len(UD_word.letters) > 1:
                words.add(UD_word)
        return words

    def _score_word(self, word: Word)->int:
        score = 0
        word_mult = 1
        for letter, position in word:
            temp = letter.value
            if not self.modifier_grid[position].used:
                if self.modifier_grid[position].type == "word":
                    word_mult *= self.modifier_grid[position].mult
                if self.modifier_grid[position].type == "letter":
                    temp *= self.modifier_grid[position].mult
            score += temp
        score *= word_mult
        return score
    
    def _mark_as_used(self, positions: list[tuple[int, int]]):
        for position in positions:
            self.modifier_grid[position].used = True

    def play_word(self, word: Word) -> list[tuple[Word, int]]:
        letters = word.letters
        positions = word.positions
        if not self._check_empty(positions):
            raise ValueError("Position on Board wasn't empty")
        if not self._in_line(positions):
            raise ValueError("Positions for word is not a stright line")

        self._place_letters(letters, positions)

        words_played = self._get_words_played(positions)

        scores = []
        for word in words_played:
            score = self._score_word(word)
            scores.append((word, score))

        self._mark_as_used(positions)

        return scores
    
    def play_game(self, words: list[Word])-> list[tuple[Word, int]]:
        game_words = []
        for word in words:
            new_words = self.play_word(word)
            game_words.extend(new_words)

        return game_words


class modifier(object):
    def __init__(self, mult: Literal[2, 3, 1], type: Literal["letter", "word"]):
        self.type: Literal["letter", "word"] = type
        self.mult: Literal[2, 3] = mult
        self.used = False

        self.colour = self._colour()

    def _colour(self):
        if self.mult == 1:
            colour = "green"
        elif self.mult == 3 and self.type == "word":
            colour = "red"
        elif self.mult == 2 and self.type == "word":
            colour = "orange"
        elif self.mult == 3 and self.type == "letter":
            colour = "blue"
        elif self.mult == 2 and self.type == "letter":
            colour = "cyan"
        return colour


def make_standard_grid() -> npt.NDArray[modifier]:
    grid = np.full((15, 15), modifier(1, "letter"))

    triple_word_coords = [
        (0, 0),
        (0, 7),
        (0, 14),
        (7, 0),
        (14, 0),
        (14, 7),
        (7, 14),
        (14, 14),
    ]
    double_word_coords = [
        (7, 7),
        (1, 1),
        (2, 2),
        (3, 3),
        (4, 4),
        (13, 1),
        (12, 2),
        (11, 3),
        (10, 4),
        (1, 13),
        (2, 12),
        (3, 11),
        (4, 10),
        (13, 13),
        (12, 12),
        (11, 11),
        (10, 10),
    ]

    triple_letter_coords = [
        (1, 5),
        (5, 1),
        (5, 5),
        (13, 5),
        (9, 1),
        (9, 5),
        (1, 9),
        (5, 13),
        (5, 9),
        (9, 13),
        (13, 9),
        (9, 9),
    ]
    double_letter_coords = [
        (0, 3),
        (3, 0),
        (6, 2),
        (2, 6),
        (6, 6),
        (14, 3),
        (11, 0),
        (8, 2),
        (12, 6),
        (8, 6),
        (0, 11),
        (3, 14),
        (6, 12),
        (2, 8),
        (6, 8),
        (14, 11),
        (11, 14),
        (8, 12),
        (12, 8),
        (8, 8),
        (3, 7),
        (7, 3),
        (11, 7),
        (7, 11),
    ]

    for coord in triple_word_coords:
        grid[coord] = modifier(3, "word")

    for coord in double_word_coords:
        grid[coord] = modifier(2, "word")

    for coord in triple_letter_coords:
        grid[coord] = modifier(3, "letter")

    for coord in double_letter_coords:
        grid[coord] = modifier(2, "letter")

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

test_word1 = {
    (7, 7): Letter("P"),
    (8, 7): Letter("E"),
    (9, 7): Letter("N"),
    (10, 7): Letter("I"),
}

test_Word1 = Word(list(test_word1.values()), list(test_word1.keys()))

print(test_word1)
print(test_Board.play_word(test_Word1))

# %%

test_word2 = {
    (11, 7): Letter("S"),
    (11, 8): Letter("I"),
    (11, 9): Letter("M"),
    (11, 10): Letter("P"),
}
test_Word2 = Word(list(test_word2.values()), list(test_word2.keys()))

print(test_word2)
print(test_Board.play_word(test_Word2))

test_Board.draw()
# %%

test_game = [
    test_Word1,
    test_Word2,
]

test_Board2 = Board()

results = test_Board2.play_game(test_game)

print(results)

test_Board2.draw()
# %%

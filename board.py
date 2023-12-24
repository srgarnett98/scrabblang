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

    @classmethod
    def from_string_and_init_pos(cls, string: str, init_pos: tuple[int, int], down_or_right: Literal["down", "right"])->'Word':
        letter_list = [Letter(x.upper()) for x in string]
        if down_or_right == "right":
            change_index = (True, False)
        elif down_or_right == "down":
            change_index = (False, True)
        else:
            raise ValueError("down_or_right must be 'down' or 'right")
        
        positions = []
        for i, letter in enumerate(letter_list):
            new_pos = (init_pos[0]+i*change_index[0],
                       init_pos[1]+i*change_index[1])
            positions.append(new_pos)

        return cls(letter_list, positions)


class Board(object):
    def __init__(self):
        self.grid: dict[tuple[int, int], Letter] = {}

    def draw(self):
        fig, ax = plt.subplots()
        for position, letter in self.grid.items():
            print(position)
            modifier = Modifier.find_modifier_at_x(position)
            print(modifier)
            rect = Rectangle((position[0] - 0.5, position[1] - 0.5), 1, 1, color = modifier._colour(), alpha = 0.3)
            ax.add_patch(rect)
            ax.relim()
            ax.autoscale_view()
            plt.text(position[0]-0.25, position[1]-0.25, letter.char)
        ax.invert_yaxis()
        plt.show()
        pass

    def _check_empty(self, positions: list[tuple[int, int]]) -> bool:
        for position in positions:
            if position in self.grid:
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
            if position in self.grid:
                raise ValueError("Position in grid is not empty to place a letter")
            self.grid[position] = letter

    def _get_LR_word(self, position: tuple[int, int]) -> Word:
        lhs = position[0]
        can_move_left = False
        if (lhs-1, position[1]) in self.grid:
            can_move_left = True
        while can_move_left:
            lhs -= 1
            if not (lhs-1, position[1]) in self.grid:
                can_move_left = False

        rhs = position[0]
        can_move_right = False
        if (rhs + 1, position[1]) in self.grid:
            can_move_right = True
        while can_move_right:
            rhs += 1
            if not (rhs + 1, position[1]) in self.grid:
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
        if (position[0], lhs - 1) in self.grid:
            can_move_left = True
        while can_move_left:
            lhs -= 1
            if not (position[0], lhs - 1) in self.grid:
                can_move_left = False

        rhs = position[1]
        can_move_right = False
        if (position[0], rhs + 1) in self.grid:
            can_move_right = True
        while can_move_right:
            rhs += 1
            if not (position[0], rhs + 1) in self.grid:
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

    def _score_word(self, word: Word, new_poses: tuple[int, int])->int:
        score = 0
        word_mult = 1
        for letter, position in word:
            modifier = Modifier.find_modifier_at_x(position)
            temp = letter.value
            if position in new_poses:
                if modifier.mode == "word":
                    word_mult *= modifier.mult
                if modifier.mode == "letter":
                    temp *= modifier.mult
            score += temp

        score *= word_mult
        return score

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
            score = self._score_word(word, positions)
            scores.append((word, score))

        return scores
    
    def play_game(self, words: list[Word])-> list[tuple[Word, int]]:
        game_words = []
        for word in words:
            new_words = self.play_word(word)
            game_words.extend(new_words)

        return game_words


class Modifier(object):
    def __init__(self, mult: Literal[2, 3, 1], mode: Literal["letter", "word"]):
        self.mode: Literal["letter", "word"] = mode
        self.mult: Literal[2, 3] = mult
        self.colour = self._colour()

    def __repr__(self):
        return "mult:" + str(self.mult) + " mode: " + self.mode

    def _colour(self):
        if self.mult == 1:
            colour = "green"
        elif self.mult == 3 and self.mode == "word":
            colour = "red"
        elif self.mult == 2 and self.mode == "word":
            colour = "orange"
        elif self.mult == 3 and self.mode == "letter":
            colour = "blue"
        elif self.mult == 2 and self.mode == "letter":
            colour = "cyan"
        return colour

    @classmethod
    def find_modifier_at_x(cls, position: tuple[int, int]):
        local_position = (np.abs(position[0]) % 15, np.abs(position[1]) % 15)

        triple_word_coords = [
            (0, 7), (0, 8), (7, 0), (8, 0),
            (7, 7), (7, 8), (8, 7), (8, 8),
        ]
        double_word_coords = [
            (0, 0),
            (3, 3), (4, 4), (5, 5), (6, 6),
            (9, 9), (10, 10), (11, 11), (12, 12),
        ]

        triple_letter_coords = [
            (2, 2), (2, 6), (6, 2),
            (9, 2), (13, 2), (13, 6),
            (2, 9), (2, 13), (6, 13),
            (9, 13), (13, 13), (13, 9),
        ]
        double_letter_coords = [
            (1, 1), (0, 4), (1, 5), (4, 0), (5, 1), (4, 7), (7, 4),
            (14, 1), (14, 5), (11, 0), (10, 1), (10, 7), (8, 4),
            (1, 14), (0, 11), (1, 10), (5, 14), (4, 8), (7, 11),
            (14, 14), (14, 10), (10, 14), (11, 8), (8, 11),
        ]

        if local_position in triple_word_coords:
            return Modifier(3, 'word')
        elif local_position in double_word_coords:
            return Modifier(2, 'word')
        elif local_position in triple_letter_coords:
            return Modifier(3, 'letter')
        elif local_position in double_letter_coords:
            return Modifier(2, 'letter')
        else:
            return Modifier(1, 'letter')


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

if __name__ == "__main__":

    test_Board = Board()

    test_word1 = {
        (0, 0): Letter("P"),
        (1, 0): Letter("E"),
        (2, 0): Letter("N"),
        (3, 0): Letter("I"),
    }

    test_Word1 = Word(list(test_word1.values()), list(test_word1.keys()))

    print(test_word1)
    print(test_Board.play_word(test_Word1))

    # %%

    test_word2 = {
        (4, 0): Letter("S"),
        (4, 1): Letter("I"),
        (4, 2): Letter("M"),
        (4, 3): Letter("P"),
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

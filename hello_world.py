# %%
from board import Board, Word, Letter, LETTER_VALUES
from board import (
    A, B, C, D, E, F, G, H, I, J, K, L, M, N, O ,P, Q, R, S, T, U, V, W, X, Y, Z,
)
from stack_manip import Stack

# %%

hello_world_board = Board()

game = [
    Word.from_string_and_init_pos('SAT', (-1, 0), 'right'),
    Word.from_string_and_init_pos('SE', (1, -2), 'down'),
    Word.from_string_and_init_pos('DD', (0, 1), 'down'),
    Word.from_string_and_init_pos('TIME', (-1, -4), 'down'),
    Word.from_string_and_init_pos('NEX', (-4, -4), 'right'),
    # this spells H
    Word.from_string_and_init_pos('ET', (2, -2), 'right'),
    Word.from_string_and_init_pos('AD', (-2, 2), 'right'), 
    Word.from_string_and_init_pos('DD', (-2, 3), 'down'),
    Word.from_string_and_init_pos('IMES', (3, -1), 'down'),
    Word.from_string_and_init_pos('MINI', (-7, -5), 'right'),
    Word([M, N, U, S], [(-6, -6), (-6, -4), (-6, -3), (-6, -2)]),
    # this spells He
    Word([N, X, T], [(2, 1), (4, 1), (5, 1)]),
    Word.from_string_and_init_pos('SNOW', (-4, -6), 'right'),
    Word.from_string_and_init_pos('SET', (-2, -7), 'right'),
    Word([Letter(' ', 'I'), M, E, S], [(5, 2), (5, 3), (5, 4), (5, 5)]),
    Word([N, X, T], [(4, 4), (6, 4), (7, 4)]),
    # this spells Hel
    Word.from_string_and_init_pos('SE', (0, -9), 'down'),
    Word([T, Letter(' ', 'I'), M, E, S], [(4, -6), (4, -5), (4, -4), (4, -3), (4, -2)]),
    Word.from_string_and_init_pos('NEX', (7, 1), 'down'),
    # this spells Hell
    Word.from_string_and_init_pos('TOM', (-6, 3), 'right'),
    Word.from_string_and_init_pos('SE', (-6, 1), 'down'),
    Word.from_string_and_init_pos('AD', (-4, 4), 'right'),
    Word([I, Letter(' ', 'M'), E, S], [(5, -6), (6, -6), (7, -6),(8, -6)]),
    Word.from_string_and_init_pos('MINU', (-4, -9), 'right'),
]

#%%

results = hello_world_board.play_game(game)

# %%

print(results)

# %%

hello_world_board.draw()

#%%

hello_world_stack = Stack()

hello_world_stack.set_execute_list(results)

hello_world_stack.execute()

print(hello_world_stack.stack)

hello_world_stack._print()
# %%

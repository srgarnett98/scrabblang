# %%
from board import Board, Word, Letter
from stack_manip import Stack

# %%
test_Board = Board()

test_Game = [
    Word.from_string_and_init_pos('ADD', (0, 0), 'right'),
    Word.from_string_and_init_pos('NEE', (3, -3), 'down'),
    Word.from_string_and_init_pos('EXT', (4, -3), 'right'),
    Word.from_string_and_init_pos('DD', (0, 1), 'down'),
    Word.from_string_and_init_pos('PRIN', (5, -7), 'down'),
]

results = test_Board.play_game(test_Game)

print(results)

#%% 

test_Board.draw()   

# %%
test_Stack = Stack()
test_Stack.set_execute_list(results)
test_Stack.execute()
print(test_Stack.stack)
# %%

# %%

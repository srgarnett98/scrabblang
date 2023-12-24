Scrabble Esolang

An esoteric lnguage, interpreted in python where a program is a valid game of scrabble.

Potentially strict and less strict programs, one where the program msut fit on a valid scrabble board and use only the tiles available in one scrabble bag.


Usage

The Stack!

The way this program works is it manipulates an extendeable array of ints. It also keeps track of a index that it is currently pointing at. Most operations will either move the pointer ("NEXT"/"PREV") or perform some operation on the int currently pointed at. The "NEXT" command will create a new value of 0 if it is moving into empty space.

Commands

(when i say stack[pointer] i mean the value element of the stack that the pointer is currently on)

"NEXT": increments the pointer by 1. Appends a 0 value and moves there if it was already at the end of the stack.
"PREV": decrements the pointer by 1. Raises an error if it would crash into the start. I could make it also preppend a value to the stack, but I didnt!

"SET": Sets stack[pointer] to the score that this word made.
"REMOVE": Sets stack[pointer] to 0

"ADD": Adds the score that this word made to stack[pointer]
"MINUS": Subtracts the score that this word made from stack[pointer] (stack[pointer] - score)
"TIMES": Multiplies stack[pointer] by the score that this word made
"DIVIDE": Divides stack[pointer] by the score that this word made. python // divide
"MODULO": Modulo's stack[pointer] by the score that this word made. python %

"REPEAT": Repeats the last <score> words, with the same scores. This includes words that have no function.

"IF": If stack[pointer] == 0, then the program will not perform operations until it reaches the next "ENDIF". Technically if(stack[pointer] == 0): if_depth += 1. If if_depth >0, most commands dont function.
"ENDIF": Ends the top if level. Should act as a closing bracket to the if. No clue what behaviour is if you've done some repeats. Not my problem. Technically this decrements the if_depth.

"PRINT": Prints the stack as [chr(x) for x in stack]

Code Usage

```python
from board import Board, Word
from stack_manip import Stack

# create a board instance to play words on
board = Board()

words_to_be_played = [
    Word1, Word2.... # a word is a list of letters and list of positions
]

# results is a list of (Word, score)
results = board.play_game(words_to_be_played)

stack = Stack()

# results is already in the correct format to generate a list of commands
stack.set_execute_list(results)
stack.execute()
```

To Be Implemented

-Checks for scrabble validity

Currently the program just lets you place letters in any straight line, disjointed or w/e. Would be nice to make sure that they are a continuous line on the board.

It also doesnt check that all words made are valid in the scrabble disctionary (or a valid scrabble-esolang function name).

-Checks for ordering

In the case that a word makes 2 or more valid words, the current ordering is left-right words in some order, then up-down words in some order. This could make a program possibly unpredicteable when writing since the "some order" may depend on the order of the letters in the word passed to it
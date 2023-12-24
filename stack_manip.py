# %%
import numpy as np

from board import Word

from typing import Callable


# %%
class Stack(object):
    def __init__(self):
        self.stack: list[int] = [0]
        self.pointer: int = 0
        self.if_depth: int = 0

        self.execute_list: list[tuple[Word, int]] = []
        self.execute_list_pointer: int = 0

    def __repr__(self):
        return [str(x) for x in self.stack].__repr__()

    def set_execute_list(self, words: list[tuple[Word, int]]):
        self.execute_list = words

    def _execute_single(self, word: Word, score_arg: int):
        string_to_execute = "".join([x.blank_override if x.char == ' ' else x.char for x in word.letters])
        # print(string_to_execute + " with score_arg:" + str(score_arg))
        func = self._get_func(string_to_execute)
        func(score_arg)

    def execute(self):
        while self.execute_list_pointer < len(self.execute_list):
            word, score_arg = self.execute_list[self.execute_list_pointer]
            self._execute_single(word, score_arg)
            self.execute_list_pointer += 1

        self.execute_list_pointer = 0

    def _get_func(self, string: str) -> Callable:
        func_dict = {
            "PRINT": self._print,
            "NEXT": self._next,
            "PREV": self._prev,
            "SET": self._set,
            "REMOVE": self._remove,
            "ADD": self._add,
            "MINUS": self._minus,
            "TIMES": self._times,
            "DIVIDE": self._divide,
            "MODULO": self._modulo,
            "REPEAT": self._repeat,
            "IF": self._if,
            "ENDIF": self._endif,
        }
        if string in func_dict:
            return func_dict[string]
        else:
            return self._unknown

    def if_decorator(func):
        def inner(*args, **kwargs):
            if args[0].if_depth == 0:
                func(*args, **kwargs)

        return inner

    @if_decorator
    def _print(self, score_arg: int = None):
        print("".join([chr(x) for x in self.stack]))

    @if_decorator
    def _unknown(self, score_arg: int = None):
        pass

    @if_decorator
    def _next(self, score_arg: int = None):
        # score arg does nothing
        if self.pointer == len(self.stack) - 1:
            self.stack.append(0)
        self.pointer += 1

    @if_decorator
    def _prev(self, score_arg: int = None):
        # score arg does nothing
        if self.pointer == 0:
            raise IndexError("Pointer is at 0: cannot decrement")
        self.pointer -= 1

    @if_decorator
    def _set(self, score_arg: int):
        self.stack[self.pointer] = score_arg

    @if_decorator
    def _remove(self, score_arg: int = None):
        self.stack[self.pointer] = 0

    @if_decorator
    def _add(self, score_arg: int):
        self.stack[self.pointer] += score_arg

    @if_decorator
    def _minus(self, score_arg: int):
        self.stack[self.pointer] -= score_arg

    @if_decorator
    def _times(self, score_arg: int):
        self.stack[self.pointer] *= score_arg

    @if_decorator
    def _divide(self, score_arg: int):
        self.stack[self.pointer] = self.stack[self.pointer] // score_arg

    @if_decorator
    def _modulo(self, score_arg: int):
        self.stack[self.pointer] = self.stack[self.pointer] % score_arg

    @if_decorator
    def _repeat(self, score_arg: int):
        if self.execute_list_pointer < score_arg:
            raise IndexError("Repeat goes too far back")
        self.execute_list_pointer -= score_arg

    def _if(self, score_arg: int = None):
        if not self.stack[self.pointer] or self.if_depth > 0:
            self.if_depth += 1

    def _endif(self, score_arg: int = None):
        if self.if_depth > 0:
            self.if_depth -= 1


# %%

if __name__ == "__main__":
    test_Stack = Stack()
    test_Stack.stack = [104, 101, 108, 108, 111]

    test_Stack._execute_single(Word.init_dummy("ADD"), 24)

    test_Stack._print()

    # %%

    test_word_list = [
        (Word.init_dummy("Minus"), 103),
        (Word.init_dummy("IF"), 0),
        (Word.init_dummy("Minus"), 1),
        (Word.init_dummy("if"), 35),
        (Word.init_dummy("add"), 25),
        (Word.init_dummy("endif"), 14),
        (Word.init_dummy("add"), 24),
        (Word.init_dummy("endif"), 4),
        (Word.init_dummy("add"), 7),
    ]

    test_Stack.set_execute_list(test_word_list)
    test_Stack.execute()

    test_Stack._print()
    print(test_Stack)
# %%

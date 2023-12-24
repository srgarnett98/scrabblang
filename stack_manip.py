# %%
import numpy as np

#%%
class Stack(object):

    def __init__(self):
        self.stack: list[int] = [0]
        self.pointer: int = 0
        self.if_depth:int = 0

        self.execute_list: list[function] = []
        self.execute_list_pointer: int = 0
    
    def __repr__(self):
        return [str(x) for x in self.stack].__repr__()
    
    def if_decorator(func):
        def inner(*args, **kwargs):
            if args[0].if_depth == 0:
                func(*args, **kwargs)
        return inner

    def print(self):
        print(''.join([chr(x) for x in self.stack]))
    
    @if_decorator
    def _unknown(self, score_arg:int = None):
        pass

    @if_decorator
    def _next(self, score_arg:int = None):
        # score arg does nothing
        if self.pointer == len(self.stack):
            self.stack.append(0)
        self.pointer += 1

    @if_decorator
    def _prev(self, score_arg:int = None):
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
    def _minus(self, score_arg:int):
        self.stack[self.pointer] -= score_arg

    @if_decorator
    def _times(self, score_arg:int):
        self.stack[self.pointer] *= score_arg
    
    @if_decorator
    def _divide(self, score_arg:int):
        self.stack[self.pointer] = self.stack[self.pointer] // score_arg

    @if_decorator
    def _modulo(self, score_arg:int):
        self.stack[self.pointer] = self.stack[self.pointer] % score_arg

    @if_decorator
    def _repeat(self, score_arg:int):
        if self.execute_list_pointer < score_arg:
            raise IndexError("Repeat goes too far back")
        self.execute_list_pointer -= score_arg

    def _if(self, score_arg:int = None):
        if not self.stack[self.pointer] or self.if_depth > 0:
            self.if_depth += 1

    def _endif(self, score_arg:int = None):
        if self.if_depth > 0:
            self.if_depth -= 1
# %%
        
test_Stack = Stack()
test_Stack.stack = [104, 101, 108, 108, 111]

test_Stack._minus(103)
test_Stack._if()
test_Stack._minus(1)
test_Stack._if()
test_Stack._add(25)
test_Stack._endif()
test_Stack._add(24)
test_Stack._endif()
test_Stack._add(7)

test_Stack.print()
print(test_Stack)
# %%

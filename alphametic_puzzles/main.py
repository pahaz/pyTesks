# -*- encoding: utf-8 -*-
from itertools import permutations, cycle
from Tools.Scripts.ftpmirror import raw_input
import re

__author__ = 'pahaz'

if __name__ == "__main__":
    while True:
        puzzle = raw_input("puzzle> ")
        if not puzzle: break

        puzzle = re.sub(r'\s', '', puzzle).replace('=', '==')
        variables = set(puzzle) - set("=-+*")
        invalid_replaces_for_zero = set(re.findall(r'\b(\w)', puzzle))

        is_solved = False
        for permutation in permutations(map(str, range(10)), len(variables)):
            test_puzzle = puzzle
            has_invalid_replaces = False
            for v, n in zip(variables, permutation):
                if n == '0' and v in invalid_replaces_for_zero:
                    has_invalid_replaces = True
                    break
                test_puzzle = test_puzzle.replace(v, n)

            if not has_invalid_replaces and eval(test_puzzle):
                is_solved = True
                print(puzzle, 'is', test_puzzle)

        if not is_solved:
            print(puzzle, 'can not be solved')

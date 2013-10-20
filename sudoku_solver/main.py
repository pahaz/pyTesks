# -*- encoding: utf-8 -*-

__author__ = 'pahaz'
import math
import random


def read_sudoku(_in):
    with open(_in) as f:
        lines = [map(int, list(x.strip('\n'))) for x in f.readlines() if x]
    return [item for line in lines for item in line]


def write_sudoku(_out, arr):
    with open(_out, 'w') as _out:
        for i, x in enumerate(arr):
            _out.write(str(x))
            if i % 9 == 8:
                _out.write('\n')


class Sudoku(object):
    def __init__(self, arr):
        self.__array = arr
        self.__size = int(math.sqrt(len(arr)))
        self.__cube_size = int(math.sqrt(self.__size))
        self.__res = []

    def varints_for(self, _array_, at_index):
        variants_all = set(range(1, self.__size + 1))
        x, y = self.convert_index_to_position(at_index)
        cube = set(self.get_cube_from(_array_, at_index))
        coll = set(self.get_coll_from(_array_, x))
        row = set(self.get_row_from(_array_, y))
        return variants_all - cube - row - coll

    def convert_index_to_position(self, index):
        row, cell = divmod(index, self.__size)
        return cell, row

    def convert_position_to_index(self, pos):
        return pos[0] * self.__size + pos[1]

    def get_cube_position(self, val):
        if type(val) == int:
            val = self.convert_index_to_position(val)

        i, _ = divmod(val[0], self.__cube_size)
        j, _ = divmod(val[1], self.__cube_size)
        return j, i

    def get_cube_from(self, _array_, for_position_or_index):
        i, j = self.get_cube_position(for_position_or_index)
        kn = self.__cube_size
        return [_array_[self.convert_position_to_index((x, y))]
                for x in range(i * kn, i * kn + kn)
                for y in range(j * kn, j * kn + kn)]

    def get_row_from(self, _array_, at_row_index):
        return _array_[at_row_index * self.__size:(at_row_index + 1) * self.__size]

    def get_coll_from(self, _array_, at_coll_index):
        return [_array_[x] for x in range(at_coll_index, len(self.__array), self.__size)]

    def solve(self, raise_on_resolve=False, arr=None):
        if arr is None:
            arr = self.__array[:]

        arr = arr[:]
        var_counts = 0

        if 0 in arr:
            zero_index = arr.index(0)
            variants = self.varints_for(arr, zero_index)

            for x in variants:
                arr[zero_index] = x
                var_counts += self.solve(raise_on_resolve, arr)

            return var_counts
        else:
            self.__res.append(arr)
            if raise_on_resolve:
                raise StopIteration(arr)
            return 1

#8..........36......7..9.2...5...7.......457.....1...3...1....68..85...1..9....4..
#812753649943682175675491283154237896369845721287169534521974368438526917796318452
# in.txt example
"""
800000000
003600000
070090200
050007000
000045700
000100030
001000068
008500010
090000400
"""
if __name__ == "__main__":
    try:
        _in = read_sudoku('in.txt')
    except:
        arr = map(int, list('812753649943682175675491283154237896369845721287169534521974368438526917796318452'))

        # shuffle rows
        su = Sudoku(arr)
        rows = [[su.get_row_from(arr, i),
                su.get_row_from(arr, i+1),
                su.get_row_from(arr, i+2)] for i in range(0, 10, 3)]
        random.shuffle(rows)
        arr = [z for l in rows for x in l for z in x]

        mem, r = 0, 0
        while Sudoku(arr).solve() == 1:
            r = random.randrange(81)
            mem = arr[r]
            arr[r] = 0

        arr[r] = mem
        write_sudoku('in.txt', arr)
    else:
        sudoku = Sudoku(_in)
        try:
            count_rez = sudoku.solve(True)
        except StopIteration as e:
            arr = e.args[0]
            write_sudoku('out.txt', arr)

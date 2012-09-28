#!/usr/bin/env python
# Corey Goldberg - 2011-2012


"""
SST browser-bot that solves sudoku puzzles.

see: http://testutils.org/sst
"""


from sudoku import solve
from sst.actions import *


go_to('http://view.websudoku.com/?level=4')  # evil

grid_ids = ['f%s%s' % (row, col) for col in xrange(9)
    for row in xrange(9)]

grid = [get_element(id=id).get_attribute('value') or '.'
    for id in grid_ids]

solution = solve(grid)

for (id, val) in zip(grid_ids,
        (solution[k] for k in sorted(solution))):
    write_textfield(id, val, check=False, clear=False)

click_element(get_element(name='submit'))

assert_text_contains('message', 'Congratulations!')

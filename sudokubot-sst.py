#!/usr/bin/env python
# Corey Goldberg - 2011-2012


"""
SST browser-bot that solves sudoku puzzles.

see: http://testutils.org/sst
"""


from sst.actions import *
import sudoku


GAME_LEVEL = 4  # evil

go_to('http://view.websudoku.com/?level=%s' % GAME_LEVEL)
grid_ids = ['f%s%s' % (row, col) for col in xrange(9) for row in xrange(9)]
grid = [get_element(id=id).get_attribute('value') or '.' for id in grid_ids]
solution = sudoku.solve(grid)
solution_grid = (solution[k] for k in sorted(solution))
for id, val in zip(grid_ids, solution_grid):
    write_textfield(get_element(id=id), val, check=False, clear=False)
click_element(get_element(name='submit'))
assert_text_contains(get_element(id='message'), 'Congratulations!')

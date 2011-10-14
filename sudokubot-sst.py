#!/usr/bin/env python
# Corey Goldberg - 2011


"""
SST browser-bot that solves sudoku puzzles.

see: https://launchpad.net/selenium-simple-test
"""


from sst.actions import *
import _sudoku as sudoku


GAME_LEVEL = 4  # evil
NUM_GAMES = 2


def main():
    bot = SudokuBot(GAME_LEVEL)
    for _ in xrange(NUM_GAMES):
        print 'game #%d' % (bot.puzzles_solved + 1)
        bot.play()
        bot.display_solution()


class SudokuBot(object):
    def __init__(self, game_level=4):
        self.game_level = game_level
        self._puzzles_solved = 0
        self._solution = None
    
    @property
    def puzzles_solved(self):
        return self._puzzles_solved
        
    def play(self):
        goto('http://view.websudoku.com/?level=%s' % self.game_level)
        grid_ids = ['f%s%s' % (row, col) for col in xrange(9) for row in xrange(9)]
        grid = [get_element(id=id).get_attribute('value') or '.' for id in grid_ids]
        solution = sudoku.solve(grid)
        solution_grid = (solution[k] for k in sorted(solution))
        for id, val in zip(grid_ids, solution_grid):
            get_element(id=id).send_keys(val)
        element_click(get_element(name='submit'))
        assert 'Congratulations!' in get_element(id='message').text
        self._solution = solution
        self._puzzles_solved += 1
        
    def display_solution(self):
        if self._solution is None:
            raise Exception('no puzzles solved yet')
        else:
            sudoku.display(self._solution)

    
main()

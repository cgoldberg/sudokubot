#!/usr/bin/env python
# Corey Goldberg - 2011


"""selenium webdriver browser-bot that solves sudoku puzzles."""


import time
from selenium import webdriver
import _sudoku as sudoku


GAME_LEVEL = 4  # evil


def main():
    bot = SudokuBot(GAME_LEVEL, pause=2.0)
    while True:
        print 'game #%d' % (bot.puzzles_solved + 1)
        bot.play()
        bot.display_solution()
        print '----------------'


class SudokuBot(object):
    def __init__(self, game_level=4, pause=0.0):
        self.game_level = game_level
        self.pause = pause
        self._puzzles_solved = 0
        self._solution = None
    
    @property
    def puzzles_solved(self):
        return self._puzzles_solved
        
    def play(self):
        browser = webdriver.Firefox()
        browser.get('http://view.websudoku.com/?level=%s' % self.game_level)
        grid_ids = ['f%s%s' % (row, col) for col in xrange(9) for row in xrange(9)]       
        grid = [browser.find_element_by_id(id).get_attribute('value') or '.' for id in grid_ids]
        solution = sudoku.solve(grid)
        solution_grid = (solution[k] for k in sorted(solution))
        for id, val in zip(grid_ids, solution_grid):
            browser.find_element_by_id(id).send_keys(val)
        browser.find_element_by_name('submit').click()
        assert 'Congratulations!' in browser.find_element_by_id('message').text
        if self.pause:
            time.sleep(self.pause)
        browser.quit()
        self._solution = solution
        self._puzzles_solved += 1
        
    def display_solution(self):
        if self._solution is None:
            raise Exception('no puzzles solved yet')
        else:
            sudoku.display(self._solution)

    
if __name__ == '__main__':
    main()

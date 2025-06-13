#!/usr/bin/env python


import time

from selenium import webdriver
from selenium.webdriver.common.by import By

import sudoku


NUM_GAMES = 5  # number of games to play
GAME_LEVEL = 4  # evil
TIME_BETWEEN_GAMES = 2  # secs


def main():
    bot = SudokuBot()
    for i in range(NUM_GAMES):
        print(f"Playing game #{i + 1}")
        result = bot.play(level=GAME_LEVEL)
        print(result)
        print("----------------")
        time.sleep(TIME_BETWEEN_GAMES)
    bot.quit()
    print("Done")


class SudokuBot:

    def __init__(self):
        options = webdriver.ChromeOptions()
        options.add_argument("--disable-infobars")
        options.add_argument("--window-size=1200,800")
        self.driver = webdriver.Chrome(options=options)

    def play(self, level=4):
        self.driver.get(f"https://east.websudoku.com/?level={level}")
        grid_ids = [f"f{row}{col}" for col in range(9) for row in range(9)]
        grid = [
            self.driver.find_element(By.ID, id).get_attribute("value") or "."
            for id in grid_ids
        ]
        solution = sudoku.solve(grid)
        solution_grid = (solution[key] for key in sorted(solution.keys()))
        for id, value in zip(grid_ids, solution_grid):
            self.driver.find_element(By.ID, id).send_keys(value)
        self.driver.find_element(By.NAME, "submit").click()
        message = self.driver.find_element(By.ID, "message").text
        if "Congratulations!" in message:
            return message
        return "You Lost!"

    def quit(self):
        self.driver.quit()


if __name__ == "__main__":
    main()

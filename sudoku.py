#!/usr/bin/env python

"""
Solve Every Sudoku Puzzle
http://norvig.com/sudoku.html

Original code from:
    - https://github.com/norvig/pytudes/blob/main/py/sudoku.py
    - Copyright (c) 2010-2017 Peter Norvig
Modifications:
    - Copyright (c) 2025 Corey Goldberg
"""


import unittest
from itertools import chain


"""
Throughout this program we have:
    r is a row, e.g. 'A'
    c is a column, e.g. '3'
    s is a square, e.g. 'A3'
    d is a digit, e.g. '9'
    u is a unit, e.g. ['A1','B1','C1','D1','E1','F1','G1','H1','I1']
    grid is a grid, e.g. 81 non-blank chars, e.g. starting with '.18...7...
    values is a dict of possible values, e.g. {'A1':'12349', 'A2':'8', ...}
"""


def cross(A, B):
    """Cross product of elements in A and elements in B."""
    return [a + b for a in A for b in B]


digits = "123456789"
rows = "ABCDEFGHI"
cols = digits
squares = cross(rows, cols)
unitlist = (
    [cross(rows, c) for c in cols]
    + [cross(r, cols) for r in rows]
    + [cross(rs, cs) for rs in ("ABC", "DEF", "GHI") for cs in ("123", "456", "789")]
)
units = {s: [u for u in unitlist if s in u] for s in squares}
peers = {s: set(chain.from_iterable(units[s])) - {s} for s in squares}


################ Parse a Grid ################


def parse_grid(grid):
    """Convert grid to a dict of possible values, {square: digits}, or
    return False if a contradiction is detected."""
    # To start, every square can be any digit; then assign values from the grid
    values = {s: digits for s in squares}
    for s, d in grid_values(grid).items():
        if d in digits and not assign(values, s, d):
            return False  # Fail if we can't assign d to square s
    return values


def grid_values(grid):
    """Convert grid into a dict of {square: char} with '0' or '.' for empties."""
    chars = [c for c in grid if c in digits or c in "0."]
    if len(chars) != 81:
        print(grid, chars, len(chars))
    assert len(chars) == 81
    return dict(zip(squares, chars))


################ Constraint Propagation ################


def assign(values, s, d):
    """Eliminate all the other values (except d) from values[s] and propagate.
    Return values, except return False if a contradiction is detected."""
    other_values = values[s].replace(d, "")
    if all(eliminate(values, s, d2) for d2 in other_values):
        return values
    return False


def eliminate(values, s, d):
    """Eliminate d from values[s]; propagate when values or places <= 2.
    Return values, except return False if a contradiction is detected."""
    if d not in values[s]:
        return values  ## Already eliminated
    values[s] = values[s].replace(d, "")
    # If a square s is reduced to one value d2, then eliminate d2 from the peers
    if len(values[s]) == 0:
        return False  # Contradiction: removed last value
    elif len(values[s]) == 1:
        d2 = values[s]
        if not all(eliminate(values, s2, d2) for s2 in peers[s]):
            return False
    # If a unit u is reduced to only one place for a value d, then put it there
    for u in units[s]:
        dplaces = [s for s in u if d in values[s]]
        if len(dplaces) == 0:
            return False  # Contradiction: no place for this value
        elif len(dplaces) == 1:
            # d can only be in one place in unit; assign it there
            if not assign(values, dplaces[0], d):
                return False
    return values


################ Display as 2-D grid ################


def display(values):
    """Display these values as a 2-D grid."""
    width = 1 + max(len(values[s]) for s in squares)
    line = "+".join(["-" * (width * 3)] * 3)
    for r in rows:
        print(
            "".join(
                values[r + c].center(width) + ("|" if c in "36" else "") for c in cols
            )
        )
        if r in "CF":
            print(line)
    print()


################ Search ################


def solve(grid):
    return search(parse_grid(grid))


def search(values):
    """Using depth-first search and propagation, try all possible values."""
    if values is False:
        return False  # Failed earlier
    if all(len(values[s]) == 1 for s in squares):
        return values  # Solved!
    # Chose the unfilled square s with the fewest possibilities
    n, s = min((len(values[s]), s) for s in squares if len(values[s]) > 1)
    for d in values[s]:
        result = search(assign(values.copy(), s, d))
        if result:
            return result


################ Tests ################


class TestSudoku(unittest.TestCase):

    results = []

    @classmethod
    def tearDownClass(cls):
        total_solved = 0
        total_puzzles = 0
        for result in cls.results:
            total_solved += result[0]
            total_puzzles += result[1]
        print(f"\nSolved {total_solved} of {total_puzzles} puzzles")

    def solve_all(self, file_path):
        """Solve a sequence of grids from a file."""
        with open(file_path) as f:
            grids = f.readlines()
        results = [self.solve_grid(grid) for grid in grids]
        self.assertEqual(len(results), len(grids))
        self.results.append((sum(results), len(results)))

    def solve_grid(self, grid):
        """A puzzle is solved if each unit is a permutation of the digits 1 to 9."""
        values = solve(grid)

        def unitsolved(unit):
            return {values[s] for s in unit} == set(digits)

        return values is not False and all(unitsolved(unit) for unit in unitlist)

    def test_solve_easy(self):
        self.solve_all("test_files/sudoku-easy50.txt")

    def test_solve_hard(self):
        self.solve_all("test_files/sudoku-top95.txt")

    def test_solve_hardest(self):
        self.solve_all("test_files/sudoku-hardest.txt")

    def test_unit_square(self):
        self.assertEqual(len(squares), 81)

    def test_unit_unitlist(self):
        self.assertEqual(len(unitlist), 27)

    def test_unit_units(self):
        self.assertTrue(all(len(units[s]) == 3 for s in squares))
        self.assertEqual(
            units["C2"],
            [
                ["A2", "B2", "C2", "D2", "E2", "F2", "G2", "H2", "I2"],
                ["C1", "C2", "C3", "C4", "C5", "C6", "C7", "C8", "C9"],
                ["A1", "A2", "A3", "B1", "B2", "B3", "C1", "C2", "C3"],
            ],
        )

    def test_unit_peers(self):
        self.assertTrue(all(len(peers[s]) == 20 for s in squares))
        self.assertEqual(
            peers["C2"],
            {
                "A2",
                "B2",
                "D2",
                "E2",
                "F2",
                "G2",
                "H2",
                "I2",
                "C1",
                "C3",
                "C4",
                "C5",
                "C6",
                "C7",
                "C8",
                "C9",
                "A1",
                "A3",
                "B1",
                "B3",
            },
        )


if __name__ == "__main__":
    unittest.main(verbosity=2)

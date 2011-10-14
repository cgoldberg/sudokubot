=========
sudokubot
=========

selenium webdriver browser-bot that solves sudoku puzzles.

------------
Requirements
------------

 * Python 2.6+
 * Selenium WebDriver client bindings::
    
    pip install selenium
    
------------
Instructions
------------

pure Selenium WebDriver version::
    
    $ cd sudokubot
    $ python sudokubot.py

SST framework version.
copy `sudokubot-sst.py` and `_sudoku.py` to your SST `/tests` directory and invoke::

    $ cd selenium-simple-test
    $ ./sst-run sudokubot-sst

----
Info
----

 * http://seleniumhq.org/
 * https://launchpad.net/selenium-simple-test
 * http://www.websudoku.com/
 * http://norvig.com/sudoku.html
 * http://en.wikipedia.org/wiki/Sudoku

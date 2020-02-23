# Binairo

## Introduction

This is a Python program which automatically solves a [Binairo puzzle](https://www.puzzle-binairo.com/) by only completing cells whose values can be deduced definitely. No backtracking is required to solve any of the puzzles on this website.

More advanced algorithms can solve harder Binairo puzzles by reducing it to a [Boolean satisfiability problem](https://link.springer.com/content/pdf/10.1007/s11786-017-0322-4.pdf).

Here is a sample puzzle and its solution:
<p float="left">
  <img src="/images/binairo_unsolved.png" height="300" />
  <img src="/images/binairo_solved.png" height="300" />
</p>

## Instructions

This program requires the [PyAutoGUI library](https://pyautogui.readthedocs.io/en/latest/).

To run the program:
1. Position the terminal window over the web browser, leaving the puzzle board visible.
2. Upon receiving the terminal prompt, hover the cursor over the top left corner of the board.
3. Repeat with the bottom left corner.
4. Input the dimensions of the board, and the program will solve the puzzle from there.

# aoc - Advent of Code

This repository contains code written to solve problems present in the _Advent
of Code_-advent calendar.

## Python

Each year solved in Python has the structure
```
   20XX/
    |- helpers.py
    |- 1.py
    |- 2.py
    |- ...
    |- inputs/
    |   |- 1
    |   ...
    `- solutions/
        |- 1.json
        ...
```

Each day is solved in its own file, e.g. `5.py`, with inputs in `inputs/5` and solutions in an array in `solutions/5.json`. The problem gets solved by running
```sh
$ python3 5.py
Part 1: 1234
Part 2: 4576
```

The structure of each python file is basically as follows:
```python3
# 5.py
def solve(text):
    yield 1234
    yield 4576


if __name__ == "__main__":
    from helpers import main_template

    main_template("5", solve)
```
where the `main_template` from `helpers.py` handles all the things that are common between days, like reading the input/solution file, printing the `yield`ed results, and asserting equality.

This main-template accepts some useful options:
```man
$ python 5.py -h
usage: python3 5.py [-h] [--input INPUT] [--solution SOLUTION] [--timer] [--no-assert]

Solves the problems 1 and 2 from Advent of Code, day 5

options:
  -h, --help           show this help message and exit
  --input INPUT        Path to problem input
  --solution SOLUTION  Path to json-formatted problem solutions
  --timer              Print table of time taken for the two parts
  --no-assert          Do not assert that computed answer equals solution
  
Good luck!
```
These options are particularly handy when still creating the solution. For example,
```
$ python3 5.py --input /dev/null --no-assert --timer
Part 1: 
Part 2: 

                Day 5                 
--------------------------------------
Blocks: 2.002716064453125e-05
Part 1    73% - 1.4781951904296875e-05
Part 2    26% - 5.245208740234375e-06
--------------------------------------
```
Provides a dummy input-file, so test-input can be used without even creating the proper file; There is no assert, and that also removes the need to create a solutions file; There is a table of timer-statistics printed at the end.

## Notes to self

Cat a file with 4 spaces of indent, for easy pasting into e.g. Reddit:
```sh
$ cat filename | sed 's/^/    /'
```

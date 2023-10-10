# aoc - Advent of Code

This repository contains code written to solve problems present in the _Advent
of Code_-advent calendar.


## Problem input

The creator of Advent of Code has requested that participants not publish their
problem inputs. For this reason they are ignored in this repository, however
I store them locally in the folder `aoc-problems`, along with solutions:

```
./aoc-problems/
    |- 2015/
    |   |- 1/
    |   |   |- input
    |   |   '- solution.json
...
```

All files `solution.json` have the structure
```json
[
    "answer to problem 1",
    "answer to problem 2"
]
```


## Python

The `python` folder contains solutions written in Python, along with a runner
script `main.py`.

```
./python/
    |- main.py
    |- 2015/
    |   |- 1.py
    |   |- 2.py
    |   '...
    |- 2020/
    |   |- 1.py
...
```

The runner script can run a specific year-and-day problem, all days one year,
or all years. Each problem output gets compared against the stored solutions, unless the flag `-n/--no-assert` is specified. As an example:
```bash
$ ./main.py -y 2015 -d 1 -n -t
# AoC - Year 2015, Day 1: Not Quite Lisp
# Part 1: 232
# Part 2: 1783
# 
# AoC - Year 2015, Day 1: Not Quite Lisp 
# -----------------------------------------
# Blocks: 0.0005440711975097656
#   Part 1:    79% - 0.00043010711669921875
#   Part 2:    20% - 0.00011396408081054688
# -----------------------------------------
```

Each solution file `{day}.py` has the format

```python
"""Title of problem"""
from typing import Iterator


def solve(text: str) -> Iterator:
    yield None
    yield None
```

The `main.py` script expects to be able to import a method called `solve`
from each file, and that `solve` returns a generator of solutions to part 1 and 2.
Because the generator halts between each iteration, the different parts can be
timed.

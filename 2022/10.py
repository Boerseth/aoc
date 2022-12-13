def simulate(instructions):
    X = 1
    cycle = 0
    for instruction in instructions:
        for _ in range(len(instruction)):  # either ("noop") or ("addx", int)
            cycle += 1
            yield X, cycle, (cycle // 40) % 6, (cycle - 1) % 40
        if instruction[0] == "addx":
            X += int(instruction[1])


def solve(text):
    data = list(simulate(map(str.split, text.splitlines())))
    yield sum(X * cycle for X, cycle, *_ in data if cycle % 40 == 20)

    lit_pixels = {(row, col) for X, _, row, col in data if abs(X - col) <= 1}
    screen = [["#" if (r, c) in lit_pixels else " " for c in range(40)] for r in range(6)]
    yield "\n" + "\n".join("".join(line) for line in screen)


MESSAGE_1 = """
### ### #  # ##    #  # #  # ##  ### ###
#   #   #  # # #   #  # #  # # # #   #  
### ### ## # # #   ## # #  # # # ### ###
  # #   # ## # #   # ## #  # # # #     #
  # #   #  # # #   #  # #  # # # #     #
### ### #  # ##    #  #  ##  ##  ### ###"""[1:]
MESSAGE_2 = """
## #       #   ##        ##    ##   ##  
   #       #  #  #      #  #  #### #### 
  #  ###  #   ####  ##  #      #######  
  #  #    #   #  # #  # #       #####   
 #   #   #    #  # #  # #  #     ###    
 #   #   #    #  #  ##   ##       #     """[1:]
MESSAGE_3 = """
########################################
########################################
########################################
########################################
########################################
########################################"""[1:]


def create(message):
    message = "".join(message.split("\n"))
    X = 1


if __name__ == "__main__":
    from helpers import main_template

    main_template("10", solve)

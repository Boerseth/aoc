def solve(text):
    # Find communicator message start position (len(unique) == 4) and stop (== 14)
    yield next(i for i in range(4, len(text)) if len(set(text[i - 4 : i])) == 4)
    yield next(i for i in range(14, len(text)) if len(set(text[i - 14 : i])) == 14)


if __name__ == "__main__":
    from helpers import main_template

    main_template("6", solve)

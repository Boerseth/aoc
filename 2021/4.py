def solve(text):
    lines = text.splitlines()
    bingo_numbers = [int(num) for num in lines.pop(0).split(",")]
    assert len(lines) % 6 == 0
    n_boards = len(lines) // 6
    bingo_boards = [
        [[int(num) for num in line.split()] for line in lines[6 * i + 1 : 6 * (i + 1)]]
        for i in range(n_boards)
    ]


    def has_won(board, called_numbers):
        return any(all(num in called_numbers for num in line) for line in [*board, *zip(*board)])


    def score(board, called_numbers, last_number):
        return last_number * sum(num for line in board for num in line if num not in called_numbers)


    # Part 1
    def find_score_of_first_bingo_winner(numbers, boards):
        called_numbers = set()
        for num in numbers:
            called_numbers.add(num)
            for board in boards:
                if has_won(board, called_numbers):
                    return score(board, called_numbers, num)
        return -1


    # Part 2
    def find_score_of_last_bingo_winner(numbers, boards):
        called_numbers = set()
        for num in numbers:
            called_numbers.add(num)
            if len(boards) == 1 and has_won(boards[0], called_numbers):
                return score(boards[0], called_numbers, num)
            boards = [board for board in boards if not has_won(board, called_numbers)]
        return -1


    # Recursively
    def find_score_of_first_bingo_winner_r(boards, called_numbers, remaining_numbers):
        if not remaining_numbers:
            return -1
        current_number = remaining_numbers[0]
        called_numbers.add(current_number)
        for board in boards:
            if has_won(board, called_numbers):
                return score(board, called_numbers, current_number)
        return find_score_of_first_bingo_winner_r(boards, called_numbers, remaining_numbers[1:])


    def find_score_of_last_bingo_winner_r(boards, called_numbers, remaining_numbers):
        if not remaining_numbers:
            return -1
        current_number = remaining_numbers[0]
        called_numbers.add(current_number)
        if len(boards) == 1 and has_won(boards[0], called_numbers):
            return score(boards[0], called_numbers, current_number)
        return find_score_of_last_bingo_winner_r(
            [b for b in boards if not has_won(b, called_numbers)], called_numbers, remaining_numbers[1:]
        )


    # Both in one, recursively
    def find_extreme_winning_score(boards, called_numbers, remaining_numbers, looking_for_first):
        if not remaining_numbers:
            return -1
        current_number = remaining_numbers[0]
        called_so_far = called_numbers | {current_number}

        # Valid check in both cases
        if len(boards) == 1 and has_won(boards[0], called_so_far):
            return score(boards[0], called_so_far, current_number)

        boards_next_round = []
        for board in boards:
            if has_won(board, called_so_far):
                if looking_for_first:
                    return score(board, called_so_far, current_number)
            else:
                boards_next_round.append(board)

        return find_extreme_winning_score(
            boards_next_round, called_so_far, remaining_numbers[1:], looking_for_first
        )

    yield find_extreme_winning_score(bingo_boards, set(), bingo_numbers, True)
    yield find_extreme_winning_score(bingo_boards, set(), bingo_numbers, False)


if __name__ == "__main__":
    from helpers import main_template

    main_template("4", solve)

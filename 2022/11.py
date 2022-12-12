def parse_monkey(monkey_text):
    lines = list(map(str.strip, monkey_text.splitlines()))
    return {
        "items": [int(i) for i in lines[1].split(": ")[1].split(", ")],
        "operation": eval(f"lambda old: {lines[2].split(' = ')[1]}"),
        "prime": int(lines[3].split()[-1]),
        "if_true": int(lines[4].split()[-1]),
        "if_false": int(lines[5].split()[-1]),
        "count": 0,
    }


def round(items, operation, prime, relief, big_divisor):
    if relief != 1:
        inspected_items = [operation(item) // relief for item in items]
    else:
        inspected_items = [operation(item) % big_divisor for item in items]
    destination_true = [i for i in inspected_items if not i % prime]
    destination_false = [i for i in inspected_items if i % prime]
    return destination_true, destination_false


def keep_away(monkeys, round_count, relief, big_divisor):
    for _ in range(round_count):
        for monkey in monkeys:
            destination_true, destination_false = round(
                monkey["items"], monkey["operation"], monkey["prime"], relief, big_divisor
            )
            monkey["count"] += len(monkey["items"])
            monkey["items"] = []
            monkeys[monkey["if_true"]]["items"] += destination_true
            monkeys[monkey["if_false"]]["items"] += destination_false


def multiply(factors):
    product = 1
    for factor in factors:
        product *= factor
    return product


def monkey_business(text, round_count, relief):
    monkeys = [parse_monkey(monkey_text) for monkey_text in text.split("\n\n")]
    big_divisor = multiply([monkey["prime"] for monkey in monkeys])
    keep_away(monkeys, round_count, relief, big_divisor)
    inspection_counts = sorted([monkey["count"] for monkey in monkeys], reverse=True)
    return inspection_counts[0] * inspection_counts[1]


def solve(text):
    yield monkey_business(text, 20, 3)
    yield monkey_business(text, 10_000, 1)


def solutions():
    yield 99840
    yield 20683044837


if __name__ == "__main__":
    from helpers import main_template

    with open(f"inputs/11", "r") as f:
        text = f.read()
    main_template(lambda: solve(text), solutions)

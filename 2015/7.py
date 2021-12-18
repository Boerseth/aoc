instructions = [line.strip().split(" -> ") for line in open("input_7", "r").readlines()]


# The keys of this dict are the wire-names, and its values will be their signal.
# Looping through the expressions, the dict will gradually fill up as we know
# more and more.
solved_circuit = {}


def solved(key):
    return key in solved_circuit


def store(key, value):
    if key in solved_circuit:
        pass
    solved_circuit[key] = value


def get_value(key):
    return solved_circuit[key]


def evaluate_1_element(element):
    if element.isdigit():
        return int(element)
    if solved(element):
        return get_value(element)
    return None


def evaluate_2_elements(operator, x):
    assert operator == "NOT"
    if x.isdigit():
        store(x, int(x))
    if solved(x):
        return ~ get_value(x)
    return None


def evaluate_3_elements(x, operator, y):
    assert operator in ["AND", "OR", "LSHIFT", "RSHIFT"]
    if x.isdigit():
        store(x, int(x))
    if y.isdigit():
        store(y, int(y))
    if not solved(x) or not solved(y):
        return None

    if operator == "AND":
        return get_value(x) & get_value(y)
    if operator == "OR":
        return get_value(x) | get_value(y)
    if operator == "LSHIFT":
        return (get_value(x) << int(y)) % 2 ** 16
    if operator == "RSHIFT":
        return (get_value(x) >> int(y)) % 2 ** 16
    return None



def try_to_evaluate(expression):
    expression_parts = expression.split()
    if len(expression_parts) == 1:
        return evaluate_1_element(expression)
    if len(expression_parts) == 2:
        return evaluate_2_elements(*expression_parts)
    assert len(expression_parts) == 3
    return evaluate_3_elements(*expression_parts)



# Part 1
while "a" not in solved_circuit:
    for expression, assigned in instructions:
        if not solved(assigned):
            if (value := try_to_evaluate(expression)) is not None:
                store(assigned, int(value) % 2 ** 16)
print("Part 1:", solved_circuit["a"])



# Part 2
solved_circuit = {"b": solved_circuit["a"]}
while "a" not in solved_circuit:
    for expression, assigned in instructions:
        if not solved(assigned):
            if (value := try_to_evaluate(expression)) is not None:
                store(assigned, int(value) % 2 ** 16)
print("Part 2:", solved_circuit["a"])

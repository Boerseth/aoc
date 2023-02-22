lsoc = [line.strip() for line in open("inputs/8", "r").readlines()]


def memory(line):
    assert line[0] == line[-1] == '"'
    line = line[1:-1]

    line = line.replace("\\\\", ".")

    i = 0
    while i < len(line):
        if line[i:i+2] == "\\x":
            line = line[:i] + "." + line[i+4:]
        i += 1

    line =  line.replace('\\"', ".")
    return line


illegal = {'"': '\\"', "\\": "\\\\"}


def escape(line):
    escaped_line = "".join(c if c not in illegal else illegal[c] for c in line)
    return f'"{escaped_line}"'


# Part 1:
print("Part 1:", sum(len(line) - memory(line) for line in lsoc))


# Part 2:
print("Part 2:", sum(len(escape(line)) - len(line) for line in lsoc))

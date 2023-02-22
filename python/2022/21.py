"""Monkey Math"""

def new_node(name):
    return {
        "name": name,
        "value": None,
        "parent": None,
        "children": None,
        "operator": None,
    }


def apply_operator(operator, values):
    return int(eval(f"{values[0]} {operator} {values[1]}"))


def set_node_value(tree, node_id):
    node = tree[node_id]
    if value := node["value"]:
        return
    for child in node["children"]:
        set_node_value(tree, child)
    child_values = [tree[child_id]["value"] for child_id in node["children"]]
    value = apply_operator(node["operator"], child_values)
    node["value"] = value


def parse(text):
    tree = {}

    lines = [l.split(": ") for l in text.splitlines()]
    for line in text.splitlines():
        monkey, expression = line.split(": ")
        if monkey not in tree:
            tree[monkey] = new_node(monkey)

        words = [int(w) if w.isdigit() else w for w in expression.split()]
        match words:
            case [number]:
                tree[monkey]["value"] = number
            case monkey1, operator, monkey2:
                tree[monkey]["children"] = [monkey1, monkey2]
                tree[monkey]["operator"] = operator
                for child in tree[monkey]["children"]:
                    if child not in tree:
                        tree[child] = new_node(child)
                    tree[child]["parent"] = monkey
    # Might as well populate right away:
    set_node_value(tree, "root")
    return tree


def invert_relation(old_operator, old_parent, old_children, new_parent):
    assert new_parent in old_children
    other_child = next(c for c in old_children if c != new_parent)

    # FIXME: Terribly hacky; Set root value to 1 and do this:
    if "root" == old_parent:
        return "*", ["root", other_child]

    if old_operator == "+":
        return "-", [old_parent, other_child]
    if old_operator == "*":
        return "/", [old_parent, other_child]
    if old_operator == "-":
        new_operator = "+" if old_children.index(new_parent) == 0 else "-"
        return new_operator, [other_child, old_parent]
    # old_operator == "/"
    new_operator = "*" if old_children.index(new_parent) == 0 else "/"
    return new_operator, [other_child, old_parent]


def pivot_around_node(tree, node_id):
    old_node = tree[node_id]
    if old_node["parent"] is None:
        assert old_node["name"] == "root"
        old_node["value"] = 1
        for old_child in old_node["children"]:
            if node_id in tree[old_child]["children"]:
                old_node["parent"] = old_child
                return
        return
    old_parent_node = tree[old_node["parent"]]
    new_operator, new_children = invert_relation(
        old_parent_node["operator"],
        old_parent_node["name"],
        old_parent_node["children"],
        node_id,
    )

    new_parent = None
    if old_children := old_node["children"]:
        for child in old_children:
            if grandchildren := tree[child]["children"]:
                if node_id in grandchildren:
                    new_parent = child

    tree[node_id] = {
        "name": node_id,
        "value": None,
        "parent": new_parent,
        "children": new_children,
        "operator": new_operator,
    }

    pivot_around_node(tree, old_parent_node["name"])


def solve(text):
    # text = TEST_INPUT
    tree = parse(text)
    yield tree["root"]["value"]

    pivot_around_node(tree, "humn")
    set_node_value(tree, "humn")
    yield tree["humn"]["value"]

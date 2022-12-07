ROOT = "root"


class File:
    def __init__(self, _type: str, size: int, content: list) -> None:
        self.type = _type
        self.size = size
        self.content = content


def cd(current_path, change_directory):
    if change_directory == "/":
        return ROOT
    if change_directory == "..":
        return current_path[:current_path.rfind("/")]
    return f"{current_path}/{change_directory}"


def create_hierarchy(description):
    current_path = ""
    filesystem = {}

    for verb, noun, output in description:
        assert verb in ["cd", "ls"]

        if verb == "cd":
            assert not output
            current_path = cd(current_path, noun)
            if current_path not in filesystem:
                filesystem[current_path] = {
                    "type": "dir",
                    "size": 0,
                    "content": []
                }
        else:
            assert verb == "ls"
            assert noun is None
            for (spec, name) in output:
                path_of_object = f"{current_path}/{name}"
                filesystem[current_path]["content"].append(path_of_object)
                if spec == "dir":
                    filesystem[path_of_object] = {
                        "type": "dir",
                        "size": 0,
                        "content": []
                    }
                else:
                    assert spec.isdigit()
                    filesystem[path_of_object] = {
                        "type": "file",
                        "size": int(spec),
                        "content": None
                    }
    return filesystem



def solve():
    with open(f"inputs/7", "r") as f:
        text = f.read()

    description = []
    for line in text.splitlines():
        if line.startswith("$ cd "):
            description.append(("cd", line.split()[-1], []))
        elif line.startswith("$ ls"):
            description.append(("ls", None, []))
        else:
            spec, name = line.split()
            assert spec.startswith("dir") or spec.isdigit()
            description[-1][2].append((spec, name))

    filesystem = create_hierarchy(description)
    locations = sorted(filesystem.keys(), key=lambda f: len(f.split("/")), reverse=True)
    for location in locations:
        if filesystem[location]["type"] == "file":
            continue
        for content_loc in filesystem[location]["content"]:
            filesystem[location]["size"] += filesystem[content_loc]["size"]

    total_size_of_small_dirs = 0
    for loc, info in filesystem.items():
        if info["type"] == "dir" and info["size"] <= 100000:
            total_size_of_small_dirs += info["size"]
    yield total_size_of_small_dirs

    used_space = filesystem["root"]["size"]
    total_space = 70000000
    requirement = 30000000
    to_be_deleted = used_space - (total_space - requirement)
    directory_sizes = sorted(info["size"] for info in filesystem.values() if info["size"] >= to_be_deleted)
    yield directory_sizes[0]

    import json

    yield 0


def solutions():
    yield 0
    yield 0


if __name__ == "__main__":
    from helpers import main_template

    main_template(solve, solutions, with_assert=False)

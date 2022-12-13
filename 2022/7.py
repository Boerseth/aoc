ROOT = ""
DIR, FILE = "dir", "file"
SMALL_SIZE, TOTAL_SPACE, REQUIRED_SPACE = 100000, 70000000, 30000000


def cd(path, destination):
    if destination == "/":
        return ROOT
    if destination == "..":
        return path[:path.rfind("/")]
    return f"{path}/{destination}"


def new_content(spec: str) -> dict:
    if spec.isdigit():
        return {"type": FILE, "size": int(spec), "content": None}
    assert spec == DIR
    return {"type": DIR, "size": 0, "content": []}


def parse_input(text: str) -> dict[str, dict]:
    # directories initialised with size 0; computed afterwards
    filesystem = {ROOT: new_content(DIR)}
    path = ROOT
    for command, *output_lines in map(str.splitlines, text.split("\n$ ")):
        if command.startswith("cd "):
            path = cd(path, command[3:])
        if command.startswith("ls"):
            if path in filesystem and filesystem[path]["content"]:
                continue  # Already ls'd here
            for spec, name in map(str.split, output_lines):
                content_path = f"{path}/{name}"
                filesystem[content_path] = new_content(spec)
                filesystem[path]["content"].append(content_path)

    # populate directory sizes
    directory_paths = [p for p, info in filesystem.items() if info["type"] == DIR]
    for dir_path in sorted(directory_paths, key=lambda p: p.count("/"), reverse=True):
        for content_path in filesystem[dir_path]["content"]:
            filesystem[dir_path]["size"] += filesystem[content_path]["size"]

    return filesystem


def solve(text):
    filesystem = parse_input(text)

    directory_sizes = [d["size"] for d in filesystem.values() if d["type"] == DIR]
    yield sum(size for size in directory_sizes if size <= SMALL_SIZE)

    allowed_space = TOTAL_SPACE - REQUIRED_SPACE
    to_be_deleted = filesystem[ROOT]["size"] - allowed_space
    yield min(size for size in directory_sizes if size >= to_be_deleted)


if __name__ == "__main__":
    from helpers import main_template

    main_template("7", solve)

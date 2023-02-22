"""Trench Map"""

def neighbours(z):
    for dz in [-1 + 1j, 1j, 1 + 1j, -1, 0, 1, -1 - 1j, -1j, 1 - 1j]:
        yield z + dz


def solve(text):
    lines = [line.strip() for line in text.splitlines()]
    enhancer = [1 if c == "#" else 0 for c in lines[0]]

    def will_be_on(z, image, is_inverted):
        index = sum(2 ** (8 - i) for i, zn in enumerate(neighbours(z)) if (zn in image) != is_inverted)
        return bool(enhancer[index]) == is_inverted

    def enhance_infinite_flipper(image, N):
        image_is_inverted = False
        for _ in range(N):
            candidates = {z for c in image for z in neighbours(c)}
            image = {z for z in candidates if will_be_on(z, image, image_is_inverted)}
            image_is_inverted = not image_is_inverted
        return image

    image = {
        i + j * 1j
        for j, row in enumerate(lines[2:][::-1])
        for i, c in enumerate(row) if c == "#"
    }
    yield len(enhance_infinite_flipper(image, 2))
    yield len(enhance_infinite_flipper(image, 50))

"""
quit()


# Below is a solution for the test input, which did not require a flipping
# inversion of the pixel value from iteration to iteration


enhancer_string = (
    "..#.#..#####.#.#.#.###.##.....###.##.#..###.####..#####..#....#."
    ".#..##..###..######.###...####..#..#####..##..#.#####...##.#.#.."
    "#.##..#.#......#.###.######.###.####...#.##.##..#..#..#####....."
    "#.#....###..#.##......#.....#..#..#..##..#...##.######.####.####"
    ".#.#...#.......#..#.#.#...####.##.#......#..#...##.#.##..#...##."
    "#.##..###.#......#.#.......#.#.#.####.###.##...#.....####.#..#.."
    "#.##.#....##..#.####....##...##..#...#......#.#.......#.......##"
    "..####..#...#.#.#...##..#.#..###..#####........#..####......#..#"
)
image_chars = (
    "#..#.\n"
    "#....\n"
    "##..#\n"
    "..#..\n"
    "..###"
)

enhancer = [1 if c == "#" else 0 for c in enhancer_string]
lines = image_chars.splitlines()
image = {i + j * 1j for j, row in enumerate(lines[::-1]) for i, c in enumerate(row) if c == "#"}


def show_image(image):
    i_min = int(min(z.imag for z in image))
    i_max = int(max(z.imag for z in image))
    r_min = int(min(z.real for z in image))
    r_max = int(max(z.real for z in image))
    for i in reversed(list(range(i_min, i_max + 1))):
        for r in range(r_min, r_max + 1):
            print("#" if r + i * 1j in image else ".", end="")
        print()


def will_be_on(z, image):
    index = sum(2 ** (8 - i) for i, zn in enumerate(neighbours(z)) if zn in image)
    return bool(enhancer[index])


show_image(image)
candidates = {z for c in image for z in neighbours(c)}
image = {z for z in candidates if will_be_on(z, image)}
show_image(image)
candidates = {z for c in image for z in neighbours(c)}
image = {z for z in candidates if will_be_on(z, image)}
show_image(image)
"""

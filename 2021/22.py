def boxes_overlap(box_1, box_2):
    return not any(
        max1 <= min2 or max2 <= min1 for (min1, max1), (min2, max2) in zip(box_1, box_2)
    )


def shift_zip(sequence, n=1):
    return list(zip(sequence[:-n], sequence[n:]))


def chop_up_box(box, chop_box):
    if not boxes_overlap(box, chop_box):
        return [box]
    vals = [
        [vmin] + [v for v in vchop if vmin < v < vmax] + [vmax]
        for (vmin, vmax), vchop in zip(box, chop_box)
    ]
    return [
        (xx, yy, zz)
        for xx in shift_zip(vals[0])
        for yy in shift_zip(vals[1])
        for zz in shift_zip(vals[2])
    ]


def get_overlap(box_1, box_2):
    if not boxes_overlap(box_1, box_2):
        return None
    return [
        (max(min1, min2), min(max1, max2))
        for (min1, max1), (min2, max2) in zip(box_1, box_2)
    ]


def split_up_box_from_others(box, other_boxes):
    split_boxes = [box]
    matches = []
    for turn_on_or_off, other_box in other_boxes:
        overlap = get_overlap(box, other_box)
        if not overlap:
            continue
        matches.append((turn_on_or_off, other_box))
        split_boxes = [
            split
            for old_split in split_boxes
            for split in chop_up_box(old_split, overlap)
        ]
    return split_boxes, matches


def is_inside_other(small_box, other_box):
    return all(
        omin <= smin < smax <= omax
        for (smin, smax), (omin, omax) in zip(small_box, other_box)
    )


def get_volume(coords):
    (xmin, xmax), (ymin, ymax), (zmin, zmax) = coords
    return (xmax - xmin) * (ymax - ymin) * (zmax - zmin)


def sub_box_previous_setting(sub_box, previous_steps_reverse_order):
    for already_on, previous_box in previous_steps_reverse_order:
        if boxes_overlap(sub_box, previous_box):
            return already_on
    return None


def reboot_core(boxes):
    cores_flipped_on = 0
    for i, (turn_on_or_off, box) in enumerate(boxes):
        previous_steps_rev = list(reversed(boxes[:i]))
        sub_boxes, overlapping_previous_steps = split_up_box_from_others(box, previous_steps_rev)
        for sub_box in sub_boxes:
            previous_setting = sub_box_previous_setting(sub_box, overlapping_previous_steps)
            volume = get_volume(sub_box)
            if turn_on_or_off and not previous_setting:
                cores_flipped_on += volume
            if not turn_on_or_off and previous_setting:
                cores_flipped_on -= volume
    return cores_flipped_on


def parse_line(line):
    on_off, box_description = line.strip().split()
    (xmin, xmax), (ymin, ymax), (zmin, zmax) = [
        [int(e) for e in part.split("=")[1].split("..")]
        for part in box_description.split(",")
    ]
    # Add 1 to max to make intervals half-inclusive
    return on_off == "on", ((xmin, xmax + 1), (ymin, ymax + 1), (zmin, zmax + 1))


def solve(text):
    boxes = [parse_line(line) for line in text.strip().splitlines()]

    init_region = ((-50, 51), (-50, 51), (-50, 51))
    init_boxes = [(on_off, box) for on_off, box in boxes if is_inside_other(box, init_region)]

    yield reboot_core(init_boxes)
    yield reboot_core(boxes)



if __name__ == "__main__":
    from helpers import main_template

    main_template("22", solve)

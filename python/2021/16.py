"""Packet Decoder"""

SUM, PRD, MIN, MAX, VAL, GTH, LTH, EQL = range(8)


class BitFeed:
    def __init__(self, bits):
        self.bits = bits

    def get(self, n):
        out, self.bits = self.bits[:n], self.bits[n:]
        return out

    def all_zero(self):
        return all(b == "0" for b in self.bits)


def parse(bit_feed):
    version, packet_type = int(bit_feed.get(3), 2), int(bit_feed.get(3), 2)
    if packet_type == VAL:
        content_string = ""
        while bit_feed.get(1) == "1":
            content_string += bit_feed.get(4)
        content = int(content_string + bit_feed.get(4), 2)
    elif bit_feed.get(1) == "1":
        content = [parse(bit_feed) for _ in range(int(bit_feed.get(11), 2))]
    else:
        content = []
        sub_bit_feed = BitFeed(bit_feed.get(int(bit_feed.get(15), 2)))
        while not sub_bit_feed.all_zero():
            content.append(parse(sub_bit_feed))
    return version, packet_type, content


def collect_version_numbers(packet):
    version_number, _, content = packet
    if not isinstance(content, list):
        return [version_number]
    return [version_number] + [
        num for pack in content for num in collect_version_numbers(pack)
    ]


def evaluate(packet):
    _, packet_type, contents = packet
    if packet_type == VAL:
        return contents
    c = [evaluate(cont) for cont in contents]
    if packet_type in [SUM, MIN, MAX]:
        return {SUM: sum, MIN: min, MAX: max}[packet_type](c)
    return eval({PRD: "*", GTH: ">", LTH: "<", EQL: "=="}[packet_type].join(map(str, c)))


def solve(text):
    outer_packet = parse(BitFeed(f"{int(text.strip(), 16):>08b}"))
    yield sum(collect_version_numbers(outer_packet))
    yield evaluate(outer_packet)

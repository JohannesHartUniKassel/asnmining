class RangeMap:
    def __init__(self):
        self.range_map = {}

    def add_range(self, start, end, value):
        self.range_map[(start, end)] = value

    def get_value(self, key):
        for (start, end), value in self.range_map.items():
            if start <= key <= end:
                return value
        return None
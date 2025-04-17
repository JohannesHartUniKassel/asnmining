import csv
from range_map import RangeMap


def split_range(string):
    parts = string.split('-')
    if len(parts) == 1:
        return int(parts[0]), int(parts[0])
    else:
        return int(parts[0]), int(parts[1])
    
def extract_rir(string):
    return string.replace("Assigned by ", "")

def create_iana_index(iana_16_file, iana_32_file) -> RangeMap:
    iana_range_map = RangeMap()
    with open(iana_16_file, 'r') as f:
        reader = csv.reader(f)
        next(reader)
        for row in reader:
            range = split_range(row[0])
            iana_range_map.add_range(range[0], range[1], extract_rir(row[1]))
    with open(iana_32_file, 'r') as f:
        reader = csv.reader(f)
        next(reader)
        for row in reader:
            range = split_range(row[0])
            iana_range_map.add_range(range[0], range[1], extract_rir(row[1]))
    return iana_range_map
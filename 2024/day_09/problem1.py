"""
Advent of Code 2024
Day: 09
Problem: 01
Author: Nathan Rand
Date: 12.09.24
"""

_INPUT_FILE_NAME = "input.txt"


def _unpack_disk_map(disk_map: str):
    uncompressed_disk_map = []
    job_id = 0
    for place, digit in enumerate(disk_map):
        is_file = place % 2 == 0
        uncompressed_disk_map.extend(
            [job_id] * int(digit) if is_file else [None] * int(digit)
        )
        if is_file:
            job_id += 1

    return uncompressed_disk_map


def main():
    """Advent of Code - Day 09 - Part 01 [Disk Fragmenter]"""
    # Read in our disk map
    with open(_INPUT_FILE_NAME, "r", encoding="utf-8") as f:
        disk_map = f.read()

    # Create our uncompressed disk map
    # NOTE: this makes the assumption any job id still takes up a single block
    # if it depends on the length of the job id num, then idk... lol
    uncompressed_disk_map = _unpack_disk_map(disk_map)

    # March our two pointers towards the middle while tracking our sum
    front = 0
    back = len(uncompressed_disk_map) - 1
    filesystem_checksum = 0
    while front <= back:
        if uncompressed_disk_map[front] is not None:
            filesystem_checksum += front*uncompressed_disk_map[front]
            front += 1
        else:
            while uncompressed_disk_map[back] is None:
                back -= 1

            filesystem_checksum += front*uncompressed_disk_map[back]
            front += 1
            back -= 1

    # Output our result
    print(
        "The resulting filesystem checksum after performing the necessary "
        f"file compression is: {filesystem_checksum}"
    )


if __name__ == "__main__":
    main()

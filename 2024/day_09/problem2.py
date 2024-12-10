"""
Advent of Code 2024
Day: 09
Problem: 02
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
    """Advent of Code - Day 09 - Part 02 [Disk Fragmenter]"""
    # Read in our disk map
    with open(_INPUT_FILE_NAME, "r", encoding="utf-8") as f:
        disk_map = f.read()

    # Create our uncompressed disk map
    # NOTE: this makes the assumption any job id still takes up a single block
    # if it depends on the length of the job id num, then idk... lol
    uncompressed_disk_map = _unpack_disk_map(disk_map)

    # March our two pointers towards the middle while tracking our sum
    # NOTE: but now we need to move our files in chunks, or not at all
    front = 0
    back = len(uncompressed_disk_map) - 1
    filesystem_checksum = 0
    while front <= back:
        # If we are looking at files we can just march forward as our "front"
        # has no free space behind it
        if uncompressed_disk_map[front] is not None:
            filesystem_checksum += front*uncompressed_disk_map[front]
            front += 1
            continue

        # Now we are looking at free space, so we try to move the last file span
        # in our uncompressed memory forward if a large enough space exists

        # First, move our back pointer to the next span to track and determine its length
        while uncompressed_disk_map[back] is None:
            back -= 1

        file_size = 0
        job_id = uncompressed_disk_map[back]
        while uncompressed_disk_map[back] == job_id:
            file_size += 1
            back -= 1

        # Now march another front pointer forward to try and find space for it,
        # if found, move it there, otherwise, do nothing
        search_ptr = front
        running_space_size = 0
        while search_ptr <= back:
            if uncompressed_disk_map[search_ptr] is not None:
                search_ptr += 1
                running_space_size = 0
                continue

            running_space_size += 1
            # If we find our spot, perform the move and continue, otherwise, do nothing
            if running_space_size == file_size:
                uncompressed_disk_map[search_ptr -
                                      file_size+1:search_ptr+1] = [job_id] * file_size
                uncompressed_disk_map[back+1:back +
                                      file_size+1] = [None] * file_size
                break

            search_ptr += 1

    # At the end, add up all remaining stuff past the front pointer
    for i in range(front, len(uncompressed_disk_map)):
        if uncompressed_disk_map[i] is not None:
            filesystem_checksum += i*uncompressed_disk_map[i]

    test_sum = 0
    for i in range(0, len(uncompressed_disk_map)):
        if uncompressed_disk_map[i] is not None:
            test_sum += i*uncompressed_disk_map[i]
    print(test_sum)

    # Output our result
    print(
        "The resulting filesystem checksum after performing the necessary "
        f"file compression is: {filesystem_checksum}"
    )


if __name__ == "__main__":
    main()

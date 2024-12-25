"""
Advent of Code 2024
Day: 18
Problem: 02
Author: Nathan Rand
Date: 12.22.24
"""
_INPUT_FILE_NAME = "input.txt"
_NUM_BYTES_FALLEN = 1024
_MEMORY_BOUNDS = [0, 70]


def _get_neighboring_bytes(byte: tuple, bytes: set):
    possible_neighbor_bytes = [
        (byte[0] + 1, byte[1]),
        (byte[0] - 1, byte[1]),
        (byte[0], byte[1] + 1),
        (byte[0], byte[1] - 1),
        (byte[0] + 1, byte[1] + 1),
        (byte[0] + 1, byte[1] - 1),
        (byte[0] - 1, byte[1] + 1),
        (byte[0] - 1, byte[1] - 1)
    ]

    return [neighbor for neighbor in possible_neighbor_bytes if neighbor in bytes]


def main():
    """Advent of Code - Day 18 - Part 02 [RAM Run]"""
    # Read in our falling bytes file and grab only those that have fallen
    with open(_INPUT_FILE_NAME, "r", encoding="utf-8") as f:
        all_bytes = [
            tuple([int(pos) for pos in byte_str.split(",")])
            for byte_str in f.read().split("\n")
        ]

    bytes = set(all_bytes[:_NUM_BYTES_FALLEN])
    blocking_byte = None
    last_fallen_byte = all_bytes[_NUM_BYTES_FALLEN]
    next_byte_ptr = _NUM_BYTES_FALLEN
    while blocking_byte is None:
        # Get bytes along the bottom edge
        bytes_along_the_edge = [
            byte for byte in bytes if _MEMORY_BOUNDS[1] == byte[1]]

        for byte_along_edge in bytes_along_the_edge:
            byte_stack = [byte_along_edge]
            visited_bytes = set()
            while byte_stack:
                # Get currrent byte from the stack
                curr_byte = byte_stack.pop()
                if curr_byte in visited_bytes:
                    continue

                # Check if we are at the other wall from our DFS, if so,
                # then we form a blocking path and there is no more valid solution
                if curr_byte[0] == _MEMORY_BOUNDS[1]:
                    blocking_byte = last_fallen_byte
                    break

                # Add the current byte to the ones we have visited
                visited_bytes.add(curr_byte)

                # Get the neighboring bytes
                neighboring_bytes = _get_neighboring_bytes(curr_byte, bytes)

                unvisited_neighbors = [
                    neighbor for neighbor in neighboring_bytes
                    if neighbor not in visited_bytes
                ]

                byte_stack.extend(unvisited_neighbors)

            # If we have finally found our blocking byte, break out of the loop
            if blocking_byte:
                break

        next_byte_ptr += 1
        bytes.add(all_bytes[next_byte_ptr])
        last_fallen_byte = all_bytes[next_byte_ptr]

    print(
        f"The falling byte that makes it so there is no more valid "
        "paths through the North Pole Computer's memory space is "
        f"at position: {blocking_byte}"
    )


if __name__ == "__main__":
    main()

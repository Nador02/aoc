"""
Advent of Code 2023
Day: 10
Problem: 01
Author: Nathan Rand
Date: 09.18.2024
"""
from typing import List

_STARTING_CHAR = "S"

def _remove_invalid_locations(locations: tuple, x_max: int, y_max: int):
    valid_indices = []
    for i, location in enumerate(locations):
        if location[0] > x_max or location[0] < 0:
            continue
        elif location[1] > y_max or location[1] < 0:
            continue
        valid_indices.append(i)
    
    # Only add valid locations to our valid locations list and return that
    return [valid_location for i, valid_location in enumerate(locations) if i in valid_indices]

def get_surrounding_locations(location: tuple, x_max: int, y_max: int):
    surrounding_locations = [
        (location[0], location[1]+1),
        (location[0], location[1]-1),
        (location[0]+1, location[1]),
        (location[0]-1, location[1]),
    ]
    return _remove_invalid_locations(surrounding_locations, x_max, y_max)

        
def pipe_connections(pipe: str, location: tuple):
    """Takes in a pipe and returns the two locations it is pointing."""
    match pipe:
        case "|":
            return (location[0], location[1]-1),  (location[0], location[1]+1)
        case "-":
            return (location[0]-1, location[1]),  (location[0]+1, location[1])
        case "L":
            return (location[0]+1, location[1]),  (location[0], location[1]-1)
        case "J":
            return (location[0]-1, location[1]),  (location[0], location[1]-1)
        case "7":
            return (location[0]-1, location[1]),  (location[0], location[1]+1)
        case "F":
            return (location[0]+1, location[1]),  (location[0], location[1]+1)
        case ".":
            return None
        case default:
            raise ValueError(f"Incorrect pipe {pipe} provided.")

def get_pipe(pipe_map: List[List[str]], location: tuple):
    return pipe_map[location[1]][location[0]]

        
def main():
    with open("input.txt", "r") as f:
        # First read in our file data and define our left/right instructions
        pipe_map = f.read().split("\n")
    
    # Find our starting index
    start_idx = None
    for y, pipe_row in enumerate(pipe_map):
        if _STARTING_CHAR not in pipe_row:
            continue
        start_idx = (pipe_row.index(_STARTING_CHAR), y)
    x_max = len(pipe_map[0])-1
    y_max = len(pipe_map)-1

    # Determine our two pointers' initial locations
    surrounding_locations = get_surrounding_locations(start_idx, x_max, y_max)
    pointer_locations = []
    for location in surrounding_locations:
        connections = pipe_connections(get_pipe(pipe_map, location), location)

        # Check if a neighboring location is none, if so, continue
        if connections is None:
            continue
        
        # If a connection is our starting index, add to our pointer locations
        if start_idx in connections:
            pointer_locations.append(location)
    ptr1 = pointer_locations[0]
    ptr2 = pointer_locations[1]

    # March forward until our two pointers meet, when they do, this is the furthest distance
    distance = 1
    prev_ptr1 = start_idx
    prev_ptr2 = start_idx
    while ptr1 != ptr2:
        # March ptr1 forward
        ptr1_connections = pipe_connections(get_pipe(pipe_map, ptr1), ptr1)
        next_ptr1 = ptr1_connections[0] if ptr1_connections[0] != prev_ptr1 else ptr1_connections[1]
        prev_ptr1 = ptr1
        ptr1 = next_ptr1

        # March ptr2 forward
        ptr2_connections = pipe_connections(get_pipe(pipe_map, ptr2), ptr2)
        next_ptr2 = ptr2_connections[0] if ptr2_connections[0] != prev_ptr2 else ptr2_connections[1]
        prev_ptr2 = ptr2
        ptr2 = next_ptr2
    
        # Increment our distance
        distance += 1

    # Output the resulting distance
    print(f"The farthest pipe tile from the starting point in the loop is: {distance} tiles away")

if __name__ == "__main__":
    main() 
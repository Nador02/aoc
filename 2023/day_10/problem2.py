"""
Advent of Code 2023
Day: 10
Problem: 02
Author: Nathan Rand
Date: 09.21.2024
"""
from typing import List
import numpy as np

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

    ptr = pointer_locations[0]
    prev_ptr = start_idx
    end_ptr = pointer_locations[1]
    x_cords = [start_idx[0], ptr[0]]
    y_cords = [start_idx[1], ptr[1]]
    # March forward until our two pointers meet, when they do, this is the furthest distance
    while ptr != end_ptr:
        # March ptr forward
        ptr_connections = pipe_connections(get_pipe(pipe_map, ptr), ptr)
        next_ptr = ptr_connections[0] if ptr_connections[0] != prev_ptr else ptr_connections[1]
        prev_ptr = ptr
        ptr = next_ptr

        # Add to our cords
        x_cords.append(ptr[0])
        y_cords.append(ptr[1])
    
    # Append the original starting values for the shoelace formula
    x_cords.append(start_idx[0])
    y_cords.append(start_idx[1])

    # Create our 2x2 matrices and grab their determinant to get the resulting
    # area (A) from the shoelace formula by summing
    # (https://en.wikipedia.org/wiki/Shoelace_formula)
    A = 0
    for i in range(len(x_cords)-1):
        A += (y_cords[i+1]+y_cords[i])*(x_cords[i]-x_cords[i+1])
    A = abs(A/2)

    # Then we apply Pick's theorem to get the number of interior nodes
    # (https://en.wikipedia.org/wiki/Pick%27s_theorem)
    bordering_nodes = len(x_cords)-1
    interior = A-(bordering_nodes/2)+1

    # Output our result
    print(f"The number of enclosed points in the loop is: {int(interior)}")

if __name__ == "__main__":
    main() 
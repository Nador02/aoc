"""
Advent of Code 2023
Day: 08
Problem: 01
Author: Nathan Rand
Date: 08.17.2024
"""
import re

_MAP_NODE_PATTERN = r'[a-zA-Z]{3}'
_STARTING_NODE = "AAA"
_DESTINATION_NODE = "ZZZ"
        
def main():
    with open("input.txt", "r") as f:
        # First read in our file data and define our left/right instructions
        map_data = f.read().split("\n")
        instructions = list(map_data[0])

        # Next, make our map graph structure
        map_graph = {}
        for i in range(2, len(map_data)):
            node, neighbor1, neighbor2 = re.findall(_MAP_NODE_PATTERN, map_data[i])
            map_graph[node] = {
                "L": neighbor1,
                "R": neighbor2
            }
        
        # March through our graph based on our L/R instructions until we reach ZZZ, 
        # tracking each step we take in a counter
        step_count = 0
        instruction_ptr = 0
        current_node = _STARTING_NODE
        while current_node != _DESTINATION_NODE:
            # Go to our next node based on the current instruction
            instruction = instructions[instruction_ptr]
            current_node = map_graph[current_node][instruction]

            # Iterate on our step counter and instruction ptr and continue
            # NOTE: we make sure to loop our instruction ptr here if we require more steps
            # then we have provided instructions :)
            step_count += 1
            instruction_ptr = instruction_ptr + 1 if instruction_ptr < len(instructions)-1 else 0
            
        # Print out the resulting number of steps it took to reach the destination node
        print(f"It took a total of {step_count} steps to escape the haunted "
              "wasteland by reaching the destination node!")

if __name__ == "__main__":
    main() 
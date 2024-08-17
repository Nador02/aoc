"""
Advent of Code 2023
Day: 08
Problem: 02
Author: Nathan Rand
Date: 08.17.2024
"""
import re
import numpy as np

_MAP_NODE_PATTERN = r'[a-zA-Z\d]{3}' # <- add digits to our potential node IDs
_START_TRAILING_CHAR = "A"
_DESTINATION_TRAILING_CHAR = "Z"
        
def main():
    with open("input.txt", "r") as f:
        # First read in our file data and define our left/right instructions
        map_data = f.read().split("\n")
        instructions = list(map_data[0])

        # Next, make our map graph structure
        map_graph = {}
        current_nodes = []
        for i in range(2, len(map_data)):
            node, neighbor1, neighbor2 = re.findall(_MAP_NODE_PATTERN, map_data[i])
            map_graph[node] = {
                "L": neighbor1,
                "R": neighbor2
            }
            
            # Check if this is a starting node
            if node[-1] == _START_TRAILING_CHAR:
                current_nodes.append(node)

        # March through our graph based on our L/R instructions until we reach ZZZ, 
        # tracking each step we take in a counter
        step_count = 1
        instruction_ptr = 0
        cycles = {}
        completed_cycle_lengths = {}
        while len(completed_cycle_lengths.keys()) < len(current_nodes):
            # Determine our instruction (left or right) for this step
            instruction = instructions[instruction_ptr]

            # Go through all nodes and take a step
            next_nodes = []
            for node in current_nodes:
                next_node = map_graph[node][instruction]
                if next_node[-1] == _DESTINATION_TRAILING_CHAR:
                    if next_node in cycles and next_node not in completed_cycle_lengths:
                        completed_cycle_lengths[next_node] = step_count-cycles[next_node]
                    elif next_node not in cycles:
                        cycles[next_node] = step_count
                next_nodes.append(map_graph[node][instruction])

            current_nodes = next_nodes

            # Iterate on our step counter and instruction ptr and continue
            # NOTE: we make sure to loop our instruction ptr here if we require more steps
            # then we have provided instructions :)
            step_count += 1
            instruction_ptr = instruction_ptr + 1 if instruction_ptr < len(instructions)-1 else 0
        
        # Print out the resulting number of steps it took to reach the destination node
        print(f"It took a total of {np.lcm.reduce(list(completed_cycle_lengths.values()))} steps to escape the haunted "
              "wasteland by reaching the destination node!")

if __name__ == "__main__":
    main() 
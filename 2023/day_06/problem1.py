"""
Advent of Code 2023
Day: 06
Problem: 01
Author: Nathan Rand
Date: 08.11.2024
"""
import regex as re
import numpy as np

time_pressed = lambda total_time, dist: [(1/2)*(total_time-np.sqrt(total_time**2 - 4*dist)), (1/2)*(total_time+np.sqrt(total_time**2 - 4*dist))]


def main():
    with open("input.txt", "r") as f:
        # Extract our times and distance data
        times_string, distances_string = f.read().split("\n")
        times = [int(time) for time in re.findall(r"\d+", times_string)]
        distances = [int(distance) for distance in re.findall(r"\d+", distances_string)]

        # Iterate over each determining the number of possible ways to win
        # based on the derived quadratic equation
        num_ways_win = []
        for i in range(len(times)):
            times_pressed = time_pressed(times[i], distances[i])

            # Now bring our numbers up and down one to get the required one-millisecond increments that are closest
            # that would allow us to win
            winning_times_pressed = [np.floor(times_pressed[0])+1, np.ceil(times_pressed[1])-1]
            
            # Add their difference plus one (the number of ways to win for this quadratic function)
            # to the list and continue on to the next game time and distance
            num_ways_win.append(winning_times_pressed[1]-winning_times_pressed[0]+1)

        # Compute and display our result
        print(f"The number of ways to win for each case multiplied together equals: {int(np.prod(num_ways_win))}")

if __name__ == "__main__":
    main() 
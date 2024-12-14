"""
Advent of Code 2024
Day: 12
Problem: 02
Author: Nathan Rand
Date: 12.13.24
"""

_INPUT_FILE_NAME = "input.txt"


def _get_neighboring_plots_in_region(garden: dict, plot: tuple):
    plant = garden[plot]
    potential_neighbor_plots = [
        (plot[0]-1, plot[1]),
        (plot[0]+1, plot[1]),
        (plot[0], plot[1]-1),
        (plot[0], plot[1]+1),
    ]
    return [neighbor for neighbor in potential_neighbor_plots if garden.get(neighbor) == plant]


def _num_corners_at_plot(garden, plot):
    plant = garden[plot]
    num_corners = 0

    # Quadrant 4
    # ----------
    # Concave
    if garden.get((plot[0]+1, plot[1]+1)) != plant and garden.get((plot[0], plot[1]+1)) == plant and garden.get((plot[0]+1, plot[1])) == plant:
        num_corners += 1
    # Convex
    if garden.get((plot[0], plot[1]+1)) != plant and garden.get((plot[0]+1, plot[1])) != plant:
        num_corners += 1

    # Quadrant 1
    # ----------
    # Concave
    if garden.get((plot[0]-1, plot[1]+1)) != plant and garden.get((plot[0], plot[1]+1)) == plant and garden.get((plot[0]-1, plot[1])) == plant:
        num_corners += 1
    # Convex
    if garden.get((plot[0], plot[1]+1)) != plant and garden.get((plot[0]-1, plot[1])) != plant:
        num_corners += 1

    # Quadrant 3
    # ----------
    # Concave
    if garden.get((plot[0]+1, plot[1]-1)) != plant and garden.get((plot[0], plot[1]-1)) == plant and garden.get((plot[0]+1, plot[1])) == plant:
        num_corners += 1
    # Convex
    if garden.get((plot[0], plot[1]-1)) != plant and garden.get((plot[0]+1, plot[1])) != plant:
        num_corners += 1

    # Quadrant 2
    # ----------
    # Concave
    if garden.get((plot[0]-1, plot[1]-1)) != plant and garden.get((plot[0], plot[1]-1)) == plant and garden.get((plot[0]-1, plot[1])) == plant:
        num_corners += 1
    # Convex
    if garden.get((plot[0], plot[1]-1)) != plant and garden.get((plot[0]-1, plot[1])) != plant:
        num_corners += 1

    return num_corners


def main():
    """Advent of Code - Day 12 - Part 02 [Garden Groups]"""
    # Read in our garden grid
    with open(_INPUT_FILE_NAME, "r", encoding="utf-8") as f:
        garden_grid = f.read().split("\n")

    # Load it into our default dict struct
    garden = {}
    for row, garden_plots in enumerate(garden_grid):
        for col, plant in enumerate(garden_plots):
            garden[(row, col)] = plant

    # For each plot in our garden, perform a BFS to determine all regions
    visited_plots = set()
    fencing_price = 0
    for (row, col), plant in garden.items():
        # If we have already visited this plot and added it to a region
        # move on to the next plot
        if (row, col) in visited_plots:
            continue

        # We have not visited this plot yet and its corresponding region
        # so do a BFS grabbing all neighboring plots that make up the region
        plot_queue = [(row, col)]
        area = 0
        sides = 0
        while plot_queue:
            # Get the next plot in the queue
            curr_plot = plot_queue.pop(0)

            # If we have already visited this plot, skip over it
            if curr_plot in visited_plots:
                continue

            # Grab neighboring plots that are in this region (same plant)
            # and then add them to our queue to be explored next
            neighbors_in_region = _get_neighboring_plots_in_region(
                garden,
                curr_plot
            )
            area += 1

            # Check if this is a corner, if so, add to our number of sides accordingly
            sides += _num_corners_at_plot(garden, curr_plot)

            # If this is an interior node, extend the queue and just continue
            plot_queue.extend(neighbors_in_region)
            visited_plots.add(curr_plot)

        fencing_price += area*sides

    # Output our result
    print(f"Total fencing price in our garden: {fencing_price}")


if __name__ == "__main__":
    main()

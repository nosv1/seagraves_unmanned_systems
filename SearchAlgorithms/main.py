from matplotlib.lines import Line2D
import matplotlib.pyplot as plt
import random

from Colors import Colors
from AStar import AStar
from RRT import RRT
from Scenario import Scenario

def main() -> None:
    scenario: Scenario = Scenario().loader(
        # "scenarios/AStar_10x10_bot-0o5_grid-0o5.json"
        # "scenarios/AStar_10x10_bot-0o5_grid-0o5_random.json"
        # "scenarios/AStar_50x50_bot-0o5_grid-0o5.json"
        # "scenarios/RRT_10x10_bot-0o5_grid-0o5.json"
        # "scenarios/RRT_10x10_bot-0o5_grid-0o5_random.json"
        "scenarios/RRT_50x50_bot-0o5_grid-0o5.json"
    )

    print("Setting up plot...")
    fig, ax = plt.subplots()
    fig.set_size_inches(8, 8)
    
    # set colors
    fig.patch.set_facecolor(Colors.grey)
    ax.set_facecolor(Colors.grey)
    ax.title.set_color(Colors.light_grey)
    ax.xaxis.label.set_color(Colors.light_grey)
    ax.yaxis.label.set_color(Colors.light_grey)

    # set axis labels
    ax.tick_params(axis='x', colors=Colors.light_grey)
    ax.tick_params(axis='y', colors=Colors.light_grey)

    # set title
    ax.set_title(
        f"{scenario.algorithm.__class__.__name__}\n"
        f"Time: TBD, Cost: TBD"
    )

    # set axis limits
    ax.set_xlim(
        scenario.grid.min_x - scenario.grid.grid_spacing * 2, 
        scenario.grid.max_x + scenario.grid.grid_spacing * 2
    )
    ax.set_ylim(
        scenario.grid.min_y - scenario.grid.grid_spacing * 2, 
        scenario.grid.max_y + scenario.grid.grid_spacing * 2
    )

    print("Plotting legend...")
    ax.legend(
        handles=[
            Line2D([0], [0], marker='o', markersize=10, color=Colors.red, lw=4, label="Obstacles"),
            Line2D([0], [0], marker='o', markersize=10, color=Colors.light_purple, lw=4, label="Open Set"),
            Line2D([0], [0], marker='o', markersize=10, color=Colors.light_grey, lw=4, label="Closed Set"),
            Line2D([0], [0], color=Colors.light_blue, lw=4, label="Path"),
            Line2D([0], [0], marker='o', markersize=10, color="g", lw=4, label="Start"),
            Line2D([0], [0], marker='o', markersize=10, color="r", lw=4, label="Goal"),
        ],
        fancybox=True,
        shadow=True,
        loc="upper right"
    )
    # print("Plotting obstacles")
    # scenario.plot_obstacles(ax, Colors.red)
    print("Plotting nodes...")
    scenario.plot_nodes(ax, invalid_nodes=True, valid_nodes=False)
    print("Plotting start and goal...")
    scenario.plot_start_and_goal(ax)

    while True:
        try:
            print("Finding path...")
            scenario.algorithm.stopwatch.start()
            scenario.algorithm.find_path(ax)
            scenario.algorithm.stopwatch.stop()
            print(f"Path found... Time: {scenario.algorithm.stopwatch.elapsed_time:.5f}s")
            break
        except ValueError:
            print("No path found...")
            main()

    # set title
    ax.set_title(
        f"{scenario.algorithm.__class__.__name__}\n"
        f"Time: {scenario.algorithm.stopwatch.elapsed_time:.2f}s, Cost: {scenario.algorithm._path[0].total_cost:.2f}"
    )

    print("Plotting open set...")
    scenario.plot_open_set(ax, color=Colors.light_purple)
    print("Plotting closed set...")
    scenario.plot_closed_set(ax, Colors.light_grey)
    print("Plotting path...")
    scenario.plot_path(ax, Colors.light_blue)

    print("Showing plot...")
    plt.pause(100)

if __name__ == "__main__":
    main()
# Simply uncomment a scenario at the top of main() and run it.
# Scenario's are loaded via ./Scenario.Scenario.loader()

import copy
from matplotlib.lines import Line2D
import matplotlib.pyplot as plt

from Colors import Colors
from Scenario import Scenario
from Stopwatch import Stopwatch

def main() -> None:
    scenario: Scenario = Scenario().loader(
        #####  the naming structure for scenarios  #####
        # "scenarios / SearchType _ grid-size _ bot-size _ grid-spacing.json"
        # "scenarios/AStar_10x10_bot-0o5_grid-0o5.json"  --> -->
        # "scenarios / AStar _ 10x10 grid _ bot radius 0.5 _ grid spacing 0.5"
        # if 'random' is at the end, then random start/goal pos and/or obstacle pos
        #####

        #####  scenarios in the "scenarios" folder  #####
        # "scenarios/AStar_10x10_bot-0o5_grid-0o5.json"
        # "scenarios/AStar_10x10_bot-0o5_grid-0o5_random.json"
        # "scenarios/AStar_15x15_bot-0o5_grid-0o5a.json"       # Exam2 Problem 3
        "scenarios/AStar_15x15_bot-0o5_grid-0o5b.json"       # Exam2 Problem 4
        # "scenarios/AStar_15x15_bot-0o5_grid-1o0.json"        # HW5 problem 1a
        # "scenarios/AStar_50x50_bot-0o5_grid-0o5.json"        # HW3 problem 2
        # "scenarios/AStar_50x50_bot-0o5_grid-0o5_random.json"
        # "scenarios/Dijkstra_15x15_bot-0o5_grid-1o0.json"     # HW5 problem 1b
        # "scenarios/RRT_10x10_bot-0o5_grid-0o5.json"
        # "scenarios/RRT_10x10_bot-0o5_grid-0o5_random.json"
        # "scenarios/RRT_15x15_bot-0o5_grid-1o0.json"          # HW5 problem 1c
        # "scenarios/RRT_50x50_bot-0o5_grid-0o5.json"          # HW3 problem 3
        #####
    )

    # we setup the plot before we find the path for debugging - if we want to 
    # plot while the algorithm is running.
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
        loc="upper right",
        bbox_to_anchor=(1.125, 1.0)
    )

    from Node import Node
    # nodes = [  # problem 3
    #     Node(0,0),
    #     Node(9,4),
    #     Node(4,4),
    #     Node(1,9),
    #     Node(9,7),
    #     Node(6,14)
    # ]
    nodes = [  # problem 4 and 5
        Node(1,1),
        Node(9,7),
        Node(1,9),
        Node(4,4),
        Node(9,4),
        Node(6,14),
        Node(3,11),
        Node(14,1),
        Node(1,14),
        Node(14,14),
        Node(7,10)
    ]

    cost_matrix: dict[str, dict[str, float]] = {}
    path_matrix: dict[str, dict[str, list[Node]]] = {}
    
    stopwatch = Stopwatch()
    stopwatch.start()
    for i, start in enumerate(nodes):
        for j, goal in enumerate(nodes):
            if i == j:
                continue
            scenario.algorithm.reset()
            start.reset()
            goal.reset()
            scenario.algorithm.start = start
            scenario.algorithm.goal = goal
            scenario.algorithm.find_path()
            cost_matrix[start.id, goal.id] = scenario.algorithm.path[0].total_cost
            path_matrix[start.id, goal.id] = scenario.algorithm.path

    from itertools import permutations
    goals_permutations = list(permutations(nodes[1:]))
    print(f"Number of permutations: {len(goals_permutations)}")
    
    scenario_paths = []
    min_cost = float('inf')
    for i, permutation in enumerate(goals_permutations):
        # print(f"Permutation {i+1}/{len(goals_permutations)}", end="\r")
        
        total_cost = 0
        start = nodes[0]
        paths = []

        for goal in permutation:
            cost = cost_matrix[start.id, goal.id]
            total_cost += cost
            paths.append((start, goal, path_matrix[start.id, goal.id]))
            start = goal
        total_cost += cost_matrix[scenario.start.id, permutation[0].id]

        if total_cost < min_cost:
            min_cost = total_cost
            scenario_paths = paths
    stopwatch.stop()

    for i, (start, goal, path) in enumerate(scenario_paths):
        scenario.start = start
        scenario.goal = goal
        scenario.algorithm._path = path
        # print("Plotting obstacles")
        # scenario.plot_obstacles(ax, Colors.red)
        print("Plotting nodes...")
        scenario.plot_nodes(ax, invalid_nodes=True, valid_nodes=False)

        print("Plotting start and goal...")
        scenario.plot_start_and_goal(ax, i+1)

        # find a path
        # if we use random start/goal, we make sure they're are valid, otherwise we
        # try again. We also try again if the path fails or is not long enough to be 
        # interesting - at the time of writing this, the path must be 2/3 of the 
        # width of the grid.
        # while True:
        #     if (
        #         (scenario.has_random_start or scenario.has_random_goal) and 
        #         scenario.start.distance_to(scenario.goal) < scenario.grid.max_x / 1.5
        #     ):
        #         print("Start and goal not interesting enough... Regenerating...")
        #         plt.close()
        #         main()
        #         return

        #     try:
        #         print("Finding path...")
        #         scenario.algorithm.stopwatch.start()
        #         scenario.algorithm.find_path()
        #         scenario.algorithm.stopwatch.stop()
        #         print(f"Path found... Time: {scenario.algorithm.stopwatch.elapsed_time:.5f}s")
        #         break

        #     except ValueError:
        #         print("No path found... Regenerating...")
        #         plt.close()
        #         main()
        #         return

        # set title
        ax.set_title(
            f"{scenario.algorithm.__class__.__name__}\n"
            # f"Time: {scenario.algorithm.stopwatch.elapsed_time:.3f}s, Cost: {scenario.algorithm._path[0].total_cost:.2f}"
            f"Time: {stopwatch.elapsed_time:.3f}s, Cost: {min_cost:.2f}"
        )

        # print("Plotting open set...")
        # scenario.plot_open_set(ax, color=Colors.light_purple)
        # print("Plotting closed set...")
        # scenario.plot_closed_set(ax, Colors.light_grey)
        print("Plotting path...")
        scenario.plot_path(ax, Colors.light_blue)

    print("Showing plot...")
    # using plt.pause for debugging, plt.show wasn't working when I was using
    # plt.pause within the algorithm classes
    plt.pause(1000)

if __name__ == "__main__":
    main()
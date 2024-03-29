import logging
import matplotlib.pyplot as plt
import matplotlib.patches as patches

from Node import Node
from Obstacle import Obstacle

class Grid:
    def __init__(self, 
        min_x: int,
        max_x: int,
        min_y: int,
        max_y: int, 
        grid_spacing: float, 
        obstacles: list[Obstacle]
    ) -> None:
        self.min_x = min_x
        self.max_x = max_x
        self.min_y = min_y
        self.max_y = max_y
        self.grid_spacing = grid_spacing
        self.obstacles = obstacles

        self._nodes: dict = self.get_nodes()
        
    ############################################################################

    def get_nodes(self) -> dict[str, Node]:
        """
        Creates a list of nodes in the grid
        """
        nodes: dict[str, Node] = {}
        for row in range(int(self.max_x / self.grid_spacing + 1)):
            for col in range(int(self.max_y / self.grid_spacing + 1)):
                node = Node(
                    x=col * self.grid_spacing,
                    y=row * self.grid_spacing,
                )
                node.parent_index = self.calculate_node_index(node.x, node.y)
                nodes[node._id] = node
        return nodes

    def calculate_node_index(self, x: float, y: float) -> int:
        """
        Calculates the index of a node in the grid
        
        :param x: x-coordinate of the node
        :param y: y-coordinate of the node
        :return: index of the node
        """
        # index = row_len * y + x
        return int(
            ((self.max_x / self.grid_spacing) + 1) *  # row len * 
            (y / self.grid_spacing) +                 # y +
            (x / self.grid_spacing)                   # x
        )

    def inflate_obstacles(self, inflation_amount: float):
        """
        Inflate every obstacle's radius by the inflation amount
        """
        for obstacle in self.obstacles:
            obstacle.radius += inflation_amount

    def inflate_bounds(self, inflation_amount: float):
        """
        Shrink the bounds of the grid by the shrink amount
        """
        self.min_x += inflation_amount
        self.max_x -= inflation_amount
        self.min_y += inflation_amount
        self.max_y -= inflation_amount

    ############################################################################
    # NODE VALIDITY

    def node_in_obstacle(self, position: Node) -> bool:
        """
        Checks if a position is in an obstacle
        :param position: position to check
        :return: True if in obstacle, False otherwise
        """
        return any(obstacle.is_colliding(position) for obstacle in self.obstacles)
        
    def node_in_bounds(self, position: Node) -> bool:
        """
        Checks if a position is in the bounds of the grid
        :param position: position to check
        :return: True if in bounds, False otherwise
        """
        return (
            position.x >= self.min_x and
            position.x <= self.max_x and
            position.y >= self.min_y and
            position.y <= self.max_y
        )

    def is_valid_node(self, position: Node) -> bool:
        """
        Checks if a position is valid
        :param position: position to check
        :return: True if valid, False otherwise
        """
        in_bounds = self.node_in_bounds(position)
        in_obstacle = self.node_in_obstacle(position)
        is_valid = in_bounds and not in_obstacle

        if not is_valid:
            if not in_bounds:
                logging.info(f":Node:Out of bounds: {position}")
            if in_obstacle:
                logging.info(f":Node:In obstacle: {position}")

        return is_valid

    def get_valid_nodes(self) -> list[Node]:
        """
        Returns a list of valid nodes
        """
        return [node for _id, node in self._nodes.items() if self.is_valid_node(node)]

    ############################################################################
    # PLOTTING
    
    def plot_obstacles(self, ax: plt.Axes, color: str) -> None:
        """
        Plots the obstacles in the grid
        :param ax: matplotlib axes to plot on
        :param color: color of the obstacles
        """
        for obstacle in self.obstacles:
            ax.add_artist(patches.Circle(
                (obstacle.x, obstacle.y),
                obstacle.radius,
                color=color,
                fill=True
            ))

    ############################################################################
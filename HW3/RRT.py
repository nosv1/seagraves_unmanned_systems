import random
import matplotlib.pyplot as plt

from Grid import Grid
from Node import Node
from Path import Path


class RRT(Path):
    def __init__(self, step_length: float, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.step_length = step_length

    def generate_random_node(self) -> Node:
        self._random_node = Node(
            x=random.uniform(self.grid.min_x, self.grid.max_x),
            y=random.uniform(self.grid.min_y, self.grid.max_y)
        )
        return self._random_node

    def step_towards_node(self, root: Node, node: Node) -> Node:
        distance: float = root.distance(node)
        return Node(
            x=root.x + self.step_length * (node.x - root.x) / distance,
            y=root.y + self.step_length * (node.y - root.y) / distance,
            start_to_node_cost=root.start_to_node_cost + self.step_length,
            parent=root
        )

    def find_closest_node(self, node: Node) -> Node:
        closest_node: Node = None
        closest_distance: float = float('inf')
        for n in self._open_set.values():
            distance: float = n.distance(node)
            if distance < closest_distance:
                closest_node = n
                closest_distance = distance
        return closest_node

    def find_path(self) -> None:
        while self._current_node.distance(self.goal) > self.step_length:
            while True:
                random_node: Node = self.generate_random_node()
                closest_node: Node = self.find_closest_node(random_node)
                self._current_node = self.step_towards_node(closest_node, random_node)
                if self.grid.is_valid_node(self._current_node):
                    self._open_set[self._current_node.id] = self._current_node
                    break
        self.goal.start_to_node_cost = (
            self._current_node.start_to_node_cost + 
            self._current_node.distance(self.goal)
        )
        self.goal.parent = self._current_node

        self._path = [self.goal]
        while self._path[-1].parent:
            self._path.append(self._path[-1].parent)
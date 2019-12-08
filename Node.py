
from stats import ROADS
import numpy as np
from collections import namedtuple

default_father = namedtuple('dummy_node', ['state'])


class Node:
    def __init__(self, junction, cost=0, acc_cost=0, father=default_father(np.inf)):
        self.state = junction
        self.cost = cost
        self.acc_cost = acc_cost
        self.father = father

    def equal(self, node):
        return self.state == node.state

    def expand(self, start, end, cost, heuristic):
        junction = ROADS[int(self.state)]
        neighbors = []
        for link in junction.links:
            curr_node = link.target
            if not curr_node == self.father.state or curr_node == start:
                acc_cost = self.acc_cost + cost(link)
                neighbors.append((Node(curr_node, acc_cost + heuristic(curr_node, end), acc_cost, self)))
        return neighbors

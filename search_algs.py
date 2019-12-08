from PriorityQueue import PriorityQueue
from Node import Node
from ways import info, compute_distance
from stats import ROADS
import copy
import numpy as np
import csv


def best_first_graph_search(start, end, f, h=lambda x, y: 0):
    frontier = PriorityQueue()
    frontier.append(Node(start))
    goal = Node(end)
    closed_list = set()
    while frontier:
        node = frontier.pop()
        if goal.equal(node):
            return node
        closed_list.add(node.state)
        for child in node.expand(start, end, f, h):
            in_queue = frontier.get(child)
            if child.state not in closed_list and in_queue is None:
                frontier.append(child)
            elif in_queue is not None and child.cost < in_queue[2].cost:
                frontier.replace(child)
    return None


def uniform_cost_search(start, end, cost):
    return best_first_graph_search(start, end, f=cost)


def a_star(start, end, cost, heuristic):
    return best_first_graph_search(start, end, f=cost, h=heuristic)


def track_back(end):
    curr = copy.deepcopy(end)
    route = []
    while not curr.state == np.inf:
        route.append(curr.state)
        curr = curr.father
    return route[::-1]


def cost_func(link):
    return float(link.distance) / float(info.SPEED_RANGES[link.highway_type][1])


def heuristic_func(src, dest):
    src_junc = ROADS[src]
    dest_junc = ROADS[dest]
    return float(compute_distance(src_junc.lat, src_junc.lon, dest_junc.lat, dest_junc.lon)) / 110.0


def ida_search(path, bound, cost, heuristic, start, end):
    node = path[-1]
    f = node.cost
    if f > bound:
        return f
    if node.state == end:
        return 'FOUND'
    min_cost = np.inf
    for succ in node.expand(start, end, cost, heuristic):
        if succ not in path:
            path.append(succ)
            t = ida_search(path, bound, cost, heuristic, start, end)
            if t == 'FOUND':
                return 'FOUND'
            if t < min_cost:
                min_cost = t
            path.pop()
    return min_cost


def ida_star(start, end, cost, heuristic):
    bound = heuristic(start, end)
    path = [Node(start)]
    while bound < np.inf:
        t = ida_search(path, bound, cost, heuristic, start, end)
        if t == 'FOUND':
            return path, bound
        bound = t
    return 'NOT_FOUND'


def track_back_ida(solution):
    return solution[0][::-1]


if __name__ == '__main__':

    def export_solutions_ucs(problems):
        solution = 0
        f = open("results/UCSRuns.txt", "w+")
        for problem in problems:
            solution = uniform_cost_search(int(problem[0]), int(problem[1]), cost_func)
            f.write(str(solution.acc_cost) + '\n')
        f.close()

    def export_solutions_astar(problems):
        solution = 0
        f = open("results/AStarRuns.txt", "w+")
        for problem in problems:
            solution = a_star(int(problem[0]), int(problem[1]), cost_func, heuristic_func)
            f.write(str(solution.acc_cost) + '\n')
        f.close()

    def export_solutions_ida_star(problems):
        solution = 0
        f = open("results/IDAStarRuns.txt", "w+")
        for index, problem in enumerate(problems):
            solution = ida_star(int(problem[0]), int(problem[1]), cost_func, heuristic_func)
            f.write(str(solution[1]) + '\n')
            if index == 4:
                break
        f.close()


    with open('./db/problem.csv', mode='r') as csv_file:
        reader = csv.reader(csv_file, delimiter=',',
                            quotechar='|', quoting=csv.QUOTE_MINIMAL)
        problems = [(row[0], row[1]) for row in reader if not row == '']

    export_solutions_ucs(problems)
    export_solutions_astar(problems)
    export_solutions_ida_star(problems)
    # 213125, 303449
    # 109861, 106930
    # start = 213125
    # end = 303449
    # solution = ida_star(start, end, cost_func, heuristic_func)
    # print(solution)
    # reached_ucs = uniform_cost_search(start, end, cost_func)
    # print(track_back(reached_ucs))
    # print(reached_ucs.acc_cost)
    # reached_astar = a_star(start, end, cost_func, heuristic_func)
    # # print(track_back(reached_astar))
    # print(reached_astar.cost)
    # print(reached_astar.acc_cost)

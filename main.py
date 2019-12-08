'''
Parse input and run appropriate code.
Don't use this file for the actual work; only minimal code should be here.
We just parse input and call methods from other modules.
'''

#do NOT import ways. This should be done from other files
#simply import your modules and call the appropriate functions

from search_algs import a_star, uniform_cost_search, ida_star, track_back, cost_func, heuristic_func, track_back_ida


def find_ucs_rout(source, target):
    return track_back(uniform_cost_search(source, target, cost_func))


def find_astar_route(source, target):
    return track_back(a_star(source, target, cost_func, heuristic_func))


def find_idastar_route(source, target):
    return track_back_ida(ida_star(source, target, cost_func, heuristic_func))
    

def dispatch(argv):
    from sys import argv
    source, target = int(argv[2]), int(argv[3])
    if argv[1] == 'ucs':
        path = find_ucs_rout(source, target)
    elif argv[1] == 'astar':
        path = find_astar_route(source, target)
    elif argv[1] == 'idastar':
        path = find_idastar_route(source, target)
    print(' '.join(str(j) for j in path))


if __name__ == '__main__':
    from sys import argv
    dispatch(argv)

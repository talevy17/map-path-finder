'''
This file should be runnable to print map_statistics using 
$ python stats.py
'''

from collections import namedtuple
from ways import load_map_from_csv, info
import numpy as np
import copy


def map_statistics(roads):
    '''return a dictionary containing the desired information
    You can edit this function as you wish'''
    Stat = namedtuple('Stat', ['max', 'min', 'avg'])
    junctions = roads.junctions()
    num_of_junctions = len(junctions)
    num_of_links = 0
    max_dist = 0
    max_out = 0
    min_dist = np.inf
    min_out = np.inf
    avg_dist = 0
    avg_out = 0
    link_type_dict = {}
    for road in info.TYPE_INDICES:
        link_type_dict[road] = 0
    for junction in junctions:
        links = list(junction.links)
        num_of_curr = len(links)
        avg_out += num_of_curr
        num_of_links += num_of_curr
        if num_of_curr > max_out:
            max_out = copy.deepcopy(num_of_curr)
        if num_of_curr < min_out:
            min_out = copy.deepcopy(num_of_curr)
        for link in links:
            dist = link.distance
            avg_dist += dist
            if dist > max_dist:
                max_dist = copy.deepcopy(dist)
            if dist < min_dist:
                min_dist = copy.deepcopy(dist)
            link_type_dict[link.highway_type] += 1
    avg_dist /= num_of_links
    avg_out /= num_of_junctions
    return {
        'Number of junctions' : num_of_junctions,
        'Number of links' : num_of_links,
        'Outgoing branching factor' : Stat(max=max_out, min=min_out, avg=avg_out),
        'Link distance' : Stat(max=max_dist, min=min_dist, avg=avg_dist),
        # value should be a dictionary
        # mapping each road_info.TYPE to the no' of links of this type
        'Link type histogram' : link_type_dict,  # tip: use collections.Counter
    }


ROADS = load_map_from_csv()
STATS = map_statistics(ROADS)


def print_stats():
    for k, v in map_statistics(ROADS).items():
        print('{}: {}'.format(k, v))

        
if __name__ == '__main__':
    from sys import argv
    assert len(argv) == 1
    print_stats()

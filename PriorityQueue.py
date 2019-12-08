import heapq as pq
import copy


class PriorityQueue:
    def __init__(self):
        self.queue = []
        self.count = 0

    def append(self, elem):
        self.count += 1
        pq.heappush(self.queue, (elem.cost, copy.deepcopy(self.count), elem))

    def __len__(self):
        return len(self.queue)

    def pop(self):
        return pq.heappop(self.queue)[2] \
            if not self.__len__() == 0 \
            else None

    def get(self, item):
        for value in self.queue:
            if item.equal(value[2]):
                return value
        return None

    def __contains__(self, item):
        return self.get(item) is not None

    def replace(self, item):
        elem = self.get(item)
        self.queue.remove(elem)
        pq.heapify(self.queue)
        self.append(item)

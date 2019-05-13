class PriorityQueue():
    """Implementation of a priority queue"""
    def __init__(self):
        self.queue = []
        self.node_finder = dict()
        self.current = 0
        self.REMOVED_SYMBOL = '<removed>'

    def next(self):
        if self.current >=len(self.queue):
            self.current
            raise StopIteration

        out = self.queue[self.current]
        while out == self.REMOVED_SYMBOL:
            self.current += 1
            out = self.queue[self.current]
        self.current += 1
        return out

    def pop(self):
        # TODO: finish this
        while self.queue:
            node = heapq.heappop(self.queue)
            nodeId = node[1]
            if nodeId is not self.REMOVED_SYMBOL:
                try:
                    del self.node_finder[nodeId]
                except KeyError:
                    dummy=1
                return node
        #raise KeyError('pop from an empty priority queue')

    def remove(self, nodeId):
        node = self.node_finder[nodeId]
        node[1] = self.REMOVED_SYMBOL

    def __iter__(self):
        return self

    def __str__(self):
        return 'PQ:[%s]'%(', '.join([str(i) for i in self.queue]))

    def append(self, node):
        # node = (priority, nodeId)
        nodeId = node[1]
        nodePriority = node[0]
        node = [nodePriority, nodeId]
        self.node_finder[nodeId] = node
        heapq.heappush(self.queue, node)

    def update(self, node):
        nodeId = node[1]
        nodePriority = node[0]
        node = [nodePriority, nodeId]
        self.remove(nodeId)
        self.node_finder[nodeId] = node
        heapq.heappush(self.queue, node)

    def getPriority(self, nodeId):
        return self.node_finder[nodeId][0]

    def __contains__(self, key):
        self.current = 0
        return key in [n for v,n in self.queue]

    def __eq__(self, other):
        return self == other

    def size(self):
        return len([1 for priority, node in self.queue if node!=self.REMOVED_SYMBOL])

    def clear(self):
        self.queue = []

    def top(self):
        return self.queue[0]

    __next__ = next

def bidirectional_a_star(graph, start, goal):
    if start == goal:
        return []

    pq_s = PriorityQueue()
    pq_t = PriorityQueue()
    closed_s = dict()
    closed_t = dict()
    g_s = dict()
    g_t = dict()

    g_s[start] = 0
    g_t[goal] = 0

    cameFrom1 = dict()
    cameFrom2 = dict()

    def euclidean_distance(graph, v, goal):
        xv, yv = graph.node[v]['pos']
        xg, yg = graph.node[goal]['pos']
        return ((xv-xg)**2 + (yv-yg)**2)**0.5

    def h1(v): # heuristic for forward search (from start to goal)
        return euclidean_distance(graph, v, goal)

    def h2(v): # heuristic for backward search (from goal to start)
        return euclidean_distance(graph, v, start)

    cameFrom1[start] = False
    cameFrom2[goal] = False

    pq_s.append((0+h1(start), start)) 
    pq_t.append((0+h2(goal), goal))

    done = False
    i = 0

    mu = 10**301 # 10**301 plays the role of infinity
    connection = None

    while pq_s.size() > 0 and pq_t.size() > 0 and done == False:
        i = i + 1
        if i % 2 == 1: # alternate between forward and backward A*
            fu, u = pq_s.pop()
            closed_s[u] = True
            for v in graph[u]:
                weight = graph[u][v]['weight']
                if v in g_s:
                    if g_s[u] + weight < g_s[v]:
                        g_s[v] = g_s[u] + weight
                        cameFrom1[v] = u
                        if v in closed_s:
                            del closed_s[v]
                        if v in pq_s:
                            pq_s.update((g_s[v]+h1(v), v))
                        else:
                            pq_s.append((g_s[v]+h1(v), v))
                else:
                    g_s[v] = g_s[u] + weight
                    cameFrom1[v] = u
                    pq_s.append((g_s[v]+h1(v), v))
        else:
            fu, u = pq_t.pop()
            closed_t[u] = True
            for v in graph[u]:
                weight = graph[u][v]['weight']
                if v in g_t:
                    if g_t[u] + weight < g_t[v]:
                        g_t[v] = g_t[u] + weight
                        cameFrom2[v] = u
                        if v in closed_t:
                            del closed_t[v]
                        if v in pq_t:
                            pq_t.update((g_t[v]+h2(v), v))
                        else:
                            pq_t.append((g_t[v]+h2(v), v))
                else:
                    g_t[v] = g_t[u] + weight
                    cameFrom2[v] = u
                    pq_t.append((g_t[v]+h2(v), v))

        if u in closed_s and u in closed_t:
            if g_s[u] + g_t[u] < mu:
                mu = g_s[u] + g_t[u]
                connection = u
                try:
                    stopping_distance = max(min([f for (f,x) in pq_s]), min([f for (f,x) in pq_t]))
                except ValueError:
                    continue
                if mu <= stopping_distance:
                    done = True
                    connection = u
                    continue

    if connection is None:
        # start and goal are not connected
        return None

    #print cameFrom1
    #print cameFrom2

    path = []
    current = connection
    #print current
    while current != False:
        #print predecessor
        path = [current] + path
        current = cameFrom1[current]

    current = connection
    successor = cameFrom2[current]
    while successor != False:
        path = path + [successor]
        current = successor
        successor = cameFrom2[current]

    return path
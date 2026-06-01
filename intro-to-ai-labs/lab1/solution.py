import sys, getopt
from collections import deque
import heapq


class Node:
    def __init__(self, name, cost, index, prev_index):
        self.name = name
        self.cost = cost
        self.index = index
        self.prev_index = prev_index

    def __lt__(self, other):
        if self.cost == other.cost:
            return self.name < other.name
        else:
            return self.cost < other.cost

class Output_data:
    def __init__(self, alg, found, visited, path, cost):
        self.alg = alg
        self.found = found
        self.visited = visited
        self.path = path[::-1]
        self.path_len = len(path)
        self.cost = cost

def data_processing(ss):
    f = open(ss)
    lines = f.readlines()
    f.close()

    s0 = -1; goal = -1
    expand = {}
    for line in lines:
        if line[0] != '#':
            if s0 == -1:
                s0 = line.strip()
            elif goal == -1:
                goal = line.strip().split(' ')
            else:
                line = line.strip().split(':')
                expand[line[0]] = {}
                line[1] = line[1].strip()
                if len(line[1]) > 0:
                    pairs = line[1].split(' ')
                    for pair in pairs:
                        pair = pair.split(',')
                        expand[line[0]][pair[0]] = float(pair[1])

    return s0, expand, goal

def heuristic(h_file):
    f = open(h_file)
    lines = f.readlines()
    f.close()

    heuristic = {}
    for line in lines:
        line = line.strip().split(':')
        heuristic[line[0]] = float(line[1].strip())
    return heuristic

def output(data):
    print('# ', data.alg)
    if not data.found:
        print('[FOUND_SOLUTION]: no')
    else:
        print('[FOUND_SOLUTION]: yes')
        print('[STATES_VISITED]: ', data.visited)
        print('[PATH_LENGTH]:', data.path_len)
        print('[TOTAL_COST]: ', data.cost)
        path = '[PATH]: '
        for i in range(len(data.path)):
            if i != 0:
                path += ' => '
            path += data.path[i]
        print(path)
    return

def BFS(s0, expand, goal):
    open = deque([Node(s0, 0, '', '')])
    closed = deque()
    index = 0
    visited = set()

    while len(open) > 0:
        n = open.popleft()
        n.index = index
        closed.append(n)
        visited.add(n.name)

        if (n.name in goal):
            path = []
            cost = n.cost
            while n.prev_index != '':
                path.append(n.name)
                n = closed[n.prev_index]
            path.append(n.name)
            return Output_data('BFS', 1, len(visited), path, cost)
        
        succ = list(expand[n.name])
        succ.sort()
        for m in succ:
            if m not in visited:
                open.append(Node(m, n.cost + expand[n.name][m], '', index))
        
        index += 1
    return Output_data('BFS', 0)

def UCS(s0, expand, goal):
    open = [Node(s0, 0.0, '', '')]
    heapq.heapify(open)
    closed = []
    index = 0
    visited = {}

    while len(open) > 0:
        n = heapq.heappop(open)
        n.index = index
        closed.append(n)
        visited[n.name] = n.cost

        if (n.name in goal):
            path = []
            cost = n.cost
            while n.prev_index != '':
                path.append(n.name)
                n = closed[n.prev_index]
            path.append(n.name)
            return Output_data('UCS', 1, len(visited), path, cost)
        
        for m in expand[n.name]:
            if m not in visited or (m in visited and visited[m] > n.cost + expand[n.name][m]):
                heapq.heappush(open, Node(m, n.cost + expand[n.name][m], '', index))
        
        index += 1
    return Output_data('UCS', 0)

def Astar(s0, expand, goal, h_file):
    h = heuristic(h_file)
    open = [Node(s0, h[s0], 0, '')]
    closed = []
    index = 0
    visited = {}
    open_closed = {s0: 0}

    while len(open) > 0:
        n = open.pop(0)
        n.index = index
        n.cost -= h[n.name]
        closed.append(n)
        visited[n.name] = n.cost

        if (n.name in goal):
            path = []
            cost = n.cost
            while n.prev_index != '':
                path.append(n.name)
                n = closed[n.prev_index]
            path.append(n.name)
            return Output_data('A-star ' + h_file, 1, len(visited), path, cost)
        
        for m in expand[n.name]:
            if m in open_closed:
                if open_closed[m] < n.cost + expand[n.name][m]:
                    continue
                else:
                    del open_closed[m]
            open.append(Node(m, n.cost + expand[n.name][m] + h[m], '', index))
            open = sorted(sorted(open, key=lambda node: node.name), key=lambda node: node.cost)
            open_closed[m] = n.cost + expand[n.name][m]

        index += 1        
    return Output_data('A-star ' + h_file, 0)

def optimistic_check(expand, goal, h_file):
    optimistic = 1
    h = heuristic(h_file)

    print('# HEURISTIC-OPTIMISTIC ' + h_file)
    nodes = list(h.keys())
    nodes.sort()
    for node in nodes:
        hstar = UCS(node, expand, goal).cost
        if (h[node] <= hstar):
            print('[CONDITION]: [OK] h(' + node + ') <= h*: ' + str(h[node]) + ' <= ' + str(hstar))
        else:
            print('[CONDITION]: [ERR] h(' + node + ') <= h*: ' + str(h[node]) + ' <= ' + str(hstar))
            optimistic = 0
    
    if optimistic:
        print('[CONCLUSION]: Heuristic is optimistic.')
    else:
        print('[CONCLUSION]: Heuristic is not optimistic.')
    return

def consistent_check(expand, goal, h_file):
    h = heuristic(h_file)
    consistent = 1

    print('# HEURISTIC-CONSISTENT ' + h_file)
    nodes = list(h)
    nodes.sort()
    for node in nodes:
        next_nodes = list(expand[node])
        next_nodes.sort()

        for nxt in next_nodes:
            c = expand[node][nxt]
            if (h[node] <= h[nxt] + c):
                print('[CONDITION]: [OK] h(' + node + ') <= h(' + nxt + ') + c: ' + str(h[node]) + ' <= ' + str(h[nxt]) + ' + ' + str(c))
            else:
                print('[CONDITION]: [ERR] h(' + node + ') <= h(' + nxt + ') + c: ' + str(h[node]) + ' <= ' + str(h[nxt]) + ' + ' + str(c))
                consistent = 0

    if consistent:
        print('[CONCLUSION]: Heuristic is consistent.')
    else:
        print('[CONCLUSION]: Heuristic is not consistent.')

    return

## https://www.tutorialspoint.com/python/python_command_line_arguments.htm
def main(argv):
    opts, args = getopt.getopt(argv, '', ['alg=', 'ss=', 'h=', 'check-optimistic', 'check-consistent'])
    for opt, arg in opts:
        if (opt == '--ss'):
            data = data_processing(arg)
            s0 = data[0]
            expand = data[1]
            goal = data[2]
        elif (opt == '--h'):
            h_file = arg
    for opt, arg in opts:
        if (opt == '--check-optimistic'):
            optimistic_check(expand, goal, h_file)
        elif (opt == '--check-consistent'):
            consistent_check(expand, goal, h_file)
        elif (opt == '--alg'):
            if (arg == 'bfs'):
                output(BFS(s0, expand, goal))
            elif (arg == 'ucs'):
                output(UCS(s0, expand, goal))
            elif (arg == 'astar'):
                output(Astar(s0, expand, goal, h_file))
    return

if __name__ == '__main__':
   main(sys.argv[1:])
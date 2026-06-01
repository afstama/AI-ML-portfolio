import sys, getopt

class State:
    def __init__(self, name, cost, index, prev_index):
        self.name = name
        self.cost = cost
        self.index = index
        self.prev_index = prev_index

    def __lt__(self, other):
        if self.cost != other.cost:
            return self.cost < other.cost
        else:
            return self.name < other.name

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

    return s0, goal, expand

def heuristic(h_file):
    f = open(h_file)
    lines = f.readlines()
    f.close()

    heuristic = {}
    for line in lines:
        line = line.strip().split(':')
        heuristic[line[0]] = float(line[1].strip())
    return heuristic

class Output:
    def __init__(self, name, found, states, path, cost):
        self.name = name
        self.found = found
        self.states = states
        self.path = path
        self.path_length = len(path)
        self.cost = cost

def output(sol):
    print('# ', sol.name)
    if not sol.found:
        print('[FOUND_SOLUTION]: no')
    else:
        print('[FOUND_SOLUTION]: yes')
        print('[STATES_VISITED]: ', sol.states)
        print('[PATH_LENGTH]:', sol.path_length)
        print('[TOTAL_COST]: ', sol.cost)
        path = '[PATH]: '
        for i in range(len(sol.path)):
            if i != 0:
                path += ' => '
            path += sol.path[i]
        print(path)
    return


def BFS(s0, goal, expand):
    opn = [State(s0, 0, '', '')]
    closd = []
    visited = set()
    index = 0

    while (len(opn) > 0):
        n = opn.pop(0)
        n.index = index
        index += 1
        closd.append(n)
        visited.add(n.name)

        if (n.name in goal):
            path = []
            cost = n.cost
            while (n.prev_index != ''):
                path.insert(0, n.name)
                n = closd[n.prev_index]
            path.insert(0, n.name)
            return Output('BFS', 1, len(visited), path, cost)
        
        neighbours = list(expand[n.name].keys())
        neighbours.sort()
        for m in neighbours:
            opn.append(State(m, expand[n.name][m] + n.cost, '', n.index))

    return Output('BFS', 0)

def UCS(s0, goal, expand):
    opn = [State(s0, 0, '', '')]
    closd = []
    visited = set()
    index = 0

    while (len(opn) > 0):
        n = opn.pop(0)
        n.index = index
        index += 1
        closd.append(n)
        visited.add(n.name)

        if n.name in goal:
            path = []
            cost = n.cost
            while n.prev_index != '':
                path.insert(0, n.name)
                n = closd[n.prev_index]
            path.insert(0, n.name)
            return Output('UCS', 1, len(visited), path, cost)
        
        for m in expand[n.name]:
            opn.append(State(m, expand[n.name][m] + n.cost, '', n.index))
            opn.sort()

    return Output('UCS', 0)

def Astar(s0, goal, expand, h_file):
    h = heuristic(h_file)
    opn = [State(s0, 0, '', '')]
    closd = []
    visited = set()
    index = 0
    opn_closd = {s0: h[s0]}

    while (len(opn) > 0):
        n = opn.pop(0)
        n.index = index
        closd.append(n)
        visited.add(n.name)
        index += 1

        if n.name in goal:
            path = []
            cost = n.cost
            while n.prev_index != '':
                path.insert(0, n.name)
                cost -= h[n.name]
                n = closd[n.prev_index]
            ##cost -= h[n.name]
            path.insert(0, n.name)
            return Output('A-star ' + h_file, 1, len(visited), path, cost)
        
        for m in expand[n.name]:
            if m in opn_closd:
                if opn_closd[m] < expand[n.name][m] + n.cost:
                    continue
                else:
                    opn_closd[m] = n.cost + expand[n.name][m]
            opn.append(State(m, n.cost + expand[n.name][m] + h[m], '', n.index))
            opn.sort()

    return Output('A-star ' + h_file, 0)


def optimistic_check(goal, expand, h_file):
    print('# HEURISTIC-OPTIMISTIC ' + h_file)
    h = heuristic(h_file)
    optimistic = 1
    states = list(h)
    states.sort()

    for state in states:
        num = UCS(state, goal, expand).cost
        if (h[state] <= num):
            print('[CONDITION]: [OK] h(' + state + ') <= h*: ' + str(h[state]) + ' <= ' + str(num))
        else:
            print('[CONDITION]: [ERR] h(' + state + ') <= h*: ' + str(h[state]) + ' <= ' + str(num))
            optimistic = 0
    if (optimistic):
        print('[CONCLUSION]: Heuristic is optimistic.')
    else:
        print('[CONCLUSION]: Heuristic is not optimistic.')
    return

def consistent_check(goal, expand, h_file):
    print('# HEURISTIC-CONSISTENT ' + h_file)
    h = heuristic(h_file)
    consistent = 1
    states = list(h)
    states.sort()

    for state in states:
        neighbours = list(expand[state])
        neighbours.sort()

        for neighbour in neighbours:
            c = expand[state][neighbour]
            if (h[state] <= h[neighbour] + c):
                print('[CONDITION]: [OK] h(' + state + ') <= h(' + neighbour + ') + c: ' + str(h[state]) + ' <= ' + str(h[neighbour]) + ' + ' + str(c))
            else:
                print('[CONDITION]: [ERR] h(' + state + ') <= h(' + neighbour + ') + c: ' + str(h[state]) + ' <= ' + str(h[neighbour]) + ' + ' + str(c))
                consistent = 0

    if (consistent):
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
            goal = data[1]
            expand = data[2]
        elif (opt == '--h'):
            h_file = arg
    for opt, arg in opts:
        if (opt == '--check-optimistic'):
            optimistic_check(goal, expand, h_file)
        elif (opt == '--check-consistent'):
            consistent_check(goal, expand, h_file)
        elif (opt == '--alg'):
            if (arg == 'bfs'):
                output(BFS(s0, goal, expand))
            elif (arg == 'ucs'):
                output(UCS(s0, goal, expand))
            elif (arg == 'astar'):
                output(Astar(s0, goal, expand, h_file))
    return

if __name__ == '__main__':
   main(sys.argv[1:])

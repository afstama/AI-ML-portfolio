import sys

def negLiteral(literal):
    if literal[0] == '~':
        return literal[1:]
    return '~' + literal

class Clause:
    def __init__(self, literals):
        self.literals = literals
        self.literals.sort()
    def __str__(self):
        return str(self.literals)
    def __repr__(self):
        return str(self.literals)
    def __eq__(self, other):
        return self.literals == other.literals
    def isSubset(self, other):
        return set(self.literals).issubset(set(other.literals))
    def toGoal(self):
        goal = []
        for literal in self.literals:
            goal.append(Clause([negLiteral(literal)]))
        return goal
    def isTautology(self):
        for literal in self.literals:
            if negLiteral(literal) in self.literals:
                return True
        return False

def processData(resFile, comFile):
    with open(resFile) as f:
        lines = f.readlines()
    clauses = []
    for line in lines:
        line = line.strip().lower()
        if line[0]  == '#':
            continue
        line = line.split(' v ')
        clauses.append(Clause(line))

    if not comFile:
        goal = clauses.pop(-1).toGoal()
        return clauses, goal
    
    commands = []
    with open(comFile) as f:
        lines = f.readlines()
    for line in lines:
        line = line.strip().lower()
        commands.append([Clause(line[:-1].strip().split(' v ')), line[-1]])
    return clauses, commands

def cleanData(clauses, checked, unchecked):
    cleanUnchecked = []
    for clause in unchecked:
        clause.literals = list(set(clause.literals))
        if not clause.isTautology():
            cleanUnchecked.append(clause)

    clean = []
    for i in range(len(cleanUnchecked)):
        uncheckedClause = cleanUnchecked[i]
        isSub = False
        for clause in clauses:
            if clause.isSubset(uncheckedClause):
                isSub = True
                break
        if not isSub:
            j = 0
            while j < len(checked):
                if checked[j].isSubset(uncheckedClause):
                    isSub = True
                    break
                if uncheckedClause.isSubset(checked[j]):
                    del checked[j]
                    continue
                j += 1
            if not isSub:
                for j in range(len(cleanUnchecked)):
                    if j != i and cleanUnchecked[j].isSubset(uncheckedClause):
                        isSub = True
                        break
                if not isSub:
                    clean.append(uncheckedClause)
    return clean

def SoS(clauses, sos, index):
    new = []
    while index < len(sos):
        newClause = sos[index]
        for oldClause in clauses+sos[:index]:
            resolvents = list(set(newClause.literals + oldClause.literals))
            changed =False
            for literal in newClause.literals:
                negliteral = negLiteral(literal)
                if negliteral in oldClause.literals:
                    ##resolvents = newClause.literals + oldClause.literals
                    resolvents.remove(literal)
                    resolvents.remove(negliteral)
                    changed = True
            if changed:
                if len(resolvents) == 0:
                    new.append(Clause(['NIL']))
                    return new
                found = False
                resolventClause = Clause(resolvents)
                for clause in clauses + sos:
                    if clause.isSubset(resolventClause):
                        found = True
                        break
                if not found:
                    new.append(Clause(resolvents))
                    if resolventClause.isSubset(newClause):
                        del sos[index]
                        index -= 1
        index += 1
    return new

def resolution(clauses, goal):
    sos = goal.copy()
    index = 0

    while True:
        new = SoS(clauses, sos, index)
        ##new = cleanData(clauses, sos, new)
        index = len(sos)
        sos += new
        if len(new) == 0:
            return 0, clauses, goal, sos
        if new[-1].literals[0] == 'NIL':
            return 1, clauses, goal, sos

def resolutionOutput(success, clauses, goal, sos):
    goalOutput = ''
    for clause in goal:
        goalOutput += negLiteral(clause.literals[0]) + ' v '
    goalOutput = goalOutput[:-3]

    if not success:
        print(f'[CONCLUSION]: {goalOutput} is unknown')
        return
    
    print(f'[CONCLUSION]: {goalOutput} is true')

def cooking(clauses, commands):
    clauses = cleanData([], [], clauses)

    for command in commands:
        if command[1] == '?':
            goal = command[0].toGoal()
            res = resolution(clauses, goal)
            resolutionOutput(res[0], res[1], res[2], res[3])
        elif command[1] == '+':
            clauses.append(command[0])
            clauses = cleanData([], [], clauses)
        elif command[1] == '-':
            for clause in clauses:
                if set(clause.literals) == set(command[0].literals):
                    clauses.remove(clause)
                    break


def main(argv):
    if 'resolution' in argv:
        data = processData(argv[1], 0)
        clauses = data[0]
        goal = data[1]
        clauses = cleanData([], [], clauses)
        res = resolution(clauses, goal)
        print(res)
        resolutionOutput(res[0], res[1], res[2], res[3])
    elif 'cooking' in argv:
        data = processData(argv[1], argv[2])
        cooking(data[0], data[1])
    return

if __name__ == '__main__':
   main(sys.argv[1:])
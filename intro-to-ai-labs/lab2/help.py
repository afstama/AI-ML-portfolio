import sys

def negLiteral(literal):
    if literal[0] == '~':
        return literal[1:]
    return '~' + literal

class Clause:
    def __init__(self, literals):
        self.literals = literals
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

def cleanClauses(clauses):
    clean = []

    for i in range(len(clauses)):
        issubset = False
        if not clauses[i].isTautology():
            for j in range(len(clauses)):
                if i != j and clauses[j].isSubset(clauses[i]):
                    issubset = True
                    break
            if not issubset:
                clauses[i].literals = list(set(clauses[i].literals))
                clean.append(clauses[i])
    
    return clean

def SoS(clauses, sos, index):
    new = []
    for sosClause in sos[index:]:
        i = 0
        while i < len(clauses):
            clause = clauses[i]
            for literal in sosClause.literals:
                negliteral = negLiteral(literal)
                if negliteral in clause.literals:
                    resolvents = clause.literals + sosClause.literals
                    resolvents.remove(literal)
                    resolvents.remove(negliteral)
                    resolvents = list(set(resolvents))
                    if len(resolvents) == 0:
                        new.append(Clause(['NIL']))
                        return new, sos
                    resolventClause = Clause(resolvents)
                    if not resolventClause.isTautology():
                        new.append(resolventClause)
            i += 1
    
    while index < len(sos):
        j = 0
        while j < index:
            for literal in sos[index].literals:
                negliteral = negLiteral(literal)
                if negliteral in sos[j].literals:
                    resolvents = sos[i].literals + sos[j].literals
                    resolvents.remove(literal)
                    resolvents.remove(negliteral)
                    resolvents = list(set(resolvents))
                    if len(resolvents) == 0:
                        new.append(Clause(['NIL']))
                        return new, sos
                    resolventClause = Clause(resolvents)
                    if not resolventClause.isTautology():
                        new.append(resolventClause)
                        if resolventClause.isSubsset(sosClause[i]):
                            del sosClause[i]
                            i -= 1
                            j -= 1
            j += 1
        index += 1

    return new, sos

def resolutionOutput(success, goal):
    goalOutput = ''
    for clause in goal:
        goalOutput += negLiteral(clause.literals[0]) + ' v '
    goalOutput = goalOutput[:-3]
    if not success:
        print(f'[CONCLUSION]: {goalOutput} is unknown')
        return
    print(f'[CONCLUSION]: {goalOutput} is true')

def resolution(clauses, goal):
    sos = goal.copy()
    index = 0

    while True:
        strategySos = SoS(clauses, sos,  index)
        new = strategySos[0]
        sos = strategySos[1]
        index = len(sos)
        sos += new
        if len(new) == 0:
            return 0, sos
        if new.pop(-1).literals[0] == 'NIL':
            return 1, sos

def main(argv):
    if 'resolution' in argv:
        data = processData(argv[1], 0)
        clauses = cleanClauses(data[0])
        goal = data[1]
        res = resolution(clauses, goal)
        resolutionOutput(res[0], goal)
    return

if __name__ == '__main__':
   main(sys.argv[1:])
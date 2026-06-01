import sys

def negLiteral(literal):
    if literal[0] == '~':
        return literal[1:]
    return '~' + literal

class Clause:
    def __init__(self, literals, index, parent1, parent2):
        self.literals = literals
        self.index = ''
        self.parent1 = parent1
        self.parent2 = parent2
    def __str__(self):
        out = ''
        for literal in self.literals:
            out += literal + ' v '
        return out[:-3]
    def __repr__(self):
        out = ''
        for literal in self.literals:
            out += literal + ' v '
        return out[:-3]
    def __eq__(self, other):
        return self.literals == other.literals
    def __hash__(self):
        return hash(self.literals)
    def isSubset(self, other):
        return self.literals.issubset(other.literals)
    def toGoal(self):
        goal = []
        for literal in self.literals:
            goal.append(Clause(set([negLiteral(literal)]), '', '', ''))
        return goal
    def isTautology(self):
        for literal in self.literals:
            if negLiteral(literal) in self.literals:
                return True
        return False

def processData(clausesFile, commandsFile):
    with open(clausesFile) as f:
        lines = f.readlines()
    clauses = []
    for line in lines:
        line = line.strip().lower()
        if line[0] == '#':
            continue
        line = line.split(' v ')
        clauses.append(Clause(set(line), '', '', ''))
    
    if not commandsFile:
        goal = clauses.pop(-1).toGoal()
        return clauses, goal
    
    commands = []
    with open(commandsFile) as f:
        lines = f.readlines()
    for line in lines:
        line = line.strip().lower()
        sign = line[-1]
        literals = set()
        for atom in line[:-2].split(' v '):
            literals.add(atom)
        commands.append([Clause(literals, '', '', ''), sign])
    return clauses, commands

def cleanClauses(clauses):
    clean = []
    for i in range(len(clauses)):
        if clauses[i].isTautology():
            continue
        found = False
        for j in range(len(clauses)):
            if i != j and clauses[j].isSubset(clauses[i]):
                found = True
                break
        if not found:
            clean.append(clauses[i])
    return clean

def resolution(clauses, goal):
    allClauses = clauses + goal
    index1 = len(clauses)

    while index1 < len(allClauses):
        sosClause = allClauses[index1]
        index2 = index1 - 1
        while index2 >= 0:
            clause = allClauses[index2]
            for literal in sosClause.literals:
                neglit = negLiteral(literal)
                if neglit in clause.literals:
                    resolvents = sosClause.literals.union(clause.literals)
                    resolvents.remove(literal)
                    resolvents.remove(neglit)
                    if len(resolvents) == 0:
                        allClauses.append(Clause({'NIL'}, '', clause, sosClause))
                        return 1, allClauses
                    resClause = Clause(resolvents, '', clause, sosClause)
                    if not resClause.isTautology():
                        found = False
                        for j in range(len(allClauses)):
                            if allClauses[j].isSubset(resClause):
                                found = True
                                break
                        if not found:
                            allClauses.append(resClause)
            index2 -= 1
        index1 += 1
    return 0, allClauses

def constructPath(clause, path, index):
    if clause.parent1.index == '':
        p = constructPath(clause.parent1, path, index)
        path = p[0]
        index = p[1]
        if (clause.parent2.index == ''):
            p = constructPath(clause.parent2, path, index)
            path = p[0]
            index = p[1]
        path.append(clause)
        clause.index = index
        return path, index+1
    if clause.parent2.index == '':
        p = constructPath(clause.parent2, path, index)
        path = p[0]
        index = p[1]
        path.append(clause)
        clause.index = index
        return path, index+1
    path.append(clause)
    clause.index = index
    return path, index+1

def resolutionOutput(clauses, goal, success, allClauses):
    goalOutput = ''
    for clause in goal:
        for literal in clause.literals:
            goalOutput += negLiteral(literal) + ' v '
    goalOutput = goalOutput[:-3]

    if not success:
        print(f'[CONCLUSION]: {goalOutput} is unknown')
        return
    
    for i in range(len(clauses)):
        clauses[i].index = i
        print(f'{i+1}. {clauses[i]}')
    for i in range(len(goal)):
        goal[i].index = i+len(clauses)
        print(f'{i+len(clauses)+1}. {goal[i]}')
    path = []
    p = constructPath(allClauses[-1], path, len(clauses+goal))
    ##print(p)
    print('===============')
    for i in range(len(p[0])):
        print(f'{len(clauses+goal)+i+1}. {p[0][i]} ({p[0][i].parent1.index+1}, {p[0][i].parent2.index+1})')
    print('===============')
    print(f'[CONCLUSION]: {goalOutput} is true')

def cookingOutput(clauses, goal, success, allClauses):
    goalOutput = ''
    for clause in goal:
        for literal in clause.literals:
            goalOutput += negLiteral(literal) + ' v '
    goalOutput = goalOutput[:-3]

    if not success:
        print(f'[CONCLUSION]: {goalOutput} is unknown')
        return
    
    path = []
    p = constructPath(allClauses[-1], path, 0)
    ##print(p)
    border = False
    for i in range(p[1]):
        if p[0][i] not in (clauses+goal):
            if not border:
                print('===============')
                border = True
            print(f'{i+1}. {p[0][i]} ({p[0][i].parent1.index+1}, {p[0][i].parent2.index+1})')
        else:
            print(f'{i+1}. {p[0][i]}')
    print('===============')
    print(f'[CONCLUSION]: {goalOutput} is true')

def cooking(clauses, commands):
    print('Constructed with knowledge:')
    for clause in clauses:
        print(clause)
    print()
    
    for command in commands:
        print(f"User's command: {str(command[0])} {command[1]}")
        match command[1]:
            case '?':
                for clause in clauses:
                    clause.index = ''
                goal = command[0].toGoal()
                res = resolution(clauses, goal)
                cookingOutput(clauses, goal, res[0], res[1])
            case '+':
                clauses.append(command[0])
            case '-':
                clauses.remove(command[0])
        print()
    return

def main(argv):
    if 'resolution' in argv:
        data = processData(argv[1], 0)
        goal = data[1]
        clauses = cleanClauses(data[0])
        res = resolution(clauses, goal)
        ##print(res)
        resolutionOutput(clauses, goal, res[0], res[1])
    elif 'cooking' in argv:
        data = processData(argv[1], argv[2])
        ##print(data)
        cooking(data[0], data[1])
    return

if __name__ == '__main__':
   main(sys.argv[1:])
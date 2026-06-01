import sys
import math

def processData(dataset):
    with open(dataset) as f:
        lines = f.readlines()

    features = lines[0].strip().split(',')
    goal = features.pop()
    gValues = set()
    fSets = {}
    for feature in features:
        fSets[feature] = set()

    cases = []
    for i in range(1, len(lines)):
        line = lines[i].strip().split(',')
        cases.append({})
        for j in range(len(features)):
            cases[i-1][features[j]] = line[j]
            fSets[features[j]].add(line[j])
        cases[i-1][goal] = line[-1]
        gValues.add(line[-1])
    
    return fSets, goal, gValues, cases

class Node:
    def __init__(self, feature, value, parent):
        self.feature = feature
        self.value = value
        self.parent = parent
    def __repr__(self):
        return f'{self.feature}={self.value}'
    def __str__(self):
        return f'{self.feature}={self.value}'

class ID3:
    def __init__(self, hp=None):
        self.hp = hp
        self.depth = 0
        self.visited = []

    def fit(self, dataset):
        self.features, self.goal, self.gValues, cases = processData(dataset)
        self.fitRecursive(cases)
        self.paths = self.findPaths()
        self.printPaths()

    def fitRecursive(self, cases, currNode=None):
        if currNode != None:
            self.visited.append(currNode)

        freq = {}
        for case in cases:
            if case[self.goal] in freq:
                freq[case[self.goal]] += 1
            else:
                freq[case[self.goal]] = 1

        E0 = 0
        for f in freq:
            try:
                E0 -= (freq[f]/len(cases)) * math.log2(freq[f]/len(cases))
            except:
                E0 = 0
        if E0 == 0 or len(self.features) == 0 or self.depth == self.hp:
            freqKeys = sorted(freq, key=lambda k: (-freq[k], k))
            self.visited.append(Node(self.goal, freqKeys[0], currNode))
            return
        
        ig = {}
        for feature in self.features:
            ig[feature] = E0
            for value in self.features[feature]:
                total = 0
                E = 0
                valueFreq = {}
                for case in cases:
                    if case[feature] == value:
                        total += 1
                        if case[self.goal] in valueFreq:
                            valueFreq[case[self.goal]] += 1
                        else:
                            valueFreq[case[self.goal]] = 1
                for f in valueFreq:
                    try:
                        E -= (valueFreq[f]/total) * math.log2(valueFreq[f]/total)
                    except:
                        E = 0
                ig[feature] -= (total/len(cases)) * E
        
        ## printing IG and finding maxIG
        sortedIgKeys = sorted(ig, key=lambda k: (-ig[k], k))
        nextFeature = sortedIgKeys[0]
        for feature in sortedIgKeys:
            print('IG({:s})={:0.4f}'.format(feature, ig[feature]), end=' ')
        print()

        for value in self.features[nextFeature]:
            nextCases = []
            for case in cases:
                if case[nextFeature] == value:
                    nextCases.append(case)
            if len(nextCases) == 0:
                continue
            prevFeature = self.features[nextFeature]
            del self.features[nextFeature]
            node = Node(nextFeature, value, currNode)
            self.depth += 1
            self.fitRecursive(nextCases, node)
            self.depth -= 1
            self.features[nextFeature] = prevFeature

        ##print(self.visited)
        return
    
    def findPaths(self):
        paths = []
        for node in self.visited:
            if node.feature == self.goal:
                path = []
                self.findPath(node, path)
                paths.append(path)
        return paths
    
    def findPath(self, node, path):
        path.insert(0, node)
        if node.parent != None:
            self.findPath(node.parent, path)
        return
    
    def printPaths(self):
        print('[BRANCHES]:')
        for path in self.paths:
            for i in range(len(path)):
                if path[i].feature == self.goal:
                    print(path[i].value)
                else:
                    print(f'{i+1}:{path[i]}', end=' ')
    
    def predict(self, dataset):
        cases = self.getCases(dataset)
        predictions = []
        
        print('[PREDICTIONS]: ', end='')
        freq = {}
        for case in cases:
            if case[self.goal] not in freq:
                freq[case[self.goal]] = 1
            else:
                freq[case[self.goal]] += 1

        for case in cases:
            found = False
            for path in self.paths:
                if found:
                    break
                for el in path:
                    if el.feature == self.goal:
                        predictions.append(el.value)
                        print(el.value, end=' ')
                        found = True
                        break
                    if el.value != case[el.feature]:
                        break
            if not found:
                sortedFreq = sorted(freq, key=lambda k: (-freq[k], k))
                predictions.append(sortedFreq[0])
                print(sortedFreq[0], end=' ')
        
        ## accuracy
        print('\n[ACCURACY]: {:0.5f}'.format(self.accuracy(cases, predictions)))
        print('[CONFUSION_MATRIX]:')
        gValues = list(self.gValues)
        gValues.sort()
        for g1 in gValues:
            for g2 in gValues:
                print(self.confMatrix[g1][g2], end=' ')
            print()

    def getCases(self, dataset):
        with open(dataset) as f:
            lines = f.readlines()
        
        features = lines[0].strip().split(',')
        cases = []
        for i in range(1, len(lines)):
            line = lines[i].strip().split(',')
            cases.append({})
            for j in range(len(features)):
                cases[i-1][features[j]] = line[j]
        return cases

    def accuracy(self, cases, predictions):
        self.confMatrix = {}
        for g1 in self.gValues:
            self.confMatrix[g1] = {}
            for g2 in self.gValues:
                self.confMatrix[g1][g2] = 0

        correct = 0
        for i in range(len(cases)):
            self.confMatrix[cases[i][self.goal]][predictions[i]] += 1
            if predictions[i] == cases[i][self.goal]:
                correct += 1
        return correct/len(cases)

        

def main(argv):
    if len(argv) == 3:
        model = ID3(int(argv[-1]))
    else:
        model = ID3()
    model.fit(argv[0])
    model.predict(argv[1])
    return

if __name__ == '__main__':
   main(sys.argv[1:])

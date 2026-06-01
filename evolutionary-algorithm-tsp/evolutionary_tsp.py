import Reporter
import numpy as np
from numba import jit

# Modify the class name to match your student number.
class r0974957:

	def __init__(self):
		self.reporter = Reporter.Reporter(self.__class__.__name__)
	def r0974957(self):
		self.__init__()

	# The evolutionary algorithm's main loop
	def optimize(self, filename):
		# Read distance matrix from file.		
		file = open(filename)
		distanceMatrix = np.loadtxt(file, delimiter=",")
		file.close()

		# Your code here.
		population = initialize(individualSize=distanceMatrix.shape[0], populationSize=100, distanceMatrix=distanceMatrix)
		iter = 0
		sameBest = 0
		prevBestObjective = np.inf

		yourConvergenceTestsHere = True
		while( yourConvergenceTestsHere ):
			meanObjective = 0.0
			bestObjective = 0.0
			bestSolution = np.array([1,2,3,4,5])

			# Your code here.

			kids = np.empty((2 * len(population), distanceMatrix.shape[0]), dtype=np.int64)

			index = 0
			while index < 2*len(population):
				p1 = select(population, distanceMatrix); p2 = select(population, distanceMatrix)
				(k1, k2) = [mutate(i, iter%150) for i in crossover(p1, p2)]

				kids[index] = k1; kids[index + 1] = k2
				index += 2

			mutatedPopulation = np.array([mutate(i, iter%150) for i in population])
			mutatedPopulation = np.array([LSO2(individual=i, distanceMatrix=distanceMatrix) for i in population])
			kids = np.concatenate((kids, mutatedPopulation))

			if iter>200 == 0:
				population = eliminationSharing(population=kids, populationSize=len(population), distanceMatrix=distanceMatrix)
			else:
				population = elimination(population	=kids, size=len(population), distanceMatrix=distanceMatrix)
			fitnesses = [fitness(i, distanceMatrix) for i in population]

			bestObjective = np.min(fitnesses)
			meanObjective = np.sum(fitnesses) / len(fitnesses)
			bestSolution = population[fitnesses.index(bestObjective)]
			bestSolution = convertSolution(individual=bestSolution)

			if round(prevBestObjective, 5) == round(bestObjective, 5):
				sameBest += 1
				if sameBest >= 1000:
					yourConvergenceTestsHere = False
			else:
				sameBest = 0
			prevBestObjective = bestObjective



			# Call the reporter with:
			#  - the mean objective function value of the population
			#  - the best objective function value of the population
			#  - a 1D numpy array in the cycle notation containing the best solution 
			#    with city numbering starting from 0

			timeLeft = self.reporter.report(meanObjective, bestObjective, bestSolution)
			if timeLeft < 0 or not yourConvergenceTestsHere:
				with open('data/tour50_best.csv', 'a') as fd:
					fd.write(str(bestObjective)+'\n')
				with open('data/tour50_mean.csv', 'a') as fd:
					fd.write(str(meanObjective)+'\n')
				break

		# Your code here.
		return 0

@jit(nopython=True)
def createIndividual(individualSize):
	randOrder = np.random.choice(np.arange(1, individualSize), individualSize-1, replace=False)
	return np.concatenate((np.array([0]), randOrder))

@jit(nopython=True)
def fitness(individual, distanceMatrix):
	score = 0
	for i in np.arange(len(individual)-1):
		score += distanceMatrix[individual[i]][individual[i+1]]
	score += distanceMatrix[individual[-1]][individual[0]]
	return score

@jit(nopython=True)
def fitnessSharing(individual, distanceMatrix, population, beta=0):
	sigma = 0.05*len(individual)**2
	alpha = 0.4
	ds = distances(individual=individual, otherIndividuals=population)
	for d in ds:
		if d <= sigma:
			beta += 1-(d/sigma)**alpha
	fit = fitness(individual=individual, distanceMatrix=distanceMatrix)
	fit = fit*beta**(np.sign(fit))

	return fit

@jit(nopython=True)
def initialize(populationSize, individualSize, distanceMatrix):
	population = np.zeros((populationSize, individualSize), dtype=np.int64)
	idx = 0
	combinations = getCombinations(distanceMatrix=distanceMatrix)
	indices = np.random.choice(np.arange(1, individualSize), min(int(0.1*populationSize), individualSize-2), replace=False)
	while idx < len(indices):
		succ, individual = findNonInf(startNode=indices[idx], previousNodes=np.array([0]), combinations=combinations)
		if not succ:
			individual = createIndividual(individualSize=individualSize)
			individual = LSO(individual=individual, distanceMatrix=distanceMatrix)
		population[idx] = individual
		idx += 1
	while idx < populationSize:
		individual = createIndividual(individualSize=individualSize)
		individualExists = False
		for other in population:
			if np.array_equal(individual, other):
				individualExists = True
				break
		if not individualExists:
			population[idx] = individual
			idx += 1
	return population

@jit(nopython=True)
def select(population, distanceMatrix):
	k = int(0.1*len(population))

	individuals = population[np.random.choice(np.arange(len(population)), k, replace=False)]
	fitnesses = np.zeros(len(individuals))
	for i in range(len(individuals)):
		# fitnesses[i] = fitnessSharing(individual=individuals[i], distanceMatrix=distanceMatrix, population=individuals)
		fitnesses[i] = fitness(individual=individuals[i], distanceMatrix=distanceMatrix)

	best_index = np.argmin(fitnesses)

	return individuals[best_index].copy()

def crossover(i1, i2):
	idx = np.random.choice(np.arange(len(i1)), 1)[0]
	k = int(0.3 * len(i1))

	if idx+k < len(i1):
		o1 = i1[idx:idx+k].copy()
		o2 = i2[idx:idx+k].copy()
	else:
		o1 = np.concatenate((i1[idx:], i1[:k-(len(i1)-idx)]))
		o2 = np.concatenate((i2[idx:], i2[:k-(len(i2)-idx)]))

	o1Mask = ~np.isin(i2, o1)
	o2Mask = ~np.isin(i1, o2)

	o1Rest = i2[o1Mask][:len(i1) - len(o1)]
	o2Rest = i1[o2Mask][:len(i1) - len(o2)]

	o1 = np.concatenate((o1, o1Rest))
	o2 = np.concatenate((o2, o2Rest))

	return o1, o2

@jit(nopython=True)
def mutate(individual, iter):
	alpha = 0.4
	num = np.random.uniform(0.0, 1.0)
	if num <= alpha:
		num = np.random.choice(np.arange(3), 1)[0]
		if iter<50:
			return inverse(individual=individual)
		elif iter<100:
			return shuffle(individual=individual)
		return swap(individual=individual)
	return individual

@jit(nopython=True)
def LSO(individual, distanceMatrix):
	bestIndividual = individual.copy()
	bestFit = fitness(individual=individual, distanceMatrix=distanceMatrix)
	newIndividual = individual.copy()
	for i in np.arange(2, len(individual)):
		newIndividual[i-1], newIndividual[i] = newIndividual[i], newIndividual[i-1]
		newFit = fitness(individual=newIndividual, distanceMatrix=distanceMatrix)
		if newFit > bestFit:
			bestFit = newFit
			bestIndividual = newIndividual
	return bestIndividual

@jit(nopython=True)
def LSO2(individual, distanceMatrix):
	bestIndividual = individual.copy()
	bestFit = fitness(individual=individual, distanceMatrix=distanceMatrix)
	idx = np.random.choice(np.arange(len(individual)))
	newIndividual = individual.copy()
	for i in np.arange(len(individual)):
		newIndividual[idx], newIndividual[i] = newIndividual[i], newIndividual[idx]
		newFit = fitness(individual=newIndividual, distanceMatrix=distanceMatrix)
		if newFit < bestFit:
			newFit = bestFit
			bestIndividual = newIndividual.copy()
	return bestIndividual


@jit(nopython=True)
def elimination(population, size, distanceMatrix):
	populationNew = np.empty((size, len(population[0])), dtype=np.int64)
	fitnesses = np.empty(len(population))
	for i in np.arange(len(population)):
		fitnesses[i] = fitness(individual=population[i], distanceMatrix=distanceMatrix)
	
	while size > 0:
		idx = np.argmin(fitnesses)
		populationNew[size-1] = population[idx].copy()
		population = np.concatenate((population[:idx], population[idx+1:]))
		fitnesses = np.concatenate((fitnesses[:idx], fitnesses[idx+1:]))
		size -= 1

	return populationNew

@jit(nopython=True)
def eliminationSharing(population, populationSize, distanceMatrix):
	populationNew = np.zeros((populationSize, len(population[0])), dtype=np.int64)
	fitnesses = np.zeros(len(population))
	idx = 0
	while idx < populationSize:
		for i in np.arange(len(fitnesses)):
			fitnesses[i] = fitnessSharing(individual=population[i], distanceMatrix=distanceMatrix,
								 population=populationNew[:idx], beta=1)
		bestIdx = np.argmin(fitnesses)
		populationNew[idx] = population[bestIdx]
		idx += 1
		population = np.concatenate((population[:bestIdx], population[bestIdx+1:]))
		fitnesses = np.concatenate((fitnesses[:bestIdx], fitnesses[bestIdx+1:]))
	
	return populationNew

@jit(nopython=True)
def shuffle(individual):
	idx = np.random.choice(np.arange(len(individual)), 1)[0]
	m = int(np.random.uniform(0.2, 1.0)*(len(individual)))

	if idx+m < len(individual):
		individual[idx:idx+m] = np.random.permutation(individual[idx:idx+m])
	else:
		wrapped = np.concatenate((individual[idx:], individual[:m-(len(individual)-idx)]))
		shuffled = np.random.permutation(wrapped)
		individual[idx:] = shuffled[:len(individual)-idx]
		individual[:m-(len(individual)-idx)] = shuffled[len(individual)-idx:]

	return individual

@jit(nopython=True)
def inverse(individual):
	idx = np.random.choice(np.arange(len(individual)), 1)[0]
	m = int(np.random.uniform(0.2, 1.0)*(len(individual)))

	if idx+m < len(individual):
		individual[idx:idx+m] = np.random.permutation(individual[idx:idx+m])
	else:
		wrapped = np.concatenate((individual[idx:], individual[:m-(len(individual)-idx)]))
		inverted = np.flip(wrapped)
		individual[idx:] = inverted[:len(individual)-idx]
		individual[:m-(len(individual)-idx)] = inverted[len(individual)-idx:]

	return individual

@jit(nopython=True)
def swap(individual):
	(idx1, idx2) = np.random.choice(np.arange(len(individual)), 2, replace=False)
	individual[idx1], individual[idx2] = individual[idx2], individual[idx1]

	return individual

@jit(nopython=True)
def distances(individual, otherIndividuals, distanceMatrix):
	ds = np.zeros(len(otherIndividuals), dtype=np.int64)
	for i in np.arange(len(otherIndividuals)):
		ds[i] = np.abs(fitness(individual=individual, distanceMatrix=distanceMatrix)-fitness(individual=otherIndividuals[i], distanceMatrix=distanceMatrix))
	return ds

@jit(nopython=True)
def getCombinations(distanceMatrix):
	combinations = np.empty((distanceMatrix.shape[0], distanceMatrix.shape[0]), dtype=np.int64)
	for i in range(distanceMatrix.shape[0]):
		for j in range(distanceMatrix.shape[0]):
			if not np.isinf(distanceMatrix[i][j]) and i!=j:
				combinations[i][j] = j
			else:
				combinations[i][j] = -1
	return combinations

@jit(nopython=True)
def findNonInf(startNode, previousNodes, combinations):
	followingNodes = np.random.permutation(combinations[startNode][combinations[startNode]!=-1])
	stack = [(startNode, previousNodes, followingNodes)]

	while stack:
		node, prevNodes, nextNodes = stack.pop()
		if len(prevNodes) == len(combinations) - 1:
			if 0 in nextNodes:
				return 1, np.append(prevNodes, node)
			return 0, prevNodes
		for nextNode in nextNodes:
			if nextNode not in prevNodes:
				followingNodes = np.random.permutation(combinations[nextNode][combinations[nextNode]!=-1])
				stack.append((nextNode, np.append(prevNodes, node), followingNodes))
				
	return 0, prevNodes

@jit(nopython=True)
def convertSolution(individual):
	if individual[0] == 0:
		return individual
	
	for i in range(len(individual)):
		if individual[i] == 0:
			idx = i
			break
	individual = np.concatenate((individual[idx:], individual[:idx]))
	return individual

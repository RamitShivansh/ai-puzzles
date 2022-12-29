import random
import matplotlib.pyplot as plt
import time




# Q1. 8 QUEENS PROBLEM
class State8Queen:
    def __init__(self, boardSize = 8, board = None):

        self.n = boardSize
        self.board = board or [0 for _ in range(self.n)]
        self.fitness = self.findFitness()

    def findFitness(self, board = None):

        fitness = 29
        row = [0 for _ in range(8)]
        diag1 = [0 for _ in range(15)]
        diag2 = [0 for _ in range(15)]

        board = board or self.board

        for i in range(self.n):
            
            cur = board[i]
            
            row[cur] += 1
            diag1[cur + i] += 1
            diag2[7 + cur - i] += 1

        for i in row:
            fitness -= (i * (i - 1) // 2)
        for i in diag1:
            fitness -= (i * (i - 1) // 2)
        for i in diag2:
            fitness -= (i * (i - 1) // 2)

        return fitness

    def crossover(self, other, index = None):

        index = index or random.randint(0, self.n - 1)
        return self.board[:index] + other.board[index:]

class GeneticAlgo8Queen:

    def __init__(self, population = 20, mutProb = 0.05, boardSize = 8):

        self.population = population
        self.generation = 0
        self.states = [State8Queen(boardSize) for _ in range(20)]  # initial population size = 20
        self.sumFitness = sum([state.fitness for state in self.states])
        self.maxFitness = max([state.fitness for state in self.states])
        self.bestFitness = 1
        self.bestSolution = self.states[0]

        self.fitness = [1]

        self.mutProb = mutProb
        self.boardSize = boardSize

    def mutate(self, state):

        col = None
        row = None
        maxFit = state.fitness

        for i in range(self.boardSize):
            for j in range(self.boardSize):
                newFit = State8Queen(board=state.board[:i] + [j] + state.board[i+1:]).findFitness()

                if maxFit < newFit:
                    maxFit = newFit
                    col = i
                    row = j
        
        if col == None or row == None:
            state.board[random.randint(0, 7)] = random.randint(0, 7)
            return

        state.board[col] = row
                

    def randomPick(self):
        prob = [i.fitness / self.sumFitness for i in self.states]
        res = random.choices(range(0, len(prob)), weights=prob, k=2)
        return res[0], res[1]

    def reproduce(self, x, y):

        return State8Queen(board=self.states[x].crossover(self.states[y]))

    def nextGen(self):

        children = []

        while len(children) < self.population:
            
            x,y = self.randomPick()
            print(x,y)

            newChild = self.reproduce(x,y)

            if newChild.fitness < 29 and random.random() < self.mutProb:
                self.mutate(newChild)
                newChild.fitness = newChild.findFitness()

            children.append(newChild)

        return children

    def run(self):

        defMutProb = self.mutProb
        mutProbs = [1 / self.mutProb]

        while self.bestFitness < 29:

            self.states = self.nextGen()
            self.sumFitness = sum([state.fitness for state in self.states])
            self.maxFitness = max([state.fitness for state in self.states])

            self.fitness.append(self.maxFitness)
            mutProbs.append(1 / self.mutProb)

            if(self.fitness[-1] == self.fitness[-2]):
                self.mutProb += 0.05
            else:
                self.mutProb = defMutProb
            
            self.generation += 1

            if self.bestFitness < self.maxFitness:
                self.bestFitness = self.maxFitness
                for i in self.states:
                    if self.bestFitness == i.fitness:
                        self.bestSolution = i

            print("\nCurrent Generation:", self.generation, "\tCurrent best fitness:", self.maxFitness)

        print("\nBEST SOLUTION:")
        printBoard(self.bestSolution.board)

        plt.plot(range(self.generation + 1), self.fitness)
        # plt.show()

        return self.generation

def printBoard(state):

    print(state)

    for i in range(8):
        for j in state:
            if j != i:
                print("x", end = " ")
            else:
                print("Q", end = " ")

        print("")






















# Q2. Travelling Salesman Problem

MAX_DIST = 1000

adjList = dict()
adjList['A'] = {'A' : 0, 'B' : MAX_DIST, 'C' : MAX_DIST, 'D' : MAX_DIST, 'E' : MAX_DIST, 'F' : MAX_DIST, 'G' : 0.15, 'H' : MAX_DIST, 'I' : MAX_DIST, 'J' : 0.2, 'K' : MAX_DIST, 'L' : 0.12, 'M' : MAX_DIST, 'N' : MAX_DIST}
adjList['B'] = {'A' : MAX_DIST, 'B' : 0, 'C' : MAX_DIST, 'D' : MAX_DIST, 'E' : MAX_DIST, 'F' : MAX_DIST, 'G' : MAX_DIST, 'H' : 0.19, 'I' : 0.4, 'J' : MAX_DIST, 'K' : MAX_DIST, 'L' : MAX_DIST, 'M' : MAX_DIST, 'N' : 0.13}
adjList['C'] = {'A' : MAX_DIST, 'B' : MAX_DIST, 'C' : 0, 'D' : 0.6, 'E' : 0.22, 'F' : 0.4, 'G' : MAX_DIST, 'H' : MAX_DIST, 'I' : 0.2, 'J' : MAX_DIST, 'K' : MAX_DIST, 'L' : MAX_DIST, 'M' : MAX_DIST, 'N' : MAX_DIST}
adjList['D'] = {'A' : MAX_DIST, 'B' : MAX_DIST, 'C' : 0.6, 'D' : 0, 'E' : MAX_DIST, 'F' : 0.21, 'G' : MAX_DIST, 'H' : MAX_DIST, 'I' : MAX_DIST, 'J' : MAX_DIST, 'K' : 0.3, 'L' : MAX_DIST, 'M' : MAX_DIST, 'N' : MAX_DIST}
adjList['E'] = {'A' : MAX_DIST, 'B' : MAX_DIST, 'C' : 0.22, 'D' : MAX_DIST, 'E' : 0, 'F' : MAX_DIST, 'G' : MAX_DIST, 'H' : MAX_DIST, 'I' : 0.18, 'J' : MAX_DIST, 'K' : MAX_DIST, 'L' : MAX_DIST, 'M' : MAX_DIST, 'N' : MAX_DIST}
adjList['F'] = {'A' : MAX_DIST, 'B' : MAX_DIST, 'C' : 0.4, 'D' : 0.21, 'E' : MAX_DIST, 'F' : 0, 'G' : MAX_DIST, 'H' : MAX_DIST, 'I' : MAX_DIST, 'J' : MAX_DIST, 'K' : 0.37, 'L' : 0.6, 'M' : 0.26, 'N' : 0.9}
adjList['G'] = {'A' : 0.15, 'B' : MAX_DIST, 'C' : MAX_DIST, 'D' : MAX_DIST, 'E' : MAX_DIST, 'F' : MAX_DIST, 'G' : 0, 'H' : MAX_DIST, 'I' : MAX_DIST, 'J' : MAX_DIST, 'K' : 0.55, 'L' : 0.18, 'M' : MAX_DIST, 'N' : MAX_DIST}
adjList['H'] = {'A' : MAX_DIST, 'B' : 0.19, 'C' : MAX_DIST, 'D' : MAX_DIST, 'E' : MAX_DIST, 'F' : MAX_DIST, 'G' : MAX_DIST, 'H' : 0, 'I' : MAX_DIST, 'J' : 0.56, 'K' : MAX_DIST, 'L' : MAX_DIST, 'M' : MAX_DIST, 'N' : 0.17}
adjList['I'] = {'A' : MAX_DIST, 'B' : 0.4, 'C' : 0.2, 'D' : MAX_DIST, 'E' : 0.18, 'F' : MAX_DIST, 'G' : MAX_DIST, 'H' : MAX_DIST, 'I' : 0, 'J' : MAX_DIST, 'K' : MAX_DIST, 'L' : MAX_DIST, 'M' : MAX_DIST, 'N' : 0.6}
adjList['J'] = {'A' : 0.2, 'B' : MAX_DIST, 'C' : MAX_DIST, 'D' : MAX_DIST, 'E' : MAX_DIST, 'F' : MAX_DIST, 'G' : MAX_DIST, 'H' : 0.56, 'I' : MAX_DIST, 'J' : 0, 'K' : MAX_DIST, 'L' : 0.16, 'M' : MAX_DIST, 'N' : 0.5}
adjList['K'] = {'A' : MAX_DIST, 'B' : MAX_DIST, 'C' : MAX_DIST, 'D' : 0.3, 'E' : MAX_DIST, 'F' : 0.37, 'G' : 0.55, 'H' : MAX_DIST, 'I' : MAX_DIST, 'J' : MAX_DIST, 'K' : 0, 'L' : MAX_DIST, 'M' : 0.24, 'N' : MAX_DIST}
adjList['L'] = {'A' : 0.12, 'B' : MAX_DIST, 'C' : MAX_DIST, 'D' : MAX_DIST, 'E' : MAX_DIST, 'F' : 0.6, 'G' : 0.18, 'H' : MAX_DIST, 'I' : MAX_DIST, 'J' : 0.16, 'K' : MAX_DIST, 'L' : 0, 'M' : 0.4, 'N' : MAX_DIST}
adjList['M'] = {'A' : MAX_DIST, 'B' : MAX_DIST, 'C' : MAX_DIST, 'D' : MAX_DIST, 'E' : MAX_DIST, 'F' : 0.26, 'G' : MAX_DIST, 'H' : MAX_DIST, 'I' : MAX_DIST, 'J' : MAX_DIST, 'K' : 0.24, 'L' : 0.4, 'M' : 0, 'N' : MAX_DIST}
adjList['N'] = {'A' : MAX_DIST, 'B' : 0.13, 'C' : MAX_DIST, 'D' : MAX_DIST, 'E' : MAX_DIST, 'F' : 0.9, 'G' : MAX_DIST, 'H' : 0.17, 'I' : 0.6, 'J' : 0.5, 'K' : MAX_DIST, 'L' : MAX_DIST, 'M' : MAX_DIST, 'N' : 0}

def findPathLength(path):

    global adjList

    pathLength = 0

    for i in range(len(path) - 1):
        pathLength += adjList[path[i]][path[i + 1]]

    pathLength += adjList[path[-1]][path[0]]

    return pathLength

class StateTSP:

    def __init__(self, numCities = 14, path = None):
        self.n = numCities
        self.path = path or [chr(i + 65) for i in range(self.n)]
        # self.path.append('A')
        self.fitness = self.findFitness()

    def findFitness(self):
        return 1 / findPathLength(self.path)

class GeneticAlgoTSP:

    def __init__(self, population = 20, mutProb = 0.05, pathLength = 14):
        self.population = population
        self.generation = 0
        self.states = [StateTSP() for _ in range(20)]
        self.sumFitness = sum([state.fitness for state in self.states])
        self.maxFitness = max([state.fitness for state in self.states])
        self.bestFitness = self.states[0].fitness
        self.bestSolution = self.states[0].path

        self.fitnessGraph = [self.states[0].fitness]

        self.mutProb = mutProb
        self.pathLength = pathLength

    def mutate(self, state):
        x, y = 0,0
        minDist = findPathLength(state.path)

        for i in range(len(state.path)):
            for j in range(i + 1, len(state.path)):
                state.path[i], state.path[j] = state.path[j], state.path[i]
                newDist = findPathLength(state.path)
                if abs(newDist - minDist) > 0.001 and newDist < minDist:
                    minDist = newDist
                    x,y = i,j
                state.path[i], state.path[j] = state.path[j], state.path[i]

        if x == y:
            for _ in range(random.randint(1, int(self.mutProb // 0.05))):
                indexes = random.sample(range(self.pathLength), 2)
                state.path[indexes[0]], state.path[indexes[1]] = state.path[indexes[1]], state.path[indexes[0]]
            return

        state.path[x], state.path[y] = state.path[y], state.path[x]        


    def randomPick(self):
        
        prob = [i.fitness / self.sumFitness for i in self.states]
        res = random.choices(range(len(prob)), weights=prob, k=2)
        return res[0], res[1]

    def reproduce(self, x, y):

        bestChild = self.states[x].path
        bestFit = max(self.states[x].fitness, self.states[y].fitness)
        
        for i in range(len(self.states[x].path)):
            for j in range(i, len(self.states[x].path)):
                childPath = ['_' for _ in range(self.pathLength)]
                childPath[i:j + 1] = self.states[x].path[i:j + 1]

                childPathIndex = 0
                
                for k in self.states[y].path:
                    if i == childPathIndex:
                        childPathIndex = j + 1
                    if k not in childPath:
                        childPath[childPathIndex] = k
                        childPathIndex += 1

                childPathFitness = 1 / findPathLength(childPath)

                if childPathFitness > bestFit:
                    bestChild = childPath
                    bestFit = childPathFitness


        if bestChild != self.states[x].path and bestChild != self.states[y].path:
            return StateTSP(path=bestChild)
        
        a = random.randint(0, self.pathLength - 1)
        b = random.randint(a, self.pathLength - 1)

        childPath = ['_' for _ in range(self.pathLength)]

        childPath[a:b+1] = self.states[x].path[a:b+1]

        childPathIndex = 0
        
        for i in self.states[y].path:
            if a == childPathIndex:
                childPathIndex = b + 1
            if i not in childPath:
                childPath[childPathIndex] = i
                childPathIndex += 1

        assert '_' not in childPath

        return StateTSP(path=childPath)

    def nextGen(self):

        children = []

        while len(children) < self.population:
            
            x, y = self.randomPick()

            newChild = self.reproduce(x, y)

            if random.random() < self.mutProb:
                self.mutate(newChild)
                newChild.fitness = newChild.findFitness()

            children.append(newChild)

        return children

    def run(self):

        defMutProb = self.mutProb

        while self.generation < 1000:
            self.states = self.nextGen()
            
            self.sumFitness = sum([state.fitness for state in self.states])
            
            maxFitChild = self.states[0].path
            self.maxFitness = self.states[0].fitness

            for i in self.states:
                if i.fitness > self.maxFitness:
                    self.maxFitness = i.fitness
                    maxFitChild = i.path

            if self.maxFitness > self.bestFitness:
                self.bestSolution = maxFitChild
                self.bestFitness = self.maxFitness

            self.fitnessGraph.append(self.maxFitness)

            if(self.fitnessGraph[-1] == self.fitnessGraph[-2]):
                self.mutProb += 0.05
            else:
                self.mutProb = defMutProb


            self.generation += 1

            print("\nCurrent Generation:", self.generation, "\tCurrent best fitness:", self.maxFitness)

        print("\nBEST SOLUTION:")
        print(self.bestSolution, "\tDISTANCE:", 1 / self.bestFitness)

        plt.plot(range(self.generation + 1), self.fitnessGraph)
        # plt.show()

        return self.generation













if __name__ == "__main__":
   
    # GeneticAlgo8Queen(50, 0.25).run()
    # GeneticAlgoTSP().run()

    a = input("Enter 1 for 8 Queens and 2 for TSP: ")

    if a == '1':
        st = time.time()
        GeneticAlgo8Queen(20, 0.6).run()
        print("\n\nTime taken:", time.time() - st)
    elif a == '2':
        st = time.time()
        GeneticAlgoTSP(40, 0.1).run()
        print("\n\nTime taken:", time.time() - st)
    else:
        print("Invalid Input")
        exit(0)

    plt.xlabel("Generations")
    plt.ylabel("Fitness")
    plt.title("Improved Algorithm")
    plt.show()
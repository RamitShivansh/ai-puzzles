from GeneticAlgorithm import GeneticAlgorithm
from NQueensPuzzle.StateNQueen import StateNQueen
import random

size = 8
pop = 50
gen = 10000
boards = [[i for i in range(size)] for _ in range(pop)]
for i in boards:
    random.shuffle(i)
states = [StateNQueen(size, board=i) for i in boards]

GeneticAlgorithm().run(states, gen, 0, 100, 0.25, 1, 0.25)
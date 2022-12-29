from commons.State import State
from math import sqrt, pow
import random

class GeneticAlgorithm:
    def pick(self, n: int, wts: list = None):
        """pick n pairs of states for crossover.

        Parameters
        ----------
        n: int
            number of pairs to form
        wts: list
            weights for corresponding state. if empty
            list is given, the selections are made 
            with equal probability.

        Returns
        -------
        list of k states which are to be crossed.
        """
        wts = wts or [i.f / self.sum_fit for i in self.states]
        m = random.choices(range(len(wts)), weights=wts, k=n)
        f = random.choices(range(len(wts)), weights=wts, k=n)

        return [(i, j) for i, j in zip(m, f)]
    
    def next_gen(self, mut_prob: float, population: int):
        """create next generation by randomly picking and
        crossing over states from current generation. randomly
        mutate some of the states in new generation based on 
        mutProb.

        Parameters
        ----------
        mut_prob: float
            probability of mutation
        population: int
            population of the new generation

        Returns
        -------
        a list of all states of the new generation. 
        """
        parents = self.pick(population)
        children = [self.states[x].crossover(self.states[y]) for x, y in parents]
        children = [child.mutate() if random.random() < mut_prob else child for child in children]
        return children

    def run(self, init_states: list[State], max_gen: int, max_fit: float, max_pop: int, mut_prob: float, pop_growth: float = 1.0, mut_prob_growth: float = 0.05):
        """find optimal solution

        Parameters
        ----------
        init_states: list[T]
            1st generation
        max_gen: int
            maximum generations to run in case desired fitness is not found.
        max_fit: float
            desired fitness wanted.
        max_pop: int
            maximum allowed population
        mut_prob: float
            probability of mutation
        pop_growth: float
            factor by which population should grow/decline every generation.
        mut_prob_growth: float
            factor by which population should grow/decline every generation.

        Returns
        -------
        Number of generations the code ran for.
        """
        self.states = None
        cur_max_fit = None
        fits = [max([state.f for state in init_states])]
        mp = mut_prob
        for gen in range(max_gen + 1):
            self.states = self.next_gen(
                mut_prob=mp,
                population=int(min(max_pop, pop_growth * len(self.states)))
            ) if gen > 0 else init_states
            self.sum_fit = sum([state.f for state in self.states])
            cur_max_fit = max([state.f for state in self.states])

            fits.append(cur_max_fit)
            if cur_max_fit == fits[-2]:
                mut_prob += mut_prob_growth
            else:
                mp = mut_prob

            avg_fit = self.sum_fit / len(self.states)
            print(
                "Generation: {:{w1}} | Population: {:5d} | Average Fitness: {:{w2}.2f} | Max Fitness: {:{w2}.2f} | Standard Deviation: {:{w2}.2f}"\
                    .format(
                        gen, 
                        len(self.states),
                        avg_fit, 
                        cur_max_fit, 
                        sqrt(sum([pow((i.f - avg_fit), 2) for i in self.states]) / len(self.states)),
                        w1 = len(str(max_gen)), 
                        w2 = 10
                    )
            )

            if cur_max_fit == max_fit:
                print("Found best state in {} generations".format(gen))
                best_state = [i for i in self.states if i.f == cur_max_fit][0]
                print("Following is the best state")
                print(best_state)
                return gen

        
        print("Could not find best state in {} generations".format(gen))
        best_state = [i for i in self.states if i.f == cur_max_fit][0]
        print("Following is the best state in the latest generation:")
        print(best_state)
            
        return max_gen
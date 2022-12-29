class State:
    """This interface is to represent states of 
    genetic algorithm. Implement these methods so that
    it can be plugged into the genetic algo code.
    """
    def fitness(self, other=None, alt=None) -> int:
        """find fitness of the state

        Parameters
        ----------
        other: representation of the state
            pass this if you want to calculate fitness of some
            other state without initialising an object.
        alt: function
            call this function to calculate fitness if specified
        
        Returns
        -------
        an integer that represent current fitness.
        more the fitness, the larger the result.
        """
        pass

    def crossover(self, other: 'State') -> 'State':
        """defines how to cross states for reproduction.

        Parameters
        ----------
        others: State
            other state to crossover with

        Returns
        -------
        a new state with properties of both self and other
        """
        pass

    def mutate(self) -> 'State':
        """change a property of the state,
        randomly or based on some heuristic.
        """
        pass
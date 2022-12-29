from commons.State import State
import random

class StateNQueen(State):
    """defines how n queens are positioned on a chess board.

    Representation
    --------------
    The state is represented in form of a list. Every index of the 
    list indicates a column and every element of the list is an 
    integer indicating the row number of the queen. For example:-
    [0, 1, 2, 3] represents 4 queen present along the diagonal of a
    4x4 chessboard.
    """
    def __init__(self, board_size: int = 8, board: list[int] = None):
        # size of the board
        self.n = board_size
        # the board
        self.board = board or [0 for _ in range(self.n)]
        # current fitness
        self.f = self.fitness()

    def fitness(self, other = None) -> int:
        """fitness is the negative of number of pairs of queens
        clashing on the board. 0 is the highest achievable number.
        """
        board = self.board
        n = self.n
        if other is not None:
            board = other
            n = len(board)
        # number of clashing pairs of queens
        clashing = 0

        # count of queens in that particular row or diagonal
        row = [0 for _ in range(n)]
        d1 = [0 for _ in range(2 * n - 1)]
        d2 = [0 for _ in range(2 * n - 1)]

        for i, cur in enumerate(board):
            row[cur] += 1
            d1[cur + i] += 1
            d2[n - 1 + cur - i] += 1

        for i in [row, d1, d2]:
            for j in i:
                clashing += (j * (j - 1) // 2)

        return -clashing

    def mutate(self) -> 'State':
        """
        Find the best neighbor of the current state. If the current state
        is a local maxima, randomly mutate it.
        """
        col = None
        row = None
        max_fit = self.f

        for i in range(self.n):
            for j in range(self.n):
                new_fit = self.fitness(
                    other=self.board[:i] + [j] + self.board[i+1:])
                if max_fit < new_fit:
                    col = i
                    row = j
                    max_fit = new_fit

        # if no neighbors with better fitness is found, randomly mutate it
        if col == None or row == None:
            if random.random() < 0.5:
                x = [i for i in range(self.n)]
                random.shuffle(x)
                return StateNQueen(self.n, board=x)
            col = random.randint(0, self.n - 1)
            row = random.randint(0, self.n - 1)
        res = StateNQueen(self.n, board=self.board[:col] + [row] + self.board[col+1:])
        return res


    def crossover(self, other: State) -> State:
        """
        Randomly choose an integer x in range [0, n) and concatenate
        A[:x] and B[x:]. This becomes the child of A and B.
        """
        index = random.randint(0, self.n - 1)
        return StateNQueen(self.n, self.board[:index] + other.board[index:])

    def __repr__(self) -> str:
        res = str(self.board) + "\n"

        for i in range(self.n):
            for j in self.board:
                if j != i:
                    res += "x "
                else:
                    res += "Q "
            res += "\n"
        res += "Fitnes: {}".format(self.f)

        return res
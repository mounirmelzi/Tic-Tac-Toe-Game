import copy
import time
import random
random.seed(time.time() * (10**4))



class Board():
    def __init__(self, startingBoard=None):
        if startingBoard is None:
            self.board = [[None, None, None] for _ in range(3)] # Empty board
        else:
            self.board = startingBoard


    def isEmpty(self):
        return all(self.board[i][j] == None for i in range(3) for j in range(3))


    def isFull(self):
        return all(self.board[i][j] != None for i in range(3) for j in range(3))


    def valideMoves(self):
        return [(i, j) for i in range(3) for j in range(3) if self.board[i][j] is None]


    def isFree(self, i, j):
        return self.board[i][j] is None


    def insert(self, symbole, i, j):
        self.board[i][j] = symbole


    def print(self):
        print("+---------+")
        for i in range(3):
            print("   |   |   ")
            for j in range(3):
                if self.board[i][j] is not None:
                    print(f" {self.board[i][j]} ", end="")
                else:
                    print(f"   ", end="")
                if j != 2:
                    print("|", end="")
            print("\n   |   |   ")
            print("+---------+")



class Game:
    def __init__(self, player1=None, player2=None):
        self.board: Board = Board() # Empty board
        self.player1: Player | AIplayer = player1
        self.player2: Player | AIplayer = player2
        self.currentPlayer: Player | AIplayer = random.choice([player1, player2])


    def isEnd(self):
        if self.board.isFull():
            return True
        if self.player1.isWinner(self):
            return True
        if self.player2.isWinner(self):
            return True
        return False


    def playMove(self, x=None, y=None):
        if x is None and y is None:
            i, j = self.currentPlayer.chooseMove(self)
        else:
            i, j = x, y
        self.currentPlayer.playMove(self, i, j)

        # Update current player
        if self.currentPlayer == self.player1:
            self.currentPlayer = self.player2
        else:
            self.currentPlayer = self.player1

        return (i, j)



class Player:
    def __init__(self, name, symbole, maximizing):
        self.name: str = name
        self.symbole: str = symbole
        self.maximizing = maximizing


    def __eq__(self, other):
        return self.name == other.name


    def chooseMove(self, game: Game):
        print(f"{self.name} it's your turn to choose your next move where you put {self.symbole}:")
        while True:
            try:
                i = int(input("Enter line number (0-2): "))
                j = int(input("Enter column number (0-2): "))
                if (0 <= i <= 2) and (0 <= j <= 2) and game.board.isFree(i, j):
                    return (i, j)
                else:
                    print("You have choosed invalid move!")
            except:
                print("Error! Enter an integer ...")
            
    
    def playMove(self, game: Game, i, j):
        if not game.board.isFree(i, j):
            return False
        game.board.insert(self.symbole, i, j)
        return True


    def isWinner(self, game: Game):
        return(
            any(all(game.board.board[i][j] == self.symbole for j in range(3)) for i in range(3))
            or
            any(all(game.board.board[i][j] == self.symbole for i in range(3)) for j in range(3))
            or
            (game.board.board[0][0] == self.symbole and game.board.board[1][1] == self.symbole and game.board.board[2][2] == self.symbole)
            or
            (game.board.board[0][2] == self.symbole and game.board.board[1][1] == self.symbole and game.board.board[2][0] == self.symbole)
        )



class AIplayer(Player):
    def __init__(self, symbole, name="AI-Player", maximizing=None, level=0):
        super().__init__(name, symbole, maximizing)
        self.level = level


    def __randomChoice(self, game: Game):
        return random.choice(game.board.valideMoves())


    def __minimax(self, game: Game, maximizing: bool) -> tuple[int, tuple[int, int]]:
        if self == game.player1:
            other = game.player2
        else:
            other = game.player1

        # base cases:
        if self.isWinner(game):
            if self.maximizing:
                return 1, None
            else:
                return -1, None
        elif other.isWinner(game):
            if other.maximizing:
                return 1, None
            else:
                return -1, None
        elif game.board.isFull():
            return 0, None

        valideMoves = game.board.valideMoves()

        # rec call:
        if maximizing:
            bestMove = None
            maxEval = -100
            for move in valideMoves:
                tempGame = copy.deepcopy(game)
                if self.maximizing:
                    self.playMove(tempGame, *move)
                else:
                    other.playMove(tempGame, *move)
                eval = self.__minimax(tempGame, False)[0]

                if eval == 1:
                    return eval, move

                if eval > maxEval:
                    maxEval = eval
                    bestMove = move
            return maxEval, bestMove
        else:
            bestMove = None
            minEval = 100
            for move in valideMoves:
                tempGame = copy.deepcopy(game)
                if not self.maximizing:
                    self.playMove(tempGame, *move)
                else:
                    other.playMove(tempGame, *move)
                eval = self.__minimax(tempGame, True)[0]

                if eval == -1:
                    return eval, move

                if eval < minEval:
                    minEval = eval
                    bestMove = move
            return minEval, bestMove


    def chooseMove(self, game):
        game = copy.deepcopy(game)
        for _ in range(5):
            rand = random.randint(1, 100)

        if self.level == 1:
            if rand < 70: # 70%
                eval = "<random>"
                move = self.__randomChoice(game)
            else: # 30%
                eval, move = self.__minimax(game, self.maximizing)
        
        elif self.level == 2:
            if rand < 40: # 40%
                eval = "<random>"
                move = self.__randomChoice(game)
            else: # 60%
                eval, move = self.__minimax(game, self.maximizing)

        elif self.level == 3:
            if rand < 10: # 10%
                eval = "<random>"
                move = self.__randomChoice(game)
            else: # 90%
                eval, move = self.__minimax(game, self.maximizing)

        return move

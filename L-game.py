import os
import math

class LGame:
    def __init__(self):
        self.grid = [['0' for _ in range(4)] for _ in range(4)]
        self.p1Pos = [(0, 2), (1, 2), (0, 1), (2, 2)]
        self.placePiece(self.p1Pos, 'L1')
        self.p2Pos = [(1, 1), (2, 1), (3, 1), (3, 2)] 
        self.placePiece(self.p2Pos, 'L2')
        self.neutralPieces = [(0, 0), (3, 3)]
        self.placeNeutralPieces()
        self.lPositions = {
            'N': [(0, 0), (1, 0), (2, 0), (2, 1)],
            'NM': [(0, 1), (1, 1), (2, 1), (2, 0)],
            'E': [(0, 0), (0, 1), (0, 2), (1, 0)],
            'EM': [(0, 0), (0, 1), (0, 2), (1, 2)],
            'S': [(0, 1), (0, 0), (1, 1), (2, 1)],
            'SM': [(0, 0), (1, 0), (2, 0), (2, -1)],
            'W': [(0, 2), (1, 0), (1, 1), (1, 2)],
            'WM': [(0, 0), (1, 0), (1, 1), (1, 2)],
        }
        self.currentPlayer = 'L1'
        self.p1Type = None
        self.p2Type = None
        self.aiDepth = None

    def clearScreen(self):
        os.system('cls' if os.name == 'nt' else 'clear')

    def isValidMove(self, positions):
        for x, y in positions:
            if not (0 <= x < 4 and 0 <= y < 4):
                return False
            if self.grid[x][y] != '0':
                return False
        return True

    def genLegalMoves(self, player):
        currPos = self.p1Pos if player == 'L1' else self.p2Pos
        for x, y in currPos:
            self.grid[x][y] = '0'
        legalMoves = []
        for i in range(4):
            for j in range(4):
                for pos in self.lPositions.values():
                    newPos = [(i + dx, j + dy) for dx, dy in pos]
                    if self.isValidMove(newPos):
                        legalMoves.append(newPos)
        for x, y in currPos:
            self.grid[x][y] = player
        legalMoves = [move for move in legalMoves if move != currPos]
        return legalMoves

    def placePiece(self, positions, player):
        for x, y in positions:
            self.grid[x][y] = player

    def removePiece(self, positions):
        for x, y in positions:
            self.grid[x][y] = '0'

    def placeNeutralPieces(self):
        for x, y in self.neutralPieces:
            self.grid[x][y] = 'N'

    def printGrid(self):
        self.clearScreen()
        for row in self.grid:
            print(" | ".join(f"{cell:2}" for cell in row))
            print("-" * 17)

    def startGame(self):
        while True:
            mode = input("Select mode: (1) Human vs Human, (2) Human vs Computer, (3) Computer vs Computer: ")
            if mode in ['1', '2', '3']:
                break
        if mode == '1':
            self.p1Type = 'human'
            self.p2Type = 'human'
        elif mode == '2':
            self.p1Type = 'human'
            self.p2Type = 'ai'
        else:
            self.p1Type = 'ai'
            self.p2Type = 'ai'

        first = input("Who goes first? Enter '1' for Player1, '2' for Player2: ")
        if first == '2':
            self.currentPlayer = 'L2'
        else:
            self.currentPlayer = 'L1'

        if self.p1Type == 'ai' or self.p2Type == 'ai':
            d = input("Enter search depth (e.g. 3): ")
            if d.isdigit():
                self.aiDepth = int(d)
            else:
                self.aiDepth = 3

        self.printGrid()

        while True:
            legalMoves = self.genLegalMoves(self.currentPlayer)
            if not legalMoves:
                winner = 'L2' if self.currentPlayer == 'L1' else 'L1'
                print(f"No legal moves left for {self.currentPlayer}. {winner} wins!")
                break
            print(f"Current Player: {self.currentPlayer}")
            cType = self.p1Type if self.currentPlayer == 'L1' else self.p2Type
            if cType == 'human':
                print("Legal moves (choose a number):")
                for idx, move in enumerate(legalMoves):
                    print(f"{idx}: {move}")
                userInput = input("Enter move index or 'q' to quit: ")
                if userInput.lower() == 'q':
                    print("Quitting the game.")
                    break
                if not userInput.isdigit():
                    continue
                moveIndex = int(userInput)
                if moveIndex < 0 or moveIndex >= len(legalMoves):
                    continue
                chosenMove = legalMoves[moveIndex]
            else:
                chosenMove = self.chooseAiMoveMinimax(legalMoves, self.currentPlayer, self.aiDepth)
            self.makeMove(chosenMove)
            self.printGrid()
            self.moveNeutralPiece()
            self.printGrid()
            self.currentPlayer = 'L2' if self.currentPlayer == 'L1' else 'L1'

    def makeMove(self, newPositions):
        oldPositions = self.p1Pos if self.currentPlayer == 'L1' else self.p2Pos
        self.removePiece(oldPositions)
        self.placePiece(newPositions, self.currentPlayer)
        if self.currentPlayer == 'L1':
            self.p1Pos = newPositions
        else:
            self.p2Pos = newPositions

    def moveNeutralPiece(self):
        cType = self.p1Type if self.currentPlayer == 'L1' else self.p2Type
        if cType == 'human':
            if not self.neutralPieces:
                return
            print("Would you like to move a neutral piece? Enter 'no' to skip or the index.")
            for i, pos in enumerate(self.neutralPieces):
                print(f"{i}: {pos}")
            choice = input("Your choice: ")
            if choice.lower() == 'no':
                return
            if not choice.isdigit():
                return
            pieceIndex = int(choice)
            if pieceIndex < 0 or pieceIndex >= len(self.neutralPieces):
                return
            while True:
                coordsInput = input("Enter new coordinates for the neutral piece (x,y) or 'no' to skip: ")
                if coordsInput.lower() == 'no':
                    return
                try:
                    xStr, yStr = coordsInput.split(',')
                    x, y = int(xStr.strip()), int(yStr.strip())
                except (ValueError, IndexError):
                    continue
                if 0 <= x < 4 and 0 <= y < 4 and self.grid[x][y] == '0':
                    oldPos = self.neutralPieces[pieceIndex]
                    self.grid[oldPos[0]][oldPos[1]] = '0'
                    self.grid[x][y] = 'N'
                    self.neutralPieces[pieceIndex] = (x, y)
                    break
        else:
            if not self.neutralPieces:
                return
            aiMove = self.chooseAiNeutralMove()
            if aiMove is not None:
                pieceIndex, newX, newY = aiMove
                oldPos = self.neutralPieces[pieceIndex]
                self.grid[oldPos[0]][oldPos[1]] = '0'
                self.grid[newX][newY] = 'N'
                self.neutralPieces[pieceIndex] = (newX, newY)

    def chooseAiMoveMinimax(self, legalMoves, player, depth):
        opponent = 'L1' if player == 'L2' else 'L2'
        bestMove = None
        bestValue = -math.inf
        alpha = -math.inf
        beta = math.inf
        originalGrid = [row[:] for row in self.grid]
        originalP1Pos = self.p1Pos[:]
        originalP2Pos = self.p2Pos[:]
        originalNeutrals = self.neutralPieces[:]
        for move in legalMoves:
            self.simulateMove(player, move)
            value = self.minimax(opponent, depth - 1, alpha, beta, maximizing=(opponent == 'L2'))
            self.restoreState(originalGrid, originalP1Pos, originalP2Pos)
            self.neutralPieces = originalNeutrals[:]
            if value > bestValue:
                bestValue = value
                bestMove = move
            alpha = max(alpha, value)
            if beta <= alpha:
                break
        return bestMove

    def minimax(self, player, depth, alpha, beta, maximizing):
        if depth == 0:
            return self.heuristicEvaluation()
        legalMoves = self.genLegalMoves(player)
        if not legalMoves:
            return self.heuristicEvaluation()
        opponent = 'L1' if player == 'L2' else 'L2'
        originalGrid = [row[:] for row in self.grid]
        originalP1Pos = self.p1Pos[:]
        originalP2Pos = self.p2Pos[:]
        originalNeutrals = self.neutralPieces[:]
        if maximizing:
            value = -math.inf
            for move in legalMoves:
                self.simulateMove(player, move)
                score = self.minimax(opponent, depth - 1, alpha, beta, maximizing=(opponent=='L2'))
                self.restoreState(originalGrid, originalP1Pos, originalP2Pos)
                self.neutralPieces = originalNeutrals[:]
                value = max(value, score)
                alpha = max(alpha, value)
                if beta <= alpha:
                    break
            return value
        else:
            value = math.inf
            for move in legalMoves:
                self.simulateMove(player, move)
                score = self.minimax(opponent, depth - 1, alpha, beta, maximizing=(opponent=='L2'))
                self.restoreState(originalGrid, originalP1Pos, originalP2Pos)
                self.neutralPieces = originalNeutrals[:]
                value = min(value, score)
                beta = min(beta, value)
                if beta <= alpha:
                    break
            return value

    def simulateMove(self, player, move):
        oldPositions = self.p1Pos if player == 'L1' else self.p2Pos
        self.removePiece(oldPositions)
        self.placePiece(move, player)
        if player == 'L1':
            self.p1Pos = move
        else:
            self.p2Pos = move

    def heuristicEvaluation(self):
        l1Moves = len(self.genLegalMoves('L1'))
        l2Moves = len(self.genLegalMoves('L2'))
        return l2Moves - l1Moves

    def chooseAiNeutralMove(self):
        player = self.currentPlayer
        opponent = 'L1' if player == 'L2' else 'L2'
        bestMove = None
        bestScore = self.evaluateOpponentMoves(opponent)
        originalNeutrals = self.neutralPieces[:]
        originalGrid = [row[:] for row in self.grid]
        originalP1Pos = self.p1Pos[:]
        originalP2Pos = self.p2Pos[:]
        for i, (nx, ny) in enumerate(self.neutralPieces):
            self.grid[nx][ny] = '0'
            for x in range(4):
                for y in range(4):
                    if self.grid[x][y] == '0':
                        self.grid[x][y] = 'N'
                        self.neutralPieces[i] = (x, y)
                        newScore = self.evaluateOpponentMoves(opponent)
                        if newScore < bestScore:
                            bestScore = newScore
                            bestMove = (i, x, y)
                        self.grid[x][y] = '0'
                        self.neutralPieces[i] = (nx, ny)
            self.grid[nx][ny] = 'N'
        self.restoreState(originalGrid, originalP1Pos, originalP2Pos)
        self.neutralPieces = originalNeutrals
        return bestMove

    def evaluateOpponentMoves(self, opponent):
        return len(self.genLegalMoves(opponent))

    def restoreState(self, originalGrid, originalP1Pos, originalP2Pos):
        for i in range(4):
            for j in range(4):
                self.grid[i][j] = originalGrid[i][j]
        self.p1Pos = originalP1Pos[:]
        self.p2Pos = originalP2Pos[:]

if __name__ == "__main__":
    game = LGame()
    game.startGame()

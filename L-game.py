import os

class LGame:
    def __init__(self):
        # Initialize an empty 4x4 grid
        self.grid = [['0' for _ in range(4)] for _ in range(4)]
        
        # Setting initial positions for L1 and L2
        self.p1Pos = [(0, 0), (0, 1), (0, 2), (1, 0)]
        self.placePiece(self.p1Pos, 'L1')

        self.p2Pos = [(3, 3), (3, 2), (3, 1), (2, 3)]
        self.placePiece(self.p2Pos, 'L2')

        # Neutral pieces
        self.neutralPieces = [(1, 1), (2, 2)]
        self.placeNeutralPieces()

        # Possible L configurations
        self.LPositions = {
            'N':  [(0, 0), (1, 0), (2, 0), (2, 1)],   # North
            'NM': [(0, 1), (1, 1), (2, 1), (2, 0)],   # North-Mirrored
            'E':  [(0, 0), (0, 1), (0, 2), (1, 0)],   # East
            'EM': [(0, 0), (0, 1), (0, 2), (1, 2)],   # East-Mirrored
            'S':  [(0, 1), (0, 0), (1, 1), (2, 1)],   # South
            'SM': [(0, 0), (1, 0), (2, 0), (2, -1)],  # South-Mirrored
            'W':  [(0, 2), (1, 0), (1, 1), (1, 2)],   # West
            'WM': [(0, 0), (1, 0), (1, 1), (1, 2)],   # West-Mirrored
        }

        self.currentPlayer = 'L1'
        self.opponentType = None  # Will be set when starting the game (human or ai)

    def clear_screen(self):
        # Clears the terminal screen.
        os.system('cls' if os.name == 'nt' else 'clear')

    def isValidMove(self, positions):
        for x, y in positions:
            if not (0 <= x < 4 and 0 <= y < 4):
                return False
            if self.grid[x][y] != '0':
                return False
        return True

    def genLegalMoves(self, player):
        if player == 'L1':
            currPos = self.p1Pos
        else:
            currPos = self.p2Pos

        # Temporarily remove player's L
        for x, y in currPos:
            self.grid[x][y] = '0'

        legalMoves = []
        # Generate all possible placements
        for i in range(4):
            for j in range(4):
                for pos in self.LPositions.values():
                    newPos = [(i + dx, j + dy) for dx, dy in pos]
                    if self.isValidMove(newPos):
                        legalMoves.append(newPos)

        # Restore player's L
        for x, y in currPos:
            self.grid[x][y] = player

        # Remove the current position from legal moves
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
        self.clear_screen()  # Clear terminal before printing
        for row in self.grid:
            print(" | ".join(f"{cell:2}" for cell in row))
            print("-" * 17)

    def startGame(self):
        # Ask if opponent is human or ai
        while True:
            choice = input("Do you want to play against a 'human' or 'ai'? ")
            if choice.lower() in ['human', 'ai']:
                self.opponentType = choice.lower()
                break
            else:
                print("Invalid choice. Please type 'human' or 'ai'.")

        self.printGrid()

        while True:
            legalMoves = self.genLegalMoves(self.currentPlayer)
            
            if not legalMoves:
                # No moves for current player means the other player wins
                winner = 'L2' if self.currentPlayer == 'L1' else 'L1'
                print(f"No legal moves left for {self.currentPlayer}. {winner} wins!")
                break

            print(f"Current Player: {self.currentPlayer}")

            if self.currentPlayer == 'L1':
                # Player 1 (human)
                print("Legal moves (choose a number):")
                for idx, move in enumerate(legalMoves):
                    print(f"{idx}: {move}")
                
                user_input = input("Enter move index or 'q' to quit: ")
                if user_input.lower() == 'q':
                    print("Quitting the game. Thanks for playing!")
                    break

                if not user_input.isdigit():
                    print("Invalid input. Please enter a number.")
                    continue

                move_index = int(user_input)
                if move_index < 0 or move_index >= len(legalMoves):
                    print("Index out of range. Choose a valid move index.")
                    continue

                chosen_move = legalMoves[move_index]
            else:
                # Player 2 (could be human or AI)
                if self.opponentType == 'human':
                    print("Legal moves (choose a number):")
                    for idx, move in enumerate(legalMoves):
                        print(f"{idx}: {move}")

                    user_input = input("Enter move index or 'q' to quit: ")
                    if user_input.lower() == 'q':
                        print("Quitting the game. Thanks for playing!")
                        break

                    if not user_input.isdigit():
                        print("Invalid input. Please enter a number.")
                        continue

                    move_index = int(user_input)
                    if move_index < 0 or move_index >= len(legalMoves):
                        print("Index out of range. Choose a valid move index.")
                        continue

                    chosen_move = legalMoves[move_index]

                else:
                    # AI logic: pick the move that leads to minimal subsequent moves for opponent
                    chosen_move = self.choose_ai_move(legalMoves, 'L2')

            # Make the chosen move
            self.makeMove(chosen_move)

            # Print the updated board
            self.printGrid()

            # Offer to move a neutral piece (now AI can also do this)
            self.moveNeutralPiece()

            # Print updated board after neutral move
            self.printGrid()

            # Switch players
            self.currentPlayer = 'L2' if self.currentPlayer == 'L1' else 'L1'

    def makeMove(self, newPositions):
        # Updates board and player's positions after making a valid move
        if self.currentPlayer == 'L1':
            oldPositions = self.p1Pos
        else:
            oldPositions = self.p2Pos

        self.removePiece(oldPositions)
        self.placePiece(newPositions, self.currentPlayer)

        if self.currentPlayer == 'L1':
            self.p1Pos = newPositions
        else:
            self.p2Pos = newPositions

    def moveNeutralPiece(self):
        # If current player is human or if it's AI's turn, handle accordingly.
        if self.currentPlayer == 'L1' or (self.currentPlayer == 'L2' and self.opponentType == 'human'):
            # Human logic
            if not self.neutralPieces:
                return  # No neutral pieces to move
            print("Would you like to move a neutral piece? Enter 'no' to skip or the index of the piece.")
            for i, pos in enumerate(self.neutralPieces):
                print(f"{i}: {pos}")

            choice = input("Your choice: ")

            if choice.lower() == 'no':
                return  # Player chose not to move

            if not choice.isdigit():
                print("Invalid input. No neutral piece moved.")
                return

            piece_index = int(choice)
            if piece_index < 0 or piece_index >= len(self.neutralPieces):
                print("Invalid piece index. No neutral piece moved.")
                return

            # We have a valid piece index, now ask for new coordinates
            while True:
                coords_input = input("Enter new coordinates for the neutral piece (x,y) or 'no' to skip: ")
                if coords_input.lower() == 'no':
                    return  # Player changed their mind

                try:
                    x_str, y_str = coords_input.split(',')
                    x, y = int(x_str.strip()), int(y_str.strip())
                except (ValueError, IndexError):
                    print("Invalid format. Please enter coordinates as x,y or 'no' to skip.")
                    continue

                if 0 <= x < 4 and 0 <= y < 4 and self.grid[x][y] == '0':
                    # Valid and empty spot
                    old_pos = self.neutralPieces[piece_index]
                    self.grid[old_pos[0]][old_pos[1]] = '0'
                    self.grid[x][y] = 'N'
                    self.neutralPieces[piece_index] = (x, y)
                    break
                else:
                    print("That cell is not empty or out of range. Try again or type 'no' to skip.")

        else:
            # AI logic for moving neutral pieces
            if not self.neutralPieces:
                return  # No neutral pieces to move

            # AI will try to pick a neutral piece move that reduces the opponent's next moves.
            ai_move = self.choose_ai_neutral_move()
            if ai_move is not None:
                piece_index, new_x, new_y = ai_move
                # Execute the chosen move
                old_pos = self.neutralPieces[piece_index]
                self.grid[old_pos[0]][old_pos[1]] = '0'
                self.grid[new_x][new_y] = 'N'
                self.neutralPieces[piece_index] = (new_x, new_y)
            # If no beneficial move found, AI skips

    def choose_ai_move(self, legalMoves, player):
        opponent = 'L1' if player == 'L2' else 'L2'

        best_move = None
        best_score = float('inf')  # minimize opponent moves

        if player == 'L2':
            oldPositions = self.p2Pos
        else:
            oldPositions = self.p1Pos

        original_p1Pos = self.p1Pos[:]
        original_p2Pos = self.p2Pos[:]
        original_grid = [row[:] for row in self.grid]

        for move in legalMoves:
            # Apply the move
            self.removePiece(oldPositions)
            self.placePiece(move, player)
            if player == 'L2':
                self.p2Pos = move
            else:
                self.p1Pos = move

            opponent_moves = self.genLegalMoves(opponent)
            opponent_moves_count = len(opponent_moves)

            if opponent_moves_count == 0:
                # Immediate best outcome
                best_move = move
                self.restoreState(original_grid, original_p1Pos, original_p2Pos)
                return best_move

            if opponent_moves_count < best_score:
                best_score = opponent_moves_count
                best_move = move

            # Revert
            self.restoreState(original_grid, original_p1Pos, original_p2Pos)

        return best_move

    def choose_ai_neutral_move(self):
        # AI tries all neutral piece moves to minimize opponent's next moves.
        player = self.currentPlayer
        opponent = 'L1' if player == 'L2' else 'L2'

        best_move = None
        best_score = self.evaluate_opponent_moves(opponent)  # Current opponent moves before neutral piece move
        original_neutrals = self.neutralPieces[:]
        original_grid = [row[:] for row in self.grid]
        original_p1Pos = self.p1Pos[:]
        original_p2Pos = self.p2Pos[:]

        # Try moving each neutral piece to every empty cell
        for i, (nx, ny) in enumerate(self.neutralPieces):
            # Remove the neutral piece
            self.grid[nx][ny] = '0'
            for x in range(4):
                for y in range(4):
                    if self.grid[x][y] == '0':
                        # Place neutral piece here
                        self.grid[x][y] = 'N'
                        self.neutralPieces[i] = (x, y)

                        # Evaluate opponent moves now
                        new_score = self.evaluate_opponent_moves(opponent)
                        if new_score < best_score:
                            best_score = new_score
                            best_move = (i, x, y)

                        # Revert placement
                        self.grid[x][y] = '0'
                        self.neutralPieces[i] = (nx, ny)
            # Put the neutral piece back after trying all cells for this piece
            self.grid[nx][ny] = 'N'

        # Restore original state
        self.restoreState(original_grid, original_p1Pos, original_p2Pos)
        self.neutralPieces = original_neutrals

        return best_move

    def evaluate_opponent_moves(self, opponent):
        # Evaluate how many moves the opponent has in the current state
        return len(self.genLegalMoves(opponent))

    def restoreState(self, original_grid, original_p1Pos, original_p2Pos):
        for i in range(4):
            for j in range(4):
                self.grid[i][j] = original_grid[i][j]

        self.p1Pos = original_p1Pos[:]
        self.p2Pos = original_p2Pos[:]


if __name__ == "__main__":
    game = LGame()
    game.startGame()

class LGame:
  def __init__(self):
    #init empty 4x4 grid
    self.grid = [['0' for _ in range(4)] for _ in range(4)]
    #setting initial pos for p1 and p2 Ls
    self.p1Pos = [(0, 0), (0, 1), (0, 2), (1, 0)]
    self.placePiece(self.p1Pos, 'L1')

    self.p2Pos = [(3, 3), (3, 2), (3, 1), (2, 3)]
    self.placePiece(self.p2Pos, 'L2')

    #setting initial pos for coins
    self.neutralPieces = [(1, 1), (2, 2)]
    self.placeNeutralPieces()

    self.LPositions = {
      'N':  [(0, 0), (1, 0), (2, 0), (2, 1)],  # North
      'NM': [(0, 1), (1, 1), (2, 1), (2, 0)],  # North-Mirrored
      'E':  [(0, 0), (0, 1), (0, 2), (1, 0)],  # East
      'EM': [(0, 0), (0, 1), (0, 2), (1, 2)],  # East-Mirrored
      'S':  [(0, 1), (0, 0), (1, 1), (2, 1)],  # South
      'SM': [(0, 0), (1, 0), (2, 0), (2, -1)], # South-Mirrored
      'W':  [(0, 2), (1, 0), (1, 1), (1, 2)],  # West
      'WM': [(0, 0), (1, 0), (1, 1), (1, 2)],  # West-Mirrored
    }

  def isValidMove(self, positions):
    for x, y in positions:
      if not (0 <= x < 4 and 0 <= y < 4):
        return False

      if self.grid[x][y] != '0':
        return False
    return True

  def genLegalMoves(self, player):
    legalMoves = []
    if (player == 'L1'):
      opponent = 'L2'
      currPos = self.p1Pos
    else:
      opponent = 'L1'
      currPos = self.p2Pos
    

    for x, y in currPos:
      self.grid[x][y] = '0'

    for i in range(4):
      for j in range(4):
        for pos in self.LPositions.values():
          newPos = [(i + x, j + y) for x, y in pos]
          if self.isValidMove(newPos):
            legalMoves.append(newPos)

    for x, y in currPos:
      self.grid[x][y] = player

    legalMoves.remove(currPos)
    return legalMoves


  

  def placePiece(self, positions, player):
    # placing L pieces w proper label
    for x, y in positions:
      self.grid[x][y] = player

  def placeNeutralPieces(self):
    # placing neutral pieces w N label
    for x, y in self.neutralPieces:
      self.grid[x][y] = 'N'

  def printGrid(self):
    #prints curr grid
    for row in self.grid:
      print(" | ".join(f"{cell:2}" for cell in row))
      print("-" * 17)

  

  
  def startGame(self):
    # starting game
    self.printGrid()

    while True:
      move = input("Enter your move or q to quit")

      if move.lower() == 'q':
        print("gg")
        break

      print(self.genLegalMoves('L1'))
      self.printGrid()

if __name__ == "__main__":
  game = LGame()
  game.startGame()
  
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

  def placePiece(self, positions, label):
    # placing L pieces w proper label
    for x, y in positions:
      self.grid[x][y] = label

  def placeNeutralPieces(self):
    # placing neutral pieces w N label
    for x, y in self.neutralPieces:
      self.grid[x][y] = 'N'

  def printGrid(self):
    #prints curr grid
    for row in self.grid:
      print(" | ".join(f"{cell:2}" for cell in row))
      print("-" * 17)

  def isMoveLegal(self, move):
    return True
    # check if move is legal

  def makeMove(self, move):
    #make move
    return
  
  def startGame(self):
    # starting game
    self.printGrid()

    while True:
      move = input("Enter your move or q to quit")

      if move.lower() == 'q':
        print("gg")
        break

      if self.isMoveLegal(move):
        print(f"You entered: {move}")
        self.makeMove(move)

      self.printGrid()

if __name__ == "__main__":
  game = LGame()
  game.startGame()
  
import pygame
import pygame_menu
import sys
import os
from pygame.locals import *
from datetime import date
import sqlite3
import random
pygame.init()
pygame.font.init()

WIDTH,HEIGHT = 800,600
sqSize = 50
padding = 50
load_text = ""
letters = ['a','b','c','d','e','f','g','h']
titlefont = pygame.font.SysFont(None,100)
buttonfont = pygame.font.SysFont(None, 60)
pfont = pygame.font.SysFont(None, 20)
screen = pygame.display.set_mode((WIDTH,HEIGHT))
programIcon = pygame.image.load('images/bK.png')
pygame.display.set_caption('Brilliant Mates')
pygame.display.set_icon(programIcon)

ranksToRows = {"1":7,"2":6,"3":5,"4":4,"5":3,"6":2,"7":1,"8":0}
 
rowsToRanks = {v: k for k,v in ranksToRows.items()}
filesToCols = {"a":0,"b":1,"c":2,"d":3,"e":4,"f":5,"g":6,"h":7}
colsToFiles = {v: k for k,v in filesToCols.items()}

flipToReg = {7:0,6:1,5:2,4:3,3:4,2:5,1:6,0:7}
regToFiles = {v: k for k,v in flipToReg.items()}
fens = sqlite3.connect('saves.db')
conn = fens.cursor()
conn.execute("""CREATE TABLE IF NOT EXISTS Puzzles (
  name text,
  difficulty number,
  notation text
  )""")
conn.execute("""CREATE TABLE IF NOT EXISTS Positions (
  name text,
  date text,
  notation text
  )""")
easy_puzzles = [
  "k7/p1p5/8/1B6/8/4p1r1/8/KR6 w - - 0 1",
  "1kr5/1p1n4/2pPp3/2P5/8/3q4/R4BP1/R5K1 w - - 0 1",
  "8/8/8/7b/8/4b1k1/8/7K b - - 0 1",
  "rnbqkbnr/pp5p/4pP2/2NpP1p1/2pP4/1pP5/PP4PP/R1BQKBNR w KQkq - 0 1"
]
medium_puzzles = [
  "8/k1P5/2Q5/8/1q3B2/8/8/3K4 w - - 0 1",
  "r1bq1b1r/ppp1k1pp/8/1N1BpQ2/3P4/8/PP3PPP/n1BK3R w K - 0 1",
  "r2q3r/1npb1ppp/pn2p1k1/6B1/1pP1K2P/1P1P1N2/P1N5/R6R w - - 0 1",
  "r1b2rk1/p1pp1ppp/2pb1n2/4q3/2B1P3/3N1Q2/PPP2PPP/R1B2RK1 b Qq - 0 1",
  "5rk1/pQp1q1pp/2B1p3/4P3/P1p2Pp1/N1P2R1K/P7/R4nr1 w - - 0 2"
]
hard_puzzles = [
  "8/1k6/6R1/1K2P3/8/8/8/6R1 w - - 0 1",
  "7R/P1kr4/K2n4/1P6/8/8/2p5/8 w - - 0 1",
  "1B6/Np2p3/pk1p4/nP6/pRnKb3/1pP1r3/2PP4/8 w - - 0 1",
  "7Q/3k1ppp/p3p3/4Pn2/1bbP4/3n1N2/4KPPP/7R b - - 0 1"
]
for i,p in enumerate(easy_puzzles):
  conn.execute("INSERT INTO Puzzles VALUES (?,?,?)", ("Easy Puzzle #" + str(i),1, p))

for i,p in enumerate(medium_puzzles):
  conn.execute("INSERT INTO Puzzles VALUES (?,?,?)", ("Medium Puzzle #" + str(i),2, p))

for i,p in enumerate(hard_puzzles):
  conn.execute("INSERT INTO Puzzles VALUES (?,?,?)", ("Hard Puzzle #" + str(i),3, p))

# class for the current position of the game
class CurrentPosition():
  def __init__(self):
    self.position = [
      ["r","n","b","q","k","b","n","r"],
      ["p","p","p","p","p","p","p","p"],
      [" "," "," "," "," "," "," "," "],
      [" "," "," "," "," "," "," "," "],
      [" "," "," "," "," "," "," "," "],
      [" "," "," "," "," "," "," "," "],
      ["P","P","P","P","P","P","P","P"],
      ["R","N","B","Q","K","B","N","R"], 
    ]
    self.whiteToMove = True
    self.notation = []
    self.pgn = []
    self.whiteCastlePossible = True
    self.blackCastlePossible = True
    self.whiteEnPassantLeft = False
    self.whiteEnPassantRight = False
    self.blackEnPassantLeft = False
    self.blackEnPassantRight = False
    self.enPassantSquare = []
    self.EPRow = 0 # used to get the square where en passant is active
    self.EPCol = 0
    self.whiteInCheck = False
    self.blackInCheck = False
    self.whitePromotion = False
    self.blackPromotion = False
    self.promotionPiece = ' '
    self.promotionSquare = []
    self.flipboard = 1
    self.saveCounter = 0
  def get_positions(self):
    return conn.execute('SELECT * FROM Positions')
  def get_danger_squares(self):
    output = []
    for x,r in enumerate(self.position):
      for y,c in enumerate(r):
        print(c)
        sq = (x,y)
        if self.whiteToMove == True and c.islower():
          output.append(self.get_legal_moves(sq))
        elif self.whiteToMove == False and c.isupper():
          output.append(self.get_legal_moves(sq))
    return output
  def get_puzzles(self):
    return conn.execute('SELECT * FROM Puzzles')
  def load_random_puzzle(self,difficulty):
    puzzles = conn.execute('SELECT * FROM Puzzles WHERE difficulty = ?',str(difficulty)).fetchall()
    if len(puzzles) > 0:
      output = random.choice(puzzles)
      #print(output)
      return output[2]
    return None
  def load_position(self,fen):
    fen = fen.split()
    if fen[1] == 'b':
      self.whiteToMove = False
    else:
      self.whiteToMove = True

    if fen[2] == "-":
      self.whiteCastlePossible = False
      self.blackCastlePossible = False
    #print(fen)
    row_count = 0
    col_count = 0
    self.notation = []
    self.pgn = []
    for f in fen[0]:
      if row_count > 7 or col_count > 7:
        #print('end')
        return
      elif f.isnumeric():
        space_counter = int(f)
        while space_counter > 0:
          #print('space')
          self.position[row_count][col_count] = " "
          col_count += 1
          if col_count > 7:
            row_count += 1
            col_count = 0
          space_counter -= 1
      elif f.upper() in pieces:
        self.position[row_count][col_count] = f
        col_count += 1
        if col_count > 7:
          row_count += 1
          col_count = 0
        #print('piece placed',f)
      elif f == 'b':
        self.whiteToMove = False
        #print('color change')
      elif f == 'w':
        self.whiteToMove = True
        #print('color change')
      else:
        print('nothing')
    gameStatus = "GAME"

  def save_position(self): # current position in game to fen format in database
    #print("positions saving")
    self.saveCounter += 1
    output = ""
    space_counter = 0
    for i,r in enumerate(self.position):
      for j,c in enumerate(r):
          if c != " ":
            if space_counter > 0:
              output += str(space_counter)
              space_counter = 0
            output += c
          else:
            space_counter += 1
          if j == len(r)-1 and space_counter > 0:
            output += str(space_counter)
            space_counter = 0
      if i < len(self.position)-1:
        output += "/"
    output += " "
    if self.whiteToMove == True:
      output += "w"
    else: 
      output += "b"
    #print(output)
    date1 = date.today()
    df = date1.strftime("%m%d%y")
    conn.execute("INSERT INTO Positions VALUES (?,?,?)", ("Position " + str(self.saveCounter),df, output))
    fens.commit()
  def make_move(self,move):
    #print(move)
    
    if move.piece1 != ' ' and (move.piece1 != move.piece2) and move.piece2.upper() != 'K':
      # en passant taken as white

      if (move.piece1 == 'P' and self.whiteEnPassantLeft == True and move.Row1 - move.Row2 == 1 and 
      move.Col1 - move.Col2 == 1 and self.position[move.Row2][move.Col2] == ' '):
        self.position[move.Row2+1][move.Col2] = ' '
        #print('en passant taken',move.Row2,move.Col2)

      if (move.piece1 == 'P' and self.whiteEnPassantRight == True and move.Row1 - move.Row2 == 1 and
       move.Col1 - move.Col2 == -1 and self.position[move.Row2][move.Col2] == ' '):
        self.position[move.Row2+1][move.Col2] = ' '
        #print('en passant taken',move.Row2,move.Col2)

      if (move.piece1 == 'p' and self.blackEnPassantLeft == True and move.Row1 - move.Row2 == -1 and
       move.Col1 - move.Col2 == 1 and self.position[move.Row2][move.Col2] == ' '):
        self.position[move.Row2-1][move.Col2] = ' '
        #print('en passant taken',move.Row2,move.Col2)

      if (move.piece1 == 'p' and self.blackEnPassantRight == True and move.Row1 - move.Row2 == -1 and
       move.Col1 - move.Col2 == -1 and self.position[move.Row2][move.Col2] == ' '):
        self.position[move.Row2-1][move.Col2] = ' '
        #print('en passant taken',move.Row2,move.Col2)

      self.position[move.Row1][move.Col1] = ' '
      self.position[move.Row2][move.Col2] = move.piece1
      # king side castle
      if move.piece1.upper() == 'K' and (move.Col1+2) == move.Col2 and self.whiteInCheck == False and self.blackInCheck == False:
        temp = self.position[move.Row1][move.Col1+3]
        self.position[move.Row1][move.Col1+3] = ' '
        self.position[move.Row2][move.Col1+1] = temp
      if move.piece1 == 'K' or move.piece1 == 'R':
        self.whiteCastlePossible = False
      if move.piece1 == 'k' or move.piece1 == 'r':
        self.blackCastlePossible = False
      # queen side castle
      if move.piece1.upper() == 'K' and (move.Col1-2) == move.Col2 and self.whiteInCheck == False and self.blackInCheck == False:
        temp = self.position[move.Row1][move.Col1+3]
        self.position[move.Row1][move.Col1-4] = ' '
        self.position[move.Row2][move.Col1-1] = temp
      #en passant as black activation
      if move.piece1 == 'p' and abs(move.Row1 - move.Row2) == 2:
        ##print(self.position[move.Row2][move.Col2-1]+' hi')
        if move.Col2 < 7:
          if self.position[move.Row2][move.Col2+1] == 'P':
            self.whiteEnPassantLeft = True
            self.enPassantSquare = [move.Row2,move.Col2+1]
            #print(move.Row1,move.Row2)
            #print('left active')
        if move.Col2 > 0:
          if self.position[move.Row2][move.Col2-1] == 'P':
            self.whiteEnPassantRight = True
            self.enPassantSquare = [move.Row2,move.Col2-1]
            #print(move.Row1,move.Row2)
            #print('right active')
      # en passant as white activation
      if move.piece1 == 'P' and abs(move.Row1 - move.Row2) == 2:
        #print(self.position[move.Row2][move.Col2-1]+' hi')
        if move.Col2 < 7:
          if self.position[move.Row2][move.Col2+1] == 'p':
            self.blackEnPassantLeft = True
            self.enPassantSquare = [move.Row2,move.Col2+1]
            #print(move.Row1,move.Row2)
            #print('left active')
        if move.Col2 > 0:
          if self.position[move.Row2][move.Col2-1] == 'p':
            self.blackEnPassantRight = True
            self.enPassantSquare = [move.Row2,move.Col2-1]
            #print(move.Row1,move.Row2)
            #print('right active')
      if move.piece1.isupper():
        self.whiteEnPassantLeft = False
        self.whiteEnPassantRight = False
      if move.piece1.islower():
        self.blackEnPassantLeft = False
        self.blackEnPassantRight = False
      self.whiteToMove = not self.whiteToMove
      dan_squares = self.get_danger_squares()
      print('dan_squares: ',dan_squares)
      self.notation.append(move)
      
      # taking with en passant as white
      # pawn promotion
      if move.piece1.upper() == 'P' and (move.Row2 == 0 or move.Row2 == 7):
        if move.Row2 == 7:
          self.blackPromotion = True
        if move.Row2 == 0:
          self.whitePromotion = True
        self.promotionSquare = [move.Row2,move.Col2]
  def undo_last_move(self):
    if len(self.notation)>0 and len(self.pgn) > 0:
      # undo castle
      #print(self.notation[-1].Col2 - self.notation[-1].Col1)
      if self.notation[-1].piece1[0].upper() == 'K':
        tempRook = 'r'
        if self.notation[-1].piece1[0].isupper():
          tempRook = 'R'
        if (self.notation[-1].Col2 - self.notation[-1].Col1) == 2:
          self.position[self.notation[-1].Row1][self.notation[-1].Col2+1] = tempRook
          self.position[self.notation[-1].Row1][self.notation[-1].Col2-1] = ' '
        if (self.notation[-1].Col2 - self.notation[-1].Col1) == -2:
          self.position[self.notation[-1].Row1][self.notation[-1].Col2-2] = tempRook
          self.position[self.notation[-1].Row1][self.notation[-1].Col2+1] = ' '
        if self.notation[-1].piece1.isupper() and (self.pgn[-1] == '0-0' or self.pgn[-1] == '0-0-0'):
          self.whiteCastlePossible = True
        elif (self.pgn[-1] == '0-0' or self.pgn[-1] == '0-0-0'):
          self.blackCastlePossible = True
      #print(self.notation)
      self.position[self.notation[-1].Row1][self.notation[-1].Col1] = self.notation[-1].piece1
      self.position[self.notation[-1].Row2][self.notation[-1].Col2] = self.notation[-1].piece2
      self.notation.pop()
      self.pgn.pop()
      self.whiteToMove = not self.whiteToMove
      self.blackPromotion = False
      self.whitePromotion = False

  def bishop(self,piece,isWhite,output):
    temp = piece[0]-1
    for j in range(piece[1],7):
      if self.position[temp][j+1] == ' ':
        move = (temp,j+1)
        output.append(move)
        temp -= 1
      else:
        if self.position[temp][j+1][0].islower() == isWhite:
          move = (temp,j+1)
          output.append(move)
        break
        # bishop top left move
    temp = piece[0]
    for j in range((piece[1]), 0, -1):
      if self.position[temp-1][j-1] == ' ':
        move = (temp-1,j-1)
        output.append(move)
        temp -= 1
      else:
        if self.position[temp-1][j-1][0].islower() == isWhite:
          move = (temp-1,j-1)
          output.append(move)
        break
        # bishop bottom right move
    temp = piece[0]
    for j in range(piece[1],7):
      if temp < 7:
        if self.position[temp+1][j+1] == ' ':
          temp += 1
          move = (temp,j+1)
          output.append(move)
        else:
          if self.position[temp+1][j+1][0].islower() == isWhite:
            move = (temp+1,j+1)
            output.append(move)
          break
        # bishop bottom left move
    temp = piece[0]
    for j in range((piece[1]), 0, -1):
      if temp < 7:
        if self.position[temp+1][j-1] == ' ':
          temp += 1
          move = (temp,j-1)
          output.append(move)
        else:
          if self.position[temp+1][j-1][0].islower() == isWhite:
            move = (temp+1,j-1)
            output.append(move)
          break
  def rook(self,piece,isWhite,output):
    
    for i in range((piece[0]-1), -1, -1):
      print(self.position[i][piece[1]].lower())
      if self.position[i][piece[1]] == ' ':
        move = (i,piece[1])
        output.append(move)
      else:
        if self.position[i][piece[1]].islower() == isWhite:
          move = (i,piece[1])
          output.append(move)
        break
    for i in range((piece[0]+1),8):
      if self.position[i][piece[1]] == ' ':
        move = (i,piece[1])
        output.append(move)
      else:
        if self.position[i][piece[1]].islower() == isWhite:
          move = (i,piece[1])
          output.append(move)
        break
    for i in range((piece[1]-1), -1, -1):
      if self.position[piece[0]][i] == ' ':
        move = (piece[0],i)
        output.append(move)
      else:
        if self.position[piece[0]][i].islower() == isWhite:
          move = (piece[0],i)
          output.append(move)
        break
    for i in range((piece[1]+1),8):
      if self.position[piece[0]][i] == ' ':
        move = (piece[0],i)
        output.append(move)
      else:
        if self.position[piece[0]][i].islower() == isWhite:
          move = (piece[0],i)
          output.append(move)
        break
  def knight(self,piece,isWhite,output):
    if piece[0] > 0 and piece[1] > 1:
      if self.position[piece[0]-1][piece[1]-2] == ' ' or self.position[piece[0]-1][piece[1]-2][0].islower() == isWhite:
        move = (piece[0]-1,piece[1]-2)
        output.append(move)
    if piece[0] > 0 and piece[1] < 6:
      if self.position[piece[0]-1][piece[1]+2] == ' ' or self.position[piece[0]-1][piece[1]+2][0].islower() == isWhite:
        move = (piece[0]-1,piece[1]+2)
        output.append(move)
    if piece[0] > 1 and piece[1] > 0:
      if self.position[piece[0]-2][piece[1]-1] == ' ' or self.position[piece[0]-2][piece[1]-1][0].islower() == isWhite:
        move = (piece[0]-2,piece[1]-1)
        output.append(move)
    if piece[0] > 1 and piece[1] < 7:
      if self.position[piece[0]-2][piece[1]+1] == ' ' or self.position[piece[0]-2][piece[1]+1][0].islower() == isWhite:
        move = (piece[0]-2,piece[1]+1)
        output.append(move)
    if piece[0] < 6 and piece[1] < 7:
      if self.position[piece[0]+2][piece[1]+1] == ' ' or self.position[piece[0]+2][piece[1]+1][0].islower() == isWhite:
        move = (piece[0]+2,piece[1]+1)
        output.append(move)  
    if piece[0] < 6 and piece[1] > 0:
      if self.position[piece[0]+2][piece[1]-1] == ' ' or self.position[piece[0]+2][piece[1]-1][0].islower() == isWhite:
        move = (piece[0]+2,piece[1]-1)
        output.append(move)  
    if piece[0] < 7 and piece[1] > 1:
      if self.position[piece[0]+1][piece[1]-2] == ' ' or self.position[piece[0]+1][piece[1]-2][0].islower() == isWhite:
        move = (piece[0]+1,piece[1]-2)
        output.append(move)
    if piece[0] < 7 and piece[1] < 6:
      if self.position[piece[0]+1][piece[1]+2] == ' ' or self.position[piece[0]+1][piece[1]+2][0].islower() == isWhite:
        move = (piece[0]+1,piece[1]+2)
        output.append(move) 
  def king(self,piece,isWhite,output):
    if isWhite:
      castleType = self.whiteCastlePossible
    else:
      castleType = self.blackCastlePossible
    if piece[0] > 0:
      if self.position[piece[0]-1][piece[1]] == ' ' or self.position[piece[0]-1][piece[1]][0].islower() == isWhite:
        move = (piece[0]-1,piece[1])
        output.append(move)
      if piece[1] > 0:
        if self.position[piece[0]-1][piece[1]-1] == ' ' or self.position[piece[0]-1][piece[1]-1][0].islower() == isWhite:
          move = (piece[0]-1,piece[1]-1)
          output.append(move)

      if piece[1] < 7:
        if self.position[piece[0]-1][piece[1]+1] == ' ' or self.position[piece[0]-1][piece[1]+1][0].islower() == isWhite:
          move = (piece[0]-1,piece[1]+1)
          output.append(move)
    if piece[0] < 7:
      if self.position[piece[0]+1][piece[1]] == ' ' or self.position[piece[0]+1][piece[1]][0].islower() == isWhite:
        move = (piece[0]+1,piece[1])
        output.append(move)
      if piece[1] > 0:
        if self.position[piece[0]+1][piece[1]-1] == ' ' or self.position[piece[0]+1][piece[1]-1][0].islower() == isWhite:
          move = (piece[0]+1,piece[1]-1)
          output.append(move)
      if piece[1] < 7:
        if self.position[piece[0]+1][piece[1]+1] == ' ' or self.position[piece[0]+1][piece[1]+1][0].islower() == isWhite:
          move = (piece[0]+1,piece[1]+1)
          output.append(move)
    if piece[1] > 0:
      if self.position[piece[0]][piece[1]-1] == ' ' or self.position[piece[0]][piece[1]-1][0].islower() == isWhite:
          move = (piece[0],piece[1]-1)
          output.append(move)
    if piece[1] < 7:
      if self.position[piece[0]][piece[1]+1] == ' ' or self.position[piece[0]][piece[1]+1][0].islower() == isWhite:
          move = (piece[0],piece[1]+1)
          output.append(move)
    #  Castle
    # King Side
    if castleType == True and self.position[piece[0]][piece[1]+1] == ' ' and self.position[piece[0]][piece[1]+2] == ' ':
      move = (piece[0],piece[1]+2)
      output.append(move)
    # Queen Side
    if (castleType == True and self.position[piece[0]][piece[1]-1] == ' ' and 
    self.position[piece[0]][piece[1]-2] == ' ' and self.position[piece[0]][piece[1]-3] == ' '):
      move = (piece[0],piece[1]-2)
      output.append(move)
  def get_legal_moves(self,piece):
    print(piece)
    multiplier = 1
    #print('square is ',self.enPassantSquare)
    if self.blackPromotion == True or self.whitePromotion == True:
      return []
    output = []
    print("after",piece)
    self.selected_piece = self.position[piece[0]][piece[1]]
    if self.flipboard == 2:
      self.selected_piece = self.position[flipToReg[piece[0]]][flipToReg[piece[1]]]
      multiplier = -1
    print(self.selected_piece)
    print('yes',multiplier)
    if self.selected_piece.upper() == 'P':
      if self.selected_piece.isupper() and self.whiteToMove == True:
        if 0 < piece[0] < 7:
          if self.position[piece[0]-(1*multiplier)][piece[1]] == ' ':
            move = (piece[0]-(1*multiplier),piece[1])
            output.append(move)  
            if self.position[piece[0]-(2*multiplier)][piece[1]] == ' ' and piece[0] == 6 or piece[0] == 1:
              move = (piece[0]-(2*multiplier),piece[1])
              output.append(move)
          if piece[1] > 0:
            if self.position[piece[0]-(1*multiplier)][piece[1]-1] != ' ' and self.position[piece[0]-(1*multiplier)][piece[1]-1].islower():
              move = (piece[0]-(1*multiplier),piece[1]-1)
              output.append(move)
          if piece[1] < 7:
            if self.position[piece[0]-(1*multiplier)][piece[1]+1] != ' ' and self.position[piece[0]-(1*multiplier)][piece[1]+1].islower():
              move = (piece[0]-(1*multiplier),piece[1]+1)
              output.append(move)
         # en passant (white)
          if 0 < piece[1] < 7:
            if (self.whiteEnPassantLeft == True and self.enPassantSquare == [piece[0],piece[1]] and
             self.position[piece[0]][piece[1]-1].islower() and self.position[piece[0]-1][piece[1]+1] == ' '):
              move = (piece[0]-1,piece[1]-1)
              output.append(move)
          if 0 < piece[1] < 7:
            if (self.whiteEnPassantRight == True and self.enPassantSquare == [piece[0],piece[1]] and
             self.position[piece[0]][piece[1]+1].islower() and self.position[piece[0]-1][piece[1]-1] == ' '):
              move = (piece[0]-1,piece[1]+1)
              output.append(move)
          
      elif self.selected_piece.islower() and self.whiteToMove == False:
        if 0 < piece[0] < 7:
          #move up one 
          if self.position[piece[0]+(1*multiplier)][piece[1]] == ' ':
            move = (piece[0]+(1*multiplier),piece[1])
            output.append(move)
            # move up twice
            #print('checking', piece[0], self.position[piece[0]+(2*multiplier)][piece[1]]          
            if piece[0] == 1 or piece[0] == 6:    
              if self.position[piece[0]+(2*multiplier)][piece[1]] == ' ':
                move = (piece[0]+(2*multiplier),piece[1])
                output.append(move)
          # taking a piece
          if piece[1] < 7:
            if self.position[piece[0]+(1*multiplier)][piece[1]+1] != ' ' and self.position[piece[0]+(1*multiplier)][piece[1]+1].isupper():
              move = (piece[0]+(1*multiplier),piece[1]+1)
              output.append(move)
          if piece[1] < 8:
            if self.position[piece[0]+1][piece[1]-1] != ' ' and self.position[piece[0]+1][piece[1]-1].isupper():
              move = (piece[0]+(1*multiplier),piece[1]-1)
              output.append(move)
          # en passant (white)
          if piece[1] < 7:
            if (self.blackEnPassantRight == True and self.enPassantSquare == [piece[0],piece[1]] and
             self.position[piece[0]][piece[1]+1] == 'P' and self.position[piece[0]+1][piece[1]+1] == ' '):
              move = (piece[0]+1,piece[1]+1)
              output.append(move)
          if piece[1] < 8:
            if (self.blackEnPassantLeft == True and self.enPassantSquare == [piece[0],piece[1]] and 
            self.position[piece[0]][piece[1]-1] == 'P' and self.position[piece[0]+1][piece[1]-1] == ' '):
              move = (piece[0]+1,piece[1]-1)
              output.append(move)
    # Rook Move
    elif self.selected_piece.upper() == 'R':
      if self.selected_piece.isupper() and self.whiteToMove == True:
        self.rook(piece,True,output)
      if self.selected_piece.islower() and self.whiteToMove == False:
        self.rook(piece,False,output)
    # Bishop Move
    elif self.selected_piece.upper() == 'B':
      if self.selected_piece.isupper() and self.whiteToMove == True:
        self.bishop(piece,True,output)
      if self.selected_piece.islower() and self.whiteToMove == False:
        self.bishop(piece,False,output)
    # King Move
    elif self.selected_piece.upper() == 'K':
      if self.selected_piece.isupper() and self.whiteToMove == True:
        self.king(piece,True,output)
      if self.selected_piece.islower() and self.whiteToMove == False:
        self.king(piece,False,output)
    # Queen Move
    elif self.selected_piece.upper() == 'Q':
      if self.selected_piece.isupper() and self.whiteToMove == True:
        self.rook(piece,True,output)
        self.bishop(piece,True,output)
      if self.selected_piece.islower() and self.whiteToMove == False:
        self.rook(piece,False,output)
        self.bishop(piece,False,output)
    # Knight Move
    elif self.selected_piece.upper() == 'N':
      if self.selected_piece.isupper() and self.whiteToMove == True:
        self.knight(piece,True,output)
      if self.selected_piece.islower() and self.whiteToMove == False:
        self.knight(piece,False,output)
    print(output)
    return output



class Move(): # (1,1) = (8,a)
  

  def __init__(self,Sq1,Sq2,board,fS):
    if fS == 2:
      self.Row1 = self.getFlip(Sq1[0])
      self.Col1 = self.getFlip(Sq1[1])
      self.Row2 = self.getFlip(Sq2[0])
      self.Col2 = self.getFlip(Sq2[1])
    else:
      self.Row1 = Sq1[0]
      self.Col1 = Sq1[1]
      self.Row2 = Sq2[0]
      self.Col2 = Sq2[1]
    self.piece1 = board[self.Row1][self.Col1]
    self.piece2 = board[self.Row2][self.Col2]
  
  def getNotation(self):
    output = self.piece1.upper()
    takes = 'x'
    check = '+' # for checkmate
    if self.piece2 == ' ':
      takes = ''
    if self.piece1.upper() == 'P':
      output = ''
      if abs(self.Row1 - self.Row2) == 1 and  abs(self.Col1 - self.Col2) == 1:
        takes = 'x'
    if self.piece1 == ' ' or (self.piece1 == self.piece2) or self.piece2.upper()== 'K':
      return ' '
    if self.piece1.upper() == 'K' and (self.Col2 - self.Col1) == 2:
      return '0-0'
    if self.piece1.upper() == 'K' and (self.Col2 - self.Col1) == -2:
      return '0-0-0'
    return output + takes + self.getRankFile(self.Row2,self.Col2)

  def getRankFile(self,r,c):
    return colsToFiles[c] + rowsToRanks[r]
  def getFlip(self,n):
    return regToFiles[n]
cP = CurrentPosition()

# colors 
LIGHT = (145, 134, 105)
DARK = (92, 80, 48)
BACKGROUND = (31, 31, 31)
HIGHLIGHT = pygame.Color(255, 232, 84)
extraIMAGES = {}
# chess pieces images
IMAGES = {}
pieces = ['K','Q','B','N','P','R']
def flip_move(num):
  flipToReg = {7:0,6:1,5:2,4:3,3:4,2:5,1:6,0:7}
  regToFiles = {v: k for k,v in flipToReg.items()}
  num = flipToReg[num]
def load_images():
  pieceSize = sqSize-3
  extraIMAGES[0] = pygame.transform.scale(pygame.image.load('images/flip.png').convert_alpha(),(pieceSize,pieceSize))
  extraIMAGES[1] = pygame.transform.scale(pygame.image.load('images/undo.png').convert_alpha(),(pieceSize,pieceSize))
  extraIMAGES[2] = pygame.transform.scale(pygame.image.load('images/load.png').convert_alpha(),(pieceSize,pieceSize))
  extraIMAGES[3] = pygame.transform.scale(pygame.image.load('images/save.png').convert_alpha(),(pieceSize,pieceSize))
  extraIMAGES[4] = pygame.transform.scale(pygame.image.load('images/back2.png').convert_alpha(),(pieceSize,pieceSize))
  for p in pieces:
    IMAGES[p] = pygame.transform.scale(pygame.image.load('images/w'+p+'.png').convert_alpha(),(pieceSize,pieceSize))
    IMAGES[p.lower()] = pygame.transform.scale(pygame.image.load('images/b'+p+'.png').convert_alpha(),(pieceSize,pieceSize))
# show coordinates on board
def show_text(text,x,y,size):
  font = pygame.font.SysFont(None,size)
  text = font.render(text, True, LIGHT)
  screen.blit(text,(x,y))

def change_status(gamestatus,text):
    gameStatus = text

def draw_board(currentP,flipboard):
    colorSwitch = DARK
    for i in range(8):
      if colorSwitch == DARK:
        colorSwitch = LIGHT
      else:
        colorSwitch = DARK
      if flipboard == 1:
        a = show_text(str(i+1),padding*0.65,365-(sqSize*i)+padding,sqSize-20)
        b = show_text(letters[i],(sqSize*1.4)+(sqSize*i),9*sqSize,sqSize-20)
      elif flipboard == 2:
        a = show_text(str(i+1),padding*0.65,(sqSize*i)+padding+15,sqSize-20)
        b = show_text(letters[-i-1],(sqSize*1.4)+(sqSize*i),9*sqSize,sqSize-20)
      for j in range(8):
        pygame.draw.rect(screen,colorSwitch,((padding+sqSize*j),(padding+sqSize*i),sqSize,sqSize))
        if colorSwitch == DARK:
          colorSwitch = LIGHT
        else:
          colorSwitch = DARK

def draw_pieces(currentP,flipboard):
    # chess board generate
    if flipboard == 1:
      for i in range(8):
        for j in range(8):
          if currentP[i][j] != ' ':
            screen.blit(IMAGES[currentP[i][j]],((padding+sqSize*j),(padding+sqSize*i)))
    elif flipboard == 2:
      for i in reversed(range(1,9)):
        for j in reversed(range(1,9)):
          if currentP[-i][-j] != ' ':
            screen.blit(IMAGES[currentP[-i][-j]],((sqSize*j),(sqSize*i)))

def main():
  load_images()
  screen.fill((BACKGROUND))
  squareSelected = ()
  moveBox = ""
  possible_moves = []
  clicks = []
  running = True
  gameStatus = 'MENU'
  while running:
    screen.fill((BACKGROUND))
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
    for event in pygame.event.get():
      if event.type == QUIT:
        running = False
        fens.commit()
        fens.close()
      elif event.type == KEYDOWN and event.key == K_ESCAPE:
          running = False
          fens.commit()
          fens.close()
      elif event.type == KEYDOWN and event.key == K_f:
        screen.fill((BACKGROUND))
        if cP.flipboard == 1:
          cP.flipboard = 2
        else: 
          cP.flipboard = 1
      elif event.type == pygame.MOUSEBUTTONDOWN:
        if padding <= mouse[0] <= padding+50 and padding+(sqSize*9) <= mouse[1] <= padding+(sqSize*9)+sqSize: 
          screen.fill((BACKGROUND))
          if cP.flipboard== 1:
            cP.flipboard = 2
          else: 
            cP.flipboard = 1
        elif padding*2.6 <= mouse[0] <= padding*2.6+50 and padding+(sqSize*9) <= mouse[1] <= padding+(sqSize*9)+sqSize: 
          cP.undo_last_move()
          possible_moves = []
          squareSelected = ()
          clicks = []
        elif padding*4.2 <= mouse[0] <= padding*4.2+50 and padding+(sqSize*9) <= mouse[1] <= padding+(sqSize*9)+sqSize: 
          cP.get_positions()
          gameStatus = "LOAD"
        elif padding*6.2 <= mouse[0] <= padding*6.2+50 and padding+(sqSize*9) <= mouse[1] <= padding+(sqSize*9)+sqSize:
          cP.save_position()
        elif padding*8 <= mouse[0] <= padding*8+50 and padding+(sqSize*9) <= mouse[1] <= padding+(sqSize*9)+sqSize:
          gameStatus = 'MENU'
        print(mouse[0],mouse[1])
        row = (mouse[0]-padding)//sqSize
        col = (mouse[1]-padding)//sqSize
        #if cP.flipboard == 2:
        #  row = 7 - row
         # col = 7 - col 
        if 0<= row <= 7 and 0 <= col <= 7 and gameStatus == 'GAME':
          if squareSelected == (col,row):
            squareSelected = ()
            clicks = []
            possible_moves = []
          else:
            squareSelected = (col,row)
            clicks.append(squareSelected)
          if len(clicks) == 1:
            possible_moves = cP.get_legal_moves(clicks[0])
          if len(clicks) == 2:
            #print(clicks[1])
            if clicks[1] in possible_moves:
              move = Move(clicks[0],clicks[1],cP.position,cP.flipboard)
              cP.make_move(move)
              if move.getNotation() != ' ':
                cP.pgn.append(move.getNotation())
            squareSelected = ()
            clicks = []
            possible_moves = []

    if gameStatus == 'GAME':
      draw_board(cP.position,cP.flipboard)
      draw_pieces(cP.position,cP.flipboard)
      screen.blit(extraIMAGES[0],(padding,padding+(sqSize*9)))
      screen.blit(extraIMAGES[1],(padding*2.6,padding+(sqSize*9)))
      screen.blit(extraIMAGES[2],(padding*4.2,padding+(sqSize*9)))
      screen.blit(extraIMAGES[3],(padding*6.2,padding+(sqSize*9)))
      screen.blit(extraIMAGES[4],(padding*8,padding+(sqSize*9)))
      show_text("Flip Board",padding,padding+(sqSize*9)+52,sqSize-30)
      show_text("Undo Move",padding*2.6,padding+(sqSize*9)+52,sqSize-30)
      show_text("Load Position",padding*4.2,padding+(sqSize*9)+52,sqSize-30)
      show_text("Save Position",padding*6.2,padding+(sqSize*9)+52,sqSize-30)
      show_text("Main Menu",padding*8,padding+(sqSize*9)+52,sqSize-30)
      moveBox = ''
      s = pygame.Surface((sqSize,sqSize))
      s.set_alpha(50)               
      s.fill(HIGHLIGHT)        
      if squareSelected != ():
        screen.blit(s, (((squareSelected[1]+1)*sqSize),((squareSelected[0]+1)*sqSize))) 
      s = pygame.Surface((sqSize//2.5,sqSize//2.5))
      s.set_alpha(50)               
      s.fill(HIGHLIGHT)
      if len(possible_moves) > 0: 
        for p in possible_moves:
          if p[0] >= 0 and p[1] >= 0:
            screen.blit(s, (((p[1]+1)*sqSize+15),((p[0]+1)*sqSize+15))) 
      c = 1
      for i in range(0,len(cP.pgn)):
        if i % 2 == 0:
          show_text(str(c) + " | ",(sqSize*9)+30,padding+(i*25),sqSize-10)
          show_text(cP.pgn[i],(sqSize*9)+90,padding+(i*25),sqSize-10)
          c += 1
        else:
          show_text(cP.pgn[i],(sqSize*9)+170,padding+((i-1)*25),sqSize-10)
      if cP.whitePromotion == True:
        s = pygame.Surface((sqSize*4,sqSize*2))             
        s.fill(BACKGROUND) 
        screen.blit(s, (WIDTH//5,HEIGHT//3.5))
        s1 = pygame.Surface((sqSize,sqSize))
        s1.fill((50,50,50))
        s2 = pygame.Surface((sqSize,sqSize))
        s2.fill(HIGHLIGHT)
        if WIDTH//5 <= mouse[0] <= WIDTH//5+sqSize and HEIGHT//3 <= mouse[1] <= HEIGHT//3+sqSize: 
          screen.blit(s2,(WIDTH//5,HEIGHT//3))
          if click[0] == 1:
            cP.position[cP.promotionSquare[0]][cP.promotionSquare[1]] = 'Q'   
            cP.whitePromotion = False   
        else: 
          screen.blit(s1,(WIDTH//5,HEIGHT//3))

        if WIDTH//5+sqSize <= mouse[0] <= WIDTH//5+(2*sqSize) and HEIGHT//3 <= mouse[1] <= HEIGHT//3+sqSize: 
          screen.blit(s2,(WIDTH//5+sqSize,HEIGHT//3))
          if click[0] == 1:
            cP.position[cP.promotionSquare[0]][cP.promotionSquare[1]] = 'R'   
            cP.whitePromotion = False        
        else: 
          screen.blit(s1,(WIDTH//5+sqSize,HEIGHT//3))

        if WIDTH//5+(2*sqSize) <= mouse[0] <= WIDTH//5+(3*sqSize) and HEIGHT//3 <= mouse[1] <= HEIGHT//3+sqSize: 
          screen.blit(s2,(WIDTH//5+(sqSize*2),HEIGHT//3))
          if click[0] == 1:   
            cP.position[cP.promotionSquare[0]][cP.promotionSquare[1]] = 'B'   
            cP.whitePromotion = False     
        else: 
          screen.blit(s1,(WIDTH//5+(sqSize*2),HEIGHT//3))
        
        if WIDTH//5+(3*sqSize) <= mouse[0] <= WIDTH//5+(4*sqSize) and HEIGHT//3 <= mouse[1] <= HEIGHT//3+sqSize: 
          screen.blit(s2,(WIDTH//5+(sqSize*3),HEIGHT//3))
          if click[0] == 1:      
            cP.position[cP.promotionSquare[0]][cP.promotionSquare[1]] = 'N'   
            cP.whitePromotion = False   
        else: 
          screen.blit(s1,(WIDTH//5+(sqSize*3),HEIGHT//3))
        show_text("Pick a piece to promote to",WIDTH//5+10,HEIGHT//3.4,22)
        screen.blit(IMAGES['Q'],(WIDTH//5,HEIGHT//3))
        screen.blit(IMAGES['R'],(WIDTH//5+sqSize,HEIGHT//3))
        screen.blit(IMAGES['B'],(WIDTH//5+(sqSize*2),HEIGHT//3))
        screen.blit(IMAGES['N'],(WIDTH//5+(sqSize*3),HEIGHT//3))
        

      if cP.blackPromotion == True:
        s = pygame.Surface((sqSize*4,sqSize*2))             
        s.fill(BACKGROUND) 
        screen.blit(s, (WIDTH//5,HEIGHT//3.5))
        s1 = pygame.Surface((sqSize,sqSize))
        s1.fill((200,200,200))
        s2 = pygame.Surface((sqSize,sqSize))
        s2.fill(HIGHLIGHT)
        if WIDTH//5 <= mouse[0] <= WIDTH//5+sqSize and HEIGHT//3 <= mouse[1] <= HEIGHT//3+sqSize: 
          screen.blit(s2,(WIDTH//5,HEIGHT//3))
          if click[0] == 1:
            cP.position[cP.promotionSquare[0]][cP.promotionSquare[1]] = 'q'   
            cP.blackPromotion = False   
        else: 
          screen.blit(s1,(WIDTH//5,HEIGHT//3))

        if WIDTH//5+sqSize <= mouse[0] <= WIDTH//5+(2*sqSize) and HEIGHT//3 <= mouse[1] <= HEIGHT//3+sqSize: 
          screen.blit(s2,(WIDTH//5+sqSize,HEIGHT//3))
          if click[0] == 1:
            cP.position[cP.promotionSquare[0]][cP.promotionSquare[1]] = 'r'   
            cP.blackPromotion = False        
        else: 
           screen.blit(s1,(WIDTH//5+sqSize,HEIGHT//3))

        if WIDTH//5+(2*sqSize) <= mouse[0] <= WIDTH//5+(3*sqSize) and HEIGHT//3 <= mouse[1] <= HEIGHT//3+sqSize: 
          screen.blit(s2,(WIDTH//5+(sqSize*2),HEIGHT//3))
          if click[0] == 1:     
            cP.position[cP.promotionSquare[0]][cP.promotionSquare[1]] = 'b'   
            cP.blackPromotion = False     
        else: 
           screen.blit(s1,(WIDTH//5+(sqSize*2),HEIGHT//3))
        
        if WIDTH//5+(3*sqSize) <= mouse[0] <= WIDTH//5+(4*sqSize) and HEIGHT//3 <= mouse[1] <= HEIGHT//3+sqSize: 
          screen.blit(s2,(WIDTH//5+(sqSize*3),HEIGHT//3))
          if click[0] == 1:     
            cP.position[cP.promotionSquare[0]][cP.promotionSquare[1]] = 'n'   
            cP.blackPromotion = False   
        else: 
           screen.blit(s1,(WIDTH//5+(sqSize*3),HEIGHT//3))

        show_text("Pick a piece to promote to",WIDTH//5+10,HEIGHT//3.4,22)
        screen.blit(IMAGES['q'],(WIDTH//5,HEIGHT//3))
        screen.blit(IMAGES['r'],(WIDTH//5+sqSize,HEIGHT//3))
        screen.blit(IMAGES['b'],(WIDTH//5+(sqSize*2),HEIGHT//3))
        screen.blit(IMAGES['n'],(WIDTH//5+(sqSize*3),HEIGHT//3))
    if gameStatus == 'MENU':
      if 50 <= mouse[0] <= 270 and 200 <= mouse[1] <= 240: 
        play = buttonfont.render("Play Game", True, DARK)
        if click[0] == 1:
          gameStatus = "GAME"
          cP.position = [
          ["r","n","b","q","k","b","n","r"],
          ["p","p","p","p","p","p","p","p"],
          [" "," "," "," "," "," "," "," "],
          [" "," "," "," "," "," "," "," "],
          [" "," "," "," "," "," "," "," "],
          [" "," "," "," "," "," "," "," "],
          ["P","P","P","P","P","P","P","P"],
          ["R","N","B","Q","K","B","N","R"], 
          ]
          cP.pgn = []
          cP.notation = []
         

      else: 
        play = buttonfont.render("Play Game", True, LIGHT)

      if 50 <= mouse[0] <= 270 and 300 <= mouse[1] <= 340: 
        load = buttonfont.render("Load Position", True, DARK)
        if click[0] == 1:
          gameStatus = "LOAD"
         

      else: 
        load = buttonfont.render("Load Position", True, LIGHT)
        
      if 50 <= mouse[0] <= 220 and 500 <= mouse[1] <= 540: 
        read_me = buttonfont.render("About", True, DARK)
        if click[0] == 1:
          gameStatus = 'READ_ME'       
      else: 
        read_me = buttonfont.render("About", True, LIGHT)

      if 50 <= mouse[0] <= 220 and 400 <= mouse[1] <= 440: 
        puzzles = buttonfont.render("Puzzles", True, DARK)
        if click[0] == 1:
          gameStatus = 'PUZZLES'       
      else: 
        puzzles = buttonfont.render("Puzzles", True, LIGHT)
      title = titlefont.render("Brilliant Mates",True, DARK)
      screen.blit(title,(150,50))
      screen.blit(play,(50,200))
      screen.blit(load,(50,300))
      screen.blit(read_me,(50,500))
      screen.blit(puzzles,(50,400))
      screen.blit(IMAGES['q'],(500,180))
      screen.blit(IMAGES['K'],(550,220))
      screen.blit(IMAGES['n'],(600,280))
      screen.blit(IMAGES['B'],(650,320))
    if gameStatus == 'READ_ME':
      screen.blit(IMAGES['q'],(100,10))
      screen.blit(IMAGES['K'],(300,10))
      screen.blit(IMAGES['n'],(500,10))
      screen.blit(IMAGES['B'],(700,10))
      text1 = pfont.render("Brilliant Mates is a two person chess game where players are able to play and keep track of moves,", True, LIGHT)
      screen.blit(text1,(40,150))
      text2 = pfont.render("undo and flip board, as well as the abilities to castle and use en passant.", True, LIGHT)
      screen.blit(text2,(40,200))
      text3 = pfont.render("In the future, Brilliant Mates will include a puzzle system, importing of pgns, and a chess engine.", True, LIGHT)
      screen.blit(text3,(40,250))
      text4 = pfont.render("There is also a new game mode in the works where there will be a new piece and unique abilities for each player.", True, LIGHT)
      screen.blit(text4,(40,300))
      text4 = pfont.render("Enjoy our game and let me know how you feel about it!", True, LIGHT)
      screen.blit(text4,(40,350))
      screen.blit(IMAGES['q'],(100,500))
      screen.blit(IMAGES['K'],(300,500))
      screen.blit(IMAGES['n'],(500,500))
      screen.blit(IMAGES['B'],(700,500))
      screen.blit(extraIMAGES[4],(350,400))
      show_text("Back To Menu",335,450,sqSize-30)
      if 300 <= mouse[0] <= 400 and 400 <= mouse[1] <= 500: 
        if click[0] == 1:
          gameStatus = 'MENU'   
    if gameStatus == "LOAD":
      all_positions = cP.get_positions().fetchall()
      #print(all_positions)
      
      menu = pygame_menu.Menu('Load Position', WIDTH, HEIGHT, theme=pygame_menu.themes.THEME_DARK)
      pygame_menu.widgets.MENUBAR_STYLE_SIMPLE
      menu.add.text_input('FEN Notation :', default='')
      menu.add.button('Load Positon')
      menu.add.button('Back To Menu',change_status(gameStatus,"MENU"))
      menu.mainloop(screen)
      '''
      if 50 <= mouse[0] <= 220 and 400 <= mouse[1] <= 440: 
        read_me = buttonfont.render("game", True, DARK)
        if click[0] == 1:
          gameStatus = 'GAME'
          ##print(all_positions[1][2])
          #cP.load_position(all_positions[1][2])   
      else: 
        read_me = buttonfont.render("game", True, LIGHT)
      screen.blit(read_me,(50,400))
      '''
    if gameStatus == "PUZZLES":
      puzzle_title = titlefont.render("Puzzles",True, DARK)
      if 50 <= mouse[0] <= 600 and 200 <= mouse[1] <= 240: 
        easy = buttonfont.render("Solve Random Easy Puzzle", True, DARK)
        if click[0] == 1:
          rand_puz = cP.load_random_puzzle(1)
          if rand_puz is not None:
            cP.load_position(rand_puz)
            gameStatus = "GAME"
      else: 
        easy = buttonfont.render("Solve Random Easy Puzzle", True, LIGHT)
      screen.blit(easy,(50,200)) 

      if 50 <= mouse[0] <= 600 and 300 <= mouse[1] <= 340: 
        medium = buttonfont.render("Solve Random Medium Puzzle", True, DARK)
        if click[0] == 1:
          rand_puz = cP.load_random_puzzle(2)
          if rand_puz is not None:
            cP.load_position(rand_puz)
            gameStatus = "GAME"
      else: 
        medium = buttonfont.render("Solve Random Medium Puzzle", True, LIGHT)
      screen.blit(medium,(50,300))

      if 300 <= mouse[0] <= 600 and 400 <= mouse[1] <= 440: 
        hard = buttonfont.render("Solve Random Hard Puzzle", True, DARK)
        if click[0] == 1:
          rand_puz = cP.load_random_puzzle(3)
          if rand_puz is not None:
            cP.load_position(rand_puz)
            gameStatus = "GAME"   
      else: 
        hard = buttonfont.render("Solve Random Hard Puzzle", True, LIGHT)
      screen.blit(hard,(50,400))  
      screen.blit(puzzle_title,(250,50))
      #picked_puzzle = 
      #for i,v in enumerate(all_positions):
      #  txt = pfont.render(v[0]+"   "+v[1]+"   "+v[2], True, LIGHT)
      #  screen.blit(txt,(200,(i*50)+padding))
      #  if i == 1:
      #    load_text = v[2]
    pygame.display.flip()
if __name__ == "__main__":
  main()      
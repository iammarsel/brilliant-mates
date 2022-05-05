import pygame
import pygame_menu
import sys
import os
from pygame.locals import *
import time
pygame.init()
pygame.font.init()

WIDTH,HEIGHT = 800,600
sqSize = 50
padding = 50

letters = ['a','b','c','d','e','f','g','h']
titlefont = pygame.font.SysFont(None,100)
buttonfont = pygame.font.SysFont(None, 60)
pfont = pygame.font.SysFont(None, 20)
fps = 60
fpsClock = pygame.time.Clock()
screen = pygame.display.set_mode((WIDTH,HEIGHT))
programIcon = pygame.image.load('images/bK.png')
pygame.display.set_caption('Brilliant Mates')
pygame.display.set_icon(programIcon)


# class for the current position of the game
class CurrentPosition():
  def __init__(self):
    self.position = [
      ["bR","bN","bB","bQ","bK","bB","bN","bR"],
      ["bP","bP","bP","bP","bP","bP","bP","bP"],
      ["na","na","na","na","na","na","na","na"],
      ["na","na","na","na","na","na","na","na"],
      ["na","na","na","na","na","na","na","na"],
      ["na","na","na","na","na","na","na","na"],
      ["wP","wP","wP","wP","wP","wP","wP","wP"],
      ["wR","wN","wB","wQ","wK","wB","wN","wR"], 
    ]
    self.whiteToMove = True
    self.notation = []
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
    self.promotionPiece = 'na'
    self.promotionSquare = []
  def make_move(self,move):
    #print(move.piece1)
    if move.piece1 != 'na' and (move.piece1[0] != move.piece2[0]) and move.piece2[1] != 'K':
      # en passant taken as white
      print('check ',(move.Row1 - move.Row2),(move.Col1 - move.Col2))

      if move.piece1 == 'wP' and self.whiteEnPassantLeft == True and move.Row1 - move.Row2 == 1 and move.Col1 - move.Col2 == 1 and self.position[move.Row2][move.Col2] == 'na':
        self.position[move.Row2+1][move.Col2] = 'na'
        print('en passant taken',move.Row2,move.Col2)

      if move.piece1 == 'wP' and self.whiteEnPassantRight == True and move.Row1 - move.Row2 == 1 and move.Col1 - move.Col2 == -1 and self.position[move.Row2][move.Col2] == 'na':
        self.position[move.Row2+1][move.Col2] = 'na'
        print('en passant taken',move.Row2,move.Col2)

      if move.piece1 == 'bP' and self.blackEnPassantLeft == True and move.Row1 - move.Row2 == -1 and move.Col1 - move.Col2 == 1 and self.position[move.Row2][move.Col2] == 'na':
        self.position[move.Row2-1][move.Col2] = 'na'
        print('en passant taken',move.Row2,move.Col2)

      if move.piece1 == 'bP' and self.blackEnPassantRight == True and move.Row1 - move.Row2 == -1 and move.Col1 - move.Col2 == -1 and self.position[move.Row2][move.Col2] == 'na':
        self.position[move.Row2-1][move.Col2] = 'na'
        print('en passant taken',move.Row2,move.Col2)

      self.position[move.Row1][move.Col1] = 'na'
      self.position[move.Row2][move.Col2] = move.piece1
      # king side castle
      if move.piece1[1] == 'K' and (move.Col1+2) == move.Col2 and self.whiteInCheck == False and self.blackInCheck == False:
        temp = self.position[move.Row1][move.Col1+3]
        self.position[move.Row1][move.Col1+3] = 'na'
        self.position[move.Row2][move.Col1+1] = temp
      if move.piece1 == 'wK' or move.piece1 == 'wR':
        self.whiteCastlePossible = False
      if move.piece1 == 'bK' or move.piece1 == 'bR':
        self.blackCastlePossible = False
      # queen side castle
      if move.piece1[1] == 'K' and (move.Col1-2) == move.Col2 and self.whiteInCheck == False and self.blackInCheck == False:
        temp = self.position[move.Row1][move.Col1+3]
        self.position[move.Row1][move.Col1-4] = 'na'
        self.position[move.Row2][move.Col1-1] = temp
      #en passant as black activation
      if move.piece1 == 'bP' and abs(move.Row1 - move.Row2) == 2:
        print(move.Row1,move.Col1)
        print(self.position[move.Row2][move.Col2-1]+' hi')
        if move.Col2 < 7:
          if self.position[move.Row2][move.Col2+1] == 'wP':
            self.whiteEnPassantLeft = True
            self.enPassantSquare = [move.Row2,move.Col2+1]
            print(move.Row1,move.Row2)
            print('left active')
        if move.Col2 > 0:
          if self.position[move.Row2][move.Col2-1] == 'wP':
            self.whiteEnPassantRight = True
            self.enPassantSquare = [move.Row2,move.Col2-1]
            print(move.Row1,move.Row2)
            print('right active')
      # en passant as white activation
      if move.piece1 == 'wP' and abs(move.Row1 - move.Row2) == 2:
        print(self.position[move.Row2][move.Col2-1]+' hi')
        if move.Col2 < 7:
          if self.position[move.Row2][move.Col2+1] == 'bP':
            self.blackEnPassantLeft = True
            self.enPassantSquare = [move.Row2,move.Col2+1]
            print(move.Row1,move.Row2)
            print('left active')
        if move.Col2 > 0:
          if self.position[move.Row2][move.Col2-1] == 'bP':
            self.blackEnPassantRight = True
            self.enPassantSquare = [move.Row2,move.Col2-1]
            print(move.Row1,move.Row2)
            print('right active')
      if move.piece1[0] == 'w':
        self.whiteEnPassantLeft = False
        self.whiteEnPassantRight = False
      if move.piece1[0] == 'b':
        self.blackEnPassantLeft = False
        self.blackEnPassantRight = False
      self.notation.append(move)
      self.whiteToMove = not self.whiteToMove
      # taking with en passant as white
      # pawn promotion
      if move.piece1[1] == 'P' and (move.Row2 == 0 or move.Row2 == 7):
        if move.Row2 == 7:
          self.blackPromotion = True
        if move.Row2 == 0:
          self.whitePromotion = True
        self.promotionSquare = [move.Row2,move.Col2]
  def undo_last_move(self,pgn):
    if len(self.notation)>0 and len(pgn) > 0:
      # undo castle
      print(self.notation[-1].Col2 - self.notation[-1].Col1)
      if self.notation[-1].piece1[1] == 'K' and (self.notation[-1].Col2 - self.notation[-1].Col1) == 2:
        self.position[self.notation[-1].Row1][self.notation[-1].Col2+1] = self.notation[-1].piece1[0]+'R'
        self.position[self.notation[-1].Row1][self.notation[-1].Col2-1] = 'na'
        if self.notation[-1].piece1[0] == 'w':
          self.whiteCastlePossible = True
        else:
          self.blackCastlePossible = True
      if self.notation[-1].piece1[1] == 'K' and (self.notation[-1].Col2 - self.notation[-1].Col1) == -2:
        self.position[self.notation[-1].Row1][self.notation[-1].Col2-2] = self.notation[-1].piece1[0]+'R'
        self.position[self.notation[-1].Row1][self.notation[-1].Col2+1] = 'na'
        if self.notation[-1].piece1[0] == 'w':
          self.whiteCastlePossible = True
        else:
          self.blackCastlePossible = True
      print(self.notation)
      print(pgn)
      self.position[self.notation[-1].Row1][self.notation[-1].Col1] = self.notation[-1].piece1
      self.position[self.notation[-1].Row2][self.notation[-1].Col2] = self.notation[-1].piece2
      self.notation.pop()
      pgn.pop()
      self.whiteToMove = not self.whiteToMove
      self.blackPromotion = False
      self.whitePromotion = False

  def bishop(self,piece,possible_moves,color,output):
    opposite = ''
    if color == 1:
      opposite = 'b'
    else:
      opposite = 'w'
    temp = piece[0]-1
    for j in range(piece[1],7):
      if self.position[temp][j+1] == 'na':
        move = (temp,j+1)
        output.append(move)
        temp -= 1
      else:
        if self.position[temp][j+1][0] == opposite:
          move = (temp,j+1)
          output.append(move)
        break
        # bishop top left move
    temp = piece[0]
    for j in range((piece[1]), 0, -1):
      if self.position[temp-1][j-1] == 'na':
        move = (temp-1,j-1)
        output.append(move)
        temp -= 1
      else:
        if self.position[temp-1][j-1][0] == opposite:
          move = (temp-1,j-1)
          output.append(move)
        break
        # bishop bottom right move
    temp = piece[0]
    for j in range(piece[1],7):
      if temp < 7:
        if self.position[temp+1][j+1] == 'na':
          temp += 1
          move = (temp,j+1)
          output.append(move)
        else:
          if self.position[temp+1][j+1][0] == opposite:
            move = (temp+1,j+1)
            output.append(move)
          break
        # bishop bottom left move
    temp = piece[0]
    for j in range((piece[1]), 0, -1):
      if temp < 7:
        if self.position[temp+1][j-1] == 'na':
          temp += 1
          move = (temp,j-1)
          output.append(move)
        else:
          if self.position[temp+1][j-1][0] == opposite:
            move = (temp+1,j-1)
            output.append(move)
          break
  def rook(self,piece,possible_moves,color,output):
    opposite = ''
    if color == 1:
      opposite = 'b'
    else:
      opposite = 'w'
    for i in range((piece[0]-1), -1, -1):
      if self.position[i][piece[1]] == 'na':
        move = (i,piece[1])
        output.append(move)
      else:
        if self.position[i][piece[1]][0] == opposite:
          move = (i,piece[1])
          output.append(move)
        break
    for i in range((piece[0]+1),8):
      if self.position[i][piece[1]] == 'na':
        move = (i,piece[1])
        output.append(move)
      else:
        if self.position[i][piece[1]][0] == opposite:
          move = (i,piece[1])
          output.append(move)
        break
    for i in range((piece[1]-1), -1, -1):
      if self.position[piece[0]][i] == 'na':
        move = (piece[0],i)
        output.append(move)
      else:
        if self.position[piece[0]][i][0] == opposite:
          move = (piece[0],i)
          output.append(move)
        break
    for i in range((piece[1]+1),8):
      if self.position[piece[0]][i] == 'na':
        move = (piece[0],i)
        output.append(move)
      else:
        if self.position[piece[0]][i][0] == opposite:
          move = (piece[0],i)
          output.append(move)
        break
  def knight(self,piece,possible_moves,color,output):
    opposite = ''
    if color == 1:
      opposite = 'b'
    else:
      opposite = 'w'
    if piece[0] > 0 and piece[1] > 1:
      if self.position[piece[0]-1][piece[1]-2] == 'na' or self.position[piece[0]-1][piece[1]-2][0] == opposite:
        move = (piece[0]-1,piece[1]-2)
        output.append(move)
    if piece[0] > 0 and piece[1] < 6:
      if self.position[piece[0]-1][piece[1]+2] == 'na' or self.position[piece[0]-1][piece[1]+2][0] == opposite:
        move = (piece[0]-1,piece[1]+2)
        output.append(move)
    if piece[0] > 1 and piece[1] > 0:
      if self.position[piece[0]-2][piece[1]-1] == 'na' or self.position[piece[0]-2][piece[1]-1][0] == opposite:
        move = (piece[0]-2,piece[1]-1)
        output.append(move)
    if piece[0] > 1 and piece[1] < 7:
      if self.position[piece[0]-2][piece[1]+1] == 'na' or self.position[piece[0]-2][piece[1]+1][0] == opposite:
        move = (piece[0]-2,piece[1]+1)
        output.append(move)
    if piece[0] < 6 and piece[1] < 7:
      if self.position[piece[0]+2][piece[1]+1] == 'na' or self.position[piece[0]+2][piece[1]+1][0] == opposite:
        move = (piece[0]+2,piece[1]+1)
        output.append(move)  
    if piece[0] < 6 and piece[1] > 0:
      if self.position[piece[0]+2][piece[1]-1] == 'na' or self.position[piece[0]+2][piece[1]-1][0] == opposite:
        move = (piece[0]+2,piece[1]-1)
        output.append(move)  
    if piece[0] < 7 and piece[1] > 1:
      if self.position[piece[0]+1][piece[1]-2] == 'na' or self.position[piece[0]+1][piece[1]-2][0] == opposite:
        move = (piece[0]+1,piece[1]-2)
        output.append(move)
    if piece[0] < 7 and piece[1] < 6:
      if self.position[piece[0]+1][piece[1]+2] == 'na' or self.position[piece[0]+1][piece[1]+2][0] == opposite:
        move = (piece[0]+1,piece[1]+2)
        output.append(move) 
  def king(self,piece,possible_moves,color,output):
    if color == 1:
      castleType = self.whiteCastlePossible
      opposite = 'b'
    else:
      castleType = self.blackCastlePossible
      opposite = 'w'
    if piece[0] > 0:
      if self.position[piece[0]-1][piece[1]] == 'na' or self.position[piece[0]-1][piece[1]][0] == opposite:
        move = (piece[0]-1,piece[1])
        output.append(move)
      if piece[1] > 0:
        if self.position[piece[0]-1][piece[1]-1] == 'na' or self.position[piece[0]-1][piece[1]-1][0] == opposite:
          move = (piece[0]-1,piece[1]-1)
          output.append(move)

      if piece[1] < 7:
        if self.position[piece[0]-1][piece[1]+1] == 'na' or self.position[piece[0]-1][piece[1]+1][0] == opposite:
          move = (piece[0]-1,piece[1]+1)
          output.append(move)
    if piece[0] < 7:
      if self.position[piece[0]+1][piece[1]] == 'na' or self.position[piece[0]+1][piece[1]][0] == opposite:
        move = (piece[0]+1,piece[1])
        output.append(move)
      if piece[1] > 0:
        if self.position[piece[0]+1][piece[1]-1] == 'na' or self.position[piece[0]+1][piece[1]-1][0] == opposite:
          move = (piece[0]+1,piece[1]-1)
          output.append(move)
      if piece[1] < 7:
        if self.position[piece[0]+1][piece[1]+1] == 'na' or self.position[piece[0]+1][piece[1]+1][0] == opposite:
          move = (piece[0]+1,piece[1]+1)
          output.append(move)
    if piece[1] > 0:
      if self.position[piece[0]][piece[1]-1] == 'na' or self.position[piece[0]][piece[1]-1][0] == opposite:
          move = (piece[0],piece[1]-1)
          output.append(move)
    if piece[1] < 7:
      if self.position[piece[0]][piece[1]+1] == 'na' or self.position[piece[0]][piece[1]+1][0] == opposite:
          move = (piece[0],piece[1]+1)
          output.append(move)
    #  Castle
    # King Side
    if castleType == True and self.position[piece[0]][piece[1]+1] == 'na' and self.position[piece[0]][piece[1]+2] == 'na':
      move = (piece[0],piece[1]+2)
      output.append(move)
    # Queen Side
    if castleType == True and self.position[piece[0]][piece[1]-1] == 'na' and self.position[piece[0]][piece[1]-2] == 'na' and self.position[piece[0]][piece[1]-3] == 'na':
      move = (piece[0],piece[1]-2)
      output.append(move)
  def get_legal_moves(self,piece,possible_moves):
    print('square is ',self.enPassantSquare)
    if self.blackPromotion == True or self.whitePromotion == True:
      return []
    output = []
    self.selected_piece = self.position[piece[0]][piece[1]]
    print(self.selected_piece)
    if self.selected_piece[1] == 'P':
      if self.selected_piece[0] == 'w' and self.whiteToMove == True:
        if 0 < piece[0] < 7:
          if self.position[piece[0]-1][piece[1]] == 'na':
            move = (piece[0]-1,piece[1])
            output.append(move)  
            if self.position[piece[0]-2][piece[1]] == 'na' and piece[0] == 6:
              move = (piece[0]-2,piece[1])
              output.append(move)
          if piece[1] > 0:
            if self.position[piece[0]-1][piece[1]-1] != 'na' and self.position[piece[0]-1][piece[1]-1][0] != 'w':
              move = (piece[0]-1,piece[1]-1)
              output.append(move)
          if piece[1] < 7:
            if self.position[piece[0]-1][piece[1]+1] != 'na' and self.position[piece[0]-1][piece[1]+1][0] != 'w':
              move = (piece[0]-1,piece[1]+1)
              output.append(move)
         # en passant (white)
          if 0 < piece[1] < 7:
            if self.whiteEnPassantLeft == True and self.enPassantSquare == [piece[0],piece[1]] and self.position[piece[0]][piece[1]-1][0] == 'b' and self.position[piece[0]-1][piece[1]+1] == 'na':
              move = (piece[0]-1,piece[1]-1)
              output.append(move)
          if 0 < piece[1] < 7:
            if self.whiteEnPassantRight == True and self.enPassantSquare == [piece[0],piece[1]] and self.position[piece[0]][piece[1]+1][0] == 'b' and self.position[piece[0]-1][piece[1]-1] == 'na':
              move = (piece[0]-1,piece[1]+1)
              output.append(move)
          
      elif self.selected_piece[0] == 'b' and self.whiteToMove == False:
        if 0 < piece[0] < 7:
          #move up one 
          if self.position[piece[0]+1][piece[1]] == 'na':
            move = (piece[0]+1,piece[1])
            output.append(move)
            # move up twice
            if piece[0] == 1:
              if self.position[piece[0]+2][piece[1]] == 'na':
                move = (piece[0]+2,piece[1])
                output.append(move)
          # taking a piece
          if piece[1] < 7:
            if self.position[piece[0]+1][piece[1]+1] != 'na' and self.position[piece[0]+1][piece[1]+1][0] != 'b':
              move = (piece[0]+1,piece[1]+1)
              output.append(move)
          if piece[1] < 8:
            if self.position[piece[0]+1][piece[1]-1] != 'na' and self.position[piece[0]+1][piece[1]-1][0] != 'b':
              move = (piece[0]+1,piece[1]-1)
              output.append(move)
          # en passant (white)
          if piece[1] < 7:
            if self.blackEnPassantRight == True and self.enPassantSquare == [piece[0],piece[1]] and self.position[piece[0]][piece[1]+1] == 'wP' and self.position[piece[0]+1][piece[1]+1] == 'na':
              move = (piece[0]+1,piece[1]+1)
              output.append(move)
          if piece[1] < 8:
            if self.blackEnPassantLeft == True and self.enPassantSquare == [piece[0],piece[1]] and self.position[piece[0]][piece[1]-1] == 'wP' and self.position[piece[0]+1][piece[1]-1] == 'na':
              move = (piece[0]+1,piece[1]-1)
              output.append(move)
    # Rook Move
    elif self.selected_piece[1] == 'R':
      if self.selected_piece[0] == 'w' and self.whiteToMove == True:
        self.rook(piece,possible_moves,1,output)
      if self.selected_piece[0] == 'b' and self.whiteToMove == False:
        self.rook(piece,possible_moves,2,output)
    # Bishop Move
    elif self.selected_piece[1] == 'B':
      if self.selected_piece[0] == 'w' and self.whiteToMove == True:
        self.bishop(piece,possible_moves,1,output)
      if self.selected_piece[0] == 'b' and self.whiteToMove == False:
        self.bishop(piece,possible_moves,2,output)
    # King Move
    elif self.selected_piece[1] == 'K':
      if self.selected_piece[0] == 'w' and self.whiteToMove == True:
        self.king(piece,possible_moves,1,output)
      if self.selected_piece[0] == 'b' and self.whiteToMove == False:
        self.king(piece,possible_moves,2,output)
    # Queen Move
    elif self.selected_piece[1] == 'Q':
      if self.selected_piece[0] == 'w' and self.whiteToMove == True:
        self.rook(piece,possible_moves,1,output)
        self.bishop(piece,possible_moves,1,output)
      if self.selected_piece[0] == 'b' and self.whiteToMove == False:
        self.rook(piece,possible_moves,2,output)
        self.bishop(piece,possible_moves,2,output)
    # Knight Move
    elif self.selected_piece[1] == 'N':
      if self.selected_piece[0] == 'w' and self.whiteToMove == True:
        self.knight(piece,possible_moves,1,output)
      if self.selected_piece[0] == 'b' and self.whiteToMove == False:
        self.knight(piece,possible_moves,2,output)
    return output



class Move(): # (1,1) = (8,a)
  ranksToRows = {"1":7,"2":6,"3":5,"4":4,"5":3,"6":2,"7":1,"8":0}
 
  rowsToRanks = {v: k for k,v in ranksToRows.items()}
  filesToCols = {"a":0,"b":1,"c":2,"d":3,"e":4,"f":5,"g":6,"h":7}
  colsToFiles = {v: k for k,v in filesToCols.items()}

  flipToReg = {7:0,6:1,5:2,4:3,3:4,2:5,1:6,0:7}
  regToFiles = {v: k for k,v in flipToReg.items()}

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
    output = self.piece1[1]
    takes = 'x'
    check = '+' # for checkmate
    if self.piece2 == 'na':
      takes = ''
    if self.piece1[1] == 'P':
      output = ''
      if abs(self.Row1 - self.Row2) == 1 and  abs(self.Col1 - self.Col2) == 1:
        takes = 'x'
    if self.piece1 == 'na' or (self.piece1[0] == self.piece2[0]) or self.piece2[1] == 'K':
      return 'na'
    if self.piece1[1] == 'K' and (self.Col2 - self.Col1) == 2:
      return '0-0'
    if self.piece1[1] == 'K' and (self.Col2 - self.Col1) == -2:
      return '0-0-0'
    return output + takes + self.getRankFile(self.Row2,self.Col2)

  def getRankFile(self,r,c):
    return self.colsToFiles[c] + self.rowsToRanks[r]
  def getFlip(self,n):
    return self.regToFiles[n]
cP = CurrentPosition()

# colors 
LIGHT = (145, 134, 105)
DARK = (92, 80, 48)
BACKGROUND = (31, 31, 31)
HIGHLIGHT = pygame.Color(255, 232, 84)
extraIMAGES = {}
# chess pieces images
IMAGES = {}
def load_images():
  pieceSize = sqSize-3
  extraIMAGES[0] = pygame.transform.scale(pygame.image.load('images/flip.png').convert_alpha(),(pieceSize,pieceSize))
  extraIMAGES[1] = pygame.transform.scale(pygame.image.load('images/undo.png').convert_alpha(),(pieceSize,pieceSize))
  extraIMAGES[2] = pygame.transform.scale(pygame.image.load('images/back2.png').convert_alpha(),(pieceSize,pieceSize))
  pieces = ['K','Q','B','N','P','R']
  na = ''
  for p in pieces:
    IMAGES['w'+p] = pygame.transform.scale(pygame.image.load('images/w'+p+'.png').convert_alpha(),(pieceSize,pieceSize))
    IMAGES['b'+p] = pygame.transform.scale(pygame.image.load('images/b'+p+'.png').convert_alpha(),(pieceSize,pieceSize))
# show coordinates on board
def show_text(text,x,y,size):
  font = pygame.font.SysFont(None,size)
  text = font.render(text, True, LIGHT)
  screen.blit(text,(x,y))



def draw_board(currentP,flipboard):
    colorSwitch = DARK
    for i in range(8):
      if colorSwitch == DARK:
        colorSwitch = LIGHT
      else:
        colorSwitch = DARK
      if flipboard == 1:
        a = show_text(str(i+1),padding*0.65,360-(sqSize*i)+padding,sqSize-20)
        b = show_text(letters[i],(sqSize*1.4)+(sqSize*i),9*sqSize,sqSize-20)
      elif flipboard == 2:
        a = show_text(str(i+1),padding*0.65,(sqSize*i)+padding,sqSize-20)
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
          if currentP[i][j] != 'na':
            screen.blit(IMAGES[currentP[i][j]],((padding+sqSize*j),(padding+sqSize*i)))
    elif flipboard == 2:
      for i in reversed(range(1,9)):
        for j in reversed(range(1,9)):
          if currentP[-i][-j] != 'na':
            screen.blit(IMAGES[currentP[-i][-j]],((sqSize*j),(sqSize*i)))

def main():
  load_images()
  screen.fill((BACKGROUND))
  squareSelected = ()
  pgn = []
  moveBox = ""
  possible_moves = []
  clicks = []
  running = True
  flipboard = 1
  gameStatus = 'MENU'
  while running:
    screen.fill((BACKGROUND))
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
    for event in pygame.event.get():
        if event.type == QUIT:
          running = False
        elif event.type == KEYDOWN and event.key == K_ESCAPE:
          running = False
        elif event.type == KEYDOWN and event.key == K_f:
          screen.fill((BACKGROUND))
          if flipboard == 1:
            flipboard = 2
          else: 
            flipboard = 1
        elif event.type == pygame.MOUSEBUTTONDOWN:
          if padding <= mouse[0] <= padding+50 and padding+(sqSize*9) <= mouse[1] <= padding+(sqSize*9)+sqSize: 
            screen.fill((BACKGROUND))
            if flipboard == 1:
              flipboard = 2
            else: 
              flipboard = 1
          elif padding*2.6 <= mouse[0] <= padding*2.6+50 and padding+(sqSize*9) <= mouse[1] <= padding+(sqSize*9)+sqSize: 
            cP.undo_last_move(pgn)
            possible_moves = []
            squareSelected = ()
            clicks = []
          elif padding*4.2 <= mouse[0] <= padding*4.2+50 and padding+(sqSize*9) <= mouse[1] <= padding+(sqSize*9)+sqSize: 
            gameStatus = 'MENU'
          row = (mouse[0]-padding)//sqSize
          col = (mouse[1]-padding)//sqSize
        
          if 0<= row <= 7 and 0 <= col <= 7 and gameStatus == 'GAME':
            if squareSelected == (col,row):
              squareSelected = ()
              clicks = []
              possible_moves = []
            else:
              squareSelected = (col,row)
              clicks.append(squareSelected)
            if len(clicks) == 1:
              possible_moves = cP.get_legal_moves(clicks[0],possible_moves)
            if len(clicks) == 2:
              print(clicks[1])
              if clicks[1] in possible_moves:
                move = Move(clicks[0],clicks[1],cP.position,flipboard)
                cP.make_move(move)
                if move.getNotation() != 'na':
                  pgn.append(move.getNotation())
              squareSelected = ()
              clicks = []
              possible_moves = []

    if gameStatus == 'GAME':
      draw_board(cP.position,flipboard)
      draw_pieces(cP.position,flipboard)
      screen.blit(extraIMAGES[0],(padding,padding+(sqSize*9)))
      screen.blit(extraIMAGES[1],(padding*2.6,padding+(sqSize*9)))
      screen.blit(extraIMAGES[2],(padding*4.2,padding+(sqSize*9)))
      show_text("Flip Board",padding,padding+(sqSize*9)+52,sqSize-30)
      show_text("Undo Move",padding*2.6,padding+(sqSize*9)+52,sqSize-30)
      show_text("Back To Menu",padding*4.2,padding+(sqSize*9)+52,sqSize-30)
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
      for i in range(0,len(pgn)):
        if i % 2 == 0:
          show_text(str(c) + " | ",(sqSize*9)+30,padding+(i*25),sqSize-10)
          show_text(pgn[i],(sqSize*9)+90,padding+(i*25),sqSize-10)
          c += 1
        else:
          show_text(pgn[i],(sqSize*9)+170,padding+((i-1)*25),sqSize-10)
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
            cP.position[cP.promotionSquare[0]][cP.promotionSquare[1]] = 'wQ'   
            cP.whitePromotion = False   
        else: 
          screen.blit(s1,(WIDTH//5,HEIGHT//3))

        if WIDTH//5+sqSize <= mouse[0] <= WIDTH//5+(2*sqSize) and HEIGHT//3 <= mouse[1] <= HEIGHT//3+sqSize: 
          screen.blit(s2,(WIDTH//5+sqSize,HEIGHT//3))
          if click[0] == 1:
            cP.position[cP.promotionSquare[0]][cP.promotionSquare[1]] = 'wR'   
            cP.whitePromotion = False        
        else: 
           screen.blit(s1,(WIDTH//5+sqSize,HEIGHT//3))

        if WIDTH//5+(2*sqSize) <= mouse[0] <= WIDTH//5+(3*sqSize) and HEIGHT//3 <= mouse[1] <= HEIGHT//3+sqSize: 
          screen.blit(s2,(WIDTH//5+(sqSize*2),HEIGHT//3))
          if click[0] == 1:   
            cP.position[cP.promotionSquare[0]][cP.promotionSquare[1]] = 'wB'   
            cP.whitePromotion = False     
        else: 
           screen.blit(s1,(WIDTH//5+(sqSize*2),HEIGHT//3))
        
        if WIDTH//5+(3*sqSize) <= mouse[0] <= WIDTH//5+(4*sqSize) and HEIGHT//3 <= mouse[1] <= HEIGHT//3+sqSize: 
          screen.blit(s2,(WIDTH//5+(sqSize*3),HEIGHT//3))
          if click[0] == 1:      
            cP.position[cP.promotionSquare[0]][cP.promotionSquare[1]] = 'wN'   
            cP.whitePromotion = False   
        else: 
           screen.blit(s1,(WIDTH//5+(sqSize*3),HEIGHT//3))
        show_text("Pick a piece to promote to",WIDTH//5+10,HEIGHT//3.4,22)
        screen.blit(IMAGES['wQ'],(WIDTH//5,HEIGHT//3))
        screen.blit(IMAGES['wR'],(WIDTH//5+sqSize,HEIGHT//3))
        screen.blit(IMAGES['wB'],(WIDTH//5+(sqSize*2),HEIGHT//3))
        screen.blit(IMAGES['wN'],(WIDTH//5+(sqSize*3),HEIGHT//3))
        

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
            cP.position[cP.promotionSquare[0]][cP.promotionSquare[1]] = 'bQ'   
            cP.blackPromotion = False   
        else: 
          screen.blit(s1,(WIDTH//5,HEIGHT//3))

        if WIDTH//5+sqSize <= mouse[0] <= WIDTH//5+(2*sqSize) and HEIGHT//3 <= mouse[1] <= HEIGHT//3+sqSize: 
          screen.blit(s2,(WIDTH//5+sqSize,HEIGHT//3))
          if click[0] == 1:
            cP.position[cP.promotionSquare[0]][cP.promotionSquare[1]] = 'bR'   
            cP.blackPromotion = False        
        else: 
           screen.blit(s1,(WIDTH//5+sqSize,HEIGHT//3))

        if WIDTH//5+(2*sqSize) <= mouse[0] <= WIDTH//5+(3*sqSize) and HEIGHT//3 <= mouse[1] <= HEIGHT//3+sqSize: 
          screen.blit(s2,(WIDTH//5+(sqSize*2),HEIGHT//3))
          if click[0] == 1:     
            cP.position[cP.promotionSquare[0]][cP.promotionSquare[1]] = 'bB'   
            cP.blackPromotion = False     
        else: 
           screen.blit(s1,(WIDTH//5+(sqSize*2),HEIGHT//3))
        
        if WIDTH//5+(3*sqSize) <= mouse[0] <= WIDTH//5+(4*sqSize) and HEIGHT//3 <= mouse[1] <= HEIGHT//3+sqSize: 
          screen.blit(s2,(WIDTH//5+(sqSize*3),HEIGHT//3))
          if click[0] == 1:     
            cP.position[cP.promotionSquare[0]][cP.promotionSquare[1]] = 'bN'   
            cP.blackPromotion = False   
        else: 
           screen.blit(s1,(WIDTH//5+(sqSize*3),HEIGHT//3))

        show_text("Pick a piece to promote to",WIDTH//5+10,HEIGHT//3.4,22)
        screen.blit(IMAGES['bQ'],(WIDTH//5,HEIGHT//3))
        screen.blit(IMAGES['bR'],(WIDTH//5+sqSize,HEIGHT//3))
        screen.blit(IMAGES['bB'],(WIDTH//5+(sqSize*2),HEIGHT//3))
        screen.blit(IMAGES['bN'],(WIDTH//5+(sqSize*3),HEIGHT//3))
    if gameStatus == 'MENU':
      if 50 <= mouse[0] <= 270 and 200 <= mouse[1] <= 240: 
        play = buttonfont.render("Play Game", True, DARK)
        if click[0] == 1:
          gameStatus = "GAME"      
      else: 
        play = buttonfont.render("Play Game", True, LIGHT)
        
      if 50 <= mouse[0] <= 220 and 300 <= mouse[1] <= 340: 
        settings = buttonfont.render("READ ME", True, DARK)
        if click[0] == 1:
          gameStatus = 'READ_ME'       
      else: 
        settings = buttonfont.render("READ ME", True, LIGHT)

      if 50 <= mouse[0] <= 180 and 400 <= mouse[1] <= 440: 
        about = buttonfont.render("Exit", True, DARK) 
        if click[0] == 1:
          gameStatus = 'Exit'
          running = False           
      else: 
        about = buttonfont.render("Exit", True, LIGHT)
      title = titlefont.render("Brilliant Mates",True, DARK)
      screen.blit(title,(150,50))
      screen.blit(play,(50,200))
      screen.blit(settings,(50,300))
      screen.blit(about,(50,400))
      screen.blit(IMAGES['bQ'],(500,180))
      screen.blit(IMAGES['wK'],(550,220))
      screen.blit(IMAGES['bN'],(600,280))
      screen.blit(IMAGES['wB'],(650,320))
    if gameStatus == 'READ_ME':
      screen.blit(IMAGES['bQ'],(100,10))
      screen.blit(IMAGES['wK'],(300,10))
      screen.blit(IMAGES['bN'],(500,10))
      screen.blit(IMAGES['wB'],(700,10))
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
      screen.blit(IMAGES['bQ'],(100,500))
      screen.blit(IMAGES['wK'],(300,500))
      screen.blit(IMAGES['bN'],(500,500))
      screen.blit(IMAGES['wB'],(700,500))
      screen.blit(extraIMAGES[2],(350,400))
      show_text("Back To Menu",335,450,sqSize-30)
      if 300 <= mouse[0] <= 400 and 400 <= mouse[1] <= 500: 
        if click[0] == 1:
          gameStatus = 'MENU'       
    pygame.display.flip()
if __name__ == "__main__":
    main()      
  
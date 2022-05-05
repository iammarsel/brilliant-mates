import pygame
import sys
from pygame.locals import *
import time

# Variable to keep the main loop running

running = True
pygame.init()

letters = ['a','b','c','d','e','f','g','h']
sysfont = pygame.font.get_default_font()
font = pygame.font.SysFont(None, 30)
sysfont = pygame.font.get_default_font()
titlefont = pygame.font.SysFont(None,100)
buttonfont = pygame.font.SysFont(None, 60)

fps = 60
fpsClock = pygame.time.Clock()
 
screen = pygame.display.set_mode((800,600))
programIcon = pygame.image.load('images/bQ.png')
pygame.display.set_caption('Brilliant Mates')
pygame.display.set_icon(programIcon)

# menu status
gameStatus = 'MainMenu'

# colors 
LIGHT = (145, 134, 105)
DARK = (92, 80, 48)
BACKGROUND = (62, 32, 128)

IMAGES = {}
# chess pieces images
def load_images():
  pieceSize = 45
  pieces = ['K','Q','B','N','P','R']
  na = ''
  for p in pieces:
    IMAGES['w'+p] = pygame.transform.scale(pygame.image.load('images/w'+p+'.png').convert_alpha(),(pieceSize,pieceSize))
    IMAGES['b'+p] = pygame.transform.scale(pygame.image.load('images/b'+p+'.png').convert_alpha(),(pieceSize,pieceSize))



def show_cord(text,x,y):
  text = font.render(text, True, LIGHT)
  screen.blit(text,(x,y))

def start_menu(gs):
  if 50 <= mouse[0] <= 270 and 200 <= mouse[1] <= 240: 
    play = buttonfont.render("Play Game", True, DARK)
    if click[0] == 1:
      play_game()       
  else: 
    play = buttonfont.render("Play Game", True, LIGHT)
        
  if 50 <= mouse[0] <= 220 and 300 <= mouse[1] <= 340: 
      settings = buttonfont.render("Settings", True, DARK)
      if click[0] == 1:
        gameStatus = 'Settings'       
  else: 
      settings = buttonfont.render("Settings", True, LIGHT)

  if 50 <= mouse[0] <= 180 and 400 <= mouse[1] <= 440: 
      about = buttonfont.render("About", True, DARK) 
      if click[0] == 1:
        gameStatus = 'About'           
  else: 
      about = buttonfont.render("About", True, LIGHT)
  title = titlefont.render("Brilliant Mates",True, DARK)
  screen.blit(title,(150,50))
  screen.blit(play,(50,200))
  screen.blit(settings,(50,300))
  screen.blit(about,(50,400))
  screen.blit(IMAGES['bQ'],(500,180))
  screen.blit(IMAGES['wK'],(550,220))
  screen.blit(IMAGES['bN'],(600,280))
  screen.blit(IMAGES['wB'],(650,320))

def play_game():
    # chess board generate
    current_position = [
      ["bR","bN","bB","bQ","bK","bB","bN","bR"],
      ["bP","bP","bP","bP","bP","bP","bP","bP"],
      ["na","na","na","na","na","na","na","na"],
      ["na","na","na","na","na","na","na","na"],
      ["na","na","na","na","na","na","na","na"],
      ["na","na","na","na","na","na","na","na"],
      ["wP","wP","wP","wP","wP","wP","wP","wP"],
      ["wR","wN","wB","wQ","wK","wB","wN","wR"],
      
    ]
    colorSwitch = DARK
    for i,v in enumerate(current_position):
      if colorSwitch == DARK:
        colorSwitch = LIGHT
      else:
        colorSwitch = DARK
      show_cord(str(i+1),30,65+(50*i))
      for j,k in enumerate(v):
        pygame.draw.rect(screen,colorSwitch,(50+(50*j),50+(50*i),50,50))
        show_cord(letters[i],60+(50*i),450)
        if v[j] != 'na':
          screen.blit(IMAGES[v[j]],(52+(50*j),50+(50*i)))
        if colorSwitch == DARK:
          colorSwitch = LIGHT
        else:
          colorSwitch = DARK


while running:
  load_images()
  screen.fill((BACKGROUND))
  mouse = pygame.mouse.get_pos() 
  click = pygame.mouse.get_pressed()
  for event in pygame.event.get():
      if event.type == QUIT:
        running = False
      if event.type == KEYDOWN and event.key == K_ESCAPE:
          running = False
  if gameStatus == 'MainMenu':
    start_menu(gameStatus)
  if gameStatus == 'Game':
    play_game()
   
  
    # mouse clicking/dragging
   
  pygame.display.flip()
  fpsClock.tick(fps)

  
        
  
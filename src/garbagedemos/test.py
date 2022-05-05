import pygame
pygame.init()

SCENE_MENU = 0
SCENE_GAME = 1


def menu(screen):
    # Initialize game variables as the player, enemies and such.
    fps_cap = 30
    options = ['continue', 'save', 'quit']
    clock = pygame.time.Clock()
    # Game loop.
    while True:
        # Time management.
        clock.tick(fps_cap)
        # Handle events.
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_a:    # Go to game if you press A.
                    return SCENE_GAME
                elif event.key == pygame.K_b:  # Go to shop if you press B.
                    return SCENE_SETTINGS
        # Update the menu (like buttons, settings, ...).
        print('Updating buttons:', *options)
        # Draw the shop.
        screen.fill((0, 0, 255))  # A green menu.
        pygame.display.update()

def game(screen):
    # Initialize game variables as the player, enemies and such.
    fps_cap = 60
    player  = 'Ted'
    clock   = pygame.time.Clock()
    # Game loop.
    while True:
        # Time management.
        clock.tick(fps_cap)
        # Handle events.
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_a:    # Go to menu if you press A.
                    return SCENE_MENU
                elif event.key == pygame.K_b:  # Go to shop if you press B.
                    return SCENE_SETTINGS
        # Update the game.
        print(f'Player {player} is playing!')
        # Draw your game.
        screen.fill((0, 255, 0))  # A blue game.
        pygame.display.update()

def main():
    screen = pygame.display.set_mode((800, 600))
    scene = SCENE_MENU
    while True:
        if scene == SCENE_MENU:
            scene = menu(screen)
        elif scene == SCENE_GAME:
            scene = game(screen)
main()
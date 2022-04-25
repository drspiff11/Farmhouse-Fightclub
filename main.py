# imports
import pygame
import random
from enum import Enum, auto
import constants as const
from character import Character
from obstacles import Obstacle

pygame.init()


# enumerated types representing different states the game/main function can be in
class GameState(Enum):
    main_menu = auto()
    character_select = auto()
    help_menu = auto()
    gameplay = auto()
    end_screen = auto()


# set colors
color_white = (255, 255, 255)
color_green = (0, 255, 0)
color_blue = (0, 128, 255)
color_yellow = (255, 255, 0)
color_orange = (255, 204, 102)
color_black = (0, 0, 0)
# initialize pygame assets
intro = pygame.image.load('images/farmhouse.png')
bg_img = pygame.image.load('images/farm_basic_background.png')
chicken_spritesheet_image = pygame.image.load('images/chicken.png')
health_hearts = pygame.image.load('images/heart.png')
click = pygame.mouse.get_pressed()
bg_img = pygame.transform.scale(bg_img, (const.DISPLAY_W, const.DISPLAY_H))
health_hearts = pygame.transform.scale(health_hearts, (100, 100))
intro = pygame.transform.scale(intro, (1280, 800))
font = pygame.font.Font("AlfaSlabOne-Regular.ttf", 32)
# info for the character selection screen
char_select = [font.render('Choose your fighter!', True, color_white, color_blue),
               font.render('Select either the chicken or the cow with your mouse', True, color_white, color_blue),
               font.render('this is you', True, color_white, color_blue)]
# info for the help menu screen
help_menu = [font.render('Rules of the Game:', True, color_white, color_blue),
             font.render('Punch or kick your opponent to diminish their health!', True, color_white,
                         color_blue),
             font.render('W key to punch', True, color_white, color_blue),
             font.render('D key to kick', True, color_white, color_blue),
             font.render('U arrow key to jump', True, color_white, color_blue),
             font.render('L arrow key to run left', True, color_white, color_blue),
             font.render('R arrow key to run right', True, color_white, color_blue),
             font.render('press [space] to continue', True, color_white, color_blue)]

# text for the displaying of the health bars
cpu_health = font.render("cpu health", True, color_black)
player_health = font.render("your health", True, color_black)


# render function handles drawing based on which game state is currently active
def render(current_game_state, canvas, player_fighter, cpu_fighter, current_char_state, current_cpu_state, obstacles):

    # intro screen
    if current_game_state == GameState.main_menu:
        canvas.blit(intro, (0, 0))

    # the character selection screen
    elif current_game_state == GameState.character_select:
        canvas.fill(color_blue)
        canvas.blit(char_select[0], (440, 50))
        canvas.blit(char_select[1], (130, 100))
        canvas.blit(char_select[2], (860, 550))

        canvas.blit(player_fighter.current, (900, 500))
        canvas.blit(cpu_fighter.current, (300, 500))

        canvas.blit(help_menu[7], (750, 750))

    # the rules and controls screen
    elif current_game_state == GameState.help_menu:
        canvas.fill(color_blue)
        canvas.blit(help_menu[0], (450, 50))
        canvas.blit(help_menu[1], (120, 100))
        canvas.blit(help_menu[2], (120, 200))
        canvas.blit(help_menu[3], (120, 250))
        canvas.blit(help_menu[4], (120, 350))
        canvas.blit(help_menu[5], (120, 400))
        canvas.blit(help_menu[6], (120, 450))
        canvas.blit(help_menu[7], (750, 750))

    # the screen where the game is played
    elif current_game_state == GameState.gameplay:
        canvas.blit(bg_img, (0, 0))
        canvas.blit(cpu_health, (40, 0))
        canvas.blit(player_health, (40, 100))

        # checks both players are still alive and blits their health bars
        if cpu_fighter.health > 0:
            for h in range(0, cpu_fighter.health, 4):
                canvas.blit(health_hearts, (0 + (h * 10), 20))
        if player_fighter.health > 0:
            for h in range(0, player_fighter.health, 4):
                canvas.blit(health_hearts, (0 + (h * 10), 120))

        # handles all movements in the game based on user input via the keyboard, by using the dictionaries of the
        # characters
        if current_char_state["moving_left"]:
            canvas.blit(player_fighter.current, (player_fighter.x, player_fighter.y))
            player_fighter.moveAnimal("left", cpu_fighter.x, cpu_fighter.y, False)
            canvas.blit(cpu_fighter.current, (cpu_fighter.x, cpu_fighter.y))
        elif current_char_state["moving_right"]:
            canvas.blit(player_fighter.current, (player_fighter.x, player_fighter.y))
            player_fighter.moveAnimal("right", cpu_fighter.x, cpu_fighter.y, False)
            canvas.blit(cpu_fighter.current, (cpu_fighter.x, cpu_fighter.y))
        elif current_char_state["jumping"]:
            canvas.blit(player_fighter.current, (player_fighter.x, player_fighter.y))
            player_fighter.jumpAnimal()
            canvas.blit(cpu_fighter.current, (cpu_fighter.x, cpu_fighter.y))
        elif current_char_state["punching"]:
            canvas.blit(player_fighter.current, (player_fighter.x, player_fighter.y))
            player_fighter.punchAnimal()
            canvas.blit(cpu_fighter.current, (cpu_fighter.x, cpu_fighter.y))
        elif current_char_state["kicking"]:
            canvas.blit(player_fighter.current, (player_fighter.x, player_fighter.y))
            player_fighter.kickAnimal()
            canvas.blit(cpu_fighter.current, (cpu_fighter.x, cpu_fighter.y))
        else:
            if player_fighter.facing == "left":
                player_fighter.current = player_fighter.stand_left
            else:
                player_fighter.current = player_fighter.stand_right
            canvas.blit(cpu_fighter.current, (cpu_fighter.x, cpu_fighter.y))
            canvas.blit(player_fighter.current, (player_fighter.x, player_fighter.y))
        if current_cpu_state["moving_left"]:
            canvas.blit(cpu_fighter.current, (cpu_fighter.x, cpu_fighter.y))
            cpu_fighter.moveAnimal("left", cpu_fighter.x, cpu_fighter.y, False)
            canvas.blit(cpu_fighter.current, (cpu_fighter.x, cpu_fighter.y))
        elif current_cpu_state["moving_right"]:
            canvas.blit(cpu_fighter.current, (cpu_fighter.x, cpu_fighter.y))
            cpu_fighter.moveAnimal("right", cpu_fighter.x, cpu_fighter.y, False)
            canvas.blit(cpu_fighter.current, (cpu_fighter.x, cpu_fighter.y))
        elif current_cpu_state["jumping"]:
            canvas.blit(cpu_fighter.current, (cpu_fighter.x, cpu_fighter.y))
            cpu_fighter.jumpAnimal()
            canvas.blit(cpu_fighter.current, (cpu_fighter.x, cpu_fighter.y))
        elif current_cpu_state["punching"]:
            canvas.blit(cpu_fighter.current, (cpu_fighter.x, cpu_fighter.y))
            cpu_fighter.punchAnimal()
            canvas.blit(cpu_fighter.current, (cpu_fighter.x, cpu_fighter.y))
        elif current_cpu_state["kicking"]:
            canvas.blit(cpu_fighter.current, (cpu_fighter.x, cpu_fighter.y))
            cpu_fighter.kickAnimal()
            canvas.blit(cpu_fighter.current, (cpu_fighter.x, cpu_fighter.y))
        else:
            if cpu_fighter.facing == "left":
                cpu_fighter.current = cpu_fighter.stand_left
            else:
                cpu_fighter.current = cpu_fighter.stand_right
            canvas.blit(cpu_fighter.current, (cpu_fighter.x, cpu_fighter.y))
            canvas.blit(player_fighter.current, (player_fighter.x, player_fighter.y))

    # end screen display
    elif current_game_state == GameState.end_screen:
        font = pygame.font.Font("AlfaSlabOne-Regular.ttf", 200)
        won = font.render('You WIN', True, color_white)
        lost = font.render('You Lose...', True, color_white)
        if cpu_fighter.health > 0:
            for h in range(0, cpu_fighter.health, 4):
                canvas.blit(health_hearts, (0 + (h * 10), 20))
        if player_fighter.health > 0:
            for h in range(0, player_fighter.health, 4):
                canvas.blit(health_hearts, (0 + (h * 10), 120))

        if player_fighter.health <= 0:
            canvas.blit(lost, (40, 210))
        elif cpu_fighter.health <= 0:
            canvas.blit(won, (115, 210))


# the main function which houses the game loop
def main():
    # fps game clock
    clock = pygame.time.Clock()
    # fps locked at 45
    FPS = 45

    # initialize the canvas and windows, as well as the game loop boolean
    canvas = pygame.Surface((const.DISPLAY_W, const.DISPLAY_H))
    window = pygame.display.set_mode((const.DISPLAY_W, const.DISPLAY_H))
    running = True
    current_game_state = GameState.main_menu

    # initialize the obstacle
    obstacles = [Obstacle("left", 100, 600)]

    # sets player to the chicken
    player_fighter = Character("SpriteSheet('images/chicken.png')", "left", 120 * const.SCALE,
                               const.GROUND)

    # sets the cpu to the cow
    cpu_fighter = Character("SpriteSheet('images/cow.png')", "right", 20 * const.SCALE,
                            const.GROUND)

    # The flip method updates the entire screen with every change since it was last called
    pygame.display.flip()

    # dictionaries to map the current state of the sprite to a bool (whichever entry is True is the curr state)
    current_char_state = {"moving_left": False,
                          "moving_right": False,
                          "jumping": False,
                          "punching": False,
                          "kicking": False}

    # and analogously for the cpu
    current_cpu_state = {"moving_left": False,
                         "moving_right": False,
                         "jumping": False,
                         "punching": False,
                         "kicking": False}

    # bool that tracks whether the CPU is running from you or chasing you
    run = False

    # bool that tracks whether you are the Chicken Sprite
    chicken = True

    # game loop
    while running:
        # initialize gravity for each character
        player_fighter.gravity(obstacles)
        cpu_fighter.gravity(obstacles)

        for event in pygame.event.get():
            # exit/quit
            if event.type == pygame.QUIT:
                running = False

            # listen for space bar to transition between game states
            if event.type == pygame.KEYDOWN and current_game_state != GameState.gameplay:
                if event.key == pygame.K_SPACE and current_game_state == GameState.main_menu:
                    current_game_state = GameState.character_select
                elif event.key == pygame.K_SPACE and current_game_state == GameState.character_select:
                    current_game_state = GameState.help_menu
                elif event.key == pygame.K_SPACE and current_game_state == GameState.help_menu:
                    current_game_state = GameState.gameplay
                    # initialize player to starting position
                    player_fighter.facing = "left"
                    player_fighter.x = 120 * const.SCALE
                    player_fighter.y = const.GROUND

                    # initialize CPU to starting position
                    cpu_fighter.facing = "right"
                    cpu_fighter.x = 20 * const.SCALE
                    cpu_fighter.y = const.GROUND

            # CHARACTER SELECT SCREEN
            if current_game_state == GameState.character_select:

                if event.type == pygame.MOUSEBUTTONUP:
                    if chicken:
                        cow_rect = pygame.Rect(150, 350, 300, 300)
                        chicken_rect = pygame.Rect(750, 350, 300, 300)

                    else:
                        cow_rect = pygame.Rect(750, 350, 300, 300)
                        chicken_rect = pygame.Rect(150, 350, 300, 300)
                    if chicken_rect.collidepoint(pygame.mouse.get_pos()):
                        # player = "chicken"
                        chicken = True
                        player_fighter = Character("SpriteSheet('images/chicken.png')", "left", 120 * const.SCALE,
                                                   const.DISPLAY_H - (15 * const.SCALE))
                        cpu_fighter = Character("SpriteSheet('images/cow.png')", "right", 20 * const.SCALE,
                                                const.DISPLAY_H - (15 * const.SCALE))

                        pygame.draw.rect(canvas, color_yellow, chicken_rect)
                        pygame.draw.rect(canvas, color_blue, cow_rect)
                    elif cow_rect.collidepoint(pygame.mouse.get_pos()):
                        chicken = False
                        # player = "cow"
                        player_fighter = Character("SpriteSheet('images/cow.png')", "right", 20 * const.SCALE,
                                                   const.DISPLAY_H - (15 * const.SCALE))
                        cpu_fighter = Character("SpriteSheet('images/chicken.png')", "left", 120 * const.SCALE,
                                                const.DISPLAY_H - (15 * const.SCALE))

                        pygame.draw.rect(canvas, color_yellow, cow_rect)
                        pygame.draw.rect(canvas, color_blue, chicken_rect)

            # character movement for when a key is pressed
            if event.type == pygame.KEYDOWN and (
                    current_game_state == GameState.gameplay or current_game_state == GameState.help_menu):
                if event.key == pygame.K_LEFT:
                    current_char_state["moving_left"] = True
                    run = True
                if event.key == pygame.K_RIGHT:
                    current_char_state["moving_right"] = True
                    run = False
                if event.key == pygame.K_UP:
                    current_char_state["jumping"] = True
                if event.key == pygame.K_w:
                    current_char_state["punching"] = True
                if event.key == pygame.K_d:
                    current_char_state["kicking"] = True

            # character movement for when a key is released
            if event.type == pygame.KEYUP:
                # if you stop moving allows CPU to run towards you
                run = False
                if event.key == pygame.K_LEFT:
                    current_char_state["moving_left"] = False
                if event.key == pygame.K_RIGHT:
                    current_char_state["moving_right"] = False
                if event.key == pygame.K_UP:
                    current_char_state["jumping"] = False
                if event.key == pygame.K_w:
                    current_char_state["punching"] = False
                if event.key == pygame.K_d:
                    current_char_state["kicking"] = False

            # look in dictionary and check the states through, call the appropriate action accordingly
            if current_char_state["moving_right"]:
                player_fighter.moveAnimal("right", cpu_fighter.x, cpu_fighter.y, False)
            if current_char_state["moving_left"]:
                player_fighter.moveAnimal("left", cpu_fighter.x, cpu_fighter.y, False)
            if current_char_state["jumping"]:
                player_fighter.jumpAnimal()
            # allows character to punch
            if current_char_state["punching"]:
                if player_fighter.facing == "left" and (cpu_fighter.x - 40 <= player_fighter.x <= cpu_fighter.x + 40):
                    cpu_fighter.gotPunched("right")
                elif player_fighter.facing == "right" and (
                        cpu_fighter.x - 40 <= player_fighter.x <= cpu_fighter.x + 40):
                    cpu_fighter.gotPunched("left")
            # allows character to punch
            if current_char_state["kicking"]:
                if player_fighter.facing == "left" and (cpu_fighter.x - 40 <= player_fighter.x <= cpu_fighter.x + 40):
                    cpu_fighter.gotKicked("right")
                elif player_fighter.facing == "right" and (
                        cpu_fighter.x - 40 <= player_fighter.x <= cpu_fighter.x + 40):
                    cpu_fighter.gotKicked("left")

        # show the user and cpu sprites and call the render function
        canvas.blit(player_fighter.current, (player_fighter.x, player_fighter.y))
        canvas.blit(cpu_fighter.current, (cpu_fighter.x, cpu_fighter.y))
        render(current_game_state, canvas, player_fighter, cpu_fighter, current_char_state, current_cpu_state,
               obstacles)

        # game play screen
        if current_game_state == GameState.gameplay:
            # draw the obstacles
            for o in obstacles:
                o_rect = pygame.Rect(o.x, o.y, 300, 50)
                pygame.draw.rect(canvas, color_yellow, o_rect)
            # cpu logic: movement and attacks
            if cpu_fighter.y == const.GROUND and player_fighter.y == const.GROUND:
                if cpu_fighter.x - 50 < player_fighter.x < cpu_fighter.x + 50 and not run:
                    choice = random.randint(1, 2)
                    if choice == 1:
                        cpu_fighter.kickAnimal()
                        if cpu_fighter.facing == "left" and (
                                player_fighter.x - 40 <= cpu_fighter.x <= player_fighter.x + 40) and (
                                player_fighter.y == const.GROUND):
                            player_fighter.gotKicked("right")
                        elif cpu_fighter.facing == "right" and (
                                player_fighter.x - 40 <= cpu_fighter.x <= player_fighter.x + 40) and (
                                player_fighter.y == const.GROUND):
                            player_fighter.gotKicked("left")
                    else:
                        cpu_fighter.punchAnimal()
                        if cpu_fighter.facing == "left" and (
                                player_fighter.x - 40 <= cpu_fighter.x <= player_fighter.x + 40):
                            player_fighter.gotPunched("right")
                        elif cpu_fighter.facing == "right" and (
                                player_fighter.x - 40 <= cpu_fighter.x <= player_fighter.x + 40):
                            player_fighter.gotPunched("left")
                # if player is too close, forget all and attack
                elif cpu_fighter.x - 50 < player_fighter.x < cpu_fighter.x + 50 and run:
                    run = False
            # makes it so if you are going towards cpu it shall flee
            if run:
                if player_fighter.x > cpu_fighter.x + 5:
                    cpu_fighter.moveAnimal("left", player_fighter.x, player_fighter.y, True)
                elif player_fighter.x < cpu_fighter.x - 5:
                    cpu_fighter.moveAnimal("right", player_fighter.x, player_fighter.y, True)
                else:
                    choice = random.randint(1, 200)
                    if choice == 1:
                        cpu_fighter.jumpAnimal(obstacles)
            else:
                if player_fighter.x > cpu_fighter.x + 5:
                    cpu_fighter.moveAnimal("right", player_fighter.x, player_fighter.y, True)
                elif player_fighter.x < cpu_fighter.x - 5:
                    cpu_fighter.moveAnimal("left", player_fighter.x, player_fighter.y, True)

        # have the obstacles move back and forth
        for o in obstacles:
            o.move()

        # transition to end screen if either player loses all health
        if cpu_fighter.health <= -1 or player_fighter.health <= -1:
            current_game_state = GameState.end_screen

        window.blit(canvas, (0, 0))
        pygame.display.update()
        clock.tick(FPS)


if __name__ == '__main__':
    main()  # Actually run the game.

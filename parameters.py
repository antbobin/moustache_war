"""
Paramètres constants 
"""

import pygame

##############
# PARAMETRES #
##############

# Fenêtre 
SCREEN_WIDTH = 1920
SCREEN_HEIGHT = 1020

# Paramètres du jeu
GAME_NAME = "Soubaston"
GAME_FRAME_RATE = 60

# Fighter
FIGHTER_HEIGHT = 300
FIGHTER_WIDTH = 150
FIGHTER_SPEED = 10
FIGHTER_JUMP_SPEED = -30
FIGHTER_ATTACK_DURATION = 1000 # ms
FIGHTER_ATTACK_RANGE = 50
FIGHTER_HEALTH = 100
FIGHTER_ATTACK_DAMAGE = 10
FIGHTER_THROW_DAMAGE = 5
FIGHTER_THROW_DURATION = 2500 # ms
FIGHTER_THROW_SPEED = 25.
FIGHTER_THROW_RANGE = SCREEN_WIDTH / 3

# Pierre
ROCK_RADIUS = 10
ROCK_HEAL = 50

# Impact
IMPACT_SIZE = 50
IMPACT_DURATION = 500 #ms

# Scène
FLOOR_HEIGHT = 820
GRAVITY = 1.5

# Barre de vie
HEALTHBAR_WIDTH = 500
HEALTHBAR_HEIGHT = 30
HEALTHBAR_MARGIN = 100
HEALTHBAR_BORDER = 3

# Musique
MUSIC_VOLUME = 0.3
EFFECTS_VOLUME = 1.

# Scores
SCORE_FONTSIZE = 40

# touches en l'absence de controller
LEFT_FIGHTER_KEYS = {
    "left": pygame.K_q,
    "right" : pygame.K_d,
    "jump" : pygame.K_z,
    "attack" : pygame.K_SPACE,
    "throw" : pygame.K_f
}
RIGHT_FIGHTER_KEYS = {
    "left": pygame.K_LEFT,
    "right" : pygame.K_RIGHT,
    "jump" : pygame.K_UP,
    "attack" : pygame.K_RCTRL,
    "throw" : pygame.K_RSHIFT
}

##############
# CONSTANTES #
##############

class ORIENTATION:
    RIGHT = 0
    LEFT = 1

class ATTACK_STATUS:
    ATTACKING = 0
    COOLDOWN = 1
    READY = 2

class COLOR:
    YELLOW = (255, 255, 0)
    RED = (255, 0, 0)
    BROWN = (153, 76, 0)
    WHITE = (255, 255, 255)
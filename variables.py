#!/usr/bin/env python3
import os
import sys
import time
import pygame
import pickle
from music import *


pygame.init()
# import colors

executing_wd = os.path.dirname(os.path.realpath(sys.argv[0]))
current_wd = os.path.join(executing_wd, "assets")
highscore_wd = os.path.join(current_wd, ".Highscore")
images_wd = os.path.join(current_wd, "images")
font_wd = os.path.join(current_wd, "fonts")
ExtraImages_wd = os.path.join(current_wd, "Extra_img")
backgroundImages_wd = os.path.join(images_wd, "bac")

infoObject = pygame.display.Info()
# screenWidth, screenHeight = 1600, 900
# screenWidth, screenHeight = 400, 300
screenWidth, screenHeight = infoObject.current_w, \
    infoObject.current_h

game_display_name = "RETROVE"
# screen = pygame.display.set_mode([screenWidth,
#                                   screenHeight], pygame.FULLSCREEN)
screen = pygame.display.set_mode([screenWidth, screenHeight])
print("Screen Resolution:", screenWidth, screenHeight)
pygame.display.set_caption(game_display_name)

#  highscore = {45800: 'asdf', 79200: 'Deanna!', 102600: 'Brandon',
#   22100: 'dadmanofwhitepowers', 23100: 'somaiya', 18900: '',
#   20900: '', 27900: '', 74400: 'austin', 26600: ''}

highscoreFilename = os.path.join(highscore_wd, 'highscores.pickle')
backup_highscoreFilename = os.path.join(highscore_wd, 'bak_highscores.pickle')

try:
    highscore = pickle.load(open(highscoreFilename, "rb"))
except Exception as e:
    print(e)
    highscore = pickle.load(open(backup_highscoreFilename, "rb"))
    pickle.dump(highscore, open(highscoreFilename, "wb"),
                protocol=pickle.HIGHEST_PROTOCOL)


highscoreOrgList = highscore
highscoreLinesNum = len(highscoreOrgList.keys())
sortedHighkeyList = sorted(highscoreOrgList.keys(), reverse=True)
sorted_highValue_list = [highscoreOrgList[key]
                         for key in sortedHighkeyList]

highscore = max(sortedHighkeyList)
highscore_name = sorted_highValue_list[sortedHighkeyList.index(
    highscore)]

"""
COLORS                                                          #COLORS
"""
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (178, 34, 34)
DARK_RED = (139, 58, 58)
REALLYRED = (220, 20, 60)
BLUE = (25, 25, 112)
DARK_BLUE = (16, 78, 139)
M_BLUE = (0, 191, 255)
DEEP_ORANGE = (255, 69, 0)
AMBER = (255, 97, 3)
INDIGO = (75, 0, 130)
PURPLE = (128, 0, 128)

Intro_title_color = AMBER
Intro_title_credit_color = RED
Highscore_btn_color = INDIGO
Start_btn_color = (0, 201, 87)
Quit_btn_color = DEEP_ORANGE
High_socre_background = (34, 79, 188)
BK_color = M_BLUE
# BK_color_shade = (0, 238, 238)
Back_btn_color = (100, 149, 237)
highscore_text_color = (255, 255, 255)
Btn_highlight_color = (255, 185, 15)

block_color_list = [BLACK, AMBER, DEEP_ORANGE, INDIGO]
block_color = (220, 20, 60)

start, FirstStart = time.time(), time.time()
elasped = 0
speed = constant_speed = 2.5
increasingSpeed = 0.02
# increasingSpeed = 0.05
globalxVel = globalyVel = 7
bullet_speed = screenHeight / 35
player_up_from_bottom = 150
starting_lives = 3
sartMachineGun, machineGunNum = False, False
index, r_index = 0, 0
done = False
powerupDuration = 120
Score_takeaway_for_powerup = 100
POWERUP_SCORE = 1000
player_width, player_height = 35, 46
# highscore = 0
playerx = screenWidth / 2
playery = screenHeight - player_height - \
    player_up_from_bottom
block_width, block_height = 35, 25


allSpritesList = pygame.sprite.Group()
block_list = pygame.sprite.Group()
powerupList = pygame.sprite.Group()
powerupList2 = pygame.sprite.Group()
bulletList = pygame.sprite.Group()
player_list = pygame.sprite.Group()

# pygame.transform.scale2x(pygame.image.load(filepath).convert_alpha())

#LOCATION OF THE FONT
font_location = os.path.join(font_wd, "Chunkfive.otf")

# FILEPATH FOR THE IMAGES
# Blocks -- >
powerup_image_des = pygame.transform.scale2x(pygame.image.load(
    os.path.join(images_wd, "health_powerup.png")).convert_alpha())
powerup2_image_des = pygame.transform.scale2x(
    pygame.image.load(os.path.join(images_wd, "bullet_powerup.png")).convert_alpha())

# Assets -- >
crown_image_des = pygame.transform.scale2x(
    pygame.image.load(os.path.join(images_wd, "crown.png")).convert_alpha())
player_image_des = pygame.transform.scale2x(
    pygame.image.load(os.path.join(images_wd, "player_png.png")).convert_alpha())
bullet_image_des = pygame.transform.scale2x(
    pygame.image.load(os.path.join(images_wd, "bullet3.png")).convert_alpha())
test_sub = pygame.transform.scale2x(pygame.image.load(
    os.path.join(images_wd, "broken_health_powerup.png")).convert_alpha())

# Sprites -- >
player_sprite_image_des = pygame.image.load(
    os.path.join(ExtraImages_wd, "fatbot.png")).convert_alpha()
llama_image_des = pygame.image.load(
    os.path.join(images_wd, "llama.png")).convert_alpha()

# backgorunds image to blit -- >
background_image_list = [
    os.path.join(backgroundImages_wd, "memphis-colorful.png"),
    os.path.join(backgroundImages_wd, "naturalblack.png"),
    os.path.join(backgroundImages_wd, "dark-triangles.png"),
    os.path.join(backgroundImages_wd, "gaming-pattern.png"),
    os.path.join(backgroundImages_wd, "new_year_background.png")
]
background_image = [pygame.image.load(filepath)
                    for filepath in background_image_list]

later_name = ''

num_block = int(screenWidth / 20)
numPowerup = numPowerup2 = 4
# bulletoffset = 7
IntroTitleOffset = 200
done = False
clock = pygame.time.Clock()
score, xVel, yVel = 0, 0, 0
random_name_gen = "ALPHALT"

# if __name__ == '__main__':
#     gameloop()

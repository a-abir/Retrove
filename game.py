#!/usr/bin/env python3
"""
RETROVE
Made by Mohammad Islam
"""

import pygame
from pygame.locals import *
import random
import time
import os
import pickle
import sys
from variables import *
from spritesheet import spritesheet

# Intitializes pygame and pygame font
pygame.init()
pygame.font.init()

"""
accepts the parameter of "mute" after 
the command to mute all sounds
"""
try:
    if sys.argv[1] == "mute":
        set_all_sounds(0)
    else:
        playMusic()
except:
    pass


# checks if joystick is accessable and sets it up
joystick_working = True
try:
    pygame.joystick.init()
    joysticks = [pygame.joystick.Joystick(x)
                 for x in range(
                     pygame.joystick.get_count())]
    jstick = joysticks[0]
    jstick.init()
except Exception as E:
    joystick_working = False
    print(E, "joysticks not found")

# Block Class


class Block(pygame.sprite.Sprite):
    def __init__(self, color, triangular_mode, image=None):
        """
        Creates blocks using the color or the provided image

        The triangular mode accepts x value (int) and sets 
        the blocks location to populate the given value more
            --It can be set to follow the players x location
        """
        super().__init__()
        self.color = color
        if image == None:
            self.image = pygame.Surface(
                [block_width, block_height])
            self.image.fill(self.color)
        else:
            self.image = image

        self.rect = self.image.get_rect()
        self.rect.x = random.triangular(0, screenWidth, triangular_mode)
        self.rect.y = -random.randrange(screenHeight)

    def update(self):
        if self.rect.y < 50 and self.rect.y >\
                -10 or self.rect.y > screenHeight-100:
            self.rect.y += speed * 3
        else:
            self.rect.y += speed

    @staticmethod
    # Creates all the blocks for the game
    def createBlocks(create_powerup=None):
        global block, powerup
        if create_powerup == None:
            block = Block(random.choice(block_color_list), player.rect.x)
            block_list.add(block)
            allSpritesList.add(block)
        elif create_powerup == "powerup":
            powerup = Block(REALLYRED, screenWidth/2, powerup_image_des)
            powerupList.add(powerup)
            allSpritesList.add(powerup)
        elif create_powerup == "powerup2":
            powerup2 = Block(BLACK, screenWidth/2,  powerup2_image_des)
            powerupList2.add(powerup2)
            allSpritesList.add(powerup2)


# Background Image class
class BackgroundImage:
    def __init__(self, image):
        """
        Creates repeating image as the background

        Accepts the loaded image as the parameter and repeats the image
        to fill the whole background
        """
        self.image = image
        self.rect = self.image.get_rect()

    def draw(self):
        list(map(lambda y:
                 list(map(lambda x:
                          screen.blit(self.image, (x, y)),
                          range(0, screenWidth, self.rect.width))),
                 range(0, screenHeight, self.rect.height)))


# Player Class
class Player(pygame.sprite.Sprite):
    def __init__(self, image=None):
        """
        Creates the player object

        Accepts the parameter of an image for the player, 
        if not provided a square is used insted
        """
        super().__init__()
        if image != None:
            self.image = image
        else:
            self.image = pygame.Surface(
                [player_width, player_height],
                pygame.SRCALPHA, 32).convert_alpha()

        self.rect = self.image.get_rect()
        self.rect.y = screenHeight - self.rect.height - \
            player_up_from_bottom
        self.rect.x = screenWidth / 2


# Bullet class
class Bullet(pygame.sprite.Sprite):
    def __init__(self, image):
        super().__init__()

        # self.image = pygame.Surface([4, 10])
        self.image = image
        # self.image.fill(BLACK)

        self.rect = self.image.get_rect()
        self.rect.center = player.rect.center
        self.rect.y -= player.rect.height

    def update(self):
        self.rect.y -= bullet_speed * 1.5

    def left_diagonal(self):
        self.rect.y -= bullet_speed
        self.rect.x -= bullet_speed

    def right_diagonal(self):
        self.rect.y -= bullet_speed
        self.rect.x += bullet_speed

    @classmethod
    def fireBullet(cls):
        bullet = cls(bullet_image_des)
        # pos = pygame.mouse.get_pos()
        allSpritesList.add(bullet)
        bulletList.add(bullet)

    @classmethod
    def fireBullet_diagonal(cls, side):
        bullet = cls(bullet_image_des)
        if side.lower() == 'l':
            bullet.left_diagonal()
        elif side.lower() == 'r':
            bullet.right_diagonal()
        allSpritesList.add(bullet)
        bulletList.add(bullet)

    @classmethod
    def machine_gun(cls):
        Bullet.fireBullet()
        cls.fireBullet_diagonal("l")
        cls.fireBullet_diagonal("r")


class WriteToScreen():
    def __init__(self, msg, color, font_size):
        self.msg = msg
        self.color = color
        self.font_size = font_size
        self.myfont = pygame.font.Font(
            font_location, self.font_size, bold=True)
        self.font_render = self.myfont.render(self.msg, 1, self.color)
        self.rect = self.font_render.get_rect()

    def Blit(self, position):
        screen.blit(self.font_render, position)

    @staticmethod
    def center(msg, color, font_size, center_of_rect):
        myfont = pygame.font.Font(font_location, font_size)
        font_render = myfont.render(msg, 1, color)
        font_rect = font_render.get_rect()
        font_rect.center = center_of_rect
        screen.blit(font_render, font_rect)


# player = Player()
player = Player()
player_list.add(player)
allSpritesList.add(player)
# print(player.rect.width, player.rect.height)

player_anim = spritesheet(player_sprite_image_des, 2, 1)
llama = spritesheet(llama_image_des, 6, 1)


list(map(lambda x: Block.createBlocks(), list(range(num_block))))
list(map(lambda x: Block.createBlocks("powerup"), list(range(numPowerup))))
list(map(lambda x: Block.createBlocks("powerup2"), list(range(numPowerup2))))


def index_change(FPS, reset_index):
    global index, r_index
    r_index += 1
    if r_index % FPS == 0:
        index += 1
        r_index = 0
    if index > (reset_index.cols*reset_index.rows):
        index = 0


class loopFunc():
    def retryPowerup2Loop(self, powerup2):
        powerupList2.remove(powerup2)
        allSpritesList.remove(powerup2)
        Block.createBlocks("powerup2")

    def retryBlockLoop(self, block):
        block_list.remove(block)
        allSpritesList.remove(block)
        Block.createBlocks()

    def retryPowerupLoop(self, powerup):
        powerupList.remove(powerup)
        allSpritesList.remove(powerup)
        Block.createBlocks("powerup")


forLoop = loopFunc()


def retry_the_game():
    lives = starting_lives
    done = False
    sartMachineGun = False
    machineGunNum = False
    time_counter_powerup = 0

    list(map(lambda x: forLoop.retryBlockLoop(x), block_list))
    list(map(lambda x: forLoop.retryPowerupLoop(x), powerupList))
    list(map(lambda x: forLoop.retryPowerup2Loop(x), powerupList2))

    gameloop()


def highscorePageDisplay():
    global highscore_page, name, sortedHighkeyList, \
        sorted_highValue_list
    highscore_page = True

    while highscore_page:
        # pygame.mouse.set_visible(True)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

            elif event.type == KEYDOWN:
                if event.key == K_KP_ENTER or event.key == K_SPACE:
                    highscore_page = False
                    intro(later_name)
                if event.key == K_ESCAPE:
                    highscore_page = False
                    intro(later_name)
            if joystick_working:
                if jstick.get_axis(0) < -0.1:
                    highscore_page = False
                    exname = later_name

        start_of_high_dis_list = screenHeight / 10
        high_size_list = 30
        screen.fill(High_socre_background)
        # pygame.mouse.set_visible(False)
        # cursor_display()

        for i in range(len(sortedHighkeyList) - 1):

            start_of_high_dis_list += (high_size_list + 30)
            try:
                length_of_dash = 25 - \
                    len(str(sortedHighkeyList[i])) - \
                    len(str(sorted_highValue_list[i]))
            except:
                length_of_dash = 10
            sortedHighkeyList = sorted(
                highscoreOrgList.keys(), reverse=True)
            sorted_highValue_list = [highscoreOrgList[key]
                                     for key in sortedHighkeyList]
            WriteToScreen.center(
                sorted_highValue_list[i] + "_" * length_of_dash +
                str(sortedHighkeyList[i]), highscore_text_color,
                high_size_list, ((screenWidth / 2), start_of_high_dis_list))

        WriteToScreen.center(
            "Highscore: ", BLACK, 40, (screenWidth / 2, 50))
        button("BACK", 50, 50, 150, 50, BLUE, Back_btn_color, "BACK")

        pygame.display.update()


def button(msg, x, y, w, h, ic, ac, action=None):
    global highscore_page
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
    if x + w > mouse[0] > x and y + h > mouse[1] > y:
        pygame.draw.rect(screen, ic, (x, y, w, h))
        if click[0] == 1 and action != None:
            if action == "play":
                retry_the_game()
            elif action == "BACK":
                highscore_page = False
                intro(later_name)
            elif action == "quit":
                pygame.quit()
                quit()
            elif action == "more":
                highscore_page = True
                highscorePageDisplay()
            elif action == "vol_neg":
                set_all_sounds(0)
            elif action == "vol_pos":
                set_all_sounds(1)
    else:
        pygame.draw.rect(screen, ac, (x, y, w, h))
    if msg != "blank":
        WriteToScreen.center(msg, WHITE, 25,
                             ((x + (w / 2)), (y + (h / 2))))


def intro(exname=None):
    global name, highscore_name, highscore, \
        later_name, cur_pos

    intro_background = BackgroundImage(background_image[0])

    intro = True
    t_num = [0, 0, 0, 0]
    cur_pos = 0
    team_number = ""
    pos = pygame.mouse.get_pos()
    if exname != None:
        name = "" + exname
        later_name = ""
    else:
        name = ""

    replace_name = "ENTER NAME _"

    while intro:
        screen.fill(WHITE)
        intro_background.draw()
        pygame.mouse.set_visible(True)
        llama.draw(screen, index % llama.totalCellCount,
                   screenWidth / 2, screenHeight / 3, 4)
        index_change(.5, llama)

        if joystick_working:
            if jstick.get_button(0):
                retry_the_game()
            # if jstick.get_axis(0) < -0.1:
            # 	highscore_page = False
            # 	exname = later_name
            if jstick.get_button(2):
                # pygame.quit()
                # quit()
                pass
            if jstick.get_button(1):
                # highscore_paget_num = True
                highscorePageDisplay()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if joystick_working:
                if jstick.get_axis(0) > 0.1:
                    cur_pos = 0 if cur_pos > 3 else cur_pos
                    cur_pos += 1

                elif jstick.get_axis(0) < -0.1:
                    cur_pos = 0 if cur_pos > 3 else cur_pos
                    cur_pos -= 1

                elif jstick.get_axis(1) > 0.1:
                    cur_pos = 0 if cur_pos > 3 else cur_pos
                    t_num[cur_pos] += 1

                elif jstick.get_axis(1) < -0.1:
                    cur_pos = 0 if cur_pos > 3 else cur_pos
                    t_num[cur_pos] -= 1

                    team_number = str(abs(t_num[0])) + \
                        str(abs(t_num[1])) + \
                        str(abs(t_num[2])) + \
                        str(abs(t_num[3]))
                    name = team_number

            if event.type == KEYDOWN:
                if event.unicode.isalpha() or event.unicode.isnumeric():
                    replace_name = ""
                    name += event.unicode
                    later_name += event.unicode

                elif event.key == K_BACKSPACE:
                    name = name[:-1]
                    later_name = later_name[:-1]
                elif event.key == K_RETURN:
                    retry_the_game()

        # print(later_name)
        if score > highscore:
            highscore = score
            highscore_name = name
        dis_name = name if len(name) > 0 \
            else str(replace_name) + name

        WriteToScreen.center(
            dis_name, Intro_title_color, 100,
            ((screenWidth / 2), (screenHeight / 2)))
        WriteToScreen.center(
            "Soknorobo", Intro_title_credit_color, 20,
            ((screenWidth / 2), (screenHeight / 2) + 50))

        button("((>", (screenWidth - (screenWidth / 100) * 12),
               10, 70, 70, Btn_highlight_color,
               Quit_btn_color, "vol_neg")
        button("<))", (screenWidth - (screenWidth / 100) * 6),
               10, 70, 70, Btn_highlight_color,
               Quit_btn_color, "vol_pos")
        button("QUIT", (screenWidth / 100) * 19,
               650, 150, 70, Btn_highlight_color,
               Quit_btn_color, "quit")
        button("HIGHSCORE", (screenWidth / 100) * 44,
               650, 180, 70, Btn_highlight_color,
               Highscore_btn_color, "more")
        button("START", (screenWidth / 100) * 69,
               650, 150, 70, Btn_highlight_color,
               Start_btn_color, "play")

        Highscore_to_Display = WriteToScreen(
            "Highscore: " + str(highscore), BLACK, 40)
        Highscore_to_Display.Blit([10, 10])
        Score_to_Display = WriteToScreen(("Score: " +
                                          str(score)), BLACK, 20)
        Score_to_Display.Blit(([10, 50]))
        # pygame.draw.circle(screen, (0, 127, 255),
        #                    (screenWidth // 2,
        #                     screenHeight // 3), 80, 1)
        pygame.display.update()


def gameloop():
    global done, xVel, yVel, speed, score, \
        globalxVel, globalVel, elasped, start,\
        lives, elaspedTotalTime, BK_color, \
        FirstStart, highscore, powerup, \
        powerup2, machineGunNum, sartMachineGun, \
        timeCounterPowerup2, increasingSpeed
    done = False
    speed = constant_speed
    lives = starting_lives
    score = 0
    # pygame.mixer.music.stop()
    power_up.play()
    playMusic()
    timeCounterPowerup2 = 0
    # gameloop_background = BackgroundImage(
    #     background_image[4])
    FirstStart, start = time.time(), time.time()

    # try:
    #     if str(sys.argv[1].lower()) == "6517":
    #         score += 6517
    #     elif str(sys.argv[1].lower()) == "easy":
    #         increasingSpeed = 0.002
    #     elif str(sys.argv[1].lower()) == "normal":
    #         increasingSpeed = 0.003
    #     elif str(sys.argv[1].lower()) == "hard":
    #         increasingSpeed = 0.02
    #     # elif str(sys.argv[1]) == "mute":
    #     #     set_all_sounds(0)
    # except Exception as e:
    #     print(e)

    while not done:
        screen.fill(BK_color)
        # gameloop_background.draw()
        clock.tick(35)
        pygame.mouse.set_visible(False)

        player_anim.draw(screen, index %
                         player_anim.totalCellCount,
                         player.rect.center[0],
                         player.rect.center[1], 4)
        index_change(5, player_anim)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
                pygame.quit()
                quit()

            if joystick_working:
                if jstick.get_axis(0) < -0.1:
                    xVel = -globalxVel
                if jstick.get_axis(0) > 0.1:
                    xVel = globalxVel
                if jstick.get_axis(1) < -0.1:
                    yVel = -globalyVel
                if jstick.get_axis(1) > 0.1:
                    yVel = (globalyVel + speed)

                if jstick.get_axis(0) > -.1 and\
                        jstick.get_axis(0) < .1:
                    xVel = 0
                if jstick.get_axis(1) > -.1 and \
                        jstick.get_axis(1) < .1:
                    yVel = 0
                if jstick.get_button(0):
                    if not machineGunNum:
                        Bullet.fireBullet()
                        pygame.time.delay(10)
                        shoot.play()
                    elif machineGunNum:
                        shootM_gun.play()
                        Bullet.machine_gun()
                if jstick.get_button(1):
                    if not machineGunNum:
                        shoot.play()
                        Bullet.fireBullet()
                    elif machineGunNum:
                        shootM_gun.play()
                        Bullet.machine_gun()
                if jstick.get_button(2):
                    pygame.quit()
                    quit()

            if event.type == pygame.KEYDOWN:
                if event.key == K_ESCAPE:
                    done = True
                    xVel, yVel = 0, 0
                    player.rect.y = screenHeight - \
                        player.rect.height - \
                        player_up_from_bottom
                    player.rect.x = screenWidth / 2
                if event.key == K_SPACE:
                    if not machineGunNum:
                        shoot.play()
                        Bullet.fireBullet()
                    elif machineGunNum:
                        shootM_gun.play()
                        Bullet.machine_gun()
                    allSpritesList.draw(screen)

                if event.key == K_LEFT or event.key == K_a:
                    xVel = -globalxVel
                if event.key == K_RIGHT or event.key == K_d:
                    xVel = globalxVel
                if event.key == K_UP or event.key == K_w:
                    yVel = -globalyVel
                if event.key == K_DOWN or event.key == K_s:
                    yVel = (globalyVel + speed)
            if event.type == pygame.KEYUP:
                if event.key == K_LEFT or event.key == K_a or \
                        event.key == K_RIGHT or event.key == K_d:
                    xVel = 0
                elif event.key == K_UP or event.key == K_w or \
                        event.key == K_DOWN or event.key == K_s:
                    yVel = 0

        player.rect.x += xVel
        player.rect.y += yVel

        allSpritesList.draw(screen)
        allSpritesList.update()

        for block in block_list:
            playerHitList = pygame.sprite.spritecollide(
                player, block_list, True)

            for block in playerHitList:
                # done = True
                # playerHitList.remove(block)
                # Block.createBlocks()
                lives -= 1
                live_loss.play()
                numPowerup, numPowerup2, num_block = 5, 5, int(
                    screenWidth / 10)
                pygame.time.delay(100)

            if block.rect.bottom > screenHeight - 10 or \
                    block.rect.right > screenWidth or block.rect.right < 0:
                # block.remove(block)
                block_list.remove(block)
                allSpritesList.remove(block)
                Block.createBlocks()

            list(map(lambda x: Block.createBlocks(), playerHitList))

        for bullet in bulletList:

            blockHitList = pygame.sprite.spritecollide(
                bullet, block_list, True)

            for block in blockHitList:
                pygame.draw.circle(screen, (0, 127, 255),
                                   block.rect.center, 40, 5)
                bulletList.remove(bullet)
                allSpritesList.remove(bullet)
                Block.createBlocks()
                score += 100
                # font_render = myfont.render(str(score),1,WHITE)
                # print("score:" , score)

        # print(machineGunNum)
        for powerup in powerupList:
            playerHitList = pygame.sprite.spritecollide(
                player, powerupList, True)

            for powerup in playerHitList:
                pygame.draw.circle(screen, RED,
                                   player.rect.center, 40, 5)
                # done = True
                gainedPowerup.play()
                playerHitList.remove(powerup)
                lives += 1 if lives < 11 else 0
                Block.createBlocks("powerup")
                # sartMachineGun = True
                Powerup_start = round(time.time())
                pygame.time.delay(0)

            if powerup.rect.y > screenHeight - 10:
                powerupList.remove(powerup)
                allSpritesList.remove(powerup)
                Block.createBlocks("powerup")

                # font_render = myfont.render(str(score),1,WHITE)

        # print(machineGunNum)
        for powerup2 in powerupList2:
            playerHitList2 = pygame.sprite.spritecollide(
                player, powerupList2, True)

            for powerup2 in playerHitList2:

                # done = True
                gainedPowerup.play()
                playerHitList2.remove(powerup2)
                score += 100
                Block.createBlocks("powerup2")
                sartMachineGun = True
                # PowerupStart2 = round(time.time())

                pygame.time.delay(0)
                if lives <= 0:
                    shut_down.play()
                    xVel, yVel = 0, 0
                    player.rect.y = screenHeight - \
                        player.rect.height - player_up_from_bottom
                    player.rect.x = screenWidth / 2
                    done = True

            if powerup2.rect.y > screenHeight - 10:
                powerupList2.remove(powerup2)
                allSpritesList.remove(powerup2)
                Block.createBlocks("powerup2")

        for bullet in bulletList:
            powerupHitList = pygame.sprite.spritecollide(
                bullet, powerupList, True)

            if powerup in powerupHitList:
                screen.blit(test_sub, powerup.rect.center)
                bulletList.remove(bullet)
                allSpritesList.remove(bullet)
                Block.createBlocks("powerup")
                score = score - Score_takeaway_for_powerup \
                    if score > Score_takeaway_for_powerup else 0

            powerupHitList2 = pygame.sprite.spritecollide(
                bullet, powerupList2, True)

            if powerup2 in powerupHitList2:
                bulletList.remove(bullet)
                allSpritesList.remove(bullet)
                Block.createBlocks("powerup2")

            if bullet.rect.y < -10:
                bulletList.remove(bullet)
                allSpritesList.remove(bullet)

        if player.rect.x < 0 or player.rect.x > screenWidth - \
                player.rect.width or player.rect.y < 0 or \
                player.rect.y > screenHeight - player.rect.height:
            xVel, yVel = 0, 0
            player.rect.y = screenHeight - player.rect.height - \
                player_up_from_bottom
            player.rect.x = screenWidth / 2
            done = True

        elasped = round(time.time()) - round(start)
        if (elasped % 11) == 10:
            start = time.time()
            score += 1000

        if sartMachineGun == True:
            if timeCounterPowerup2 == powerupDuration:
                sartMachineGun = False
                machineGunNum = False
                timeCounterPowerup2 = 0
            else:
                timeCounterPowerup2 += 1
                machineGunNum = True

        # print(score, "{", timeCounterPowerup2,
        #       sartMachineGun, "}", "{", player.rect.x,
        #       player.rect.y, '} ', "{ speed:",
        #       round(speed, 4), '}')

        if lives <= 0:
            shut_down.play()
            num_block = 3
            xVel, yVel = 0, 0
            player.rect.y = screenHeight - player.rect.height - \
                player_up_from_bottom
            player.rect.x = screenWidth / 2
            done = True

        speed += increasingSpeed
        Score_to_Display = WriteToScreen(("Score: " +
                                          str(score)), BLACK, 50)
        Score_to_Display.Blit(([10, 10]))
        highscoreToDisplay = WriteToScreen(
            "Highscore: " + str(highscore), BLACK, 30)
        highscoreToDisplay.Blit([10, 60])
        elaspedTotalTime = round(time.time() - FirstStart, 5)
        elasped_to__display = WriteToScreen(
            "+" + str(elasped * 10) + "   " +
            str(elaspedTotalTime), BLACK, 30)
        elasped_to__display.Blit([screenWidth - 200, 40])
        lives_to_display = WriteToScreen("Lives:" +
                                         str(lives), BLACK, 30)
        lives_to_display.Blit([screenWidth - 150, 10])

        pygame.display.flip()
        # print("III")

    def rewrite():
        global name, highscoreLinesNum
        clean_name = name.strip("_")
        highscoreOrgList[score] = clean_name
        # print(min(sortedHighkeyList))
        if len(highscoreOrgList.keys()) > 10:
            print(len(highscoreOrgList.keys()))

            list(map(lambda x: highscoreOrgList.pop(
                min(highscoreOrgList.keys())),
                range(len(highscoreOrgList.keys()) - 10)))
        pickle.dump(highscoreOrgList,
                    open(highscoreFilename, "wb"),
                    protocol=pickle.HIGHEST_PROTOCOL)

    if score > highscore:
        highscore = score
        rewrite()

    if score > min(sortedHighkeyList):
        rewrite()

    print("FINAL SCORE:  \"", score, "\"  in",
          round(time.time() - FirstStart), "seconds")
    print("highscore: ", highscore)
    if int(score) < int(highscore):
        print("You're", int(highscore) - int(score),
              "points away from high score")
    else:
        print("Congrats your new Highscore is", score)


if __name__ == '__main__':
    intro()

import pygame
import random
from mankala_functions import *

pygame.init()
clock = pygame.time.Clock()

screen_width, screen_height = 900, 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("mankala box")
tickrate = 4


initiated = False
running = True
while running:

    if not initiated:
        conts = make_containers()
        fill_containers(conts, 4)
        moving = False
        hand = []
        drop_index = None
        player1_turn = True
        game_over = False
        initiated = True

    screen.fill((222, 184, 135))
    draw_containers(screen, conts)
    draw_beads(screen, conts)
    draw_numbers(screen, conts)
    if not game_over:
        draw_controls(screen, player1_turn)
    else:
        draw_results(screen, conts)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r and game_over:
                initiated = False
                break
            if not hand:
                pressed_num = None
                if event.key == pygame.K_1:
                    pressed_num = 1
                elif event.key == pygame.K_2:
                    pressed_num = 2
                elif event.key == pygame.K_3:
                    pressed_num = 3
                elif event.key == pygame.K_4:
                    pressed_num = 4
                elif event.key == pygame.K_5:
                    pressed_num = 5
                elif event.key == pygame.K_6:
                    pressed_num = 6
                if pressed_num is not None:
                    if not player1_turn:
                        pressed_num = 14 - pressed_num
                    hand = conts[pressed_num].content
                    conts[pressed_num].content = []
                    drop_index = pressed_num - 1
                    pressed_num = None

    if len(hand) > 0:
        # check if goal to skip
        if player1_turn:
            if drop_index == 7:
                drop_index = (drop_index - 1) % 14
        else:
            if drop_index == 0:
                drop_index = (drop_index - 1) % 14

        draw_drop_box(screen, conts[drop_index])

        drop_index = empty_hand(conts, drop_index, hand, player1_turn)

        if not hand:
            last_index = (drop_index + 1) % 14
            if last_index in [0, 7]:
                perfect_print(screen, player1_turn)
            else:
                if len(conts[last_index].content) == 1 and len(conts[14 - last_index].content) > 0:
                    if player1_turn and conts[last_index].belong == 1:
                        side_steal(screen, conts, last_index, player1_turn)
                    elif not player1_turn and conts[last_index].belong == 2:
                        side_steal(screen, conts, last_index, player1_turn)
                player1_turn = not player1_turn
            drop_index = None

            game_over = check_game_over(conts)
            if game_over:
                clean_board(conts)

    clock.tick(tickrate)

    pygame.display.update()

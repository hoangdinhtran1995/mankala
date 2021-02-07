import random
import pygame


class Container:
    def __init__(self, number, belong_to_player):
        self.number = number
        self.belong = belong_to_player
        self.content = []
        self.width = 100
        self.height = 200
        if self.number < 7:
            self.y = 50
            if self.number % 7 == 0:
                self.x = 10
                self.height = 500
            else:
                self.x = 10 + 110 * self.number
        else:
            if self.number % 7 == 0:
                self.y = 50
                self.x = 10 + 110 * self.number
                self.height = 500
            else:
                self.y = 350
                self.x = 780 - (110 * (self.number % 7))


class Bead:
    def __init__(self, color):
        self.color = color


def make_containers():
    containers = []
    player = 1
    for i in range(14):
        if i == 7:
            player = 2
        containers.append(Container(i, player))
    return containers


def fill_containers(containers, balls):
    for i in containers:
        if i.number % 7 != 0:
            for j in range(balls):
                l = 0
                h = 255
                rand_color = (random.randint(l, h), random.randint(l, h), random.randint(l, h))
                i.content.append(Bead(rand_color))


def draw_containers(display, containers):
    color = (205, 133, 63)
    for conta in containers:
        pygame.draw.rect(display, color, (conta.x, conta.y, conta.width, conta.height))


def draw_beads(display, containers):
    for c in containers:
        delta_x = 20
        delta_y = 20
        for b in c.content:
            pygame.draw.circle(display, b.color, (c.x + delta_x, c.y + delta_y), 20)
            delta_y += 30
            if delta_y >= 20 + 30 * 6 and c.number % 7 != 0:
                delta_y = 20
                delta_x += 50
            elif c.number % 7 == 0 and delta_y >= 20 + 30 * 16:
                delta_y = 20
                delta_x += 50


def draw_numbers(display, containers):
    font = pygame.font.Font("freesansbold.ttf", 30)
    for c in containers:
        beads_num = font.render(str(len(c.content)), True, (255, 255, 255))
        if 0 < c.number <= 7:
            delta_y = c.height
        else:
            delta_y = -30
        display.blit(beads_num, (int(c.width / 2 - 10 + c.x), c.y + delta_y))


def draw_controls(display, player1turn):
    font = pygame.font.Font("freesansbold.ttf", 40)
    if player1turn:
        y = 10
    else:
        y = 550
    for i in range(6):
        num = font.render('[' + str(i + 1) + ']', True, (255, 255, 255))
        display.blit(num, (145 + i * 110, y))


def perfect_print(display, player1turn):
    if player1turn:
        x, y = 10, 50
    else:
        x, y = 780,50

    g = pygame.Surface((100, 500), pygame.SRCALPHA)  # per-pixel alpha
    g.fill((0, 255, 0, 100))  # notice the alpha value in the color
    display.blit(g, (x, y))

    font = pygame.font.Font("freesansbold.ttf", 80)
    text = font.render(' Perfect!', True, (50, 255, 50))
    s = pygame.Surface((410, 200), pygame.SRCALPHA)  # per-pixel alpha
    s.fill((0, 0, 0, 200))  # notice the alpha value in the color
    display.blit(s, (240, 200))
    display.blit(text, (270, 260))


def draw_drop_box(display, container):
    s = pygame.Surface((container.width, container.height), pygame.SRCALPHA)  # per-pixel alpha
    s.fill((255, 255, 255, 50))  # notice the alpha value in the color
    display.blit(s, (container.x, container.y))


def empty_hand(containers, drop_i, hand_list, player1turn):
    containers[drop_i].content.append(hand_list[-1])
    hand_list.pop()
    drop_i = (drop_i - 1) % 14
    return (drop_i)


def side_steal(display, containers, index, player1turn):
    steal_index = 14 - index

    if player1turn:
        goal = 0
        upper = containers[index] # draw from upper box
    else:
        goal = 7
        upper = containers[steal_index]



    containers[goal].content.append(containers[index].content[0])
    for i in containers[steal_index].content:
        containers[goal].content.append(i)

    containers[index].content.clear()
    containers[steal_index].content.clear()

    r = pygame.Surface((upper.width, upper.height*2+100), pygame.SRCALPHA)  # per-pixel alpha
    r.fill((255, 0, 0, 100))  # notice the alpha value in the color
    display.blit(r, (upper.x, upper.y))

    s = pygame.Surface((410, 200), pygame.SRCALPHA)  # per-pixel alpha
    s.fill((0, 0, 0, 200))  # notice the alpha value in the color
    display.blit(s, (240, 200))

    font = pygame.font.Font("freesansbold.ttf", 80)
    text = font.render('Steal!', True, (50, 255, 50))
    display.blit(text, (300, 260))


def check_game_over(containers):
    game_over16 = True
    for i in range(6):
        if len(containers[i + 1].content) > 0:
            game_over16 = False
    game_over813 = True
    for i in range(6):
        if len(containers[i + 8].content) > 0:
            game_over813 = False
    game_over = game_over16 or game_over813
    return game_over


def clean_board(containers):
    goal = 0
    for i in range(6):
        for j in containers[i + 1].content:
            containers[goal].content.append(j)
        containers[i + 1].content.clear()
    goal = 7
    for i in range(6):
        for j in containers[i + 8].content:
            containers[goal].content.append(j)
        containers[i + 8].content.clear()


def draw_results(display, containers):
    font = pygame.font.Font("freesansbold.ttf", 40)
    score1 = len(containers[0].content)
    score2 = len(containers[7].content)
    if score1 > score2:
        text1 = font.render('Winner is Player 1!', True, (50, 255, 50))
    elif score2 > score1:
        text1 = font.render('Winner is Player 2!', True, (50, 255, 50))
    else:
        text1 = font.render('       Tied game!', True, (50, 255, 50))
    text2 = font.render(str(score1) + ' - ' + str(score2), True, (50, 255, 50))
    text3 = font.render('R to restart', True, (50, 255, 50))

    s = pygame.Surface((410, 200), pygame.SRCALPHA)  # per-pixel alpha
    s.fill((0, 0, 0, 200))  # notice the alpha value in the color
    display.blit(s, (240, 200))

    display.blit(text1, (260, 230))
    display.blit(text2, (360, 280))
    display.blit(text3, (330, 330))


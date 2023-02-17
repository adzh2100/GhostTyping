import pygame

INITIAL_GHOST_SIZE = 100, 100
MAX_GHOST_SIZE = 300

BUTTON_SIZE = 160, 60

COLOR_INACTIVE = "#CCD7C5"
COLOR_ACTIVE = "#97B684"
COLOR_BLACK = "#000000"
COLOR_WHITE = "#FFFFFF"
COLOR_GREY = "#999999"

WINDOW_WIDTH = 1200
WINDOW_HEIGHT = 1000

LIVES_OFFSET = 10
LIFE_SIZE = 50, 50

KEY_LETTER_MAP = {
    pygame.K_a: "a",
    pygame.K_b: "b",
    pygame.K_c: "c",
    pygame.K_d: "d",
    pygame.K_e: "e",
    pygame.K_f: "f",
    pygame.K_g: "g",
    pygame.K_h: "h",
    pygame.K_i: "i",
    pygame.K_j: "j",
    pygame.K_k: "k",
    pygame.K_l: "l",
    pygame.K_m: "m",
    pygame.K_n: "n",
    pygame.K_o: "o",
    pygame.K_p: "p",
    pygame.K_q: "q",
    pygame.K_r: "r",
    pygame.K_s: "s",
    pygame.K_t: "t",
    pygame.K_u: "u",
    pygame.K_v: "v",
    pygame.K_w: "w",
    pygame.K_x: "x",
    pygame.K_y: "y",
    pygame.K_z: "z",
    pygame.K_0: "0",
    pygame.K_1: "1",
    pygame.K_2: "2",
    pygame.K_3: "3",
    pygame.K_4: "4",
    pygame.K_5: "5",
    pygame.K_6: "6",
    pygame.K_7: "7",
    pygame.K_8: "8",
    pygame.K_9: "9",
    pygame.K_SPACE: " ",
    pygame.K_UNDERSCORE: "_",
}

LEADERBOARD_FILE = "lib/leaderboard.txt"
DICTIONARY_FILE = "lib/dictionary.txt"

SPEED_CHANGE_TRESHOLD = 15000
INITIAL_SPEED_CHANGE_TIME = 3000
MAX_SPEED_CHANGE_TIME = 1000
SPEED_GAP = 500

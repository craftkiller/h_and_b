import pygame

class key_bindings():

    def __init__(self):
        self.up = [pygame.K_UP, pygame.K_w]
        self.down = [pygame.K_DOWN, pygame.K_s]
        self.left = [pygame.K_LEFT, pygame.K_a]
        self.right = [pygame.K_RIGHT, pygame.K_d]
        self.barrel_left = [pygame.K_q, None]
        self.barrel_right = [pygame.K_e, None]
        self.shoot = [pygame.K_SPACE, None]
        self.dragon = [pygame.K_r, None]

    def get_string(key):
        if key == None:
            return "None"
        else:
            return pygame.key.name(key)

import pygame

class Laatikko:
    def __init__(self, x, y, koko):
        self.x = x
        self.y = y
        self.koko = koko
        self.muoto = self.luo_laatikko()

    def luo_laatikko(self):
        return pygame.Rect(self.x * self.koko, self.y * self.koko, self.koko, self.koko)
    
    def liiku(self, suunta, map, on_laatikko):
        uusi_y = self.y + suunta[0]
        uusi_x = self.x + suunta[1]
        if map[uusi_y][uusi_x] == 1:
            return False
        if on_laatikko(uusi_x, uusi_y):
            return False
        self.x += suunta[1]
        self.y += suunta[0]
        self.muoto = self.luo_laatikko()
        return True
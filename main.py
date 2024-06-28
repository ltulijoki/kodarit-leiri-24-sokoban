import pygame, sys
import box

# Määritä kenttä (0 = tyhjä, 1 = seinä, 2 = maali, 3 = laatikko)
MAP = [
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 3, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 2, 0, 0, 1, 0, 0, 1, 1, 1],
    [1, 0, 0, 3, 0, 0, 1, 0, 0, 0, 2, 1],
    [1, 0, 0, 0, 0, 2, 1, 3, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1], 
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
]

palikan_koko = 75
mapin_leveys = len(MAP[0])
mapin_korkeus = len(MAP)

VASEN = (0, -1)
OIKEA = (0, 1)
YLOS = (-1, 0)
ALAS = (1, 0)
EILIIKU = (0, 0)

pelialueen_leveys = palikan_koko * mapin_leveys
pelialueen_korkeus = palikan_koko * mapin_korkeus

class Sokoban:
    def __init__(self):
        pygame.init()
        self.pelialue = pygame.display.set_mode((pelialueen_leveys, pelialueen_korkeus))
        pygame.display.set_caption("Sokoban")

        self.pelaajan_paikka = [1, 1]
        self.pelaaja = pygame.Rect(self.pelaajan_paikka[0] * palikan_koko, self.pelaajan_paikka[1] * palikan_koko, palikan_koko, palikan_koko)

        self.tausta = pygame.Rect(0, 0, pelialueen_leveys, pelialueen_korkeus)

        self.seinapalikka = pygame.Surface((palikan_koko, palikan_koko))
        self.seinapalikka.fill("#027069")

        self.pelaajan_kuva = pygame.image.load("bird.png")
        self.pelaajan_kuva = pygame.transform.scale(self.pelaajan_kuva, (palikan_koko, palikan_koko))

        self.taustakuva = pygame.image.load("floor.png")
        self.taustakuva = pygame.transform.scale(self.taustakuva, (pelialueen_leveys, pelialueen_korkeus))

        self.maalin_kuva = pygame.image.load("goal.png")
        self.maalin_kuva = pygame.transform.scale(self.maalin_kuva, (palikan_koko, palikan_koko))

        self.laatikon_kuva = pygame.image.load("box.png")
        self.laatikon_kuva = pygame.transform.scale(self.laatikon_kuva, (palikan_koko, palikan_koko))

        self.voittokuva = pygame.image.load("voittoruutu.png")
        self.voittokuva = pygame.transform.scale(self.voittokuva, (pelialueen_leveys, pelialueen_korkeus))

        self.maalit = []
        self.laatikot = []

        self.piirra_ja_luo_maali()
        self.piirra_ja_luo_laatikot()

        self.running = True

        self.siirrot = 0
        self.fontti = pygame.font.SysFont("Arial", 24)

        self.uusipelinappi = pygame.Surface((palikan_koko * 2, palikan_koko))
        self.uusipelinappi.fill((255, 0, 0))
        self.uusipeliteksti = self.fontti.render('Uusi peli', True, (0, 0, 0))
        self.uusipelinappi.blit(self.uusipeliteksti, (25, 25))

    def piirra_lattia_ja_seinat(self):
        for y in range(mapin_korkeus):
            for x in range(mapin_leveys):
                if MAP[y][x] == 1:
                    self.pelialue.blit(self.seinapalikka, (x * palikan_koko, y *  palikan_koko))

    def piirra_ja_luo_maali(self):
        for y in range(mapin_korkeus):
            for x in range(mapin_leveys):
                if MAP[y][x] == 2:
                    maali = pygame.Rect(x * palikan_koko, y * palikan_koko, palikan_koko, palikan_koko)
                    self.maalit.append(maali)
                    self.pelialue.blit(self.maalin_kuva, maali)

    def piirra_maali(self):
        for maali in self.maalit:
            self.pelialue.blit(self.maalin_kuva, maali)

    def piirra_ja_luo_laatikot(self):
        for y in range(mapin_korkeus):
            for x in range(mapin_leveys):
                if MAP[y][x] == 3:
                    laatikko = box.Laatikko(x, y, palikan_koko)
                    self.laatikot.append(laatikko)
                    self.pelialue.blit(self.laatikon_kuva, laatikko.luo_laatikko())

    def piirra_laatikot(self):
        for laatikko in self.laatikot:
            self.pelialue.blit(self.laatikon_kuva, laatikko.luo_laatikko())

    def liiku(self, suunta):
        if suunta != EILIIKU:
            self.siirrot += 1
        uusi_y = self.pelaajan_paikka[1] + suunta[0]
        uusi_x = self.pelaajan_paikka[0] + suunta[1]
        if MAP[uusi_y][uusi_x] == 1:
            return
        laatikko = self.on_laatikko(uusi_x, uusi_y)
        if laatikko:
            if not laatikko.liiku(suunta, MAP, self.on_laatikko):
                return
        self.pelaajan_paikka[0] += suunta[1]
        self.pelaajan_paikka[1] += suunta[0]

    def on_laatikko(self, x, y):
        for laatikko in self.laatikot:
            if laatikko.x == x and laatikko.y == y:
                return laatikko
        return None

    def kaikki_maalissa(self):
        maalit = list(map(lambda m: (m.x, m.y), self.maalit))
        for laatikko in self.laatikot:
            if (laatikko.x * palikan_koko, laatikko.y * palikan_koko) not in maalit:
                return False
        return True
    
    def uusipeli(self):
        self.pelaajan_paikka = [1, 1]

        self.maalit = []
        self.laatikot = []

        self.piirra_ja_luo_maali()
        self.piirra_ja_luo_laatikot()

        self.siirrot = 0

    def kasittele_tapahtumat(self, liike):
        suunta = EILIIKU
        for tapahtuma in pygame.event.get():
            if tapahtuma.type == pygame.QUIT:
                self.running = False
            elif tapahtuma.type == pygame.KEYDOWN and liike:
                if tapahtuma.key == pygame.K_LEFT:
                    suunta = VASEN
                elif tapahtuma.key == pygame.K_RIGHT:
                    suunta = OIKEA
                elif tapahtuma.key == pygame.K_UP:
                    suunta = YLOS
                elif tapahtuma.key == pygame.K_DOWN:
                    suunta = ALAS
            elif tapahtuma.type == pygame.MOUSEBUTTONUP:
                pos = pygame.mouse.get_pos()
                if pos[0] >= pelialueen_leveys - palikan_koko * 2 and pos[1] >= pelialueen_korkeus - palikan_koko:
                    self.uusipeli()

        self.liiku(suunta)

    def kaynnista(self):
        while self.running:
            if self.kaikki_maalissa():
                self.pelialue.blit(self.voittokuva, self.tausta)
                teksti = self.fontti.render(f"Siirrot: {self.siirrot}", True, (255, 0, 0))
                self.pelialue.blit(teksti, (400, pelialueen_korkeus - 100))
                self.pelialue.blit(self.uusipelinappi, (pelialueen_leveys - palikan_koko * 2, pelialueen_korkeus - palikan_koko))
                pygame.display.flip()
                self.kasittele_tapahtumat(False)
                continue
            self.kasittele_tapahtumat(True)

            self.pelaaja = pygame.Rect(self.pelaajan_paikka[0] * palikan_koko, self.pelaajan_paikka[1] * palikan_koko,
                                       palikan_koko, palikan_koko)

            self.pelialue.blit(self.taustakuva, self.tausta)
            self.piirra_lattia_ja_seinat()
            self.piirra_maali()
            self.piirra_laatikot()
            self.pelialue.blit(self.uusipelinappi, (pelialueen_leveys - palikan_koko * 2, pelialueen_korkeus - palikan_koko))

            self.pelialue.blit(self.pelaajan_kuva, self.pelaaja)

            pygame.display.flip()

        pygame.quit()
        sys.exit()

Sokoban().kaynnista()
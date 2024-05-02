import pygame
import random

class rahasade:
    def __init__(self):
        pygame.init()

        self.lataa_kuvat()
        self.uusi_peli()

        self.korkeus = len(self.kartta)
        self.leveys = len(self.kartta[0])
        self.skaala = self.kuvat[0].get_width()

        nayton_korkeus = self.skaala * self.korkeus
        nayton_leveys = self.skaala * self.leveys
        self.naytto = pygame.display.set_mode((nayton_leveys, nayton_korkeus))

        self.naytto = pygame.display.set_mode((nayton_leveys, nayton_korkeus + self.skaala))

        self.fontti = pygame.font.SysFont("Arial", 24)

        pygame.display.set_caption("Rahasade")

        self.silmukka()

    def lataa_kuvat(self):
        self.kuvat = []
        for nimi in ["lattia", "seina", "kohde", "laatikko", "robo","valmis","kohderobo"]:
            self.kuvat.append(pygame.image.load(nimi + ".png"))

    def uusi_peli(self):
        self.pisteet = 0
        self.kartta = [[1,0,0,0,0,0,0,0,0,0,0,0,1],
                       [1,0,0,0,0,0,0,0,0,0,0,0,1],
                       [1,0,0,0,0,0,0,0,0,0,0,0,1],
                       [1,0,0,0,0,0,0,0,0,0,0,0,1],
                       [1,0,0,0,0,0,0,0,0,0,0,0,1],
                       [1,0,0,0,0,0,0,0,0,0,0,0,1],
                       [1,0,0,0,0,0,4,0,0,0,0,0,1],
                       [1,1,1,1,1,1,1,1,1,1,1,1,1]]
        
    def silmukka(self):
        while True:
            self.tutki_tapahtumat()
            self.piirra_naytto()
            

    def tutki_tapahtumat(self):
        for tapahtuma in pygame.event.get():
            if tapahtuma.type == pygame.KEYDOWN:
                if tapahtuma.key == pygame.K_LEFT:
                    self.liiku(0, -1)
                    self.luo_sade()
                    self.tarkista_tormaykset()
                    self.paivita_kartta()
                if tapahtuma.key == pygame.K_RIGHT:
                    self.liiku(0, 1)
                    self.luo_sade()
                    self.tarkista_tormaykset()
                    self.paivita_kartta()
                if tapahtuma.key == pygame.K_F2:
                    self.uusi_peli()
                if tapahtuma.key == pygame.K_ESCAPE:
                    exit()

            if tapahtuma.type == pygame.QUIT:
                exit()
                            
    def piirra_naytto(self):
        self.naytto.fill((0, 0, 0))

        teksti = self.fontti.render("Pisteet: " + str(self.pisteet), True, (255, 0, 0))
        self.naytto.blit(teksti, (25, self.korkeus * self.skaala + 10))

        teksti = self.fontti.render("F2 = uusi peli", True, (255, 0, 0))
        self.naytto.blit(teksti, (200, self.korkeus * self.skaala + 10))

        teksti = self.fontti.render("Esc = sulje peli", True, (255, 0, 0))
        self.naytto.blit(teksti, (400, self.korkeus * self.skaala + 10))

        for y in range(self.korkeus):
            for x in range(self.leveys):
                ruutu = self.kartta[y][x]
                self.naytto.blit(self.kuvat[ruutu], (x * self.skaala, y * self.skaala))

        pygame.display.flip()

    def etsi_robo(self):
        for y in range(self.korkeus):
            for x in range(self.leveys):
                if self.kartta[y][x] in [4,6]:
                    return (y, x)

    def liiku(self, liike_y, liike_x):
       
        robon_vanha_y, robon_vanha_x = self.etsi_robo()
        robon_uusi_y = robon_vanha_y + liike_y
        robon_uusi_x = robon_vanha_x + liike_x

        if self.kartta[robon_uusi_y][robon_uusi_x] == 1:
            return
        elif self.kartta[robon_uusi_y][robon_uusi_x] == 3:
            return
        elif self.kartta[robon_uusi_y][robon_uusi_x] == 2:  # Jos seuraava ruutu on raha
            self.kartta[robon_vanha_y][robon_vanha_x] -= 4
            self.kartta[robon_uusi_y][robon_uusi_x] = 6  # Robotti + Raha
            self.pisteet+=1
        else:
            self.kartta[robon_vanha_y][robon_vanha_x] -= 4
            self.kartta[robon_uusi_y][robon_uusi_x] += 4


    def luo_sade(self):
        sattuma = random.randint(0,3)
        # Luo uusi raha tai hirviö satunnaisessa x-koordinaatissa
        if sattuma == 0:
            self.kartta[0][random.randint(1, self.leveys - 2)] = 2  # Raha
        elif sattuma == 1:
            self.kartta[0][random.randint(1, self.leveys - 2)] = 3 
        else:
            self.kartta[0][random.randint(1, self.leveys - 2)] = 0 

    def paivita_kartta(self):
        # Päivitä karttaa yksi rivi kerrallaan alhaalta ylöspäin
        for y in range(self.korkeus - 1, -1, -1):
            for x in range(self.leveys):
                if self.kartta[y][x] in [2, 3]:  # Jos raha tai hirviö
                    if y < self.korkeus - 1:  # Jos ei ole alarivillä
                        # Jos seuraava ruutu on seinä, poista raha tai hirviö
                        if self.kartta[y + 1][x] == 1:
                            self.kartta[y][x] = 0
                        else:
                            # Siirrä raha tai hirviö yksi rivi alaspäin
                            self.kartta[y + 1][x] = self.kartta[y][x]
                            self.kartta[y][x] = 0

    def tarkista_tormaykset(self):
        # Tarkista, törmääkö raha tai hirviö robottiin
        for y in range(self.korkeus):
            for x in range(self.leveys):
                if self.kartta[y][x] in [2, 3]:  # Jos raha tai hirviö
                    if y < self.korkeus - 1 and self.kartta[y + 1][x] == 4:  # Jos seuraava ruutu on robotti
                        if self.kartta[y][x] == 2:  # Jos raha
                            self.pisteet += 1
                            self.kartta[y][x] = 0
                        elif self.kartta[y][x] == 3:  # Jos hirviö
                            print("Peli päättyi! Sait", self.pisteet, "pistettä.")
                            exit()  # Lopeta peli, jos robotti törmää hirviöön


if __name__ == "__main__":
    rahasade()        
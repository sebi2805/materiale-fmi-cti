import statistics
import time

import pygame, sys, copy

TIMPI_CALCULATOR = []
NR_MUTARI_P = 0
NR_MUTARI_CPU = 0
t_start = int(round(time.time() * 1000))

class GrupButoane:
    def __init__(self, listaButoane=[], indiceSelectat=0, spatiuButoane=10, left=0, top=0):
        self.listaButoane = listaButoane
        self.indiceSelectat = indiceSelectat
        self.listaButoane[self.indiceSelectat].selectat = True
        self.top = top
        self.left = left
        leftCurent = self.left
        for b in self.listaButoane:
            b.top = self.top
            b.left = leftCurent
            b.updateDreptunghi()
            leftCurent += (spatiuButoane + b.w)

    def selecteazaDupacoord(self, coord):
        for ib, b in enumerate(self.listaButoane):
            if b.selecteazaDupacoord(coord):
                self.listaButoane[self.indiceSelectat].selecteaza(False)
                self.indiceSelectat = ib
                return True
        return False

    def deseneaza(self):
        # atentie, nu face wrap
        for b in self.listaButoane:
            b.deseneaza()

    def getValoare(self):
        return self.listaButoane[self.indiceSelectat].valoare

class Buton:
    def __init__(self, display=None, left=0, top=0, w=0, h=0, culoareFundal=(53, 80, 115),
                 culoareFundalSel=(89, 134, 194), text="", font="arial", fontDimensiune=16, culoareText=(255, 255, 255),
                 valoare=""):
        self.display = display
        self.culoareFundal = culoareFundal
        self.culoareFundalSel = culoareFundalSel
        self.text = text
        self.font = font
        self.w = w
        self.h = h
        self.selectat = False
        self.fontDimensiune = fontDimensiune
        self.culoareText = culoareText
        # creez obiectul font
        fontObj = pygame.font.SysFont(self.font, self.fontDimensiune)
        self.textRandat = fontObj.render(self.text, True, self.culoareText)
        self.dreptunghi = pygame.Rect(left, top, w, h)
        # aici centram textul
        self.dreptunghiText = self.textRandat.get_rect(center=self.dreptunghi.center)
        self.valoare = valoare

    def selecteaza(self, sel):
        self.selectat = sel
        self.deseneaza()

    def selecteazaDupacoord(self, coord):
        if self.dreptunghi.collidepoint(coord):
            self.selecteaza(True)
            return True
        return False

    def updateDreptunghi(self):
        self.dreptunghi.left = self.left
        self.dreptunghi.top = self.top
        self.dreptunghiText = self.textRandat.get_rect(center=self.dreptunghi.center)

    def deseneaza(self):
        culoareF = self.culoareFundalSel if self.selectat else self.culoareFundal
        pygame.draw.rect(self.display, culoareF, self.dreptunghi)
        self.display.blit(self.textRandat, self.dreptunghiText)

def deseneaza_alegeri(display, tabla_curenta):
    btn_alg = GrupButoane(
        top=150,
        left=30,
        listaButoane=[
            Buton(display=display, w=80, h=30, text="P1 vs CPU", valoare="1"),
            Buton(display=display, w=80, h=30, text="P1 vs P2", valoare="2"),
            Buton(display=display, w=80, h=30, text="CPU vs CPU", valoare="3")
        ],
        indiceSelectat=1)
    ok = Buton(display=display, top=250, left=30, w=40, h=30, text="ok", culoareFundal=(155, 0, 55))
    btn_alg.deseneaza()
    ok.deseneaza()
    while True:
        for ev in pygame.event.get():
            if ev.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif ev.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                if not btn_alg.selecteazaDupacoord(pos):
                        if ok.selecteazaDupacoord(pos):
                            display.fill((0, 0, 0))  # stergere ecran
                            tabla_curenta.deseneaza_grid()
                            return btn_alg.getValoare()
        pygame.display.update()


def elem_identice(lista):
    if (all(elem == lista[0] for elem in lista[1:])):
        return lista[0] if lista[0] != Joc.GOL else False
    return False

SCOR_X = 0
SCOR_MAXIM = 10
SCOR_0 = 0

class Joc:
    """
    Clasa care defineste jocul. Se va schimba de la un joc la altul.
    """
    NR_COLOANE = 0
    NR_LINII = 0
    NR_NODURI = 0
    LISTA_NODURI = []
    JMIN = None
    JMAX = None
    GOL = '#'

    @classmethod
    def initializeaza(cls, display, NR_LINII, NR_COLOANE, dim_celula=100):
        cls.display = display
        cls.dim_celula = dim_celula
        cls.x_img = pygame.image.load('ics.png')
        cls.x_img = pygame.transform.scale(cls.x_img, (dim_celula, dim_celula))
        cls.zero_img = pygame.image.load('zero.png')
        cls.zero_img = pygame.transform.scale(cls.zero_img, (dim_celula, dim_celula))
        cls.celuleGrid = []  # este lista cu patratelele din grid
        cls.NR_LINII = NR_LINII
        cls.NR_COLOANE = NR_COLOANE
        for linie in range(NR_LINII):
            cls.celuleGrid.append([])
            for coloana in range(NR_COLOANE):
                patr = pygame.Rect(coloana * (dim_celula + 1), linie * (dim_celula + 1), dim_celula, dim_celula)
                cls.celuleGrid[linie].append(patr)

    def deseneaza_grid(self, jucator='JMIN', marcaj=None, end=False):  # tabla de exemplu este ["#","x","#","0",......]

        for linie in range(Joc.NR_LINII):
            for coloana in range(Joc.NR_COLOANE):
                if marcaj == (linie, coloana):
                    # daca am o patratica selectata, o desenez cu rosu
                    culoare = (255, 0, 0)
                else:
                    # altfel o desenez cu alb
                    culoare = (255, 255, 255)
                    culoareverde = (144,238,144)
                if jucator == 'JMIN':
                    pygame.draw.rect(self.__class__.display, culoareverde,
                                     self.__class__.celuleGrid[linie][coloana])  # alb = (255,255,255)
                else:
                    pygame.draw.rect(self.__class__.display, culoare,
                                     self.__class__.celuleGrid[linie][coloana])  # alb = (255,255,255)
                if self.matr[linie][coloana] == 'x':
                    if end == False or end != 'x':
                        pygame.draw.rect(self.__class__.display, culoare,
                                         self.__class__.celuleGrid[linie][coloana])  # alb = (255,255,255)
                        self.__class__.display.blit(self.__class__.x_img, (
                        coloana * (self.__class__.dim_celula + 1), linie * (self.__class__.dim_celula + 1)))
                    elif end == 'x':
                        pygame.draw.rect(self.__class__.display, (255,255,0),
                                         self.__class__.celuleGrid[linie][coloana])  # alb = (255,255,255)
                        self.__class__.display.blit(self.__class__.x_img, (
                        coloana * (self.__class__.dim_celula + 1), linie * (self.__class__.dim_celula + 1)))
                elif self.matr[linie][coloana] == '0':
                    if end == False or end != '0':
                        pygame.draw.rect(self.__class__.display, culoare,
                                         self.__class__.celuleGrid[linie][coloana])  # alb = (255,255,255)
                        self.__class__.display.blit(self.__class__.zero_img, (
                        coloana * (self.__class__.dim_celula + 1), linie * (self.__class__.dim_celula + 1)))
                    elif end == '0':
                        pygame.draw.rect(self.__class__.display, (255,255,0),
                                         self.__class__.celuleGrid[linie][coloana])  # alb = (255,255,255)
                        self.__class__.display.blit(self.__class__.x_img, (
                        coloana * (self.__class__.dim_celula + 1), linie * (self.__class__.dim_celula + 1)))
        pygame.display.flip()  # !!! obligatoriu pentru a actualiza interfata (desenul)


    # pygame.display.update()

    def cauta_succesiune(self):
        matrice = copy.deepcopy(self.matr)
        global SCOR_X, SCOR_0

        ### PE LINIE
        for i in range(self.NR_LINII):
            count = 0
            ant = None
            poz = -1
            for j in range(self.NR_COLOANE):
                if count >= 4 and ant != self.matr[i][j]:
                    if ant == 'x':
                        SCOR_X += count - 4 + 1
                    else:
                        SCOR_0 += count - 4 + 1
                    for k in range(poz, j):
                        matrice[i][k] = '#'
                    ant = self.matr[i][j]
                    count = 1
                elif self.matr[i][j] != '#':
                    if self.matr[i][j] == ant:
                        count += 1
                    else:
                        ant = self.matr[i][j]
                        count = 1
                        poz = j
                else:
                    count = 0
                    ant = None
                    poz = -1
            if count >= 4:
                if ant == 'x':
                    SCOR_X += count - 4 + 1
                else:
                    SCOR_0 += count - 4 + 1
                for k in range(poz, self.NR_COLOANE):
                    matrice[i][k] = '#'

        ### PE COLOANA
        for j in range(self.NR_COLOANE):
            count = 0
            ant = None
            poz = -1
            for i in range(self.NR_LINII):
                if count >= 4 and ant != self.matr[i][j]:
                    if ant == 'x':
                        SCOR_X += count - 4 + 1
                    else:
                        SCOR_0 += count - 4 + 1
                    for k in range(poz, i):
                        matrice[k][j] = '#'
                    ant = self.matr[i][j]
                    count = 1
                elif self.matr[i][j] != '#':
                    if self.matr[i][j] == ant:
                        count += 1
                    else:
                        ant = self.matr[i][j]
                        count = 1
                        poz = i
                else:
                    count = 0
                    ant = None
                    poz = -1
            if count >= 4:
                if ant == 'x':
                    SCOR_X += count - 4 + 1
                else:
                    SCOR_0 += count - 4 + 1
                for k in range(poz, self.NR_LINII):
                    matrice[k][j] = '#'

        # PE DIAGONALA PRINCIPALA
        for k in range(self.NR_COLOANE):
            count = 0
            ant = None
            poz = -1
            for i in range(k+self.NR_LINII):
                if k + i < self.NR_LINII:
                    if count >= 4 and ant != self.matr[i][k+i]:
                        if ant == 'x':
                            SCOR_X += count - 4 + 1
                        else:
                            SCOR_0 += count - 4 + 1
                        for k2 in range(poz, i):
                            matrice[k2][k+k2] = '#'
                        ant = self.matr[i][k+i]
                        count = 1
                    elif self.matr[i][k+i] != '#':
                        if self.matr[i][k+i] == ant:
                            count += 1
                        else:
                            ant = self.matr[i][k+i]
                            count = 1
                            poz = i
                    else:
                        count = 0
                        ant = None
                        poz = -1
            if count >= 4:
                if ant == 'x':
                    SCOR_X += count - 4 + 1
                else:
                    SCOR_0 += count - 4 + 1
                for k2 in range(poz, k+self.NR_LINII):
                    if k+k2 < self.NR_LINII:
                        matrice[k2][k+k2] = '#'
            count = 0
            ant = None
            poz = -1
            for i in range(k+self.NR_LINII):
                if k + i < self.NR_LINII:
                    if count >= 4 and ant != self.matr[k+i][i]:
                        if ant == 'x':
                            SCOR_X += count - 4 + 1
                        else:
                            SCOR_0 += count - 4 + 1
                        for k2 in range(poz, i):
                            matrice[k+k2][k2] = '#'
                        ant = self.matr[k+i][i]
                        count = 1
                    elif self.matr[k+i][i] != '#':
                        if self.matr[k+i][i] == ant:
                            count += 1
                        else:
                            ant = self.matr[k+i][i]
                            count = 1
                            poz = i
                    else:
                        count = 0
                        ant = None
                        poz = -1
            if count >= 4:
                if ant == 'x':
                    SCOR_X += count - 4 + 1
                else:
                    SCOR_0 += count - 4 + 1
                for k2 in range(poz, k+self.NR_LINII):
                    if k+k2 < self.NR_LINII:
                        matrice[k+k2][k2] = '#'

        self.matr = copy.deepcopy(matrice)

    def __init__(self, NR_LINII, NR_COLOANE, tabla=None):
        if tabla:
            self.matr = tabla
        else:
            self.matr = []
            for i in range(NR_LINII):
                self.matr.append([self.__class__.GOL] * NR_COLOANE)

    @classmethod
    def jucator_opus(cls, jucator):
        return cls.JMAX if jucator == cls.JMIN else cls.JMIN

    def final(self):
        global SCOR_X, SCOR_0, SCOR_MAXIM
        if SCOR_X >= SCOR_MAXIM:
            return 'x'
        if SCOR_0 >= SCOR_MAXIM:
            return '0'
        for i in range(self.NR_LINII):
            for j in range(self.NR_COLOANE):
                if '#' == self.matr[i][j]:
                    return False
        if SCOR_X > SCOR_0:
            return 'x'
        elif SCOR_X < SCOR_0:
            return '0'
        else:
            return 'egal'


    def mutari(self, jucator, interschimbare=0):  # jucator = simbolul jucatorului care muta
        l_mutari = []
        if jucator == 'x':
            opus = '0'
        else:
            opus = 'x'
        for i in range(self.__class__.NR_LINII):
            for j in range(self.__class__.NR_COLOANE):
                if self.matr[i][j] == Joc.GOL:
                    copie_matr = copy.deepcopy(self.matr)
                    copie_matr[i][j] = jucator
                    l_mutari.append([Joc(self.__class__.NR_LINII, self.__class__.NR_COLOANE, copie_matr),0])
                elif self.matr[i][j] == jucator and interschimbare == 0:
                    directii = [[i - 1, j], [i + 1, j],
                                [i - 1, j - 1], [i + 1, j + 1], [i - 1, j + 1], [i + 1, j - 1]]
                    for lDirectie,cDirectie in directii:
                        if 0 <= lDirectie < self.NR_LINII and 0 <= cDirectie < self.NR_COLOANE:
                            if self.matr[lDirectie][cDirectie] == 'opus':
                                copie_matr = copy.deepcopy(self.matr)
                                copie_matr[lDirectie][cDirectie] = jucator
                                copie_matr[i][j] = opus
                                l_mutari.append([Joc(self.__class__.NR_LINII, self.__class__.NR_COLOANE, copie_matr),1])

        return l_mutari

    # linie deschisa inseamna linie pe care jucatorul mai poate forma o configuratie castigatoare
    # practic e o linie fara simboluri ale jucatorului opus
    def linie_deschisa(self, lista, jucator):
        jo = self.jucator_opus(jucator)
        # verific daca pe linia data nu am simbolul jucatorului opus
        if not jo in lista:
            return 1
        return 0

    def linii_deschise(self, jucator):
        sum = 0
        for i in range(self.NR_LINII):
            sum += self.linie_deschisa(self.matr[i], jucator)
        for j in range(self.NR_COLOANE):
                sum += self.linie_deschisa([self.matr[i][j] for i in range(self.NR_LINII)], jucator)
        return sum

    def estimeaza_scor(self, adancime):
        t_final = self.final()
        # if (adancime==0):
        if t_final == self.__class__.JMAX:
            return (99 + adancime)
        elif t_final == self.__class__.JMIN:
            return (-99 - adancime)
        elif t_final == 'remiza':
            return 0
        # else:
        #     return SCOR_X-SCOR_0
        else:
            return (self.linii_deschise(self.__class__.JMAX) - self.linii_deschise(self.__class__.JMIN))

    def sirAfisare(self):
        sir = "  |"
        sir += " ".join([str(i) for i in range(self.NR_LINII)]) + "\n"
        sir += "-" * (self.NR_LINII + 1) * 2 + "\n"
        for i in range(self.NR_LINII):  # itereaza prin linii
            sir += str(i) + " |" + " ".join([str(x) for x in self.matr[i]]) + "\n"
        return sir

    def __str__(self):
        return self.sirAfisare()

    def __repr__(self):
        return self.sirAfisare()


class Stare:
    """
    Clasa folosita de algoritmii minimax si alpha-beta
    Are ca proprietate tabla de joc
    Functioneaza cu conditia ca in cadrul clasei Joc sa fie definiti JMIN si JMAX (cei doi jucatori posibili)
    De asemenea cere ca in clasa Joc sa fie definita si o metoda numita mutari() care ofera lista cu configuratiile posibile in urma mutarii unui jucator
    """

    def __init__(self, tabla_joc, j_curent, adancime, parinte=None, interschimbat=0 , estimare=None):
        self.tabla_joc = tabla_joc
        self.j_curent = j_curent

        # adancimea in arborele de stari
        self.adancime = adancime

        # estimarea favorabilitatii starii (daca e finala) sau al celei mai bune stari-fiice (pentru jucatorul curent)
        self.estimare = estimare

        # lista de mutari posibile din starea curenta
        self.mutari_posibile = []

        # cea mai buna mutare din lista de mutari posibile pentru jucatorul curent
        self.stare_aleasa = None

        self.interschimbat = interschimbat

    def mutari(self):
        l_mutari = self.tabla_joc.mutari(self.j_curent, interschimbare=self.interschimbat)
        juc_opus = Joc.jucator_opus(self.j_curent)
        l_stari_mutari = [Stare(mutare[0], juc_opus, self.adancime - 1, parinte=self, interschimbat=mutare[1]) for mutare in l_mutari]

        return l_stari_mutari

    def __str__(self):
        sir = str(self.tabla_joc) + "(Juc curent:" + self.j_curent + ")\n"
        return sir



""" Algoritmul MinMax """


def min_max(stare):
    if stare.adancime == 0 or stare.tabla_joc.final():
        stare.estimare = stare.tabla_joc.estimeaza_scor(stare.adancime)
        return stare

    # calculez toate mutarile posibile din starea curenta
    stare.mutari_posibile = stare.mutari()
    Joc.NR_NODURI += len(stare.mutari_posibile)

    # aplic algoritmul minimax pe toate mutarile posibile (calculand astfel subarborii lor)
    mutariCuEstimare = [min_max(mutare) for mutare in stare.mutari_posibile]

    if stare.j_curent == Joc.JMAX:
        # daca jucatorul e JMAX aleg starea-fiica cu estimarea maxima
        stare.stare_aleasa = max(mutariCuEstimare, key=lambda x: x.estimare)
    else:
        # daca jucatorul e JMIN aleg starea-fiica cu estimarea minima
        stare.stare_aleasa = min(mutariCuEstimare, key=lambda x: x.estimare)
    stare.estimare = stare.stare_aleasa.estimare
    return stare


def alpha_beta(alpha, beta, stare):
    if stare.adancime == 0 or stare.tabla_joc.final():
        stare.estimare = stare.tabla_joc.estimeaza_scor(stare.adancime)
        return stare

    if alpha > beta:
        return stare  # este intr-un interval invalid deci nu o mai procesez

    stare.mutari_posibile = stare.mutari()
    Joc.NR_NODURI += len(stare.mutari_posibile)

    if stare.j_curent == Joc.JMAX:
        estimare_curenta = float('-inf')

        for mutare in stare.mutari_posibile:
            # calculeaza estimarea pentru starea noua, realizand subarborele
            stare_noua = alpha_beta(alpha, beta, mutare)

            if (estimare_curenta < stare_noua.estimare):
                stare.stare_aleasa = stare_noua
                estimare_curenta = stare_noua.estimare
            if (alpha < stare_noua.estimare):
                alpha = stare_noua.estimare
                if alpha >= beta:
                    break

    elif stare.j_curent == Joc.JMIN:
        estimare_curenta = float('inf')

        for mutare in stare.mutari_posibile:

            stare_noua = alpha_beta(alpha, beta, mutare)

            if (estimare_curenta > stare_noua.estimare):
                stare.stare_aleasa = stare_noua
                estimare_curenta = stare_noua.estimare

            if (beta > stare_noua.estimare):
                beta = stare_noua.estimare
                if alpha >= beta:
                    break
    stare.estimare = stare.stare_aleasa.estimare

    return stare


def afis_daca_final(stare_curenta, FORCE=False):
    final = stare_curenta.tabla_joc.final()
    if (final or FORCE):
        if final:
            if (final == 'egal'):
                print("Este egalitate")
            else:
                stare_curenta.tabla_joc.deseneaza_grid(end=final)
                print("A castigat " + final)

        print("MINIM CALCULATOR - {}".format(min(TIMPI_CALCULATOR)))
        print("MAXIM CALCULATOR - {}".format(max(TIMPI_CALCULATOR)))
        print("AVG CALCULATOR - {}".format(sum(TIMPI_CALCULATOR)/len(TIMPI_CALCULATOR)))
        print("MEDIANA CALCULATOR - {}".format(statistics.median(TIMPI_CALCULATOR)))
        print("======================================================================")
        print("MINIM NR NODURI - {}".format(min(Joc.LISTA_NODURI)))
        print("MAXIM NR NODURI - {}".format(max(Joc.LISTA_NODURI)))
        print("AVG NR NODURI - {}".format(sum(Joc.LISTA_NODURI) / len(Joc.LISTA_NODURI)))
        print("MEDIANA NR NODURI - {}".format(statistics.median(Joc.LISTA_NODURI)))
        print("======================================================================")
        print("NUMAR MUTARI PLAYER - {}".format(NR_MUTARI_P))
        print("NUMAR MUTARI CPU - {}".format(NR_MUTARI_CPU))
        print("======================================================================")
        print("TIMP TOTAL JOC - {}".format(int(round(time.time() * 1000))-t_start))
        return True

    return False


def main():
    global t_start
    global SCOR_MAXIM
    # initializare algoritm
    tip_algoritm = 0
    raspuns_valid = False
    while not raspuns_valid:
        tip_algoritm = input("Algorimul folosit? (raspundeti cu 1 sau 2)\n 1.Minimax\n 2.Alpha-beta\n ")
        if tip_algoritm in ['1', '2']:
            raspuns_valid = True
        else:
            print("Nu ati ales o varianta corecta.")
    # initializare jucatori
    raspuns_valid = False
    while not raspuns_valid:
        Joc.JMIN = input("Doriti sa jucati cu x sau cu 0? ").lower()
        if (Joc.JMIN in ['x', '0']):
            raspuns_valid = True
        else:
            print("Raspunsul trebuie sa fie x sau 0.")
    Joc.JMAX = '0' if Joc.JMIN == 'x' else 'x'
    raspuns_valid = False
    ADANCIME_MAX = 1
    while not raspuns_valid:
        ADANCIME_MAX = int(input("Ce dificultate vrei? - 1-incepator, 2-mediu, 3-avansat "))
        if ADANCIME_MAX in [1, 2, 3]:
            raspuns_valid = True
        else:
            print("RASPUNSUL TREBUIE SA CUPRINDE OPTIUNILE DE MAI SUS")
    NR_LINII = 3
    NR_COLOANE = 3
    raspuns_valid = False
    while not raspuns_valid:
        NR_LINII = int(input("Numar de linii: "))
        NR_COLOANE = int(input("Numar de coloane "))
        if 5 <= NR_LINII <= 10 and 5 <= NR_COLOANE <= 10:
            raspuns_valid = True
        else:
            print("NR DE LINII SAU DE COLOANE NU ESTE IN INTERVALUL [5,10]")
    SCOR_MAXIM = int(input("SCOR MAXIM: "))
    # initializare tabla
    tabla_curenta = Joc(NR_LINII, NR_COLOANE)
    print("Tabla initiala")
    print(str(tabla_curenta))

    # creare stare initiala
    stare_curenta = Stare(tabla_curenta, 'x', ADANCIME_MAX)

    # setari interf grafica
    pygame.init()
    pygame.display.set_caption('NICOI ALEXANDRU - X si 0')
    # dimensiunea ferestrei in pixeli
    # dim_celula=..
    ecran = pygame.display.set_mode(
        size=(NR_COLOANE*100+(NR_COLOANE-1), NR_LINII*100+(NR_LINII-1)))  # N *100+ (N-1)*dimensiune_linie_despartitoare (dimensiune_linie_despartitoare=1)
    Joc.initializeaza(ecran, NR_LINII, NR_COLOANE)
    mod_de_joc = deseneaza_alegeri(ecran, tabla_curenta)
    global SCOR_X, SCOR_0
    de_mutat = False
    tabla_curenta.deseneaza_grid(jucator='JMIN')
    countUndo = 0
    mutariAnterioare = []
    OKprimulUndo = False
    posib_interschimbare = True
    t_start = int(round(time.time() * 1000))
    t_inainte = int(round(time.time() * 1000))
    while True:
        if (stare_curenta.j_curent == Joc.JMIN):
            # muta jucatorul
            # [MOUSEBUTTONDOWN, MOUSEMOTION,....]
            # l=pygame.event.get()


            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    afis_daca_final(stare_curenta, FORCE=True)
                    pygame.quit()  # inchide fereastra
                    sys.exit()
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_u:
                    countUndo += 1
                    mutareaAnterioara = mutariAnterioare.pop()
                    mutareaAnterioara = mutariAnterioare.pop()
                    stare_curenta = copy.deepcopy(mutareaAnterioara[0])
                    SCOR_X = mutareaAnterioara[1]
                    SCOR_0 = mutareaAnterioara[2]
                    print(mutareaAnterioara)
                    stare_curenta.tabla_joc.deseneaza_grid(jucator='JMIN')
                    stare_curenta.j_curent = Joc.jucator_opus(Joc.JMAX)
                    pygame.display.flip()
                elif event.type == pygame.MOUSEBUTTONDOWN:  # click
                    mutariAnterioare.append([copy.deepcopy(stare_curenta), SCOR_X, SCOR_0])
                    pos = pygame.mouse.get_pos()  # coordonatele clickului

                    for linie in range(Joc.NR_LINII):
                        for coloana in range(Joc.NR_COLOANE):

                            if Joc.celuleGrid[linie][coloana].collidepoint(
                                    pos):  # verifica daca punctul cu coord pos se afla in dreptunghi(celula)
                                ###############################
                                if stare_curenta.tabla_joc.matr[linie][coloana] == Joc.JMIN:
                                    if (de_mutat and linie == de_mutat[0] and coloana == de_mutat[1]):
                                        # daca am facut click chiar pe patratica selectata, o deselectez
                                        de_mutat = False
                                        stare_curenta.tabla_joc.deseneaza_grid(jucator='JMAX')
                                    else:
                                        de_mutat = (linie, coloana)
                                        # desenez gridul cu patratelul marcat
                                        stare_curenta.tabla_joc.deseneaza_grid(jucator='JMAX', marcaj=de_mutat)
                                else:
                                    mutat = False

                                    if stare_curenta.tabla_joc.matr[linie][coloana] == Joc.GOL:
                                        if de_mutat:
                                            #### eventuale teste legate de mutarea simbolului
                                            stare_curenta.tabla_joc.matr[de_mutat[0]][de_mutat[1]] = Joc.GOL
                                            de_mutat = False
                                        # plasez simbolul pe "tabla de joc"
                                        stare_curenta.tabla_joc.matr[linie][coloana] = Joc.JMIN
                                        posib_interschimbare = True
                                        mutat = True

                                    elif stare_curenta.tabla_joc.matr[linie][coloana] == Joc.JMAX:
                                        if posib_interschimbare:
                                            if de_mutat and abs(de_mutat[0]-linie) == 1 and de_mutat[1]-coloana <= 1:
                                                print(de_mutat)
                                                print(Joc.JMAX)
                                                stare_curenta.tabla_joc.matr[de_mutat[0]][de_mutat[1]] = Joc.JMAX
                                                de_mutat = False
                                                stare_curenta.tabla_joc.matr[linie][coloana] = Joc.JMIN
                                                mutat = True
                                                posib_interschimbare = False

                                    if mutat:
                                        # afisarea starii jocului in urma mutarii utilizatorului
                                        print("\nTabla dupa mutarea jucatorului")
                                        scorAnteriorX = SCOR_X
                                        scorAnterior0 = SCOR_0
                                        stare_curenta.tabla_joc.cauta_succesiune()
                                        print(str(stare_curenta))
                                        print("SCOR X: " + str(SCOR_X))
                                        print("SCOR 0: " + str(SCOR_0))
                                        stare_curenta.tabla_joc.deseneaza_grid(jucator='JMAX')
                                        # testez daca jocul a ajuns intr-o stare finala
                                        # si afisez un mesaj corespunzator in caz ca da
                                        t_dupa = int(round(time.time() * 1000))
                                        timp = str(t_dupa - t_inainte)
                                        TIMPI_CALCULATOR.append(int(timp))
                                        global NR_MUTARI_P
                                        NR_MUTARI_P += 1
                                        print("Userul a \"gandit\" timp de " + timp + " milisecunde.")
                                        if (afis_daca_final(stare_curenta)):
                                            break

                                        # S-a realizat o mutare. Schimb jucatorul cu cel opus
                                        stare_curenta.j_curent = Joc.jucator_opus(stare_curenta.j_curent)


        # --------------------------------
        else:  # jucatorul e JMAX (calculatorul)
            # Mutare calculator
            waiting = 0
            OKprimulUndo = False
            while waiting != 3 and OKprimulUndo == False:
                time.sleep(1)
                waiting += 1
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()  # inchide fereastra
                        sys.exit()
                    elif event.type == pygame.KEYDOWN and event.key == pygame.K_u:

                        countUndo += 1
                        if countUndo == 1:
                            OKprimulUndo = True
                            mutareaAnterioara = mutariAnterioare.pop()
                            stare_curenta = copy.deepcopy(mutareaAnterioara[0])
                            SCOR_X = mutareaAnterioara[1]
                            SCOR_0 = mutareaAnterioara[2]
                            stare_curenta.tabla_joc.deseneaza_grid(jucator='JMIN')
                            stare_curenta.j_curent = Joc.jucator_opus(Joc.JMAX)
                            pygame.display.flip()
            if not OKprimulUndo:
                mutariAnterioare.append([copy.deepcopy(stare_curenta), SCOR_X, SCOR_0])
                # preiau timpul in milisecunde de dinainte de mutare
                t_inainte = int(round(time.time() * 1000))
                if tip_algoritm == '1':
                    stare_actualizata = min_max(stare_curenta)
                else:  # tip_algoritm==2
                    stare_actualizata = alpha_beta(-500, 500, stare_curenta)
                stare_curenta.tabla_joc = stare_actualizata.stare_aleasa.tabla_joc
                print("Tabla dupa mutarea calculatorului")
                scorAnteriorX = SCOR_X
                scorAnterior0 = SCOR_0
                stare_curenta.tabla_joc.cauta_succesiune()
                print(str(stare_curenta))
                print("SCOR X: " + str(SCOR_X))
                print("SCOR 0: " + str(SCOR_0))
                stare_curenta.tabla_joc.deseneaza_grid(jucator='JMIN')
                # preiau timpul in milisecunde de dupa mutare
                Joc.LISTA_NODURI.append(Joc.NR_NODURI)
                print("CALCULATORUL A GENERAT {} NODURI".format(Joc.NR_NODURI))
                Joc.NR_NODURI = 0
                print("ESTIMARE CALCULATOR - {}".format(stare_actualizata.estimare))
                t_dupa = int(round(time.time() * 1000))
                print("Calculatorul a \"gandit\" timp de " + str(t_dupa - t_inainte) + " milisecunde.")
                t_inainte = int(round(time.time() * 1000))
                global NR_MUTARI_CPU
                NR_MUTARI_CPU += 1
                if (afis_daca_final(stare_curenta)):
                    break

                # S-a realizat o mutare. Schimb jucatorul cu cel opus
                stare_curenta.j_curent = Joc.jucator_opus(stare_curenta.j_curent)




if __name__ == "__main__":
    main()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()





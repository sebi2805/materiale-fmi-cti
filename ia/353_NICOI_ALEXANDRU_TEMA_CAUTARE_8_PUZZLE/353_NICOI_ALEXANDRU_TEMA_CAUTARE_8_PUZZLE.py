import copy
import sys
import time
from math import sqrt
from datetime import datetime as dt


class MatriceFrecventa:

    """
    in aceasta clasa voi pastra frecventa schimbarilor placutelor sub forma unei matrice de frecventa
    precum si statusul de placuta blocata (adica placuta care nu mai suporta interschimbari
    """


    def __init__(self, nume_fisier_restrictie, size):
        """
        :param nume_fisier_restrictie: numele fisierului care contine restrictia de placute (k)
        :param size: marimea matricei
        """
        f2 = open(nume_fisier_restrictie, "r")
        self.k = int(f2.read())
        self.matrice_frecventa = [[0 for i in range(size)] for i in range(size)]
        self.matrice_blocate = [[0 for i in range(size)] for i in range(size)]

    def add_to_matrice_frecventa(self, x, y):
        """
        :param x: linia
        :param y: coloana
        :return: void
        """
        self.matrice_frecventa[x][y] += 1

    def check_lower_from_matrice_frecventa(self, x, y):
        """
        :param x: linia
        :param y: coloana
        :return: conditia ca placuta sa mai suporte interschimbari
        """
        return self.matrice_frecventa[x][y] <= self.k

    def check_equal_from_matrice_frecventa(self,x,y):
        """
        :param x: linia
        :param y: coloana
        :return: daca s-au atins toate placutele
        """
        return self.matrice_frecventa[x][y] == self.k

    def blocheaza_placuta(self,x,y):
        """
        :param x: linia
        :param y: coloana
        :return: void
        """
        self.matrice_blocate[x][y] = 1

    def check_blocat(self,x,y):
        """
        :param x: linia
        :param y: coloana
        :return: daca placuta este blocata
        """
        if self.matrice_blocate[x][y]:
            return True
        return False

    def __str__(self):
        sir = ""
        for linie in self.matrice_blocate:
            sir += " ".join([str(elem) for elem in linie]) + "\n"
        return sir


# informatii despre un nod din arborele de parcurgere (nu din graful initial)
class NodParcurgere:
    def __init__(self, info, parinte, matriceCheckuri, cost=0, h=0):
        self.info = info
        self.parinte = parinte  # parintele din arborele de parcurgere
        self.g = cost  # consider cost=1 pentru o mutare
        self.h = h
        self.f = self.g + self.h
        self.matriceCheckuri = matriceCheckuri



    def obtineDrum(self):
        l = [self];
        nod = self
        while nod.parinte is not None:
            l.insert(0, nod.parinte)
            nod = nod.parinte
        return l

    def afisDrum(self, file, afisCost=False, afisLung=False):  # returneaza si lungimea drumului
        l = self.obtineDrum()
        for nod in l:
            file.write(str(nod))
            file.write("MATRICEA DE PLACUTE BLOCATE (0 - DEBLOCAT, 1 - BLOCAT)\n")
            file.write(str(nod.matriceCheckuri))
            file.write('---------------------------------\n')
        if afisCost:
            file.write("Cost: {}\n".format(self.g))
        if afisLung:
            file.write("Lungime:{}\n".format(len(l)))
        return len(l)

    def contineInDrum(self, infoNodNou):
        nodDrum = self
        while nodDrum is not None:
            if (infoNodNou == nodDrum.info):
                return True
            nodDrum = nodDrum.parinte

        return False

    def __repr__(self):
        sir = ""
        sir += str(self.info)
        return (sir)

    # euristica banală: daca nu e stare scop, returnez 1, altfel 0

    def __str__(self):
        sir = ""
        for linie in self.info:
            sir += " ".join([str(elem) for elem in linie]) + "\n"
        sir += "\n"
        return sir


class Graph:  # graful problemei
    def __init__(self, nume_fisier):
        f = open(nume_fisier, "r")
        sirFisier = f.read()
        try:
            listaLinii = sirFisier.strip().split("\n")
            self.start = []
            for linie in listaLinii:
                self.start.append([int(x) for x in linie.strip().split(" ")])
            print(self.start)
            # verificarea corectitudinii starii de start
            #self.scopuri = [[[1, 2, 3], [4, 5, 6], [7, 8, 0]]]
            #print(self.scopuri)
        except:
            print("Eroare la parsare!")
            sys.exit(0)  # iese din program


    # def testeaza_scop(self, nodCurent):
    #     return nodCurent.info in self.scopuri

    def testeaza_scop_matrice(self, matrice):
        if matrice[len(matrice)-1][len(matrice)-1] != 0:
            return False
        for i in range(len(matrice)):
            for j in range(len(matrice)):
                if matrice[i][j] == 0:
                    continue
                if i-1 >= 0:
                    if matrice[i][j] < matrice[i-1][j]:
                        return False
                if j-1 >= 0:
                    if matrice[i][j] < matrice[i][j-1]:
                        return False
        return True

    # va genera succesorii sub forma de noduri in arborele de parcurgere

    def nuAreSolutii(self, infoNod):
        """
        :param infoNod: matricea
        :return: verificam daca avem mai mult de n elemente distincte, daca nu, oricate interschimbari am face, nu putem realiza taskul
        , deci returnam un boolean
        """
        valoriDistincte = list(set(i for j in infoNod for i in j))
        if len(valoriDistincte) < len(infoNod):
            return True
        return False

    def genereazaSuccesori(self, nodCurent, tip_euristica="euristica banala"):
        listaSuccesori = []
        for lGol in range(len(nodCurent.info)):
            try:
                cGol = nodCurent.info[lGol].index(0)
                break
            except:
                pass
        # stanga, dreapta, sus, jos
        directii = [[lGol, cGol - 1], [lGol, cGol + 1], [lGol - 1, cGol], [lGol + 1, cGol],
                    [lGol-1, cGol-1], [lGol+1, cGol+1], [lGol-1, cGol+1], [lGol+1, cGol-1]]
        for lPlacuta, cPlacuta in directii:
            if 0 <= lPlacuta < 3 and 0 <= cPlacuta < 3:
                copieMatrice = copy.deepcopy(nodCurent.info)
                copieMatriceCheckuri = copy.deepcopy(nodCurent.matriceCheckuri)
                if not copieMatriceCheckuri.check_blocat(lPlacuta, cPlacuta):
                    copieMatrice[lGol][cGol] = copieMatrice[lPlacuta][cPlacuta]
                    copieMatrice[lPlacuta][cPlacuta] = 0
                    if not nodCurent.contineInDrum(copieMatrice):  # and not self.nuAreSolutii(copieMatrice):
                        costArc = 1
                        if (lPlacuta == lGol - 1 and cPlacuta == cGol - 1) or (
                                lPlacuta == lGol - 1 and cPlacuta == cGol - 1) or (
                                lPlacuta == lGol - 1 and cPlacuta == cGol - 1) or (
                                lPlacuta == lGol - 1 and cPlacuta == cGol - 1):
                            costArc = 2
                        copieMatriceCheckuri.add_to_matrice_frecventa(lPlacuta, cPlacuta)
                        if copieMatriceCheckuri.check_equal_from_matrice_frecventa(lPlacuta,cPlacuta):
                           copieMatriceCheckuri.blocheaza_placuta(lPlacuta, cPlacuta)

                        listaSuccesori.append(NodParcurgere(copieMatrice, nodCurent, copieMatriceCheckuri, nodCurent.g + costArc,
                                                            self.calculeaza_h(copieMatrice, tip_euristica)))


        return listaSuccesori

    # euristica banala
    def calculeaza_h(self, infoNod, tip_euristica="euristica banala"):
        if self.testeaza_scop_matrice(infoNod):
            return 0
        if tip_euristica == "euristica banala":
            return 1
        elif tip_euristica == "euristica admisibila 1" or tip_euristica == "euristica admisibila 2":
            h = 0
            for lPlacutaC in range(len(infoNod)):
                for cPlacutaC in range(len(infoNod[0])):
                    if infoNod[lPlacutaC][cPlacutaC] != 0:
                        placuta = infoNod[lPlacutaC][cPlacutaC]
                        placutaSus = -1
                        placutaStanga = -1
                        if lPlacutaC - 1 >= 0:
                            placutaSus = infoNod[lPlacutaC-1][cPlacutaC]
                        if cPlacutaC - 1 >= 0:
                            placutaStanga = infoNod[lPlacutaC][cPlacutaC-1]
                        if placutaSus > placuta or placutaStanga > placuta:
                            h += 1
                    elif lPlacutaC != len(infoNod)-1 or cPlacutaC != len(infoNod)-1:
                        if tip_euristica == "euristica admisibla 1":
                            h += 1
                        else:
                            h += abs(len(infoNod)-1 - lPlacutaC) + abs(len(infoNod)-1 - cPlacutaC)
            return h
        elif tip_euristica == "euristica neadmisibila":
            h = 0
            for lPlacutaC in range(len(infoNod)):
                for cPlacutaC in range(len(infoNod[0])):
                    if infoNod[lPlacutaC][cPlacutaC] != 0:
                        placuta = infoNod[lPlacutaC][cPlacutaC]
                        placutaSus = 0
                        placutaStanga = 0
                        if lPlacutaC - 1 >= 0:
                            placutaSus = infoNod[lPlacutaC-1][cPlacutaC]
                        if cPlacutaC - 1 >= 0:
                            placutaStanga = infoNod[lPlacutaC][cPlacutaC-1]
                        calcul_neadmisibil = sqrt(placutaSus**2 + placutaStanga**2)
                        h += calcul_neadmisibil
            return h

    def __repr__(self):
        sir = ""
        for (k, v) in self.__dict__.items():
            sir += "{} = {}\n".format(k, v)
        return (sir)


def breadth_first(gr, nrSolutiiCautate):
    # in coada vom avea doar noduri de tip NodParcurgere (nodurile din arborele de parcurgere)
    c = [NodParcurgere(gr.start, None, MatriceFrecventa(elementeParsate.inputFolder + "restrictie.txt", len(gr.start)))]
    actual_time = time.time()
    counter = 0
    maxi = 0
    while len(c) > 0:
        if len(c) > maxi:
            maxi = len(c)
        if timeout != 0 and round(1000*(time.time() - actual_time)) >= timeout:
            output.write("S-a depasit timeout-ul!")
            return
        # print("Coada actuala: " + str(c))
        # input()
        nodCurent = c.pop(0)
        if gr.testeaza_scop_matrice(nodCurent.info):
            counter += 1
            output.write("Solutie: {}\n".format(counter))
            nodCurent.afisDrum(output, afisCost=True, afisLung=True)
            output.write("Nr de noduri maxim in memorie: {}\n".format(maxi))
            output.write("TIMP EFECTUAT: {} ms\n".format(str(round(1000 * (time.time() - actual_time)))))
            output.write('=======================================================\n')
            #input()
            nrSolutiiCautate -= 1
            if nrSolutiiCautate == 0:
                return
        lSuccesori = gr.genereazaSuccesori(nodCurent)
        c.extend(lSuccesori)


def uniform_cost(gr, nrSolutiiCautate=1):
    # in coada vom avea doar noduri de tip NodParcurgere (nodurile din arborele de parcurgere)
    c = [NodParcurgere(gr.start, None, MatriceFrecventa(elementeParsate.inputFolder + "restrictie.txt", len(gr.start)), 0, gr.calculeaza_h(gr.start))]
    actual_time = time.time()
    counter = 0
    maxi = 0
    while len(c) > 0:
        if len(c) > maxi:
            maxi = len(c)
        if timeout != 0 and round(1000*(time.time() - actual_time)) >= timeout:
            output.write("S-a depasit timeout-ul!")
            return
        #print("Coada actuala: " + str(c))
        #input()
        nodCurent = c.pop(0)

        if gr.testeaza_scop_matrice(nodCurent.info):
            counter += 1
            output.write("Solutie: {}\n".format(counter))
            nodCurent.afisDrum(output, afisCost=True, afisLung=True)
            output.write("Nr de noduri maxim in memorie: {}\n".format(maxi))
            output.write("TIMP EFECTUAT: {} ms\n".format(str(round(1000 * (time.time() - actual_time)))))
            output.write('=======================================================\n')
            nrSolutiiCautate -= 1
            if nrSolutiiCautate == 0:
                return
        lSuccesori = gr.genereazaSuccesori(nodCurent)
        for s in lSuccesori:
            i = 0
            gasit_loc = False
            for i in range(len(c)):
                # ordonez dupa cost(notat cu g aici și în desenele de pe site)
                if c[i].g > s.g:
                    gasit_loc = True
                    break;
            if gasit_loc:
                c.insert(i, s)
            else:
                c.append(s)

def depth_first(gr, nrSolutiiCautate=1):
    # vom simula o stiva prin relatia de parinte a nodului curent
    actual_time = time.time()

    df(NodParcurgere(gr.start, None, MatriceFrecventa(elementeParsate.inputFolder + "restrictie.txt", len(gr.start)), 0, gr.calculeaza_h(gr.start)), nrSolutiiCautate, actual_time)


def df(nodCurent, nrSolutiiCautate, actual_time):
    if timeout != 0 and round(1000 * (time.time() - actual_time)) >= timeout:
        output.write("S-a depasit timeout-ul!")
        return
    if nrSolutiiCautate <= 0:  # testul acesta s-ar valida doar daca in apelul initial avem df(start,if nrSolutiiCautate=0)
        return nrSolutiiCautate
    #print("Stiva actuala: " + "->".join(nodCurent.obtineDrum()))
    # input()

    if gr.testeaza_scop_matrice(nodCurent.info):
        global counter_depth
        counter_depth += 1
        output.write("Solutie: {}\n".format(counter_depth))
        nodCurent.afisDrum(output, afisCost=True, afisLung=True)
        output.write("TIMP EFECTUAT: {} ms\n".format(str(round(1000 * (time.time() - actual_time)))))
        output.write('=======================================================\n')
        # input()
        nrSolutiiCautate -= 1
        if nrSolutiiCautate == 0:
            return nrSolutiiCautate
    lSuccesori = gr.genereazaSuccesori(nodCurent)
    for sc in lSuccesori:
        if nrSolutiiCautate != 0:
            if timeout != 0 and round(1000 * (time.time() - actual_time)) >= timeout:
                output.write("S-a depasit timeout-ul!")
                return
            print("Se expandeaza -> {}".format(sc.info))
            nrSolutiiCautate = df(sc, nrSolutiiCautate,actual_time)
            print("Se intoarce -> {}".format(sc.info))

    return nrSolutiiCautate


def depth_first_iterativ(gr, nrSolutiiCautate=1):
    actual_time = time.time()

    for i in range(1, (len(gr.start)**2) + 1):
        if timeout != 0 and round(1000*(time.time() - actual_time)) >= timeout:
            output.write("S-a depasit timeout-ul!")
            return
        if nrSolutiiCautate == 0:
            return
        print("**************\nAdancime maxima: ", i)
        nrSolutiiCautate = dfi(NodParcurgere(gr.start, None, MatriceFrecventa(elementeParsate.inputFolder + "restrictie.txt", len(gr.start)), 0, gr.calculeaza_h(gr.start)), i, nrSolutiiCautate,actual_time)



def dfi(nodCurent, adancime, nrSolutiiCautate,actual_time):
    #print("Stiva actuala: " + "->".join(nodCurent.obtineDrum()))
    #input()

    if adancime == 1 and gr.testeaza_scop_matrice(nodCurent.info):
        global counter_depth_it
        counter_depth_it += 1
        output.write("Solutie: {}\n".format(counter_depth_it))
        nodCurent.afisDrum(output, afisCost=True, afisLung=True)
        output.write("TIMP EFECTUAT: {} ms\n".format(str(round(1000 * (time.time() - actual_time)))))
        output.write('=======================================================\n')

        #input()
        nrSolutiiCautate -= 1
        if nrSolutiiCautate == 0:
            return nrSolutiiCautate
    if adancime > 1:
        lSuccesori = gr.genereazaSuccesori(nodCurent)
        for sc in lSuccesori:
            if nrSolutiiCautate != 0:
                nrSolutiiCautate = dfi(sc, adancime - 1, nrSolutiiCautate, actual_time)
    return nrSolutiiCautate

def a_star(gr, nrSolutiiCautate, tip_euristica):
    # in coada vom avea doar noduri de tip NodParcurgere (nodurile din arborele de parcurgere)
    # if gr.nuAreSolutii(gr.start):
    #     print("Nu are solutii!")
    #     return
    c = [NodParcurgere(gr.start, None, MatriceFrecventa(elementeParsate.inputFolder + "restrictie.txt", len(gr.start)), 0, gr.calculeaza_h(gr.start))]
    actual_time = time.time()
    counter = 0
    maxi = 0
    while len(c) > 0:
        if len(c) > maxi:
            maxi = len(c)
        if timeout != 0 and round(1000*(time.time() - actual_time)) >= timeout:
            output.write("S-a depasit timeout-ul!")
            return
        nodCurent = c.pop(0)
        if gr.testeaza_scop_matrice(nodCurent.info):
            counter += 1
            output.write("Solutie: {}\n".format(counter))
            nodCurent.afisDrum(output, afisCost=True, afisLung=True)
            output.write("Nr de noduri maxim in memorie: {}\n".format(maxi))
            output.write("TIMP EFECTUAT: {} ms\n".format(str(round(1000 * (time.time() - actual_time)))))
            output.write('=======================================================\n')
            nrSolutiiCautate -= 1
            if nrSolutiiCautate == 0:
                return
        lSuccesori = gr.genereazaSuccesori(nodCurent, tip_euristica=tip_euristica)
        for s in lSuccesori:
            i = 0
            gasit_loc = False
            for i in range(len(c)):
                # diferenta fata de UCS e ca ordonez dupa f
                if c[i].f >= s.f:
                    gasit_loc = True
                    break;
            if gasit_loc:
                c.insert(i, s)
            else:
                c.append(s)

def greedy(gr, nrSolutiiCautate, tip_euristica):
    # in coada vom avea doar noduri de tip NodParcurgere (nodurile din arborele de parcurgere)
    # if gr.nuAreSolutii(gr.start):
    #     print("Nu are solutii!")
    #     return
    c = [NodParcurgere(gr.start, None, MatriceFrecventa(elementeParsate.inputFolder + "restrictie.txt", len(gr.start)), 0, gr.calculeaza_h(gr.start))]
    actual_time = time.time()
    counter = 0
    maxi = 0
    while len(c) > 0:
        if len(c) > maxi:
            maxi = len(c)
        if timeout != 0 and round(1000*(time.time() - actual_time)) >= timeout:
            output.write("S-a depasit timeout-ul!")
            return
        nodCurent = c.pop(0)
        if gr.testeaza_scop_matrice(nodCurent.info):
            counter += 1
            output.write("Solutie: {}\n".format(counter))
            nodCurent.afisDrum(output, afisCost=True, afisLung=True)
            output.write("Nr de noduri maxim in memorie: {}\n".format(maxi))
            output.write("TIMP EFECTUAT: {} ms\n".format(str(round(1000 * (time.time() - actual_time)))))
            output.write('=======================================================\n')
            nrSolutiiCautate -= 1
            if nrSolutiiCautate == 0:
                return
        lSuccesori = gr.genereazaSuccesori(nodCurent, tip_euristica=tip_euristica)
        for s in lSuccesori:
            i = 0
            gasit_loc = False
            for i in range(len(c)):
                # diferenta fata de a* e ca ordonez dupa h
                if c[i].h >= s.h:
                    gasit_loc = True
                    break;
            if gasit_loc:
                c.insert(i, s)
            else:
                c.append(s)

class ElementeParsate:
    def __init__(self):
        self.inputFolder = sys.argv[1]
        self.outputFolder = sys.argv[2]
        self.nrSolutiiCautate = int(sys.argv[3])
        self.timeout = int(sys.argv[4])

elementeParsate = ElementeParsate()

fisiereDeIntrare = ["input_fara_solutii.txt",
                    "input_initial_care_e_si_final.txt",
                    "input_care_e_decent.txt",
                    "input_cu_crapaciuni_la_timeout.txt"]

fisiereDeIesire = ["output_fara_solutii.txt",
                    "output_initial_care_e_si_final.txt",
                    "output_care_e_decent.txt",
                    "output_cu_crapaciuni_la_timeout.txt"]


for i in range(4):
    gr = Graph(elementeParsate.inputFolder + fisiereDeIntrare[i])
    output = open(elementeParsate.outputFolder + fisiereDeIesire[i], "w")
    timeout = elementeParsate.timeout

    counter_depth = 0
    counter_depth_it = 0

    if gr.nuAreSolutii(gr.start):
        output.write("NU ARE SOLUTIE!")
        continue

    # Rezolvat cu breadth first
    output.write("\n\n##################\nSolutii obtinute cu breadth first:\n")
    breadth_first(gr, nrSolutiiCautate=elementeParsate.nrSolutiiCautate)
    output.write("\n\n##################\nSolutii obtinute cu depth first:\n")
    # print("\nObservatie: stivele sunt afisate pe orizontala, cu baza la stanga si varful la dreapta.")
    depth_first(gr, nrSolutiiCautate=elementeParsate.nrSolutiiCautate)
    output.write("\n\n##################\nSolutii obtinute cu depth first iterativ:\n")
    # print("\nObservatie: stivele sunt afisate pe orizontala, cu baza la stanga si varful la dreapta.")
    depth_first_iterativ(gr, nrSolutiiCautate=elementeParsate.nrSolutiiCautate)
    output.write("\n\n##################\nSolutii obtinute cu UCS:\n")
    # print("\nObservatie: stivele sunt afisate pe orizontala, cu baza la stanga si varful la dreapta.")
    uniform_cost(gr, nrSolutiiCautate=elementeParsate.nrSolutiiCautate)
    output.write("\n\n##################\nSolutii obtinute cu A* euristica banala:\n")
    a_star(gr, nrSolutiiCautate=elementeParsate.nrSolutiiCautate, tip_euristica="euristica banala")
    output.write("\n\n##################\nSolutii obtinute cu A* euristica admisibila 1:\n")
    a_star(gr, nrSolutiiCautate=elementeParsate.nrSolutiiCautate, tip_euristica="euristica admisibila 1")
    output.write("\n\n##################\nSolutii obtinute cu A* euristica admisibila 2:\n")
    a_star(gr, nrSolutiiCautate=elementeParsate.nrSolutiiCautate, tip_euristica="euristica admisibila 2")
    output.write("\n\n##################\nSolutii obtinute cu A* euristica neadmisibila:\n")
    a_star(gr, nrSolutiiCautate=elementeParsate.nrSolutiiCautate, tip_euristica="euristica neadmisibila")
    output.write("\n\n##################\nSolutii obtinute cu Greedy euristica banala:\n")
    greedy(gr, nrSolutiiCautate=elementeParsate.nrSolutiiCautate, tip_euristica="euristica banala")
    output.write("\n\n##################\nSolutii obtinute cu Greedy euristica admisibila 1:\n")
    greedy(gr, nrSolutiiCautate=elementeParsate.nrSolutiiCautate, tip_euristica="euristica admisibila 1")
    output.write("\n\n##################\nSolutii obtinute cu Greedy euristica admisibila 2:\n")
    greedy(gr, nrSolutiiCautate=elementeParsate.nrSolutiiCautate, tip_euristica="euristica admisibila 2")
    output.write("\n\n##################\nSolutii obtinute cu Greedy euristica neadmisibila:\n")
    greedy(gr, nrSolutiiCautate=elementeParsate.nrSolutiiCautate, tip_euristica="euristica neadmisibila")

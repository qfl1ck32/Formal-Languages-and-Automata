from graphviz import Digraph
# Se vor citi datele de intrate din fisier, fiecare pe cate o linie, in ordinea urmatoare:
    # alfabetul
    # starile
    # starea initiala
    # multimea starilor finale
    # automatul (cate trei elemente, reprezentand nodul de plecare, starea prin care trece si nodul in care ajunge, separate la final printr-o virgula)
    # cuvantul

# toate datele in liste.
#   Clasa "Automat" primeste numele fisierului de intrare (cu extensie) formatat dupa modelul de mai sus si retine
#   Metoda verificare() va afisa cuvantul dat si apartenenta acestuia la automat.
#   Metoda deseneaza(culoare_graf, culoare_sol) va primi ca argumente numele a doua culori (in limba engleza)
# folosite pentru a colora muchiile grafului care nu fac parte din solutie (primul argument)
# si muchiile care fac parte din solutie (al doilea argument).
#   Daca nu exista solutii, graful va fi desenat doar folosind culoare_graf.
#   Daca exista solutie, drumul acesteia va fi colorat folosind culoare_sol si, de asemenea, se va afisa
# in paranteza un numar, pe fiecare muchie din solutie,
# indicand ordinea parcurgerii pentru a ajunge la solutie (doar pentru grafurile fara cicluri).
#   A fost folosita o biblioteca pentru realizarea desenurilor grafurilor, si anume "graphviz".


class Automat:

    def __init__(self, nume):
        f = open('%s' % nume, 'r')
        self.alfabet = f.readline().split()
        self.stari = f.readline().split()
        self.stare_initiala = f.readline().strip()
        self.stare_actuala = self.stare_initiala
        self.stari_finale = f.readline().split()
        aux = [x for x in f.readline().split(', ')]
        self.automat = []
        self.solutie = []
        for elem in aux:
            self.automat.append((elem[0], elem[2], elem[4]))
        self.cuvant = f.readline()

    def verificare(self):
        ok = 1
        alfabet_valid = 1
        for litera in self.cuvant:
            if litera not in self.stari:
                print("Cuvantul contine o litera care nu face parte din alfabet.")
                alfabet_valid = 0
                break
        if alfabet_valid:
            if self.cuvant == 'lambda' or self.cuvant == '':
                print("λ apartine automatului.")
            else:
                for caracter in self.cuvant:
                    posibil = [x for x in self.automat if x[0] == self.stare_actuala and x[1] == caracter]
                    if posibil == []:
                        ok = 0
                        break
                    else:
                        self.stare_actuala = posibil[0][2]
                        self.solutie.append(*posibil)
                if self.stare_actuala in self.stari_finale and ok == 1:
                    print("%s apartine automatului." % self.cuvant)
                else:
                    print("%s nu apartine automatului, deoarece nu ne aflam intr-o stare finala.." % self.cuvant)
                    self.solutie = []

    def deseneaza(self, culoare_graf, culoare_sol):
        g = Digraph('G', filename = 'Automat', format = 'png')
        g.attr('node', shape = 'circle')
        g.attr('node', shape = 'doublecircle')
        for nod in self.stari_finale:
            g.node('%s' % nod)
        g.attr('node', shape = 'circle')
        g.node('%s' % self.stare_initiala)
        g.attr('node', shape = 'none')
        g.edge('', '%s' % self.stare_initiala, label = 'Start')
        g.attr('node', shape = 'circle')
        for elem in self.automat:
            if elem in self.solutie:
                g.attr('edge', color = culoare_sol)
                g.edge('%s' % elem[0], '%s' % elem[2], label = '%s' % elem[1])
                g.attr('edge', color = culoare_graf)
            else:
                g.edge('%s' % elem[0], '%s' % elem[2], label='%s' % elem[1])
        g.view()



a = Automat('data.in')
a.verificare()
a.deseneaza('black', 'red')
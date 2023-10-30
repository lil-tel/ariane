import os
from arianetk import *
from time   import *
from copy   import deepcopy
from itertools import product
from depth_first_search import*
from breadth_first_search import *

unité = 60 #taille d'une case
framerate = 10
medias = {'A':'ariane','H':'minoH', 'V':'minoV','P':'porte','T':'thesee'}#medias
direction = { ['Up','Right','Down','Left'][i] : [i,[(0,-1),(1,0),(0,1),(-1,0)][i]] for i in range(4)}

plus = lambda tuple1, tuple2, *args : tuple([ sum([t[i] for t in [tuple1,tuple2]+list(args)]) for i in range(len(tuple1))])
scal = lambda k, tuple1: tuple([k*tuple1[i] for i in range(len(tuple1))])
loc = lambda case, matrix: matrix[case[1]][case[0]]
tup = lambda matrix: tuple([tuple(l) for l in matrix])

class ArianeGUI:
    def __init__(self,chemin,aff=True):
        with open('maps/'+chemin+'.txt') as Map: laby = Map.read().split('\n')
        self.chemin = chemin
        self.n = int(laby.pop(0)) #nombre de cases
        self.affiche = aff
        self.histo = []
        self.touches = []
        self.pos = [[None for i in range(self.n)] for j in range(self.n)]
        self.murs = [[[False]*4 for i in range(self.n)] for j in range(self.n)]
        self.deux = False
        if self.affiche: cree_fenetre(self.n*unité,titre='Ariane:'+chemin)
        for li,x in product(*(range(2*self.n+1),)*2):
            caractere = laby[li][x]
            if caractere == '-':
                if self.affiche: ligne((x-1)*unité//2,li*unité//2,(x+1)*unité//2,li*unité//2)
                try:
                    self.murs[(li-0)//2][(x-1)//2][0] ^= True
                    self.murs[(li-2)//2][(x-1)//2][2] ^= True
                except: pass
            elif caractere == '|': 
                if self.affiche: ligne(x*unité//2,(li-1)*unité//2,x*unité//2,(li+1)*unité//2)
                try:
                    self.murs[(li-1)//2][(x-0)//2][3] ^= True
                    self.murs[(li-1)//2][(x-2)//2][1] ^= True
                except: pass
            elif caractere in medias: self.pos[(li-1)//2][x//2] = medias[caractere]
        self.maj_pos()
        pos1 = deepcopy(self.pos)
        self.histo.append(pos1)
        if self.affiche:
            mise_a_jour()
            self.deux = True
            self.touches=[]
            cree_fenetre(self.n*unité/2,self.n*unité,' ')
            for i in range(2):
                rectangle(i*self.n*unité/4, self.n*unité, (i+1)*self.n*unité/4,(self.n-1)*unité,'',['darkred','gold'][i],f=2)
                texte((i+.5)*self.n*unité/4,(self.n-.5)*unité,['Retour','Indice'][i],ancrage='center',f=2)

    def trouve_pos(self,media,*args):
        lst = []
        if media == "mino": return self.trouve_pos(media+"V",*args) , self.trouve_pos(media+"H",*args)
        for y,x in product(*(range(len(self.pos)),)*2):
            if self.pos[y][x] != None and (media in self.pos[y][x]):
                if args: 
                    try: self.pos[y][x] += args[0]
                    except TypeError:
                        copie = self.pos[y][x][:]
                        self.pos[y][x] = ""
                        for med in medias.values():
                            if med in copie and med not in media: self.pos[y][x] += med
                        if self.pos[y][x] == "": self.pos[y][x] = args[0]
                lst += [(x,y)]
        return lst
    
    def change_pos(self,media,case,retirer=None):
            x,y = case
            if media is None:
                copie = self.pos[y][x][:]
                self.pos[y][x] = ""
                for med in medias.values():
                    if med in copie and (retirer is None or med not in retirer): self.pos[y][x] += med
                if self.pos[y][x] == "": self.pos[y][x] = media
            elif self.pos[y][x] is None: self.pos[y][x] = media
            else: self.pos[y][x] += media            
            
    def maj(self,key):
            if key not in direction:
                if key in {'z','Z'}: self.annule()
                elif key in {'r','R'}: self.new_pos(deepcopy(histo[0]))
                return
            try:
                a = self.trouve_pos("ariane")[0]
                t = self.trouve_pos("thesee")[0]
            except IndexError:
                self.histo.append(deepcopy(self.pos))
                return "Perdu"
            if not loc(a,self.murs)[direction[key][0]]:
                self.touches.append(key)
                self.change_pos(None,a,"ariane")
                a = plus(a,direction[key][1])
                self.change_pos("ariane",a)
                self.maj_pos("ariane")
                t_a = plus(a,scal(-1,t))# a - t = a + -1 * t
                for lst in direction.values():
                    if t_a in lst and not loc(t,self.murs)[lst[0]]:
                        self.change_pos(None,t,"thesee")
                        t = plus(t,t_a)
                        self.change_pos("thesee",t)
                        self.maj_pos("thesee")
                        if a == t == self.trouve_pos("porte")[0]: return "Gagné"
                minosV,minosH = self.trouve_pos("mino")
                for mino in minosV:
                    dis = plus(a,scal(-1,mino))
                    if dis[1]:
                        sens = "Up" if( dis[1] < 0 ) else "Down"
                        x = 1
                    else:
                        sens = "Left" if( dis[0] < 0 ) else "Right"
                        x = 0
                    for i in range(abs(dis[x])):
                        if not loc(mino,self.murs)[direction[sens][0]]:
                            suivant = plus(mino,direction[sens][1])
                            if loc(suivant,self.pos) in ({None}|set(medias.values()))-{"minoV","minoH"}:
                                self.change_pos(None,mino,'minoV')
                                self.change_pos("minoV",suivant)
                                self.maj_pos()
                                mino = suivant
                                if mino == a or mino == t:
                                    self.histo.append(deepcopy(self.pos))
                                    return "Perdu"
                            else: continue
                for mino in minosH:
                    dis = plus(a,scal(-1,mino))
                    if dis[0]:
                        sens = "Left" if( dis[0] < 0 ) else "Right"
                        x = 0
                    else:
                        sens = "Up" if( dis[1] < 0 ) else "Down"
                        x = 1
                    for i in range(abs(dis[x])):
                        if not loc(mino,self.murs)[direction[sens][0]]:
                            suivant = plus(mino,direction[sens][1])
                            if loc(suivant,self.pos) in ({None}|set(medias.values()))-{"minoV","minoH"}:
                                self.change_pos(None,mino,'minoH')
                                self.change_pos("minoH",suivant)
                                self.maj_pos()
                                mino = suivant
                                if mino == a or mino == t:
                                    self.histo.append(deepcopy(self.pos))
                                    return "Perdu"
                            else: continue
                    self.histo.append(deepcopy(self.pos))
                    minos = minosV + minosH
                    if a in minos or t in minos: return "Perdu"
            else: return "mur"
            if self.affiche:
                efface('Indice')
                mise_a_jour()

    def maj_pos(self,m=None):
        if self.affiche:
            m = [m] if (m != None) else medias.values()
            for media in m: efface(media)
            [[image((i+.5)*unité,(j+.5)*unité,"media/"+x+".png",tag = x) for x in m if x in self.pos[j][i]] for j,i in product(*(range(len(self.pos)),)*2) if self.pos[j][i] != None]

    def maj_fenetre(self,ev=None):
        recents,selec = self.touches[1-self.n:],False
        x,y = (clic_x(ev),clic_y(ev)) if (ev is not None ) else (-1,-1)
        efface_tout(2)
        for i in range(len(recents)):
            if  0 <= x <= self.n*unité/2 and i*unité <= y <= (i+1)*unité: selec = True
            rectangle(-1,i*unité,self.n*unité/2,(i+1)*unité,'black','snow'if(not selec) else 'grey',.5,'recents',2)
            texte(self.n*unité/4,(i+.5)*unité,recents[i],ancrage='center',f=2,tag='recents')
        selec = [0,0]
        for i in range(2):
            selec[i] = i*self.n*unité/4 <= x <= (i+1)*self.n*unité/4 and (self.n-1)*unité <= y <= self.n*unité
            rectangle(i*self.n*unité/4, self.n*unité, (i+1)*self.n*unité/4,(self.n-1)*unité,'',(['darkred','gold'] if (not selec[i]) else ['red','yellow'])[i],f=2)
            texte((i+.5)*self.n*unité/4,(self.n-.5)*unité,['Annuler','Indice'][i],ancrage='center',f=2)
        if ev is not None and type_evenement(ev) == 'ClicGauche' and 0 <= x <= self.n*unité/2 and 0 <= y <= (self.n-1)*unité:
            for i in range(len(recents)-y//unité): self.annule()
            self.maj_fenetre()
        if ev is not None and type_evenement(ev) == 'ClicGauche' and selec[0]: self.annule()
        if ev is not None and type_evenement(ev) == 'ClicGauche' and selec[1]:
            indice = depth_fs(self.chemin,affiche=False,pos=self.pos)
            texte(0,0,(indice.chemin)[0],tag = 'Indice')

    def annule(self):
        if self.histo[1:]:
            self.histo.pop()
            self.pos = deepcopy(self.histo[-1])
            self.maj_pos()
            self.touches.pop()

    def new_pos(self,new):
        self.pos, i = new, 0
        self.histo.append(deepcopy(self.pos))
        self.maj_pos()
        for y,x in product(*(range(self.n),)*2):
            m = self.pos[y][x]
            if i==2: return
            elif m is None: continue
            elif 'ariane' in m:
                if 'thesee' in m and 'porte' in m: return 'Gagné'
                elif 'mino' in m: return 'Perdu'
                i+=1
            elif 'thesee' in m:
                if 'mino' in m: return 'Perdu'
                i+=1
        return 'Perdu'
    
    def loop(self):
        while True:
            ev = donne_evenement()
            ty = type_evenement(ev)
            if ty == 'Quitte':
                while True:
                    ret = self.fin_de_partie()
                    if ret == 'annule': break
                    elif ret in {'restart','escape','quit'}: return ret
            elif ty == 'Touche':
                maj = self.maj(touche(ev))
                if maj in {'Perdu','Gagné'}:
                    texte(0,0, "VOUS AVEZ "+maj,'red' if(maj == 'Perdu') else 'green','nw',tag = 'message')
                    while True:
                        ret = self.fin_de_partie()
                        if ret == 'annule': break
                        elif ret in {'restart','escape','quit'}:
                            efface('message')
                            return ret
                if touche(ev) == 'Escape':
                    while True:
                        ret = self.fin_de_partie()
                        if ret == 'annule': break
                        elif ret in {'restart','escape','quit'}: return ret
                        elif ret == 'play':
                            efface('fin_partie')
                            break
            if self.deux:
                ev2 = donne_evenement(2)
                ty2 = type_evenement(ev2)
                if ty2 == 'Touche': self.maj(touche(ev2))
                elif ty2 in {"ClicDroit", "ClicGauche", "Deplacement"}:
                    self.maj_fenetre(ev2)
                elif ty2 == 'RAS':
                    self.maj_fenetre()
                elif ty2 == 'Quitte':
                    ferme_fenetre(2)
                    self.deux = False
            mise_a_jour()
            sleep(1/framerate)

    def fin_de_partie(self):
        for i in range(3):
            rectangle(self.n*unité*.25, self.n*unité*(2*i+1)/7 , self.n*unité*.75, self.n*unité*2*(i+1)/7, remplissage = ('turquoise',"cyan",'red')[i],tag='fin_partie')
            texte(self.n*unité/2,self.n*unité*(2*i+1.5)/7,('réessayer','menu principal','quitter')[i], ancrage = 'center',tag='fin_partie')
        ev = donne_evenement()
        ty = type_evenement(ev)
        if ty == 'Quitte': return 'quit'
        elif ty in {"ClicDroit", "ClicGauche", "Deplacement"}:
            x,y = clic_x(ev),clic_y(ev)
            if self.n*unité*.25<=x<=self.n*unité*.75:
                i = -1
                if self.n*unité/7<=y<=self.n*unité*2/7: i = 0
                elif 3*self.n*unité/7<=y<=4*self.n*unité/7: i = 1
                elif 5*self.n*unité/7<=y<=6*self.n*unité/7: i = 2
                if i+1:
                    rectangle(self.n*unité*.25, self.n*unité*(2*i+1)/7 , self.n*unité*.75, self.n*unité*2*(i+1)/7, remplissage = ('mediumturquoise',"lightcyan",'darkred')[i],tag='fin_partie')
                    texte(self.n*unité/2,self.n*unité*(2*i+1.5)/7,('réessayer','menu principal','quitter')[i], ancrage = 'center',tag='fin_partie')
        elif ty == 'Touche':
            key = touche(ev)
            if key in {'z','Z'}:
                efface('fin_partie')
                efface('message')
                self.annule()
                return 'annule'
            elif key in {'r','R'}:
                self.new_pos(deepcopy(histo[0]))
                return 'escape'
            elif key == 'Escape':
                return 'play'
        if ty == 'ClicGauche':
            if self.n*unité*.25<=x<=self.n*unité*.75:
                if self.n*unité/7<=y<=self.n*unité*2/7:
                    ferme_fenetre(2)
                    efface_tout()
                    return 'restart' # le même jeu
                elif 3*self.n*unité/7<=y<=4*self.n*unité/7:
                    efface_tout()
                    return 'escape'
                elif 5*self.n*unité/7<=y<=6*self.n*unité/7: return 'quit'# TO DO par rapport à ton code
        mise_a_jour()
        sleep(1/framerate)
        efface('fin_partie')

class ArianeMenu:
    def __init__(self):
        #Creation de la fenetre et des cadres dans la fenetre
        cree_fenetre(1000,titre=' ')
        self.choix = self.menu_principal()
        self.loop((self.choix)[0])

    def loop(self,typ):
        ferme_fenetre()
        if self.choix == 'quit': return
        self.ari = ArianeGUI(self.choix[1][:-4]) if (typ == 'j') else depth_fs(self.choix[1][:-4])
        fin = self.ari.loop()
        if fin == 'restart': self.loop(typ)
        else:
            ferme_fenetre()
            if fin == 'escape': self.__init__()

    def repertoire(self,j):  # l'argument permet de savoir si c pour jouer ou rechercher une solution
        efface_tout()
        rectangle(10, 10, 200, 50, remplissage = "yellow")
        texte(110,30, "labyrinthe1", ancrage="center")
        rectangle(10, 60, 200, 100, remplissage = "yellow")
        texte(110,80, "labyrinthe2",  ancrage="center")
        rectangle(10, 110, 200, 150, remplissage = "yellow")
        texte(110,130, "labyrinthe3", ancrage="center")
        rectangle(10, 160, 200, 200, remplissage = "yellow")
        texte(110,180, "labyrinthe4", ancrage="center")
        rectangle(10, 210, 200, 250, remplissage = "yellow")
        texte(110,230, "labyrinthe5", ancrage="center")
        rectangle(10, 260, 200, 300, remplissage = "yellow")
        texte(110,280, "sandbox", ancrage="center")
        rectangle(10, 310, 200, 350, remplissage = "yellow")
        texte(110,330, "big1", ancrage="center")
        rectangle(10, 360, 200, 400, remplissage = "yellow")
        texte(110,380, "big2", ancrage="center")
        rectangle(260, 10, 450, 50, remplissage = "yellow")
        texte(360,30, "small1", ancrage="center")
        rectangle(260, 60, 450, 100, remplissage = "yellow")
        texte(360,80, "small2", ancrage="center")
        rectangle(260, 110, 450, 150, remplissage = "yellow")
        texte(360,130, "small3", ancrage="center")
        rectangle(260, 160, 450, 200, remplissage = "yellow")
        texte(360,180, "small4",  ancrage="center")
        rectangle(260, 210, 450, 250, remplissage = "yellow")
        texte(360,230, "defi0", ancrage="center")
        rectangle(260, 260, 450, 300, remplissage = "yellow")
        texte(360,280, "defi1", ancrage="center")
        rectangle(260, 310, 450, 350, remplissage = "yellow")
        texte(360,330, "defi2", ancrage="center")
        rectangle(260, 360, 450, 400, remplissage = "yellow")
        texte(360,380, "defi3", ancrage="center")
        rectangle(500, 10, 700, 80, remplissage = "#00ffff")
        texte(600,45, "menu pricipal", couleur = 'black', ancrage="center")
        return self.choix_jeu(j)

    def choix_jeu(self,j):
        x,y,z=attente_clic()
        if 10<=x<=200:
                if 10<=y<=50: return j, "labyrinthe1.txt"
                if 60<=y<=100: return j,"labyrinthe2.txt"
                if 110<=y<=150: return j,"labyrinthe3.txt"
                if 160<=y<=200: return j,"labyrinthe4.txt"
                if 210<=y<=250: return j,"labyrinthe5.txt"
                if 260<=y<=300: return j,"sandbox.txt"
                if 310<=y<=350: return j,"big/big1.txt"
                if 360<=y<=400: return j,"big/big2.txt"
        elif 260<=x<=450:
                if 10<=y<=50: return j,"small/small1.txt"
                if 60<=y<=100: return j,"small/small2.txt"
                if 110<=y<=150: return j,"small/small3.txt"
                if 160<=y<=200: return j,"small/small4.txt"
                if 210<=y<=250: return j,"defi/defi0.txt"
                if 260<=y<=300: return j,"defi/defi1.txt"
                if 310<=y<=350: return j,"defi/defi2.txt"
                if 360<=y<=400: return j,"defi/defi3.txt"
        elif 500<=x<=700 and 10<=y<=80: return self.menu_principal()
        return self.choix_jeu(j) # si le clic n'est pas bon

    def menu_principal(self):
        efface_tout()
        rectangle(300, 100, 600, 200, remplissage = "#00ff88")
        texte(450,150, "jouer", couleur = 'black', ancrage="center")
        rectangle(300, 300, 600,400, remplissage = "#00ff88")
        texte(450,350, "solver", couleur = 'black', ancrage="center")
        rectangle(300, 500, 600, 600, remplissage = "#00ff88")
        texte(450,550, "quitter", couleur = 'black', ancrage="center")
        x,y,z=attente_clic()
        if 300<=x<=600:
            if 100<=y<=200:
                ret = self.repertoire("j") # jouer
                return ret
            if 300<=y<=400:
                ret = self.repertoire("s") # solver
                return ret
            if 500<=y<=600:
                return 'quit'
            efface_tout()

def all_txt(chemin = 'maps'):
    lst1 = []
    return [lst1.append(x) if (x[-3:]=='txt') else lst1.extend(all_txt(chemin+'/'+x)) for x in os.listdir(chemin)] and lst1

if __name__=='__main__':
    menu = ArianeMenu()

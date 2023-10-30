from upemtk import *
from time   import *
from copy   import deepcopy
from projet_sem2 import *
from itertools import product
from depth_first_search import*
from breadth_first_search import *

unité = 60 #taille d'une case
medias = {'A':'ariane','H':'minoH', 'V':'minoV','P':'porte','T':'thesee'}#medias
direction = { ['Up','Right','Down','Left'][i] : [i,[(0,-1),(1,0),(0,1),(-1,0)][i]] for i in range(4)}

plus = lambda tuple1, tuple2, *args : tuple([ sum([t[i] for t in [tuple1,tuple2]+list(args)]) for i in range(len(tuple1))])
scal = lambda k, tuple1: tuple([k*tuple1[i] for i in range(len(tuple1))])
loc = lambda case, matrix: matrix[case[1]][case[0]]
tup = lambda matrix: tuple([tuple(l) for l in matrix])
posit = lambda: pos
histor = lambda: histo
deu = lambda: deux

def trouve_pos(media,*args):
        global pos
        lst = []
        if media == "mino": return trouve_pos(media+"V",*args) , trouve_pos(media+"H",*args)
        for y,x in product(*(range(len(pos)),)*2):
                if pos[y][x] != None and (media in pos[y][x]):
                        if args: 
                                try: pos[y][x] += args[0]
                                except TypeError:
                                        copie = pos[y][x][:]
                                        pos[y][x] = ""
                                        for med in medias.values():
                                                if med in copie and med not in media: pos[y][x] += med
                                        if pos[y][x] == "": pos[y][x] = args[0]
                        lst += [(x,y)]
        return lst
                
def change_pos(media,case,retirer=None):
        global pos
        x,y = case
        if media is None:
                copie = pos[y][x][:]
                pos[y][x] = ""
                for med in medias.values():
                        if med in copie and (retirer is None or med not in retirer): pos[y][x] += med
                if pos[y][x] == "": pos[y][x] = media
        elif pos[y][x] is None: pos[y][x] = media
        else: pos[y][x] += media

def init_pos(chemin,aff=True):
        global affiche,histo,n,pos,murs,touches
        with open('maps/'+chemin+'.txt') as Map: laby = Map.read().split('\n')
        n = int(laby.pop(0)) #nombre de cases
        affiche,histo,touches,pos,murs = aff,[],[],[[None for i in range(n)] for j in range(n)], [[[False]*4 for i in range(n)] for j in range(n)]
        if affiche: cree_fenetre(n*unité,titre='Ariane:'+chemin)
        for li,x in product(*(range(2*n+1),)*2):
                caractere = laby[li][x]
                if caractere == '-':
                        if affiche: ligne((x-1)*unité//2,li*unité//2,(x+1)*unité//2,li*unité//2)
                        try:
                                murs[(li-0)//2][(x-1)//2][0] ^= True
                                murs[(li-2)//2][(x-1)//2][2] ^= True
                        except: pass
                elif caractere == '|': 
                        if affiche: ligne(x*unité//2,(li-1)*unité//2,x*unité//2,(li+1)*unité//2)
                        try:
                                murs[(li-1)//2][(x-0)//2][3] ^= True
                                murs[(li-1)//2][(x-2)//2][1] ^= True
                        except: pass
                elif caractere in medias: pos[(li-1)//2][x//2] = medias[caractere]
        maj_pos()
        pos1 = deepcopy(pos)
        histo.append(pos1)
        if affiche: mise_a_jour()
        return pos

def init_fenetre():
        if affiche:
                global deux,touches
                deux = True
                cree_fenetre(n*unité/2,n*unité,' ')
                for i in range(2):
                        rectangle(i*n*unité/4, n*unité, (i+1)*n*unité/4,(n-1)*unité,'',['darkred','gold'][i],f=2)
                        texte((i+.5)*n*unité/4,(n-.5)*unité,['Retour','Indice'][i],ancrage='center',f=2)                
	
def maj(key):
        global histo,pos,murs,touches
        if key not in direction:
                if key in {'h','H'}: print(histo)
                elif key in {'z','Z'}: annule()
                elif key in {'n','N'}: new_pos(deepcopy(histo[0]))
                return
        touches.append(key)
        maj_fenetre()
        try:
                a = trouve_pos("ariane")[0]
                t = trouve_pos("thesee")[0]
        except IndexError:
                histo.append(deepcopy(pos))
                return "Perdu"
        if not loc(a,murs)[direction[key][0]]:
                change_pos(None,a,"ariane")
                a = plus(a,direction[key][1])
                change_pos("ariane",a)
                maj_pos("ariane")
                t_a = plus(a,scal(-1,t))# a - t = a + -1 * t
                for lst in direction.values():
                        if t_a in lst and not loc(t,murs)[lst[0]]:
                                change_pos(None,t,"thesee")
                                t = plus(t,t_a)
                                change_pos("thesee",t)
                                maj_pos("thesee")
                                if a == t == trouve_pos("porte")[0]:
                                        print("Jeu Terminé")
                                        return "Gagné"
                minosV,minosH = trouve_pos("mino")
                for mino in minosV:
                        dis = plus(a,scal(-1,mino))
                        if dis[1]:
                                sens = "Up" if( dis[1] < 0 ) else "Down"
                                for i in range(abs(dis[1])):
                                        if not loc(mino,murs)[direction[sens][0]]:
                                                suivant = plus(mino,direction[sens][1])
                                                if loc(suivant,pos) in ({None}|set(medias.values()))-{"minoV","minoH"} or "mino" not in loc(suivant,pos):
                                                        pos[mino[1]][mino[0]] = None
                                                        pos[suivant[1]][suivant[0]] = "minoV"
                                                        maj_pos()
                                                        mino = suivant
                                                        if mino == a or mino == t:
                                                                histo.append(deepcopy(pos))
                                                                return "Perdu"
                                                else: continue
                        else:
                                sens = "Left" if( dis[0] < 0 ) else "Right"
                                for i in range(abs(dis[0])):
                                        if not murs[mino[1]][mino[0]][direction[sens][0]]:
                                                suivant = plus(mino,direction[sens][1])
                                                if pos[suivant[1]][suivant[0]] in ({None}|set(medias.values()))-{"minoV","minoH"} or "mino" not in pos[suivant[1]][suivant[0]]:
                                                        pos[mino[1]][mino[0]] = None
                                                        pos[suivant[1]][suivant[0]] = "minoV"
                                                        maj_pos()
                                                        mino = suivant
                                                        if mino == a or mino == t:
                                                                histo.append(deepcopy(pos))
                                                                return "Perdu"
                                                else: continue
                for mino in minosH:
                        dis = plus(a,scal(-1,mino))
                        if dis[0]:
                                sens = "Left" if( dis[0] < 0 ) else "Right"
                                for i in range(abs(dis[0])):
                                        if not murs[mino[1]][mino[0]][direction[sens][0]]:
                                                suivant = plus(mino,direction[sens][1])
                                                if pos[suivant[1]][suivant[0]] in ({None}|set(medias.values()))-{"minoV","minoH"} or "mino" not in pos[suivant[1]][suivant[0]]:
                                                        pos[mino[1]][mino[0]] = None
                                                        pos[suivant[1]][suivant[0]] = "minoH"
                                                        maj_pos()
                                                        mino = suivant
                                                        if mino == a or mino == t:
                                                                histo.append(deepcopy(pos))
                                                                return "Perdu"
                                                else: continue
                        else:
                                sens = "Up" if( dis[1] < 0 ) else "Down"
                                for i in range(abs(dis[1])):
                                        if not murs[mino[1]][mino[0]][direction[sens][0]]:
                                                suivant = plus(mino,direction[sens][1])
                                                if pos[suivant[1]][suivant[0]] in ({None}|set(medias.values()))-{"minoV","minoH"} or "mino" not in pos[suivant[1]][suivant[0]]:
                                                        pos[mino[1]][mino[0]] = None
                                                        pos[suivant[1]][suivant[0]] = "minoH"
                                                        maj_pos()
                                                        mino = suivant
                                                        if mino == a or mino == t:
                                                                histo.append(deepcopy(pos))
                                                                return "Perdu"
                                                else: continue
                histo.append(deepcopy(pos))
                minos = minosV + minosH
                if a in minos or t in minos: return "Perdu"
        else: return "mur"
        if affiche: mise_a_jour()

def maj_pos(m=None):
        global pos
        if affiche:
                m = [m] if (m != None) else medias.values()
                for media in m: efface(media)
                [[image((i+.5)*unité,(j+.5)*unité,"media/"+x+".png",tag = x) for x in m if x in pos[j][i]] for j,i in product(*(range(len(pos)),)*2) if pos[j][i] != None]

def maj_fenetre():
        global touches
        recents = touches[-9:]
        efface('recents',2)
        for i in range(len(recents)):
                rectangle(0,i*n*unité,i*n*unité/2,(i+1)*n*unité,'black','snow',.5,'recents',2)
                texte(n*unité/4,(i+.5)*unité,recents[i],ancrage='center',f=2,tag='recents')
def annule():
        global histo, pos
        if histo[1:]:
                histo.pop()
                pos = deepcopy(histo[-1])
                maj_pos()

def in_the_path(chemin,lst):
        init_pos(chemin)
        [sleep(1/4) or maj(touche) for touche in lst]
        ferme_fenetre(1)

def new_pos(new):
        global pos,histo
        pos, i = new, 0
        histo.append(deepcopy(pos))
        maj_pos()
        for l in pos:
                for m in l:
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


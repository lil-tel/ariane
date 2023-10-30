from upemtk import*
from time import sleep

def niveau(fichier): 
    texte = open(fichier, "r")
    t=texte.read()
    ligne=t.split("\n")[:-1]
    taille=int(ligne.pop(0))*2+1
    laby=[list(elem) for elem in ligne]
    return laby,taille

def plateau(plan):
    laby,taille=plan 
    for j in range(0,taille) : 
        for i in range(0,taille):
            if laby[j][i]=="-":              # murs horizontaux
                ligne((i-1)*40,j*40,(i+1)*40,j*40)
            elif laby[j][i]=="|":                 # murs verticaux
                ligne(i*40,(j-1)*40,i*40,(j+1)*40) 




def perso_initial(plan):
    laby,taille=plan 
    persos={}
    for j in range(1,taille,2) : 
        for i in range(1,taille,2):
            if laby[j][i]=="A":
                persos["ariane"]=(i,j)
            elif laby[j][i]=="T":
                persos["thesee"]=(i,j)
            elif laby[j][i]=="V":
                persos["minoV"]=(i,j)
            elif laby[j][i]=="H":
                persos["minoH"]=(i,j)
            elif laby[j][i]=="P":                 # porte
                persos["porte"]=(i,j)
    return persos


def affiche_perso(persos):
    for elem in persos:
        image(40*persos[elem][0],40*persos[elem][1],"media/"+str(elem)+".png","center")

def cases_jouable(plan,perso):
    laby,taille=plan 
    jouable=[]
    x,y=perso
    for i,j in [(x,y-1),(x,y+1),(x+1,y),(x-1,y)]:
        if laby[j][i] not in ["-","|"]:
            jouable.append((i,j))
    return jouable


def deplacement_ariane(ariane,touche,jeu):

    if touche == 'Up':
        sens= (0,-1)
    elif touche == 'Down':
        sens=(0,1)
    elif touche == 'Right':
        sens=(1,0)
    else:
        sens=(-1,0)

    if (sens[0]+ariane[0],sens[1]+ariane[1]) in cases_jouable(jeu,ariane) :
        x,y=2*sens[0]+ariane[0],2*sens[1]+ariane[1]
        if jeu[0][y][x] not in ["H","V"]:
            return (x,y)
    return ariane

   
#def deplacemet_minoH(ariane,mino,jeu):
#    a,b=min(
if __name__ == "__main__":
    # initialisation du jeu
    framerate = 10   # taux de rafraîchissement du jeu en images/s
    plans={'n':["labyrinthe1.txt","labyrinthe2.txt","labyrinthe3.txt","labyrinthe4.txt","labyrinthe5.txt",
            "sandbox.txt"]}
    jeu=niveau("maps/labyrinthe1.txt")
    cree_fenetre(1200,1200)
    #mur(niveau("maps/"+choice(plans['n'])))
    plateau(jeu)
    joueurs=perso_initial(jeu)
    affiche_perso(joueurs)




#=============MOTEUR DU JEU=============#
    while True:
        # gestion des événements
        ev = donne_evenement()

        if type_evenement(ev) =='Touche':
            xa,ya=joueurs["ariane"]
            x,y=deplacement_ariane(joueurs["ariane"],touche(ev),jeu)                 #deplacement ariane
            if (x,y)!= joueurs["ariane"]:
                jeu[0][y][x],jeu[0][ya][xa]=jeu[0][ya][xa],jeu[0][y][x]
                joueurs["ariane"]=(x,y)
                if set(cases_jouable(jeu,joueurs["ariane"])).intersection(cases_jouable(jeu,joueurs["thesee"])):
                    joueurs["thesee"]=joueurs["ariane"]
                if joueurs["ariane"]==joueurs["thesee"]==joueurs["porte"]:
                    fin="gagné"
                    break
                #if joueurs["minoH"][1] in [joueurs["ariane"][1],joueurs["thesee"][1]]:
                    
        efface_tout()
        plateau(jeu)
        affiche_perso(joueurs)
        mise_a_jour()
        sleep(1/framerate)
    #affiche_fin(fin)
    #sleep(3)
    ferme_fenetre()

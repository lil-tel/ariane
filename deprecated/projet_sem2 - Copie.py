from upemtk import*
from time import sleep
from fun import*

if __name__ == "__main__":
    # initialisation du jeu
    plans={'n':["labyrinthe1.txt","labyrinthe2.txt","labyrinthe3.txt","labyrinthe4.txt","labyrinthe5.txt",
            "sandbox.txt"]}
    jeu=niveau("maps/labyrinthe1.txt")
    cree_fenetre(900,900)
    #mur(niveau("maps/"+choice(plans['n'])))
    plateau(jeu)
    joueurs=perso_initial(jeu)
    affiche_perso(joueurs)
    fin=" "



#=============MOTEUR DU JEU=============#
    while True:
        # gestion des événements
        ev = donne_evenement()

        if type_evenement(ev) =='Touche':
            xa,ya=joueurs["ariane"]
            x,y=deplacement_ariane(joueurs["ariane"],touche(ev),jeu[0])                 #deplacement ariane
            if (x,y)!= joueurs["ariane"]:
                jeu[0][y][x],jeu[0][ya][xa]=jeu[0][ya][xa],jeu[0][y][x]
                joueurs["ariane"]=(x,y)
                if set(cases_jouable(jeu[0],joueurs["ariane"])).intersection(cases_jouable(jeu[0],joueurs["thesee"])):
                    joueurs["thesee"]=joueurs["ariane"]
                if joueurs["ariane"]==joueurs["thesee"]==joueurs["porte"]:
                    fin=["GAGNÉ","green"]
                xv,yv=joueurs["minoV"]
                x,y=deplacemet_minoV(joueurs["ariane"],joueurs["thesee"],joueurs["minoV"],jeu[0])
                joueurs["minoV"]=(x,y)
                jeu[0][yv][xv]=" "
                jeu[0][y][x]="V"
                if joueurs["minoV"] in [joueurs["thesee"],joueurs["ariane"]]:
                    fin= ["PERDU","red"]
                xh,yh=joueurs["minoH"]
                x,y=deplacemet_minoH(joueurs["ariane"],joueurs["thesee"],joueurs["minoH"],jeu[0])
                joueurs["minoH"]=(x,y)
                jeu[0][yh][xh]=" "
                jeu[0][y][x]="H"
                if joueurs["minoH"] in [joueurs["thesee"],joueurs["ariane"]]:
                    fin=["PERDU","red"]

        efface_tout()
        plateau(jeu)
        affiche_perso(joueurs)
        mise_a_jour()
        if fin !=" ":
            break
    texte(400,400, "VOUS AVEZ "+fin[0],fin[1],'center')
    attente_clic()
    ferme_fenetre()

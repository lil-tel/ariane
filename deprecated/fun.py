from upemtk import*

def menu():
    #Creation de la fenetre et des cadres dans la fenetre
    cree_fenetre(900, 900)
    #Creation des boutons
    rectangle(10, 10, 200, 50, remplissage = "yellow")
    texte(110,30, "labyrinthe1", couleur = 'black', ancrage="center")
    rectangle(10, 60, 200, 100, remplissage = "yellow")
    texte(110,80, "labyrinthe2", couleur = 'black', ancrage="center")
    rectangle(10, 110, 200, 160, remplissage = "yellow")
    texte(110,130, "labyrinthe3", couleur = 'black', ancrage="center")
    rectangle(10, 160, 200, 200, remplissage = "yellow")
    texte(110,180, "labyrinthe4", couleur = 'black', ancrage="center")
    rectangle(10, 210, 200, 250, remplissage = "yellow")
    texte(110,230, "labyrinthe5", couleur = 'black', ancrage="center")
    rectangle(10, 260, 200, 300, remplissage = "yellow")
    texte(110,280, "sandbox", couleur = 'black', ancrage="center")
    rectangle(10, 310, 200, 350, remplissage = "yellow")
    texte(110,330, "small1", couleur = 'black', ancrage="center")
    rectangle(10, 360, 200, 400, remplissage = "yellow")
    texte(110,380, "small2", couleur = 'black', ancrage="center")
    rectangle(10, 410, 200, 450, remplissage = "yellow")
    texte(110,430, "small2", couleur = 'black', ancrage="center")
    rectangle(10, 460, 200, 500, remplissage = "yellow")
    texte(110,480, "small3", couleur = 'black', ancrage="center")
    rectangle(10, 460, 200, 500, remplissage = "yellow")
    texte(110,480, "small4", couleur = 'black', ancrage="center")
    rectangle(10, 460, 200, 500, remplissage = "yellow")
    texte(110,480, "big1", couleur = 'black', ancrage="center")
    rectangle(10, 460, 200, 500, remplissage = "yellow")
    texte(110,480, "big2", couleur = 'black', ancrage="center")
    rectangle(10, 460, 200, 500, remplissage = "yellow")
    texte(110,480, "defi0", couleur = 'black', ancrage="center")
menu()
attente_clic()

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
    image(40*persos["porte"][0],40*persos["porte"][1],"media/porte.png","center")
    image(40*persos["ariane"][0],40*persos["ariane"][1],"media/ariane.png","center")
    image(40*persos["thesee"][0],40*persos["thesee"][1],"media/thesee.png","center")
    for elem in ["minoH","minoV"]:
        image(40*persos[elem][0],40*persos[elem][1],"media/"+str(elem)+".png","center")
def cases_jouable(plan,perso):
    jouable=[]
    x,y=perso
    for i,j in [(x,y-1),(x,y+1),(x+1,y),(x-1,y)]:
        if plan[j][i] not in ["-","|"]:
            jouable.append((i,j))
    return jouable


def deplacement_ariane(ariane,touche,plan):

    if touche == 'Up':
        sens= (0,-1)
    elif touche == 'Down':
        sens=(0,1)
    elif touche == 'Right':
        sens=(1,0)
    else:
        sens=(-1,0)

    if (sens[0]+ariane[0],sens[1]+ariane[1]) in cases_jouable(plan,ariane) :
        x,y=2*sens[0]+ariane[0],2*sens[1]+ariane[1]
        if plan[y][x] not in ["H","V"]:
            return (x,y)
    return ariane


    

def deplacemet_minoH(ariane,thesee,mino,plan):
    xm,ym=mino
    xa,ya=ariane
    xt,yt=thesee

    if ym==yt:
        b=True
        for i in range(min(xm,xt)+1,max(xm,xt)+1,2):
            b=b and plan[ym][i]!="|" and plan[ym][i+1]!="V"
        if b:
            return (xt,yt)
    if xm==xt:
        b=True
        for i in range(min(ym,yt)+1,max(ym,yt)+1,2):
            b=b and plan[i][xm]!="-" and plan[i+1][xm]!="V"
        if b:
            return (xt,yt)
    if xm< xa:
        while plan[ym][xm+1]!="|" and xm!= xa and plan[ym][xm+2]!="V":
            xm+=2
        return (xm,ym)
    if xm>xa:
        while plan[ym][xm-1]!="|"and xm!= xa and plan[ym][xm-2]!="V":
            xm-=2
        return (xm,ym)
    if ym< ya:
        while plan[ym+1][xm]!="-"and ym!= ya and plan[ym+2][xm]!="V":
            ym+=2
        return (xm,ym)
    if ym> ya:
        while plan[ym-1][xm]!="-"and ym!= ya and plan[ym-2][xm]!="V":
            ym-=2
        return (xm,ym)
    return mino

  

def deplacemet_minoV(ariane,thesee,mino,plan):
    xm,ym=mino
    xa,ya=ariane
    xt,yt=thesee

    if ym==yt:
        b=True
        for i in range(min(xm,xt)+1,max(xm,xt)+1,2):
            b=b and plan[ym][i]!="|" and plan[ym][i+1]!="H"
        if b:
            return (xt,yt)
    if xm==xt:
        b=True
        for i in range(min(ym,yt)+1,max(ym,yt)+1,2):
            b=b and plan[i][xm]!="-" and plan[i+1][xm]!="H"
        if b:
            return (xt,yt)
    if ym< ya:
        while plan[ym+1][xm]!="-"and ym!= ya and plan[ym+2][xm]!="H":
            ym+=2
        return (xm,ym)
    if ym> ya:
        while plan[ym-1][xm]!="-"and ym!= ya and plan[ym-2][xm]!="H":
            ym-=2
        return (xm,ym)
    if xm< xa:
        while plan[ym][xm+1]!="|" and xm!= xa and plan[ym][xm+2]!="H":
            xm+=2
        return (xm,ym)
    if xm>xa:
        while plan[ym][xm-1]!="|"and xm!= xa and plan[ym][xm-2]!="H":
            xm-=2
        return (xm,ym)
    return mino
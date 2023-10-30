from upemtk import*
cree_fenetre(900)
n = 10
unité = 60
for i in range(3):
    rectangle(n*unité*.25, n*unité*(2*i+1)/7 , n*unité*.75, n*unité*2*(i+1)/7, remplissage = ("#00ff88","#00ffff",'red')[i],tag='fin_partie')
    texte(n*unité/2,n*unité*(2*i+1.5)/7,('réessayer','menu principal','quitter')[i], ancrage = 'center',tag='fin_partie')
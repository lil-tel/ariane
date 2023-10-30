from libraries import *

if __name__=="__main__":
        init_pos("sandbox")
        init_fenetre()
        while True:
                ev = donne_evenement()
                ty = type_evenement(ev)
                if ty == 'Quitte':
                        ferme_fenetre()
                        break
                elif ty == 'Touche':
                        maj(touche(ev))
                if deu():
                        ev2 = donne_evenement(2)
                        ty2 = type_evenement(ev2)
                        if ty2 == 'Quitte': ferme_fenetre(2)
                mise_a_jour()

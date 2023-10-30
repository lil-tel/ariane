from ariane import *

class breadth_fs:
    def __init__(self,maps="sandbox",affiche=True,pos=None):
        self.ari = ArianeGUI(maps,affiche)
        if pos is not None: self.ari.new_pos(pos)
        if self.ari.deux: self.ari.deux = bool(ferme_fenetre(2))
        self.x0 = deepcopy(self.ari.pos)
        self.chemin = self.parlar(affiche)
    
    def parlar(self,affiche):
        file,visites = [(self.x0,[None])],{tup(self.x0)}
        while file:
            s,touches = file.pop(0)
            self.ari.new_pos(s)
            for d in direction:
                x = self.ari.maj(d)
                t = deepcopy(self.ari.pos)
                if tup(t) not in visites:
                    file += [(t,touches+[d])]
                    visites |= {tup(t)}
                if x == 'Gagné': return (touches+[d])[1:]
                if x!='mur': self.ari.annule()
        return False


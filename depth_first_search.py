from ariane import *

class depth_fs:
    def __init__(self,maps='sandbox',n='inf',affiche=True,pos = None):
        self.ari = ArianeGUI(maps,affiche)
        if pos is not None: self.ari.new_pos(pos)
        if self.ari.deux:
            ferme_fenetre(2)
            self.ari.deux = False
        self.visites = set(())
        self.chemin = self.backpack(n)
        if affiche: ferme_fenetre(1)

    def backpack(self,n=30):
        if type(n) is int and n < 0: return 
        for touche in direction:
            x = self.ari.maj(touche)
            pos = tup(self.ari.pos)
            if pos not in self.visites:
                if x == "Gagné": return [touche]
                if x is None:
                    self.visites |= {pos}
                    backpack_kid = self.backpack(n-1 if(type(n) is int) else 'inf')
                    if backpack_kid: return [touche]+backpack_kid
            if x!="mur": self.ari.annule()


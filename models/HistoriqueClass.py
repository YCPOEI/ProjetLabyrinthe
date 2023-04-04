class Historique(object):
    def __init__(self, nom, date, temps):
        self.nom = nom
        self.date = date
        self.temps = temps

    def afficher(self):
        return f"<{self.nom}>; <{str(self.date)}>; <{str(self.temps)}>"

    def __str__(self):
        return f"{self.nom} {self.date} {self.temps}"

    def __repr__(self):
        return f"objet = labyrinthe_resolu(nom='{self.nom}',date='{self.date}',temps='{self.temps}')"

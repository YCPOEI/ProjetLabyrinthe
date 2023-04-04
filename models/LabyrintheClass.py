class Labyrinthe(object):
    def __init__(self, fichier):
        self.fichier = fichier
        self.lab_table = obtenirLabyrinthe(fichier)

    def __str__(self):
        return f"Labyrinthe[{self.fichier};{self.lab_table}]"

    def __repr__(self):
        return f"objet = Labyrinthe(fichier={self.fichier},lab_table={self.lab_table})"

    def get_fichier(self):
        return self.fichier

    def set_fichier(self, fichier):
        self.fichier = fichier

    def get_lab_table(self):
        return self.lab_table

    def set_lab_table(self, lab_table):
        self.lab_table = lab_table


def obtenirLabyrinthe(fichier):  # Function returning the labyrinth as a list
    with open(fichier, "r") as file:
        contenu = file.read()
        lignes = contenu.split("\n")  # Separate every line as a table (1 dimension)
        labyrinthe = []
        for i in range(0, len(lignes)):
            labyrinthe.append([*lignes[i]])
    return labyrinthe

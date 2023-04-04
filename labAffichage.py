# -*- coding: utf-8 -*-
from models.HistoriqueClass import Historique
from models.LabyrintheClass import Labyrinthe
import labMoteur
import sql_commands as sql


def labMenu():
    choix = 0
    conn = sql.creation_historique()  # Create a table

    while choix != 3:
        print("1) Voir l'historique")
        print("2) Résoudre un labyrinthe")
        print("3) Quitter")
        choix = int(input("\nVotre choix : "))
        if choix == 1:
            AfficherHistoriques(labMoteur.select_historique(conn))
        elif choix == 2:
            labMoteur.resoudreLabyrinthe(conn)
        elif choix == 3:
            print("\nVous avez bien quitté le programme")
            sql.close(conn)
            exit(0)
        else:
            print("Choix incorrect, faites un nouveau choix")


def AfficherLabyrinthe(
    lab_table,
):  # Show the labyrinth, solved or unsolved (based on the given lab_table)
    for i in range(0, len(lab_table)):
        for j in range(0, len(lab_table[i])):
            print(lab_table[i][j], end="")
        print("")


def AfficherLabyrintheResolu(
    lab_table, chemin
):  # Change the empty spaces of the labyrinth by the path chosen by our application
    if chemin == "":
        print("Le labyrinthe n'a pas été résolu!")
    else:
        for point_chemin in chemin:
            lab_table[point_chemin[0]][point_chemin[1]] = "O"
    AfficherLabyrinthe(lab_table)


def AfficherHistoriques(rows):
    print("rows:", rows)
    if rows == None:
        print("Aucun historique n'a été trouvé")
        return
    if len(rows) <= 0:
        print("Aucun historique n'a été trouvé")
        return
    for row in rows:
        elements = row[1].split("; ")
        print(f"Fichier : {elements[0]}, Date : {elements[1]}, Temps : {elements[2]}ms")


def showFile(file):
    print("Fichier : ", file)


def showSolvedLab(resultLab, labyrinth_solution, totalTime):
    print("resultatFinal:")
    print(AfficherLabyrintheResolu(resultLab, labyrinth_solution))
    print("Temps : ", totalTime, " ms")

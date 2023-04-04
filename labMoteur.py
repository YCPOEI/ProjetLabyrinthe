# -*- coding: utf-8 -*-
import os
import random
import time
import datetime
from models.LabyrintheClass import Labyrinthe
from models.HistoriqueClass import Historique
import labAffichage
import sql_commands as sql


def resoudreLabyrinthe(
    conn,
):  # Main function of the program (the function that will be called)
    global labyrinth_solution  # Initiate a global variable to recover the path used by the recursive function "trouverCheminLabyrinthe"
    labyrinth_solution = ""
    try:
        lab = Labyrinthe(
            choisirLabyrintheAleatoire()
        )  # Choose a random labyrinthe in the folder "Cartes"
    except:
        raise Exception("Aucune Carte n'a été trouvée")
    labAffichage.showFile(lab.get_fichier())
    begin_time = time.time()  # Track the time of the beginning of the solving process
    try:
        entree = trouverentree_labyrinthe(
            lab.get_lab_table()
        )  # Get the labyrinthe entrance
        sortie = trouverentree_labyrinthe(
            lab.get_lab_table(), entree
        )  # Get the labyrinth exit (entrance and exit are technically interchangeable)
    except:
        raise Exception("This labyrinth lack an entrance or exit!")
    try:
        trouverCheminLabyrinthe(lab.get_lab_table(), entree, sortie, [])
    except:
        raise Exception(
            "That's weird, we encountered an error while solving this labyrinth, seems like someone didn't test their code properly"
        )
    end_time = (
        time.time()
    )  # Get the end time for the solving process (to get the time taken)
    totalTime = (end_time - begin_time) * 1000000 / 1000

    insert_historique(conn, lab, totalTime)
    src = lab.get_fichier()
    dest = os.path.join(os.path.dirname(__file__),'.\\Resolus')+'/'+src.split('/')[-1]
    os.rename(src,dest)

    resultLab = lab.get_lab_table()
    labAffichage.showSolvedLab(resultLab, labyrinth_solution, totalTime)


def choisirLabyrintheAleatoire():
    chemin = os.path.join(
        os.path.dirname(__file__), ".\\Cartes"
    )  # Get the path of the "Cartes" folder
    str_chemin = (
        chemin + "/" + random.choice(os.listdir(chemin))
    )  # Get a random file of the folder
    return str_chemin


def trouverentree_labyrinthe(
    lab_table, entree_labyrinthe=0
):  # Check every border case for an entrance/exit, put a coodonate in entree_labyrinthe to avoid getting the same entrance twice
    # Return a tuple of 2 int that are the coordonates
    for ligne in range(0, len(lab_table)):  # Check all lines
        if (
            ligne == 0 or ligne == len(lab_table) - 1
        ):  # Check every character of the first and last line
            for colonne in range(0, len(lab_table[ligne])):
                if lab_table[ligne][colonne] == ".":
                    if (ligne, colonne) != entree_labyrinthe:
                        return (ligne, colonne)
        else:
            if (
                lab_table[ligne][0] == "."
            ):  # Check the first and last character of each line other than the first and last
                if (ligne, 0) != entree_labyrinthe:
                    return (ligne, 0)
            if lab_table[ligne][-1] == ".":
                if (ligne, len(lab_table[ligne]) - 1) != entree_labyrinthe:
                    return (ligne, len(lab_table[ligne]) - 1)


def trouverCheminLabyrinthe(
    lab_table, depart, arrivee, chemin=[], tries=0
):  # Recursive function to solve the maze and return in the global variable labyrinth_solution the path used
    global labyrinth_solution  # Get the labyrinth_solution global variable
    if labyrinth_solution != "":  # Stop the process if a path was already found
        return
    for (
        chemin_points
    ) in chemin:  # Stop the process if the current case was already searched
        if chemin_points == depart:
            return
    if (
        depart == arrivee
    ):  # Save the path and stop the process as we have reached the exit
        chemin.append(depart)
        labyrinth_solution = chemin
        return
    if tries > 1000:
        return
    print(depart)
    chemin.append(depart)  # Add the current position in the path taken
    if depart[0] > 0:  # Move Up
        if lab_table[depart[0] - 1][depart[1]] == ".":
            trouverCheminLabyrinthe(
                lab_table, (depart[0] - 1, depart[1]), arrivee, chemin.copy(), tries + 1
            )

    if depart[1] > 0:  # Move left
        if lab_table[depart[0]][depart[1] - 1] == ".":
            trouverCheminLabyrinthe(
                lab_table, (depart[0], depart[1] - 1), arrivee, chemin.copy(), tries + 1
            )

    if depart[0] < len(lab_table) - 1:  # Move down
        if lab_table[depart[0] + 1][depart[1]] == ".":
            trouverCheminLabyrinthe(
                lab_table, (depart[0] + 1, depart[1]), arrivee, chemin.copy(), tries + 1
            )

    if depart[1] < len(lab_table[0]) - 1:  # Move right
        if lab_table[depart[0]][depart[1] + 1] == ".":
            trouverCheminLabyrinthe(
                lab_table, (depart[0], depart[1] + 1), arrivee, chemin.copy(), tries + 1
            )


# Insert into table function
def insert_historique(conn, lab, totalTime):
    histoLab = Historique(
        lab.get_fichier().split("/")[-1], time.time(), totalTime
    )  # create object in class Historique
    entree_bdd = histoLab.afficher()  # create entry
    sql.add_task(conn, entree_bdd)  # Add entry in table
    # sql.close(conn) #close connection


# Select from table function
def select_historique(conn):
    return sql.select(conn)  # Show entries from table
    # sql.close(conn) #close connection

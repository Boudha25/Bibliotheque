#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# -*- coding: latin-1 -*-
##############################
#   Auteur: Stéphane April   #
#   Juin 2023 ver.2.0    #
##############################

import datetime
import tkinter as tk
from tkinter import *
from BaseDeDonnee import Database
from MenuEtFonction import MenuBar
from tkinter import simpledialog


class Application(tk.Tk, Database):
    def __init__(self):
        tk.Tk.__init__(self)
        Database.__init__(self)

        # Menu
        menubar = MenuBar(self)
        self.config(menu=menubar)

        # Titre de la fenêtre principale.
        self.title("Gestion bibliothèque")
        self.state('zoomed')

        # Utilisation de l'attribut durée d'emprunt d'un livre de la classe MenuBar.
        self.duree_default = MenuBar(self)

        # image dans un canvas
        self.logo = PhotoImage(file="girl_book.png")
        self.zone_dessin = Canvas(self, width=1366, height=650, bg='white', bd=2, relief="ridge")
        self.zone_dessin.create_image(1450, 10, anchor=NE, image=self.logo)
        self.zone_dessin.pack(side=TOP, fill=NONE, expand=NO)

        # Création du bouton emprunter.
        self.bouton_emprunter = tk.Button(self,
                                          text="Emprunter",
                                          font='Arial 25 bold',
                                          width=15,
                                          command=self.emprunter,
                                          bg='green')
        # Création du bouton Rendre.
        self.bouton_rendre = tk.Button(self,
                                       text="Rendre",
                                       font='Arial 25 bold',
                                       width=15,
                                       command=self.rendre,
                                       bg='yellow')

        # Insertion des boutons dans le Canevas.
        self.zone_dessin.create_window(255, 600, window=self.bouton_emprunter)
        self.zone_dessin.create_window(650, 600, window=self.bouton_rendre)

        # Création des labels des champs de saisie.
        self.lbl_scan_isbn = tk.Label(self,
                                      width='10',
                                      text="Code ISBN",
                                      font='Arial 20 bold',
                                      bg='white')

        self.lbl_no_classe = tk.Label(self,
                                      width='10',
                                      text="# Classe",
                                      font='Arial 20 bold',
                                      bg='white')

        # Création des champs de saisie.
        # Déclaration des variables.
        self.saisie_isbn = tk.StringVar()
        self.status = None

        # met la case vide et transforme la str en int.
        self.saisie_isbn.set('')
        self.scan_isbn = tk.Entry(self,
                                  bd=5,
                                  textvariable=self.saisie_isbn,
                                  font="Georgia 20",
                                  justify=CENTER,
                                  width=13)
        self.scan_isbn.bind('<Tab>', lambda event: self.affiche_information_livre())
        self.saisie_isbn.set(self.scan_isbn.get())
        self.scan_isbn.focus_set()  # met le curseur dans le Entry.

        # Déclaration des variables.
        self.no_classe_eleve = tk.IntVar()
        self.no_classe_eleve.set('')  # met la case vide.
        self.label_info_isbn = tk.IntVar

        self.no_classe = tk.Entry(self,
                                  bd=5,
                                  textvariable=self.no_classe_eleve,
                                  font="Georgia 20",
                                  justify=CENTER,
                                  width=4)

        # Insertion des labels et des champs dans le canevas.
        self.zone_dessin.create_window(280, 510, window=self.scan_isbn)
        self.zone_dessin.create_window(680, 510, window=self.no_classe)
        self.zone_dessin.create_window(280, 460, window=self.lbl_scan_isbn)
        self.zone_dessin.create_window(680, 460, window=self.lbl_no_classe)

        # Création des variables pour les champs d'affichage.
        self.label_info_message = tk.StringVar()
        self.label_info_message.set("Balayez le code ISBN: ")
        self.affiche_titre = tk.StringVar()
        self.affiche_titre.set("Titre")
        self.affiche_auteur = tk.StringVar()
        self.affiche_auteur.set("Auteur")
        self.affiche_isbn = tk.StringVar()
        self.affiche_isbn.set("ISBN")
        self.affiche_status = tk.IntVar()
        self.affiche_status.set(0)
        self.id_livre = tk.IntVar()

        # Création des champs d'affichage des données.
        self.entree_message = tk.Label(self,
                                       height='3',
                                       width='40',
                                       textvariable=self.label_info_message,
                                       font='Arial 20 bold',
                                       bg='white',
                                       relief="ridge")

        self.entree_titre = tk.Label(self,
                                     height='3',
                                     width='40',
                                     textvariable=self.affiche_titre,
                                     font='Arial 20 bold',
                                     bg='white',
                                     relief="ridge")

        self.entree_auteur = tk.Label(self,
                                      height='3',
                                      width='40',
                                      textvariable=self.affiche_auteur,
                                      font='Arial 20 bold',
                                      bg='white',
                                      relief="ridge")

        self.entree_isbn = tk.Label(self,
                                    height='3',
                                    width='40',
                                    textvariable=self.affiche_isbn,
                                    font='Arial 20 bold',
                                    bg='white',
                                    relief="ridge")

        # affichage et positionnement des labels.
        self.zone_dessin.create_window(450, 100, window=self.entree_message)
        self.zone_dessin.create_window(450, 195, window=self.entree_titre)
        self.zone_dessin.create_window(450, 290, window=self.entree_auteur)
        self.zone_dessin.create_window(450, 385, window=self.entree_isbn)

    def affiche_information_livre(self):
        # On fait une requête pour vérifier si le livre existe dans la Bd local
        # à l'aide de la méthode recherche de la classe Database.
        isbn = self.saisie_isbn.get()
        existance_du_livre = Database.recherche(self, isbn)
        if existance_du_livre:
            # Si le livre existe, on vérifie s'il y a plusieurs exemplaires.
            copie = Database.compteur_de_copies(self, isbn, )
            # S'il existe plusieurs exemplaires, on demande de quel exemplaire il s'agit.
            if copie > 1:
                # Récupère le choix de l'usager.
                copie_select = self.quelle_copie(isbn)
                # Sélectionne le titre dans la liste de tuple des résultats.
                tuple_livre_a_emprunter = existance_du_livre[copie_select]
                # met les données dans des variables pour afficher les informations du livre.
                self.id_livre.set(tuple_livre_a_emprunter[0])
                self.affiche_isbn.set(tuple_livre_a_emprunter[1])
                self.affiche_titre.set(tuple_livre_a_emprunter[2])
                self.affiche_auteur.set(tuple_livre_a_emprunter[4])
                self.affiche_status.set(tuple_livre_a_emprunter[9])
            else:
                # met les données dans des variables pour afficher les informations du livre.
                for row in existance_du_livre:
                    self.id_livre.set(row[0])
                    self.affiche_isbn.set(row[1])
                    self.affiche_titre.set(row[2])
                    self.affiche_auteur.set(row[4])
                    self.affiche_status.set(row[9])
            if self.affiche_status.get() == 0:
                # Affiche les informations du livre à l'utilisateur.
                self.entree_message.configure(bg="white")
                self.label_info_message.set("livre à emprunter:\n")
                self.affiche_titre.set("Titre:{0}\n".format(self.affiche_titre.get()))
                self.affiche_auteur.set("Auteur:{0}\n".format(self.affiche_auteur.get()))
                self.affiche_isbn.set("Code ISBN:{0}\n".format(self.affiche_isbn.get()))
            else:
                self.entree_message.configure(bg="yellow")
                # Requête dans la bd pour savoir qui a emprunté le livre.
                # Appel à la méthode pour savoir qui a emprunté le livre.
                identification_du_livre = self.id_livre.get()
                id_eleve = Database.qui_a_emprunte(self, identification_du_livre)

                self.label_info_message.set("Le livre est déjà emprunté par l'élève \n"
                                            "numéro:{0}".format(id_eleve))
        else:
            self.label_info_message.set("ERREUR! Mauvais code balayé,\n ou l'ajouter à la base de donnée."
                                        "\n Le livre n'existe pas dans la base de donnée.")
            self.scan_isbn.delete(0, END)  # Efface les champs Entry
            self.no_classe.delete(0, END)

    def quelle_copie(self, isbn):
        # Demande à l'utilisateur d'inscrire le # de copie à emprunter.
        copieEmprunter = simpledialog.askinteger("Attention?",
                                                 "Ce livre contient plusieurs exemplaires\n"
                                                 "Quel # de copie vous voulez emprunter?\n"
                                                 "Inscrire 0 si c'est l'original.\nCopie#:",
                                                 parent=self, minvalue=0, maxvalue=10)
        return copieEmprunter

    def verification_numero_eleve(self):
        # Vérifie si le champ est vide et qu'il contient des chiffres.
        try:
            self.no_classe_eleve.get()
        except tk.TclError:
            self.label_info_message.set("Tu dois inscrire ton numéro d'élève.\n"
                                        "Ton numéro d'élève doit être un chiffre entre 1 et 30.")
        # On vérifie si le numéro d'élève est compris entre 1 et 30.
        try:
            eleve = int(self.no_classe_eleve.get())
            if 1 <= eleve < 31:
                self.no_classe_eleve.set(eleve)
                return eleve
        except ValueError:
            self.label_info_message.set("Ton numéro d'élève doit être entre 1 et 30.")

    def erreur_no_classe(self):
        self.label_info_message.set("Ton numéro d'élève doit être entre 1 et 30.")

    def emprunter(self):
        # Méthode pour emprunter un livre.

        # Vérification que le code barre scanné contient 10 ou 13 chiffres.
        isbn_a_valider = self.saisie_isbn.get()
        valide = MenuBar.valider_champ_saisie(isbn_a_valider)
        if not valide:
            self.label_info_message.set("ISBN non valide,\n il doit contenir 10 ou 13 chiffres.")

        # Méthode qui vérifie si le numéro d'élève est correct.
        if self.verification_numero_eleve():
            id_eleve = self.verification_numero_eleve()
        else:
            self.erreur_no_classe()

        # Récupération des informations pour ajout dans la BD.
        id_livre = self.id_livre.get()
        isbn = isbn_a_valider
        date_emprunt = datetime.date.today()

        # Récupération de l'attribut de la classe MenuBar.
        nb_jour = self.trouve_duree_emprunt()
        print("Nombre de jour:", nb_jour)
        if nb_jour == 0:
            nb_jour = 40
            print("Nombre de jour mis a 40:", nb_jour)
        date_retour = date_emprunt + datetime.timedelta(days=nb_jour)

        # Si le livre est disponible, on ajoute l'emprunt dans la BD.
        if self.affiche_status.get() == 0:
            Database.ajout_emprunt(self, id_livre, id_eleve, isbn, date_emprunt, date_retour)
            # vérifie si au moins 1 ligne a été modifiée dans la base de donnée.
            if self.cur.rowcount != 0:
                # Met le status du livre à 1 (emprunté)
                Database.change_status(self, 1, id_livre)
                if self.cur.rowcount != 0:
                    self.label_info_message.set("L'emprunt à bien été enregistré à l'élève:\n"
                                                " numéro {0}\n"
                                                " date de retour: {1}".format(id_eleve, date_retour))
                    self.scan_isbn.delete(0, END)  # Efface les champs Entry
                    self.no_classe.delete(0, END)
                    self.scan_isbn.focus_set()  # met le curseur dans le champ scan_isbn.
                    self.after(5000, self.clear_champs)

    def trouve_duree_emprunt(self):

        try:
            duree = self.duree_default.duree_emprunt.get()
            duree = int(duree)
            print(type(duree))
            print("Durée:", duree)
            return duree

        except ValueError as e:
            print(e)

    def rendre(self):
        # Méthode pour rendre un livre.

        # Vérification que le code barre scanné contient 10 ou 13 chiffres.
        isbn_a_valider = self.saisie_isbn.get()
        valide = MenuBar.valider_champ_saisie(isbn_a_valider)
        if not valide:
            self.label_info_message.set("ISBN non valide,\n il doit contenir 10 ou 13 chiffres.")
        # Met le status du livre à 1 (emprunté)
        id_livre = self.id_livre.get()
        Database.change_status(self, 0, id_livre)
        # vérifie si au moins 1 ligne a été modifiée dans la base de donnée.
        if self.cur.rowcount != 0:
            self.entree_message.configure(bg="green")
            self.label_info_message.set("Le retour à bien été enregistré.")
            self.after(5000, self.clear_champs)

    def clear_champs(self):
        # Remet les labels dans leur état d'origine.
        self.entree_message.configure(bg="white")
        self.label_info_message.set("Balayez le code ISBN: ")
        self.affiche_titre.set("Titre")
        self.affiche_auteur.set("Auteur")
        self.affiche_isbn.set("ISBN")
        self.scan_isbn.delete(0, END)  # Efface les champs Entry
        self.no_classe.delete(0, END)
        # met le curseur dans le Entry.
        self.scan_isbn.focus_set()


if __name__ == "__main__":
    app = Application()
    app.title("Gestion bibliothèque scolaire.")
    app.mainloop()

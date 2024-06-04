#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# -*- coding: latin-1 -*-

import json
import sqlite3
import tkinter as tk
import urllib.request
from BaseDeDonnee import Database
from datetime import date
from PIL import ImageTk
from tkinter import ttk
from tkinter.messagebox import showinfo
from tkinter import messagebox
from urllib.request import urlopen


class MenuBar(tk.Menu, Database):
    def __init__(self, parent):
        tk.Menu.__init__(self, parent)

        # Variable pour la base de donnée.
        self.date_emprunt = None
        self.date_retour = None
        self.id_eleve = tk.IntVar()
        self.id_livre = tk.IntVar()
        self.isbn = tk.IntVar()
        self.titre = tk.StringVar()
        self.auteur = tk.StringVar()
        self.resume = tk.StringVar()
        self.nbPage = tk.IntVar()
        self.langage = tk.StringVar()
        self.url = tk.StringVar()
        self.dateInscription = tk.StringVar()
        self.status = tk.IntVar()

        # Attribut servant à la base de donnée.
        self.conn = sqlite3.connect('biblio.db', detect_types=sqlite3.PARSE_DECLTYPES)
        self.cur = self.conn.cursor()

        # Attribut donné pour savoir si les données proviennent de Google ou manuellement.
        self.provenance_variable = None

        # Attribut date.  Enregistre la date courante.
        self.aujourdhui = date.today()

        # Attribut servant pour la bd Google.
        self.base_api_link = None

        # Création et assignation des variables de la fenêtre #2 et #5 ajout manuel et automatique.
        self.label_info_message = tk.StringVar()
        self.label_info_message.set("Remplir les champs \nTitre, Auteur et Isbn")
        self.label_info_titre = tk.StringVar()
        self.label_info_titre.set("")
        self.label_info_auteur = tk.StringVar()
        self.label_info_auteur.set("")
        self.label_info_isbn = tk.StringVar()
        self.label_info_isbn.set("")

        # Création des attributs Widget de la fenêtre 2 et 5, ajout manuel et automatique.
        self.fenetre2 = None
        self.fenetre5 = None
        self.label_message = None
        self.label_titre = None
        self.label_auteur = None
        self.label_isbn = None
        self.entry_info_titre = None
        self.entry_info_auteur = None
        self.entry_info_isbn = None
        self.bouton_ajout = None
        self.fermer_fenetre = None

        # Création des attributs de la fenêtre3 liste.
        self.fenetre3 = None
        self.text = tk.StringVar()
        self.text.set("Liste")
        self.listBox = None
        self.cadre = None
        self.listButton = None
        self.empruntButton = None
        self.informationButton = None
        self.populaireButton = None
        self.liste_de_recherche = None
        self.liste_rechercher = tk.StringVar()
        self.bouton_champ_recherche = None
        self.champ_recherche = None
        self.variable_rechercher = tk.StringVar()
        self.retardButton = None
        self.supprimerButton = None
        self.closeButton = None

        # Création et assignation des variables de la fenêtre4 configuration.
        self.fenetre4 = None
        self.duree_emprunt = tk.StringVar()
        self.label_duree_emprunt = None
        self.nb_jour_emprunt = tk.Entry()
        self.fermer_fenetre = None

        # Création et assignation des variables de la fenêtre6.
        self.livre_select = None
        self.fenetre6 = None
        self.label_image = None

        # Création du menu.
        MenuBarr = tk.Menu(self, tearoff=False)
        self.sousMenu = tk.Menu(MenuBarr, tearoff=0)
        self.add_cascade(label='Menu', menu=self.sousMenu)
        self.sousMenu.add_command(label='Ajout livre', command=self.ajout_livre)
        self.sousMenu.add_command(label='Ajout manuel', command=self.ajout_manuel)
        self.sousMenu.add_command(label='Listes', command=self.liste)
        self.sousMenu.add_command(label='Configuration', command=self.configuration)
        self.sousMenu.add_separator()
        self.sousMenu.add_command(label='Quitter', command=self.quit)
        # Menu Aide.
        AideMenu = tk.Menu(self, tearoff=False)
        self.aideMenu = tk.Menu(AideMenu, tearoff=0)
        self.add_cascade(label='Aide', menu=self.aideMenu)
        self.aideMenu.add_command(label="À propos", command=self.aproposGest)

    def ajout_livre(self):
        # creation de la fenetre secondaire pour ajouter ou supprimer des livres.
        self.fenetre2 = tk.Toplevel(self)
        self.fenetre2.geometry("600x550")
        self.fenetre2.focus_set()

        # Titre de la fenêtre principale.
        self.fenetre2.title("Ajout de livre")

        # Met l'attribut provenance_variable à False pour indiquer que les
        # données proviennent de la base dde donnée de Google.
        self.provenance_variable = False

        # Inscrit du texte dans les champs message, titre, auteur et isbn.
        self.set_label(self)

        # Bind the TAB Key pour affichage information automatiquement après un scan,
        # car le gun fait un <Tab> après un scan.
        self.fenetre2.bind('<Tab>', lambda event: self.variable_automatique())

        # Création des boutons.
        self.bouton_ajout = tk.Button(self.fenetre2,
                                      text="Ajout",
                                      font='Arial 20 bold',
                                      width=15,
                                      command=self.insertion,
                                      bg='white')

        self.fermer_fenetre = tk.Button(self.fenetre2,
                                        text="Fermer la\nfenêtre",
                                        font='Arial 15  bold',
                                        width=15,
                                        command=self.fenetre2.destroy,
                                        bg='white')

        # Création des labels.
        self.label_message = tk.Label(self.fenetre2,
                                      height='3',
                                      width='40',
                                      textvariable=self.label_info_message,
                                      font='Arial 20 bold',
                                      bg='white',
                                      relief="ridge")

        # création des champs de saisie.
        self.entry_info_titre = tk.Entry(self.fenetre2,
                                         width=40,
                                         justify='center',
                                         textvariable=self.label_info_titre,
                                         font='Arial 20 bold',
                                         bg='white',
                                         relief="ridge")
        self.entry_info_auteur = tk.Entry(self.fenetre2,
                                          width=40,
                                          justify='center',
                                          textvariable=self.label_info_auteur,
                                          font='Arial 20 bold',
                                          bg='white',
                                          relief="ridge")
        self.entry_info_isbn = tk.Entry(self.fenetre2,
                                        bd=1,
                                        textvariable=self.label_info_isbn,
                                        font="Georgia 20",
                                        justify='center',
                                        width=13,
                                        relief="ridge")
        self.entry_info_isbn.bind('<Button-1>', self.set_label)
        self.entry_info_isbn.focus_set()  # met le curseur dans le Entry.

        # Affichage des éléments.
        self.label_message.grid(row=0, column=0)
        self.entry_info_titre.grid(row=1, column=0)
        self.entry_info_auteur.grid(row=2, column=0)
        self.entry_info_isbn.grid(pady=5, row=3, column=0)
        self.bouton_ajout.grid(pady=5, row=4, column=0)
        self.fermer_fenetre.grid(pady=5, row=6, column=0)

    def ajout_manuel(self):
        # creation de la fenêtre5 secondaire pour ajouter des livres manuellement sans passer par la Bd de Google.
        self.fenetre5 = tk.Toplevel(self)
        self.fenetre5.geometry("800x500")
        self.fenetre5.focus_set()

        # Titre de la fenêtre.
        self.fenetre5.title("Ajout de livre manuellement")
        # Met l'attribut provenance_variable à true pour indiquer que les
        # données ne proviennent pas de la base dde donnée de Google.
        self.provenance_variable = True

        # Inscrit du texte dans les champs message, titre, auteur et isbn.
        self.set_label(self)

        # Création des labels.
        self.label_message = tk.Label(self.fenetre5,
                                      height='3',
                                      width='40',
                                      textvariable=self.label_info_message,
                                      font='Arial 20 bold',
                                      bg='white',
                                      relief="ridge")
        self.label_titre = tk.Label(self.fenetre5,
                                    height='1',
                                    width='20',
                                    text='Titre',
                                    font='Arial 20 bold',
                                    relief="ridge")
        self.label_auteur = tk.Label(self.fenetre5,
                                     height='1',
                                     width='20',
                                     text='Auteur',
                                     font='Arial 20 bold',
                                     relief="ridge")
        self.label_isbn = tk.Label(self.fenetre5,
                                   height='1',
                                   width='20',
                                   text='Code isbn',
                                   font='Arial 20 bold',
                                   relief="ridge")

        # création des champs de saisie.
        self.entry_info_titre = tk.Entry(self.fenetre5,
                                         bd=2,
                                         textvariable=self.label_info_titre,
                                         font="Georgia 20",
                                         justify='center',
                                         width=20)
        # Lorsqu'on clique dans le champ info titre, lance la fonction set_label.
        self.entry_info_titre.bind('<Button-1>', self.set_label)
        self.entry_info_auteur = tk.Entry(self.fenetre5,
                                          bd=2,
                                          textvariable=self.label_info_auteur,
                                          font="Georgia 20",
                                          justify='center',
                                          width=20)

        self.entry_info_isbn = tk.Entry(self.fenetre5,
                                        bd=2,
                                        textvariable=self.label_info_isbn,
                                        font="Georgia 20",
                                        justify='center',
                                        width=15)

        # Création des boutons.
        self.bouton_ajout = tk.Button(self.fenetre5,
                                      text="Ajout",
                                      font='Arial 20 bold',
                                      width=15,
                                      command=self.insertion,
                                      bg='white')
        self.fermer_fenetre = tk.Button(self.fenetre5,
                                        bd=5,
                                        text="Fermer la\nfenêtre",
                                        font='Arial 15  bold',
                                        width=15,
                                        command=self.fenetre5.destroy,
                                        bg='white')

        # Affichage des éléments de la fenetre
        self.label_message.grid(row=0, columnspan=3)
        self.label_titre.grid(row=1, column=0)
        self.entry_info_titre.grid(row=1, column=1)
        self.label_auteur.grid(row=2, column=0)
        self.entry_info_auteur.grid(row=2, column=1)
        self.label_isbn.grid(row=3, column=0)
        self.entry_info_isbn.grid(row=3, column=1)
        self.bouton_ajout.grid(row=4, column=0)
        self.fermer_fenetre.grid(row=4, column=1)

    def variable_manuel(self):
        # On amasse les données du livre.
        self.titre.set(self.label_info_titre.get())
        self.resume.set("Indisponible")
        self.auteur.set(self.label_info_auteur.get())
        self.nbPage.set(000)
        self.langage.set("fr")
        self.url.set("inconnu")
        # Enregistre la date du jour.
        self.dateInscription = self.aujourdhui.strftime("%Y-%m-%d")
        self.status = 0  # Met le livre disponible.
        return (self.titre.get(), self.resume.get(), self.auteur.get(), self.nbPage.get(), self.langage.get(),
                self.url.get(), self.dateInscription, self.status, self.provenance_variable)

    def variable_automatique(self):
        # Utilisation de la base de donnée Google Book.
        self.base_api_link = "https://www.googleapis.com/books/v1/volumes?q=isbn:"

        with urllib.request.urlopen(self.base_api_link + (self.label_info_isbn.get())) as f:
            text = f.read()

        # Vérifie si les données de la BD Google sont valides.
        decoded_text = text.decode("utf-8")
        obj = json.loads(decoded_text)  # deserializes decoded_text to a Python object
        item_info = obj["totalItems"]  # Nombre de livres trouvés avec le code ISBN.

        if item_info == 0:  # Si le nombre de livres est égal à zéro.
            self.label_info_message.set(
                "Le livre n'existe pas dans\nla base de donnée Google.\nAjouter le livre manuellement")
            self.label_info_isbn.set("")  # Efface la variable du champ Entry
        else:
            volume_info = obj["items"][0]

            # insertion des informations de livre dans des variables
            identifiant_livre = (volume_info["id"])

            # déclaration des variables et vérifie si elles ont du contenu.
            try:
                self.titre.set((volume_info["volumeInfo"]["title"]))
            except KeyError:
                self.titre.set("Titre Inconnu")

            try:
                self.resume.set((volume_info["volumeInfo"]["description"]))
            except KeyError:
                self.resume.set("Indisponible")

            try:
                auteurs = (volume_info["volumeInfo"]["authors"])  # Donne une list.
                auteur_list = [str(a) for a in auteurs]  # Sérialise la liste par caractère.
                self.auteur.set((",".join(auteur_list)))  # Remet la liste en string.
            except KeyError:
                self.auteur.set("Auteur Inconnu")

            try:
                self.nbPage.set((volume_info["volumeInfo"]["pageCount"]))
            except KeyError:
                self.nbPage.set(000)

            try:
                self.langage.set((volume_info["volumeInfo"]["language"]))
            except KeyError:
                self.langage.set("NA")

            self.label_info_titre.set(self.titre.get())
            self.label_info_auteur.set(self.auteur.get())
            self.url.set("https://books.google.com/books/content?id=%s&printsec= \
                       frontcover&img=1&zoom=5&edge=curl&source=gbs_api" % identifiant_livre)
            self.dateInscription = self.aujourdhui.strftime("%Y-%m-%d")
            self.status = 0  # Met le livre disponible.
            return (self.titre.get(), self.resume.get(), self.auteur.get(), self.nbPage.get(),
                    self.langage.get(), self.url.get(), self.dateInscription, self.status,
                    self.provenance_variable)

    def set_label(self, _event=None):
        # Méthode qui change le message lorsqu'on clique dans le champ info titre.
        if self.provenance_variable:  # Si la variable est à True. (provenance manuelle)
            self.label_info_message.set("Remplir les champs \nTitre, Auteur et Isbn")
            self.label_info_titre.set("")
            self.label_info_auteur.set("")
            self.label_info_isbn.set("")
        else:
            self.label_info_message.set("Prêt à \nbalayez le code ISBN: ")
            self.label_info_titre.set("Titre")
            self.label_info_auteur.set("Auteur")
            self.label_info_isbn.set("")

    def erreur(self):
        self.label_info_message.set("ISBN non valide,\n il doit contenir seulement\n 10 ou 13 chiffres.")

    def insertion(self):
        # Méthode qui sert à insérer les données dans la Bd.
        try:
            # On met le code isbn dans une variable et on vérifie que c'est bien des chiffres.
            self.isbn.set(int(self.label_info_isbn.get()))
        except ValueError:
            # Si le code contient autre chose que des chiffres.
            self.erreur()
            return  # Ajouté pour arrêter l'exécution en cas d'erreur

        # On utilise la méthode valider_champ_saisie pour s'assurer que le Isbn à 10 ou 13 chiffres.
        isbn_a_valider = self.isbn.get()
        valide = self.valider_champ_saisie(isbn_a_valider)
        if valide:
            # On fait une requête pour vérifier si le livre existe dans la Bd local
            # à l'aide de la méthode recherche de la classe Database.
            result = Database.recherche(self, isbn_a_valider)
            if result:
                self.label_info_message.set("Le livre existe déjà\n dans la base de donnée.")
                # Lance la méthode qui change le titre pour enregistrer les doublons.
                self.doublon()
            # On récupère les variables du livre dépendamment de la provenance des données.
            if self.provenance_variable:
                self.variable_manuel()
            else:
                # Les variables ont été récupérés automatiquement avec un Bind sur la touche <TAB> du scanneur.
                # On récupère le Titre une autre fois, car s'il a été modifié, on enregistre le bon.
                self.titre.set(self.label_info_titre.get())

            # C'est ici qu'on envoie les données à la méthode insert de la classe Database.
            self.titre.set(self.label_info_titre.get())

            Database.insert(self, self.isbn.get(), self.titre.get(), self.resume.get(), self.auteur.get(), self.nbPage.get(),
                            self.langage.get(), self.url.get(), self.dateInscription, self.status)

            # Si le livre est un doublon.
            if "copie" in self.titre.get():
                if self.cur.rowcount > 0:
                    self.label_info_message.set("Identifier ce livre comme étant: \n{0}"
                                                "\nle livre à bien été enregistré".format(self.titre.get()))
                # On vérifie s'il y a eu au moins 1 ligne d'enregistré dans la base de donnée.
            else:
                Database.validation(self)
        else:
            self.erreur()

    @staticmethod
    def valider_champ_saisie(isbn_a_valider):
        # On vérifie que le champ Isbn à seulement 10 ou 13 chiffres.
        str_saisie = str(isbn_a_valider)  # Transforme l'"int" en string pour compter les caractères.
        longueur = len(str_saisie)  # enregistre le nombre de caractères entré dans une variable
        if longueur == 10 or longueur == 13:  # Si le "ISBN" saisie contient 10 ou 13 caractères.
            return True  # Return True pour que la méthode "def insertion" accepte les données.

    def doublon(self):
        # Affiche une fenêtre et pose la question si c'est un doublon.
        response = messagebox.askquestion(title='Doublons détecté?', message='Est-ce que c\'est un doublon?')

        if response == 'yes':
            # Interroge la base de donnée pour savoir il y a combien de copie existante.
            copie = Database.compteur_de_copies(self, self.isbn.get(), )
            # Crée un attribut pour formater le titre avec le numéro de copie.
            titre = self.label_info_titre.get()
            titreDoublon = titre + " copie #{0}".format(copie)
            self.label_info_titre.set(titreDoublon)
            # On modifie la variable titre, car on ajoute le numéro de copie.
            self.titre.set(titreDoublon)

        elif response == 'no':
            messagebox.showinfo('Réponse', 'Continuez d\'ajouter des livres')
        else:
            messagebox.showwarning('Erreur', 'Erreur! Recommencez')

    def configuration(self):
        self.load_configuration()
        # creation de la fenêtre secondaire pour afficher les variables de configuration.
        self.fenetre4 = tk.Toplevel(self)
        self.fenetre4.geometry("500x500")

        # Titre de la fenêtre configuration.
        self.fenetre4.title("Configuration")

        self.label_duree_emprunt = tk.Label(self.fenetre4,
                                            text="Durée d'emprunt d'un livre\nDurée en jours.:",
                                            font=("Arial", 30))
        # création du champ de saisie.
        self.nb_jour_emprunt = tk.Entry(self.fenetre4,
                                        bd=5,
                                        textvariable=self.duree_emprunt,
                                        font="Georgia 20",
                                        justify='center',
                                        width=13)
        self.nb_jour_emprunt.focus_set()  # met le curseur dans le Entry.

        # Bouton fermer la fenêtre.
        self.fermer_fenetre = tk.Button(self.fenetre4,
                                        bd=5,
                                        text="Fermer la\nfenêtre",
                                        font='Arial 15  bold',
                                        width=13,
                                        command=self.fermer_fenetre_click,
                                        bg='white')
        # Affichage des éléments.
        self.nb_jour_emprunt.grid(row=1, column=1)
        self.label_duree_emprunt.grid(row=0, columnspan=3)
        self.fermer_fenetre.grid(row=2, column=1)

        # Configuration de la validation du champ Entry
        self.nb_jour_emprunt.config(validate="key")
        self.nb_jour_emprunt.config(validatecommand=(self.register(self.validate_entry), '%P'))

    def validate_entry(self, value):
        # Vérifie si la valeur entrée dans le champ self.nb_jour_emprunt = tk.Entry() est un nombre.
        if value.isdigit():
            return True
        else:
            # Affiche un message d'erreur si la valeur n'est pas un nombre.
            messagebox.showwarning('Erreur', 'Veuillez entrer un nombre.', parent=self.fenetre4)
            return False

    def load_configuration(self):
        # Charge la valeur sauvegardée dans un fichier texte appelé "configuration.txt" lors du démarrage du programme.
        try:
            with open("configuration.txt", "r") as f:
                self.duree_emprunt.set(f.read().strip())
        except FileNotFoundError:
            # Si le fichier de configuration n'existe pas, initialise la valeur par défaut
            self.duree_emprunt.set("40")
        return self.duree_emprunt

    def save_configuration(self):
        # Sauvegarde la valeur actuelle dans ce fichier chaque fois que l'utilisateur ferme la fenêtre de configuration.
        with open("configuration.txt", "w") as f:
            f.write(self.duree_emprunt.get())

    def fermer_fenetre_click(self):
        self.save_configuration()
        self.fenetre4.destroy()

    def quit(self):
        self.destroy()
        quit(self)

    # Fenetre À propos.
    @staticmethod
    def aproposGest():
        showinfo('À propos',
                 message="Bienvenue dans ce petit logiciel de gestion de bibliothèque.\n\n"

                         "Le logiciel permet d'emprunter ou de rendre un livre "
                         "simplement en balayant le code ISBN du livre.\n\n"

                         "Vous pouvez ensuite savoir qui possède chaque livre.\n"
                         "Vous pouvez savoir quel livre est le plus populaire.\n\n"

                         "Auteur: Stéphane April. Version 2.2\n"
                         "2023")

    def liste(self):
        # creation de la fenêtre secondaire liste pour afficher des données de la BD.
        self.fenetre3 = tk.Toplevel(self)
        self.fenetre3.state('zoomed')
        self.fenetre3.geometry("1250x700")
        self.fenetre3.title("Liste")

        # Création des widgets.
        self.cadre = tk.Label(self.fenetre3, textvariable=self.text, font=("Arial", 25))
        self.listButton = tk.Button(self.fenetre3, text="Liste", width=15, command=self.liste_livres)
        self.empruntButton = tk.Button(self.fenetre3, text="Emprunt", width=15, command=self.liste_emprunt)
        self.informationButton = tk.Button(self.fenetre3, text="Info-Livre/MAJ", width=15, command=self.item_selected)
        self.populaireButton = tk.Button(self.fenetre3, text="Populaire", width=15, command=self.liste_populaire)

        self.liste_de_recherche = ttk.Combobox(self.fenetre3, font="Arial 20", width=10,
                                               textvariable=self.liste_rechercher)
        # Valeur de la liste de sélection.
        self.liste_de_recherche['values'] = ("Isbn", "Id_livre", "Titre", "Auteur", "NbPage")
        # Met Titre comme valeur par défaut.
        self.liste_de_recherche.current(2)
        # Met la liste de sélection en lecture seule.
        self.liste_de_recherche['state'] = 'readonly'
        self.bouton_champ_recherche = tk.Button(self.fenetre3, text="Recherche", font="Arial 15",
                                                width=15, command=self.champ_rechercher)
        self.champ_recherche = tk.Entry(self.fenetre3, bd=1, font="Arial 20",
                                        width=25, textvariable=self.variable_rechercher)
        self.retardButton = tk.Button(self.fenetre3, text="Retard", width=15, command=self.liste_retard)
        self.supprimerButton = tk.Button(self.fenetre3, text="Supprimer", width=15, command=self.supprimer_livre)
        self.closeButton = tk.Button(self.fenetre3, text="Fermer", width=15, command=self.fenetre3.destroy)

        # Affichage des labels.
        self.cadre.grid(row=0, columnspan=3)
        self.listButton.grid(row=2, column=0)
        self.empruntButton.grid(row=2, column=1)
        self.informationButton.grid(row=3, column=1)
        self.populaireButton.grid(row=4, column=0)
        self.liste_de_recherche.grid(row=5, column=0, sticky='w', padx=10)
        self.bouton_champ_recherche.grid(row=5, column=0, sticky='e', padx=10)
        self.champ_recherche.grid(row=5, column=0)
        self.retardButton.grid(row=3, column=0)
        self.supprimerButton.grid(row=4, column=1)
        self.closeButton.grid(row=5, column=1)

        cols = ('1', '2', '3', '4', '5', '6', '7', '8')

        self.listBox = ttk.Treeview(self.fenetre3, columns=cols, show='headings', height=24)

        self.listBox["columns"] = cols
        self.listBox.column('1', width=75)
        self.listBox.column('2', width=150)
        self.listBox.column('3', width=320)
        self.listBox.column('4', width=280)
        self.listBox.column('5', width=70)
        self.listBox.column('6', width=75)
        self.listBox.column('7', width=150)
        self.listBox.column('8', width=150)

        for col in cols:
            # Appel de la fonction sortby pour trier les données.
            self.listBox.heading(col, text=col, command=lambda c=col: self.sortby(self.listBox, c, 0))
            self.listBox.grid(row=1, column=0, columnspan=2)
        # Lance la méthode item_selected en double click sur un item dans la liste.
        self.listBox.bind("<Double-Button-1>", self.item_selected)

    def champ_rechercher(self):
        objet = self.variable_rechercher.get()
        where = self.liste_de_recherche.get()
        # Affiche la liste des livres resultant de la recherche dans la fenêtre3.
        self.text.set("Liste des livres recherchés")
        # Efface le tableau
        self.efface_tableau()

        # Requête dans la base de donnée.
        records = Database.rechercher_un_element(self, where, objet)

        # Définition des entêtes de colonnes.
        self.titre_colonnes('Id livre', 'ISBN', 'Titre', 'Auteur', 'Status',
                            'Nb Page', '', '')
        # Place les éléments dans le tableau(listbox).
        for i, (self.id_livre, isbn, titre, auteur, status, nbPage) \
                in enumerate(records, start=1):
            self.listBox.insert("", "end", values=(self.id_livre, isbn, titre,
                                                   auteur, status, nbPage))
        # Ajout d'une barre de défilement.
        self.scrollbar()

    def sortby(self, listBox, col, descending):
        """Fonction qui permet de trier les colones des listes
           par ordre alphabétique en cliquant sur l'entête."""
        # grab values to sort
        data = [(listBox.set(child, col), child)
                for child in listBox.get_children('')]

        # Check if the data is numeric, change to float if necessary
        if all(value.replace('.', '', 1).isdigit() for value, _ in data):
            data.sort(key=lambda x: float(x[0]), reverse=descending)
        else:
            data.sort(reverse=descending)

        # Now sort the data in place
        for ix, item in enumerate(data):
            listBox.move(item[1], '', ix)

        # Switch the heading, so it will sort in the opposite direction
        listBox.heading(col, command=lambda colonne=col: self.sortby(listBox, col, int(not descending)))

    def liste_livres(self):
        # Affiche la liste de tous les livres de la Bd dans la fenêtre3.
        self.text.set("Liste des livres")
        # Efface le tableau
        self.efface_tableau()

        # Requête dans la base de donnée.
        records = Database.fetch_livre(self)

        # Tri des livres par titre
        records.sort(key=lambda x: x[2])  # Tri par le titre, index 2 dans chaque tuple

        # Définition des entêtes de colonnes.
        self.titre_colonnes('Id livre', 'ISBN', 'Titre', 'Auteur', 'Status',
                            'Nb Page', '', '')
        # Place les éléments dans le tableau(listbox).
        for i, (id_livre, isbn, titre, auteur, status, nbPage) \
                in enumerate(records, start=1):
            self.listBox.insert("", "end", values=(id_livre, isbn, titre,
                                                   auteur, status, nbPage))
        # Ajout d'une barre de défilement.
        self.scrollbar()

    def liste_emprunt(self):
        # Affiche les livres empruntés dans la fenêtre3.
        self.text.set("Liste des livres empruntés")
        # Efface le tableau
        self.efface_tableau()

        # Requête dans la base de donnée.
        records_emprunt = Database.emprunt_livre(self)

        # Tri des livres empruntés par titre
        records_emprunt.sort(key=lambda x: x[2])  # Tri par le titre, index 2 dans chaque tuple

        # Définition des entêtes de colonnes.
        self.titre_colonnes('Id livre', 'ISBN', 'Titre', 'Auteur', 'Status',
                            'Id élève', 'Date emprunt', 'Date retour')
        # Place les éléments dans le tableau(listbox).
        for i, (id_livre, isbn, titre, auteur, status,
                id_emprunt, id_eleve, date_emprunt, date_retour) \
                in enumerate(records_emprunt, start=1):
            self.listBox.insert("", "end", values=(id_livre, isbn, titre, auteur,
                                                   status, id_eleve, date_emprunt, date_retour))
        # Ajout d'une barre de défilement.
        self.scrollbar()

    def liste_populaire(self):
        # Affiche les livres empruntés le plus souvent dans la fenêtre3.
        self.text.set("Liste des livres en ordre de popularité")
        # Efface le tableau
        self.efface_tableau()

        # Requête dans la base de donnée.
        Livre_populaire = Database.livre_populaire(self)

        # Tri des livres par popularité (total d'emprunts)
        Livre_populaire.sort(key=lambda x: x[5], reverse=True)  # Tri par le total, index 5 dans chaque tuple

        # Définition des entêtes de colonnes.
        self.titre_colonnes('Id livre', 'ISBN', 'Titre', 'Auteur', 'Nb pages',
                            'Total', '', '')
        # Place les éléments dans le tableau(listbox).
        for i, (id_livre, isbn, titre, auteur, nbPage, total) \
                in enumerate(Livre_populaire, start=1):
            self.listBox.insert("", "end", values=(id_livre, isbn, titre, auteur,
                                                   nbPage, total))
        # Ajout d'une barre de défilement.
        self.scrollbar()

    def liste_retard(self):
        # Affiche les livres en retard dans la fenêtre3.
        self.text.set("Liste des emprunts en retard")
        # Efface le tableau
        self.efface_tableau()

        livres_en_retard = Database.livre_retard(self)

        # Tri des livres en retard par titre
        livres_en_retard.sort(key=lambda x: x[2])  # Tri par le titre, index 2 dans chaque tuple

        # Définition des entêtes de colonnes.
        self.titre_colonnes('Id livre', 'ISBN', 'Titre', 'Auteur', 'Status',
                            'Id élève', 'Date emprunt', 'Date retour')
        # Place les éléments dans le tableau(listbox).
        for i, (id_livre, isbn, titre, auteur, status,
                id_emprunt, id_eleve, date_emprunt, date_retour) \
                in enumerate(livres_en_retard, start=1):
            self.listBox.insert("", "end", values=(id_livre, isbn, titre, auteur,
                                                   status, id_eleve, date_emprunt, date_retour))
        # Ajout d'une barre de défilement.
        self.scrollbar()

    def supprimer_livre(self):
        messageConfirmation = messagebox.askquestion('Attention?', 'Voulez-vous supprimer définitivement ce livre?',
                                                     parent=self.fenetre3)
        if messageConfirmation == 'yes':
            # Sélection d'un livre dans la liste.
            self.selection()
            # Appel de la méthode de suppression dans la bd.
            Database.delete(self, self.livre_select)
            # On vérifie s'il y a eu au moins 1 ligne d'enregistré dans la base de donnée.
            if self.cur.rowcount > 0:
                messagebox.showinfo('Succès', "La suppression a été faite avec succès.", parent=self.fenetre3)
                # Relance la liste après la suppression.
                self.liste_livres()

        elif messageConfirmation == 'no':
            messagebox.showinfo('Response', 'La suppression à été annulée.', parent=self.fenetre3)
        else:
            messagebox.showwarning('Erreur', 'Erreur! Recommencez', parent=self.fenetre3)

    def item_selected(self, _event=None):
        # Création de la fenetre qui affiche toutes les informations d'un livre,
        # Sélection d'un livre dans la liste.
        self.selection()
        # Création de la fenêtre secondaire pour afficher des données de la BD.
        self.fenetre6 = tk.Toplevel(self)
        self.fenetre6.geometry("1250x650")
        # Titre de la fenêtre.
        self.fenetre6.title("Description")

        # Méthode qui Retourne les informations d'un livre.
        results = Database.select_un_livre(self)
        for row in results:
            self.id_livre = tk.IntVar(self.fenetre6, value=row[0])
            self.isbn = tk.IntVar(self.fenetre6, value=row[1])
            self.titre = tk.StringVar(self.fenetre6, value=row[2])
            self.resume.set(row[3])
            self.auteur = tk.StringVar(self.fenetre6, value=row[4])
            self.nbPage = tk.IntVar(self.fenetre6, value=row[5])
            self.langage = tk.StringVar(self.fenetre6, value=row[6])
            self.url.set(row[7])  # Attribut servant pour décoder l'image du livre.
            self.dateInscription = tk.StringVar(self.fenetre6, value=row[8])
            self.status = tk.IntVar(self.fenetre6, value=row[9])

        # Création des labels
        label_id_livre = tk.Label(self.fenetre6, font='Arial 20 bold', text='Id Livre:')
        label_isbn = tk.Label(self.fenetre6, font='Arial 20 bold', text='ISBN:')
        label_titre = tk.Label(self.fenetre6, font='Arial 20 bold', text='Titre:')
        label_auteur = tk.Label(self.fenetre6, font='Arial 20 bold', text='Auteur:')
        label_resume = tk.Label(self.fenetre6, font='Arial 20 bold', text='Résumé:')
        label_nbPage = tk.Label(self.fenetre6, font='Arial 20 bold', text='Nombre de pages:')
        label_langage = tk.Label(self.fenetre6, font='Arial 20 bold', text='Langage:')
        label_dateInscription = tk.Label(self.fenetre6, font='Arial 20 bold', text='Date d\'inscription:')
        label_status = tk.Label(self.fenetre6, font='Arial 20 bold', text='Status:')

        # Création des champs Entry.
        variable_id_livre = tk.Label(self.fenetre6, bd=1, textvariable=self.id_livre,
                                     font="Arial 20", bg='gray93', anchor='w', width=40)
        entry_isbn = tk.Entry(self.fenetre6, bd=1, textvariable=self.isbn, font="Arial 20", bg='gray93', width=46)
        entry_titre = tk.Entry(self.fenetre6, bd=1, textvariable=self.titre, font="Arial 20", width=46)
        entry_auteur = tk.Entry(self.fenetre6, bd=1, textvariable=self.auteur, font="Arial 20", width=46)
        texte_resume = tk.Text(self.fenetre6, font="Arial 15", bg='gray93', width=63, height=10, wrap='word')
        entry_nbPage = tk.Entry(self.fenetre6, bd=1, textvariable=self.nbPage, font="Arial 20", width=46)
        entry_langage = tk.Entry(self.fenetre6, bd=1, textvariable=self.langage, font="Arial 20", width=46)
        variable_dateInscription = tk.Label(self.fenetre6, bd=1, textvariable=self.dateInscription,
                                            font="Arial 20", bg='gray93', anchor='w', width=40)
        entry_status = tk.Entry(self.fenetre6, bd=1, textvariable=self.status, font="Arial 20", width=46)
        texte_resume.insert(tk.END, self.resume.get())  # Création de la case texte et insertion du texte.
        ys = ttk.Scrollbar(self.fenetre6, orient='vertical', command=texte_resume.yview)
        ys.grid(column=2, row=5, sticky='ns')

        # Affichage de l'image du livre
        if self.url.get() == 'inconnu':
            self.label_image = tk.Label(self.fenetre6, font='Arial 20 bold', text='Image inconnue')
        elif self.url.get() and 'http' in self.url.get():
            try:
                u = urlopen(self.url.get())
                raw_data = u.read()
                u.close()
                photo = ImageTk.PhotoImage(data=raw_data)
                self.label_image = tk.Label(self.fenetre6, image=photo)
                self.label_image.image = photo
            except Exception as e:
                self.label_image = tk.Label(self.fenetre6, font='Arial 20 bold',
                                            text='Erreur de chargement de l\'image')
        else:
            self.label_image = tk.Label(self.fenetre6, font='Arial 20 bold', text='Pas d\'image')

        self.label_image.grid(row=5, column=3, sticky='e')

        # Ajout bouton de la fenetre.
        bouton_enregistre = tk.Button(self.fenetre6, text="Enregistrer", width=15, command=self.mise_a_jour)
        bouton_enregistre.grid(row=11, column=1, sticky='w')
        fermerLaFenetre = tk.Button(self.fenetre6, text="Fermer", width=15, command=self.ferme_fenetre6)
        fermerLaFenetre.grid(row=11, column=1, sticky='e')

        # Affichage des labels.
        label_id_livre.grid(row=1, column=0, sticky='e')
        label_isbn.grid(row=2, column=0, sticky='e')
        label_titre.grid(row=3, column=0, sticky='e')
        label_auteur.grid(row=4, column=0, sticky='e')
        label_resume.grid(row=5, column=0, sticky='e')
        label_nbPage.grid(row=6, column=0, sticky='e')
        label_langage.grid(row=7, column=0, sticky='e')
        label_dateInscription.grid(row=9, column=0, sticky='e')
        label_status.grid(row=10, column=0, sticky='e')

        # Affichage des Entry.
        variable_id_livre.grid(row=1, column=1, sticky='w')
        entry_isbn.grid(row=2, column=1, sticky='w')
        entry_titre.grid(row=3, column=1, sticky='w')
        entry_auteur.grid(row=4, column=1, sticky='w')
        texte_resume.grid(row=5, column=1, ipady=20, sticky='w')
        entry_nbPage.grid(row=6, column=1, sticky='w')
        entry_langage.grid(row=7, column=1, sticky='w')
        variable_dateInscription.grid(row=9, column=1, sticky='w')
        entry_status.grid(row=10, column=1, sticky='w')

    def ferme_fenetre6(self):
        self.fenetre6.destroy()
        # Relance la liste après la suppression.
        self.liste_livres()

    def selection(self):
        # Méthode qui sélectionne l'id_livre du livre double-cliqué.
        for selected_item in self.listBox.selection():
            item = self.listBox.item(selected_item)
            self.livre_select = item['values'][0]
            return self.livre_select

    def mise_a_jour(self):
        # Méthode qui sert à mettre à jour la bd avec les informations de la fenetre6.
        # Récupération des variables de la fenetre 6 pour les mettre à jour.
        id_livre = self.id_livre.get()
        titre = self.titre.get()
        auteur = self.auteur.get()
        nbPage = self.nbPage.get()
        langage = self.langage.get()
        status = self.status.get()

        # C'est ici qu'on envoie les données à la méthode update de la classe Database.
        Database.update(self, titre, auteur, nbPage, langage, status, id_livre)
        # On vérifie s'il y a eu au moins 1 ligne d'enregistré dans la base de donnée.
        if self.cur.rowcount > 0:
            # Assignation des variables de la fenetre 6.
            self.titre.set('enregistré')
            self.auteur.set('enregistré')
            self.nbPage.set('enregistré')
            self.langage.set('enregistré')
            self.status.set('enregistré')

    def titre_colonnes(self, col1, col2, col3, col4, col5, col6, col7, col8):
        # Définition des entêtes de colonnes de la page liste.
        self.listBox.heading('1', text=col1, anchor="w")
        self.listBox.heading('2', text=col2, anchor="w")
        self.listBox.heading('3', text=col3, anchor="w")
        self.listBox.heading('4', text=col4, anchor="w")
        self.listBox.heading('5', text=col5, anchor="w")
        self.listBox.heading('6', text=col6)
        self.listBox.heading('7', text=col7)
        self.listBox.heading('8', text=col8)

    def scrollbar(self):
        # Ajout de barre de défilement vertical (scrollbar).
        scrollbar = ttk.Scrollbar(self.fenetre3, orient="vertical", command=self.listBox.yview)
        self.listBox.configure(yscroll=scrollbar.set)
        scrollbar.grid(row=1, column=2, sticky='ns')

    def efface_tableau(self):
        # Efface le tableau liste.
        for i in self.listBox.get_children():
            self.listBox.delete(i)

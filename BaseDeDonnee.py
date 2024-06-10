#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# -*- coding: latin-1 -*-
import sqlite3


class Database:
    def __init__(self):
        self.livre_select = None
        self.label_info_isbn = None
        self.label_info_auteur = None
        self.label_info_titre = None
        self.label_info_message = None

        # Attribut de la méthode compteur_de_copies.
        self.numero_de_copie = None

        self.conn = sqlite3.connect('biblio.db', detect_types=sqlite3.PARSE_DECLTYPES)
        self.cur = self.conn.cursor()
        self.cur.execute("""CREATE TABLE IF NOT EXISTS livre(id_livre INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE,
                Isbn INTEGER,
                Titre TEXT,
                Resume LONG TEXT,
                Auteur TEXT,
                NbPage INTEGER,
                Langage TEXT,
                Url TEXT,
                DateInscription INTEGER,
                Status INTEGER)""")

        self.cur.execute("""CREATE TABLE IF NOT EXISTS emprunt(id_emprunt INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE,
                Id_livre INT,
                Id_eleve INT,
                ISBN INT,
                Date_emprunt INT,
                Date_retour INT)""")

    def fetch_livre(self):
        """ Requête qui affiche la liste de livre. """
        try:
            self.cur.execute("SELECT id_livre, ISBN, Titre, Auteur, Status, NbPage FROM livre")
            rows_livre = self.cur.fetchall()
            return rows_livre
        except Exception as e:
            print("Erreur lors de l'exécution de la requête rechercher_un_element:", e)
            return None

    def rechercher_un_element(self, where, objet):
        """ Requête permet de rechercher un élément dans la liste de livre. """
        try:
            # Execute la requête SQL
            element_recherche = ('%' + objet + '%')  # permet de rechercher des mots contenant.
            sql = """SELECT id_livre, ISBN, Titre, Auteur, Status, NbPage FROM livre
                              WHERE %s LIKE "%s"
                              ORDER BY id_livre DESC
                              """ % (where, element_recherche)
            self.cur.execute(sql, )
            records = self.cur.fetchall()
            return records
        except Exception as e:
            print("Erreur lors de l'exécution de la requête rechercher_un_element:", e)
            return None

    def select_un_livre(self):
        """ Requête qui affiche les informations d'un livre dans la bd livre. """
        try:
            # Fait une requête dans la Bd avec l'id_livre sélectionné.
            req_sql = """SELECT * FROM livre WHERE id_livre = ?
                            ORDER BY id_livre LIMIT 1"""
            # Execute la requête SQL
            self.cur.execute(req_sql, (self.livre_select,))
            retour_req_sql = self.cur.fetchall()
            return retour_req_sql
        except Exception as e:
            print("Erreur lors de l'exécution de la requête select_un_livre:", e)
            return None

    def fetch_emprunt(self) -> object:
        """ Requête qui affiche la liste de tous les livres empruntés. """
        try:
            self.cur.execute("SELECT * FROM emprunt")
            rows_emprunt = self.cur.fetchall()
            return rows_emprunt
        except Exception as e:
            print("Erreur lors de l'exécution de la requête fetch_emprunt:", e)
            return None

    def insert(self, isbn, titre, resume, auteur, nbPage, langage, url, dateInscription, status):
        """ Requête ajoute un livre dans la base de donnée livre. """
        try:
            # On s'assure que le Isbn est valide avant de l'insérer dans la BD.
            isbn_a_valider = isbn
            if self.valider_champ_saisie(isbn_a_valider):
                sql_enr = "INSERT INTO livre " \
                          "(Isbn, Titre, Resume, Auteur, NbPage, Langage, Url, DateInscription, Status) " \
                          "VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)"
                val_enr = (isbn, titre, resume, auteur, nbPage, langage, url, dateInscription, status,)
                self.cur.execute(sql_enr, val_enr)  # Enregistre les données dans la BD.
                self.conn.commit()

            else:
                self.conn.rollback()
        except Exception as e:
            print("Erreur lors de l'exécution de la requête insert:", e)
            return None

    @staticmethod
    def valider_champ_saisie(isbn_a_valider):
        """ Méthode qui vérifie si l'ISBN contient 10 ou 13 caractères. """
        try:
            # On vérifie que le champ Isbn contient seulement 10 ou 13 chiffres.
            str_saisie = str(isbn_a_valider)  # Transforme l'"int" en string pour compter les caractères.
            longueur = len(str_saisie)  # Enregistre le nombre de caractères entré dans une variable.
            if longueur == 10 or longueur == 13:  # Si le "ISBN" saisi contient 10 ou 13 caractères.
                return True  # Return True pour que la méthode "def insertion" accepte les données.
            else:
                return False  # Si la longueur n'est pas de 10 ou 13, return False.
        except Exception as e:
            print("Erreur lors de la validation du champ ISBN:", e)
            return False  # Retourne False en cas d'exception.

    def emprunt_livre(self):
        """ Requête qui affiche la liste des livres empruntés. """
        try:
            self.cur.execute("""SELECT livre.id_livre, livre.ISBN, livre.Titre, livre.Auteur, livre.Status,
                            MAX(emprunt.id_emprunt), emprunt.Id_eleve, emprunt.Date_emprunt, emprunt.Date_retour
                            FROM livre 
                            INNER JOIN emprunt
                            ON livre.Id_livre = emprunt.Id_livre
                            WHERE livre.Status = 1
                            GROUP BY emprunt.Id_livre
                            ORDER BY emprunt.Date_retour
                            """)
            liste_emprunt = self.cur.fetchall()
            return liste_emprunt
        except Exception as e:
            print("Erreur lors de l'exécution de la requête emprunt_livre:", e)
            return None

    def ajout_emprunt(self, id_livre, id_eleve, isbn, date_emprunt, date_retour):
        """ Requête qui sert ajoute un livre emprunté dans la bd emprunt. """
        try:
            sql_enr = "INSERT INTO emprunt (Id_livre, Id_eleve, ISBN, Date_emprunt, Date_retour) VALUES (?, ?, ?, ?, ?)"
            val_enr = (id_livre, id_eleve, isbn, date_emprunt, date_retour)
            self.cur.execute(sql_enr, val_enr)  # Enregistre les données dans la BD.
            self.conn.commit()
        except Exception as e:
            print("Erreur lors de l'exécution de la requête ajout_emprunt:", e)
            return None

    def change_status(self, status, id_livre):
        """ Requête qui sert à modifier le status d'un livre dans la bd. """
        try:
            sql_update = "UPDATE livre SET Status = ? WHERE Id_livre = ?"
            val_update = (status, id_livre)
            self.cur.execute(sql_update, val_update)
            self.conn.commit()
        except Exception as e:
            print("Erreur lors de l'exécution de la requête change_status:", e)
            return None

    def qui_a_emprunte(self, id_livre):
        """ Requête qui vérifie si un livre est emprunté, si oui, par quel numéro d'élève. """
        try:
            sql = "SELECT id_eleve FROM emprunt WHERE id_livre = ? ORDER BY id_emprunt DESC LIMIT 1"
            # Execute la requête SQL
            self.cur.execute(sql, (id_livre,))
            # retourne le numéro de l'élève qui a emprunté le livre.
            no_eleve = self.cur.fetchall()
            numero_eleve = no_eleve[0]
            return numero_eleve
        except Exception as e:
            print("Erreur lors de l'exécution de la requête qui_a_emprunte:", e)
            self.label_info_message.set("Erreur lors de l'exécution de la requête.")
            return None

    def livre_retard(self):
        """ Requête pour sortir la liste des livres en retard. """
        try:
            self.cur.execute("""WITH
                        PREMIERE_REQUETE AS
                        (SELECT livre.id_livre, livre.ISBN, livre.Titre, livre.Auteur, livre.Status,
                        MAX(emprunt.id_emprunt), emprunt.Id_eleve, emprunt.Date_emprunt, emprunt.Date_retour
                        FROM livre 
                        INNER JOIN emprunt
                        ON livre.ISBN = emprunt.ISBN
                        WHERE livre.Status = 1 
                        GROUP BY livre.ISBN)
                        SELECT *
                        FROM PREMIERE_REQUETE
                        WHERE Status = 1 AND Date_retour < CURRENT_DATE
                        ORDER BY Date_retour
                            """)
            retard = self.cur.fetchall()
            return retard
        except Exception as e:
            print("Erreur lors de l'exécution de la requête livre_retard:", e)
            return None

    def livre_populaire(self):
        """ Requête pour vérifier combien de fois un livre a été emprunté. """
        try:
            self.cur.execute("""SELECT livre.id_livre, emprunt.ISBN, livre.Titre, livre.Auteur, livre.NbPage,  
                                COUNT(emprunt.ISBN) AS Total 
                            FROM emprunt 
                            INNER JOIN livre 
                            ON emprunt.ISBN = livre.ISBN 
                            WHERE emprunt.Date_emprunt >= DATE('NOW', '-1 YEAR')
                            GROUP BY emprunt.ISBN
                            ORDER BY Total DESC
                            """)
            populaire = self.cur.fetchall()
            return populaire
        except Exception as e:
            print("Erreur lors de l'exécution de la requête livre_populaire:", e)
            return None

    def validation(self):
        """Vérifie s'il y a eu un enregistrement dans la base de données."""
        try:
            if self.cur.rowcount > 0:
                self.label_info_message.set("Le livre a bien été enregistré")
                self.label_info_titre.set("")  # Efface la variable du champ Entry.
                self.label_info_auteur.set("")
                self.label_info_isbn.set("")
            else:
                self.label_info_message.set("Erreur d'enregistrement, recommencez !")
        except Exception as e:
            print("Erreur lors de la validation de l'enregistrement :", e)
            self.label_info_message.set("Erreur de validation, veuillez réessayer.")

    def recherche(self, isbn):
        """ Requête pour vérifier si le livre existe dans la Bd local. """
        sql = "SELECT * FROM livre WHERE ISBN = ? ORDER BY id_livre"
        try:
            # Execute la requête SQL
            self.cur.execute(sql, (isbn,))
            # Fetch all the rows in a list of lists.
            results = self.cur.fetchall()
            return results
        except Exception as e:
            print("Erreur lors de l'exécution de la requête de recherche:", e)
            return None

    def compteur_de_copies(self, isbn):
        """ Requête pour vérifier combien de fois le livre existe dans la Bd local. """
        sql = "SELECT COUNT(*) FROM livre WHERE ISBN = ?"
        try:
            # Execute la requête SQL
            self.cur.execute(sql, (isbn,))
            # Fetch the result of the query.
            result = self.cur.fetchone()
            self.numero_de_copie = result[0] if result else 0  # Converti le résultat de la requête en Integer.
            return self.numero_de_copie
        except Exception as e:
            print("Erreur lors de la comptabilisation des copies pour l'ISBN {}: {}".format(isbn, e))
            return 0  # Retourne 0 en cas d'exception.

    def update(self, titre, auteur, nbPage, langage, status, id_livre):
        req_sql = """UPDATE livre 
                    SET Titre=?, Auteur=?, NbPage=?, Langage=?, Status=?
                    WHERE id_livre = ?"""
        valeur = (titre, auteur, nbPage, langage, status, id_livre)
        self.cur.execute(req_sql, valeur)
        self.conn.commit()

    def delete(self, livre_select):
        self.cur.execute("DELETE FROM livre WHERE id_livre = ?", (livre_select,))
        self.conn.commit()

    def __del__(self):
        self.conn.close()

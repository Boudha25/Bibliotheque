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

        # Attribut de la méthode compteur_de_copies.
        self.numero_de_copie = None

    def fetch_livre(self):
        self.cur.execute("SELECT id_livre, ISBN, Titre, Auteur, Status, NbPage FROM livre")
        rows_livre = self.cur.fetchall()
        return rows_livre

    def rechercher_un_element(self, where, objet):
        # Execute la requête SQL
        element_recherche = ('%' + objet + '%')  # permet de rechercher des mots contenant.
        sql = """SELECT id_livre, ISBN, Titre, Auteur, Status, NbPage FROM livre
                          WHERE %s LIKE "%s"
                          ORDER BY id_livre DESC
                          """ % (where, element_recherche)
        self.cur.execute(sql, )
        records = self.cur.fetchall()
        return records

    def select_un_livre(self):
        # Fait une requête dans la Bd avec l'id_livre sélectionné.
        req_sql = """SELECT * FROM livre WHERE id_livre = ?
                        ORDER BY id_livre LIMIT 1"""
        # Execute la requête SQL
        self.cur.execute(req_sql, (self.livre_select,))
        retour_req_sql = self.cur.fetchall()
        return retour_req_sql

    def fetch_emprunt(self) -> object:
        self.cur.execute("SELECT * FROM emprunt")
        rows_emprunt = self.cur.fetchall()
        return rows_emprunt

    def insert(self, isbn, titre, resume, auteur, nbPage, langage, url, dateInscription, status):
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

    @staticmethod
    def valider_champ_saisie(isbn_a_valider):
        # On vérifie que le champ Isbn à seulement 10 ou 13 chiffres.
        str_saisie = str(isbn_a_valider)  # Transforme l'"int" en string pour compter les caractères.
        longueur = len(str_saisie)  # enregistre le nombre de caractères entré dans une variable
        if longueur == 10 or longueur == 13:  # Si le "ISBN" saisie contient 10 ou 13 caractères.
            return True  # Return True pour que la méthode "def insertion" accepte les données.

    def emprunt_livre(self):
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

    def ajout_emprunt(self, id_livre, id_eleve, isbn, date_emprunt, date_retour):
        sql_enr = "INSERT INTO emprunt (Id_livre, Id_eleve, ISBN, Date_emprunt, Date_retour) VALUES (?, ?, ?, ?, ?)"
        val_enr = (id_livre, id_eleve, isbn, date_emprunt, date_retour)
        self.cur.execute(sql_enr, val_enr)  # Enregistre les données dans la BD.
        self.conn.commit()

    def change_status(self, status, id_livre):
        sql_update = "UPDATE livre SET Status = ? WHERE Id_livre = ?"
        val_update = (status, id_livre)
        self.cur.execute(sql_update, val_update)
        self.conn.commit()

    def qui_a_emprunte(self, id_livre):
        sql = "SELECT id_eleve FROM emprunt WHERE id_livre = ? ORDER BY id_emprunt DESC LIMIT 1"
        # Execute la requête SQL
        self.cur.execute(sql, (id_livre,))
        # retourne le numéro de l'élève qui a emprunté le livre.
        no_eleve = self.cur.fetchall()
        numero_eleve = no_eleve[0]
        return numero_eleve

    def livre_retard(self):
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

    def livre_populaire(self):
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

    def validation(self):
        if self.cur.rowcount > 0:
            self.label_info_message.set("le livre à bien été enregistré")
            self.label_info_titre.set("")  # Efface la variable du champ Entry.
            self.label_info_auteur.set("")
            self.label_info_isbn.set("")
        else:
            self.label_info_message.set("Erreur d'enregistrement, recommencer!")

    def recherche(self, isbn):
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
        # requête pour vérifier combien de fois le livre existe dans la Bd local.
        sql = "SELECT COUNT(*) FROM livre WHERE ISBN = ?"
        # Execute la requête SQL
        self.cur.execute(sql, (isbn,))
        # Fetch all the rows in a list of lists.
        results = self.cur.fetchall()
        self.numero_de_copie = (sum(results[0]))  # Converti le résultat de la requête en Integer.
        return self.numero_de_copie

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

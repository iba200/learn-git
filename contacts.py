"""
4. Mini-projet pour appliquer les connaissances
Mini-projet : Gestionnaire de contacts simple

Crée contacts.py.
Utilise un dictionnaire pour stocker des 
contacts (clé : nom, valeur : dict avec "téléphone" et "email").
Écris des fonctions : ajouter_contact(contacts, nom, tel, email),
afficher_contacts(contacts), sauvegarder(contacts, fichier) 
(écris dans un fichier texte), charger(fichier) (lis du fichier).
Programme principal : 
    menu interactif avec input 
        (ajouter, afficher, quitter), 
    gère exceptions 
    (ex. : fichier inexistant).
"""

NOM_DU_FICHIER = 'contacts.txt'

def ajouter_contact(contacts, nom, tel, email):
    """Ajoute un contact au dictionnaire.
    
    Args:
        contacts (dict): Le dictionnaire des contacts.
        nom (str): Nom du contact (clé).
        tel (str): Téléphone.
        email (str): Email.
    """
    if nom in contacts:
        print("Contact existant !")
        return
    contacts[nom] = {"tel": tel, "email": email}
    print(f"Contact {nom} ajouté !")

def afficher_contacts(contacts):
    """Affiche les contacts.
    
    Args:
        contacts (dict): Dictionnaire qui contient les contacts.
    """
    if not contacts:
        print("Aucun contact.")
        return
    for key, value in contacts.items():
        print(f"{key} - Tel: {value['tel']} - Email: {value['email']}")

def sauvegarder(contacts, fichier):
    """Sauvegarde les contacts dans un fichier texte."""
    try:
        with open(fichier, "w", encoding="utf-8") as f:
            for item, value in contacts.items():
                f.write(f"{item},{value['tel']},{value['email']}\n")
        print("Contacts sauvegardés avec succès !")
    except Exception as e:
        print(f"Erreur lors de la sauvegarde : {e}")

def charger(fichier):
    """Charge les contacts depuis un fichier.
    
    Args:
        fichier (str): Nom du fichier.
    
    Returns:
        dict: Dictionnaire des contacts (vide si erreur).
    """
    contacts = {}
    try:
        with open(fichier, "r", encoding="utf-8") as f:
            for contact in f.readlines():
                cont = contact.strip().split(",")
                if len(cont) == 3:  # Vérifie format pour éviter IndexError
                    contacts[cont[0]] = {"tel": cont[1], "email": cont[2]}
        print("Contacts chargés avec succès !")
        return contacts
    except FileNotFoundError:
        print("Fichier non trouvé, démarrage avec une liste vide.")
        return {}
    except Exception as e:
        print(f"Erreur lors du chargement : {e}")
        return {}

def main():
    """Programme principal avec menu interactif."""
    contacts = charger(NOM_DU_FICHIER)
    while True:
        menu = input("1: Ajouter, 2: Afficher, 3: Sauvegarder, 4: Charger, 5: Quitter : ").strip()
        if menu == "1":
            nom = input("Nom : ")
            tel = input("Tel : ")
            email = input("Email : ")
            if nom and tel and email:
                ajouter_contact(contacts, nom, tel, email)
            else:
                print("Tous les champs doivent être remplis !")
        elif menu == "2":
            afficher_contacts(contacts)
        elif menu == "3":
            sauvegarder(contacts, NOM_DU_FICHIER)
        elif menu == "4":
            contacts = charger(NOM_DU_FICHIER)
        elif menu == "5":
            print("Au revoir !")
            break
        else:
            print("Choix invalide ! Veuillez choisir entre 1 et 5.")

main()
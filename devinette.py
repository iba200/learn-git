# Mini-projet : Jeu de devinette simple
secret = 8  # Nombre secret (change pour tester)
essais_restants = 5  # Nombre max d'essais
essais_liste = []  # Liste pour stocker les essais valides

while essais_restants > 0:
    print(f"Tu as {essais_restants} essais restants.")
    guess_str = input("Devine le nombre (1-10) : ").strip()  # Enlève espaces

    if guess_str.isdigit():
        guess = int(guess_str)
        if 1 <= guess <= 10:  # Vérifie la plage
            essais_liste.append(guess)  # Ajoute à la liste
            if guess > secret:
                print("Trop grand !")
            elif guess < secret:
                print("Trop petit !")
            else:
                print("Bravo, tu as gagné !")
                break  # Sort de la boucle
            essais_restants -= 1  # Décompte seulement si valide
        else:
            print("Le nombre doit être entre 1 et 10 !")  # Pas de décompte
    else:
        print("Choix invalide : entre un nombre entier !")  # Pas de décompte

# Après la boucle : messages finaux
if essais_restants == 0:
    print(f"Perdu ! Le secret était {secret}.")
print("Tes essais :", essais_liste)
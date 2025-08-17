"""
Exercice 3 : Fichiers et exceptions

Crée fichiers.py.
Écris dans un fichier "test.txt" : "Hello Python !" avec open() et write().
Lis le fichier et affiche son contenu.
Ajoute un try/except pour gérer si le fichier n'existe pas (FileNotFoundError).
"""

try:
    # Écriture
    with open("test.txt", "w", encoding="utf-8") as fichier:
        fichier.write("Hello Python !")
    print("Écriture réussie.")

    # Lecture
    with open("test.txt", "r", encoding="utf-8") as fichier:
        contenu = fichier.read()
        print("Contenu lu :", contenu)  # Affiche : Hello Python !
except FileNotFoundError:
    print("Fichier non trouvé !")
except Exception as e:
    print(f"Erreur : {e}")



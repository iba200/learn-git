"""
    Crée fonctions.py.
    Définit une fonction saluer(nom) qui prend un paramètre 
        nom et retourne une chaîne "Bonjour, [nom] !".
    Appelle-la avec ton nom et affiche le résultat.
    Bonus : Ajoute un paramètre par défaut, ex. saluer(nom="Inconnu").
"""
def saluer(nom="Inconnu"):
    """Une fonction qui retourne un salut personnalisé.

    Args:
        nom (str, optional): Le nom de la personne. Defaults to "Inconnu".

    Returns:
        str: La chaîne "Bonjour, [nom] !"
    """
    return f"Bonjour, {nom} !"

# Appel et affichage
print(saluer("TonNom"))  # Affiche : Bonjour, TonNom !
print(saluer())  # Affiche : Bonjour, Inconnu !

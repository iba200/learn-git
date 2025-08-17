"""
Crée structures.py.
Crée un dictionnaire personne = {"nom": "Doe", "age": 30, "ville": "Paris"}.
Affiche la valeur de "age",
ajoute une clé "job": "Développeur", et itère sur les clés/valeurs avec for key,
value in personne.items().
Crée un ensemble couleurs = {"rouge", "bleu", "rouge"} et affiche-le (note : pas de doublons).
"""
personne = {"nom": "Doe", "age": 30, "ville": "Paris"}

print(f"Âge : {personne['age']}")  # 30

personne["job"] = "Développeur"

for key, value in personne.items():
    print(f"{key}: {value}")

couleurs = {"rouge", "bleu", "rouge"}
print(couleurs)  # {'rouge', 'bleu'} (ordre aléatoire)

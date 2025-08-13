# Ton code ici
# ici l'utilisateur entre son age en str et strip pour enlever les espace
age_str = input("Quel est ton âge ? ").strip()
# Suite...
# on verifier si le variable age_str est un entier avec methode isdigit()
if age_str.isdigit():
    # convertion to str en int apres la verification 
    age = int(age_str)
    # message d'affichage pour indiquer a l'utilisateur son age dans l'annee prochaine
    print(f"Vous aurez {age+1} ans dans l'annee prochaine.")
    # un petit verification pour voir si il est majeur ou mineur
    # si age >= 18 il est majeur!
    if age >= 18:
        print("Vous etes majeur !")
    # sinon il est mineur
    else:
        print("Vous etes mineur !")
# sinon l'utilisateur quand entre quelque chose d'autres que des entier comme (ab, 12,4, -12)
else:
    print("Veuillez entrer un âge valide (entier positif) !")


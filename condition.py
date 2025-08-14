# projet : verificateur de nombre si il est positive , negative, ou zero

# utilisateur entre un nombre par la fonction input()
nombres_str = input("Entrer un nombre: ").strip()


if not nombres_str.isalpha():
    nombres = int(nombres_str)
    if nombres > 0:
        print("Positive!")
    elif nombres < 0 :
        print("Negative!")
    else:
        print("Zero")
else:
    print(f"Veuillez entre un nombre entier pas ca {nombres_str}!")

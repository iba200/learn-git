l = [111,23,12,3,3,2,6,7,7]


for i in range(len(l)):
    for j in range(0 ,len(l)):
        print(f"indice de (!): {l[i]}\nindice de (@): {l[j]}")
        if l[i] < l[j]:
            l[i], l[j] = l[j], l[i]
        print(f"{l}")

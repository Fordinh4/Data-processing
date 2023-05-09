fin = open("WC22-YellowCards.txt", "r")
myString = fin.readlines().strip()
fin.close()
print(myString)
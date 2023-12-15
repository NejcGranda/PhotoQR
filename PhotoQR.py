import random
import string

def koda(dolzina):
    koda = ""

    
    for i in range(dolzina):
        stevilka = random.randint(1, 9)
        crka = random.choice(string.ascii_uppercase)

        while crka == "W" or crka == "X" or crka == "Y" or crka == "Q":
            crka = random.choice(string.ascii_uppercase)

        moznost = [crka, str(stevilka)]

        znak = random.choice(moznost)
        koda += znak
    

    return koda

# url: https://svstefan.si/slike/

def 




print(koda(20))
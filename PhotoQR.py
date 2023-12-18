import random
import string
import qrcode
from os.path import exists

def generiraj_kodo(dolzina):
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

def QRkoda(koda):
    qr = qrcode.QRCode(
        version = 1,
        error_correction = qrcode.constants.ERROR_CORRECT_H,
        box_size = 10,
        border = 0
    )
    url = "https://svstefan.si/slike/" + koda + "/"
    qr.add_data(url)
    img = qr.make_image(fill_color="black", back_color="white")
    img.save("kode/" + koda + ".png")

    return img

def ali_uporabljena(koda):
    
    try:
        file = open("kode_vse.txt", "r")
    except:
        return False

    while True:
        line = file.readline()

        if line == koda:
            file.close()
            return True

        if not line:
            file.close()
            return False

def shrani_kodo(koda, datoteka):
    file = open(datoteka, "a")
    file.writelines(koda + "\n")
    file.close

def ustvari_pdf(kode):
    
    return True

stevilo = 10
dolzina = 8

kode = []

for i in range(stevilo):
    koda = generiraj_kodo(dolzina)

    while ali_uporabljena(koda) == True:
        koda = generiraj_kodo(dolzina)

    kode.append(koda)
    shrani_kodo(koda, "kode_vse.txt")
    shrani_kodo(koda, "kode_na_voljo.txt")
    QRkoda(koda)
    print(str(i) + ": " + koda)




# ime: datum, ura
import random
import string
import qrcode
from os.path import exists
import pypdf
import fitz
from PIL import Image

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
    qr.make(fit = True)
    img = qr.make_image(fill_color="black", back_color="white")
    img = img.resize((113, 113))

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

def ustvari_pdf(koda):
    pdf = fitz.open()
    page = pdf.new_page()
    img_path = "kode/RT84EFMN.png"

    levi_rob = 13.916220472440946
    levi_rob1 = 410.7666141732284
    zgornji_rob = 113.8620472440945

    for i in range(5):
    
        img = fitz.open(img_path)
        rect = fitz.Rect(levi_rob, zgornji_rob, levi_rob + 113, zgornji_rob + 113)
        page.insert_image(rect, filename = img_path)

        zgornji_rob += 188.9763779527559


    pdf.save("sv-stefan.pdf")
    pdf.close()

    return True


#### MAIN ####


stevilo = 1
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
    ustvari_pdf(koda)
    print(str(i) + ": " + koda)
    



# ime: datum, ura
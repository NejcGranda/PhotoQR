import random
import string
import qrcode

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

def QRkoda(koda):
    qr = qrcode.QRCode(
        version = 1,
        error_correction = qrcode.constants.ERROR_CORRECT_H,
        box_size = 10,
        border = 1
    )
    url = "https://svstefan.si/slike/"
    qr.add_data(url)
    img = qr.make_image(fill_color="black", back_color="white")
    img.save("sv stefan_qr.png")

    return img


koda = koda(5)

QRkoda(koda)
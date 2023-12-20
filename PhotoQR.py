import random
import string
import qrcode
from os.path import exists
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
        border = 0,
    )

    url = "https://svstefan.si/slike/" + koda + "/"
    qr.add_data(url)
    qr.make(fit = True)

    img = qr.make_image(fill_color="black", back_color="white")

    img.save("kode/" + koda + ".png")


    return True



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
    pdf = fitz.open("SvStefan-Photo-ThankYou-Card-Print.pdf")
    page = pdf[0]
    img_path = "kode/" + koda + ".png"

    mm_to_points = 2.83456
#QR
    QR_size_mm = 30
    top_margin_QR_mm = 30.126
    left_margin_QR_mm = 3.682
    left_margin_QR_mm1 = 108.682 

    QR_size = QR_size_mm * mm_to_points
    top_margin_QR = top_margin_QR_mm * mm_to_points
    left_margin_QR = left_margin_QR_mm * mm_to_points
    left_margin_QR1 = left_margin_QR_mm1 * mm_to_points

#TEXT
    text_size_mm_x = 24.346
    text_size_mm_y = 7.255
    top_margin_text_mm = 54.539
    left_margin_text_mm = 36.46
    left_margin_text_mm1 = 141.46

    text_size_x = text_size_mm_x * mm_to_points
    text_size_y = text_size_mm_y * mm_to_points
    top_margin_text = top_margin_text_mm * mm_to_points
    left_margin_text = left_margin_text_mm * mm_to_points
    left_margin_text1 = left_margin_text_mm1 * mm_to_points

    
    font_name = "hebo"


    for i in range(5):
    
    #QR
        img = fitz.open(img_path)
        rectQR_L = fitz.Rect(left_margin_QR, top_margin_QR, left_margin_QR + QR_size, top_margin_QR + QR_size)
        page.insert_image(rectQR_L, filename = img_path)

        rectQR_L = fitz.Rect(left_margin_QR1, top_margin_QR, left_margin_QR1 + QR_size, top_margin_QR + QR_size)
        page.insert_image(rectQR_L, filename = img_path)

    #TEXT
        
        text = koda
        textbox_rect = fitz.Point(left_margin_text, top_margin_text, left_margin_text + text_size_x, top_margin_text + text_size_y)
        textbox = page.insertTextbox(textbox_rect, text, fontsize = 10 )


        top_margin_QR += (57 * mm_to_points)
        top_margin_text += (57 * mm_to_points)


    pdf.save("sv-stefan.pdf")
    pdf.close()


#### MAIN ####


stevilo = 5
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
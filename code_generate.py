from dotenv import load_dotenv
import os
import random
import string
import qrcode
from os.path import exists, isfile
from os import listdir
import fitz
from PIL import Image

# Load environment variables from .env file
load_dotenv()


def generiraj_kodo(dolzina, count):
    
    koda = ""

    for i in range(dolzina - 3):
        stevilka = random.randint(1, 9)
        crka = random.choice(string.ascii_uppercase)

        while crka == "W" or crka == "X" or crka == "Y" or crka == "Q":
            crka = random.choice(string.ascii_uppercase)

        moznost = [crka, str(stevilka)]

        znak = random.choice(moznost)
        koda += znak

    # append count to the end of the code with leading zeros, 3 places
    koda += str(count).zfill(3)
    
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

def ustvari_pdf(kode, pdf_file_path):
    pdf = fitz.open("assets/SvStefan-Photo-ThankYou-Card-Print.pdf")
    page = pdf[0]

    fontsize = 14
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
    text_size_mm_x = 35
    text_size_mm_y = 10.255
    top_margin_text_mm = 53.539
    left_margin_text_mm = 36.46
    left_margin_text_mm1 = 141.46

    text_size_x = text_size_mm_x * mm_to_points
    text_size_y = text_size_mm_y * mm_to_points
    top_margin_text = top_margin_text_mm * mm_to_points
    left_margin_text = left_margin_text_mm * mm_to_points
    left_margin_text1 = left_margin_text_mm1 * mm_to_points

    for i,koda in enumerate(kode):
        print("Adding code to PDF " + str(i) + ": " + koda)
        img_path = "kode/" + koda + ".png"

        #QR
        img = fitz.open(img_path)

        if i % 2 == 0:
            # Levo
            rectQR_L = fitz.Rect(left_margin_QR, top_margin_QR, left_margin_QR + QR_size, top_margin_QR + QR_size)
            page.insert_image(rectQR_L, filename = img_path)

            textbox_rect_L = fitz.Rect(left_margin_text, top_margin_text, left_margin_text + text_size_x, top_margin_text + text_size_y)
            page.insert_textbox(textbox_rect_L, koda, fontsize = fontsize, fontfile = None, align = 0)
        else:
            # Desno
            rectQR_D = fitz.Rect(left_margin_QR1, top_margin_QR, left_margin_QR1 + QR_size, top_margin_QR + QR_size)
            page.insert_image(rectQR_D, filename = img_path)

            textbox_rect_D = fitz.Rect(left_margin_text1, top_margin_text, left_margin_text1 + text_size_x, top_margin_text + text_size_y)
            page.insert_textbox(textbox_rect_D, koda, fontsize = fontsize, fontfile = None, align = 0)

            top_margin_QR += (57 * mm_to_points)
            top_margin_text += (57 * mm_to_points)

    # Shrani
    pdf.save(pdf_file_path)
    pdf.close()

def naslednje_ime_print_pdf():
    folder_path = "pdf/"
    count = 1

    for path in listdir(folder_path):
        if path.lower().endswith('.pdf'):
            count += 1

    ime = f"print_pdf_{count:03d}.pdf"

    return ime


#### MAIN ####


stevilo = 100
dolzina = 10
count_offset = 501

vse_kode = []

for i in range(stevilo):
    koda = generiraj_kodo(dolzina, i+count_offset)

    while ali_uporabljena(koda) == True:
        koda = generiraj_kodo(dolzina, i+count_offset)

    vse_kode.append(koda)
    shrani_kodo(koda, "kode_vse.txt")
    shrani_kodo(koda, "kode_na_voljo.txt")
    QRkoda(koda)
    print("Koda " + str(i) + ": " + koda)

    # For every 10th code, print the codes to a PDF
    if (i+1) % 10 == 0:
        print("Printing PDF")
        ustvari_pdf(vse_kode, "pdf/" + naslednje_ime_print_pdf())
        vse_kode = []

# ime: datum, ura
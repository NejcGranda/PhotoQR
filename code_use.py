# Vzameš 1 kodo iz prve vrstice datoteke kode_na_voljo.txt in jo izbrišeš
# Če kode niso na voljo, napiši napako, da kode manjkajo
# Vzameš vse datoteke iz "src" in je premkaneš v "dst" z novim imenom: "<koda>_<original_ime_datoteke>"

import os
import shutil

from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

def izberi_kodo(datoteka):

    with open(datoteka, "r") as fin:
        data = fin.read().splitlines(True)

    if len(data) == 0:
        return False
    
    with open(datoteka, "w") as fout:
        fout.writelines(data[1:])

    return data[0].strip()


def premakni_file(koda, src_folder, dst_folder):

    for file_name in os.listdir(src_folder):
        src_file = src_folder + "/" + file_name
        dst_file = dst_folder + "/" + koda + "_" + file_name
        if os.path.isfile(src_file):
            shutil.move(src_file, dst_file)

    
#### MAIN ####

# Preveri če obstajajo datoteke v mapi src !

izbrana = izberi_kodo("kode_na_voljo.txt")

if izbrana == False:
    print("Ni več prostih kod")
    exit(0)

# kode_uporabljene.txt

print("Izbrana koda: " + izbrana)

premakni_file(izbrana, os.getenv('CAMERA_FOLDER'), os.getenv('LIGHTROOM_IN_FOLDER'))


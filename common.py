def pick_the_code():

    file = "kode_na_voljo.txt"

    with open(file, "r") as fin:
        data = fin.read().splitlines(True)

    if len(data) == 0:
        return False
    
    with open(file, "w") as fout:
        fout.writelines(data[1:])

    return data[0].strip()
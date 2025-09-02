def tambah(angka_1: float, angka_2: float) -> float:
    return angka_1 + angka_2

def kurang(angka_1: float, angka_2: float) -> float:
    return angka_1 - angka_2

def kali(angka_1: float, angka_2: float) -> float:
    return angka_1 * angka_2

def bagi(angka_1: float, angka_2: float) -> float:
    if angka_2 == 0:
        print("pembilang tidak boleh nol!")
    else:
        angka_1 / angka_2

def pangkat(angka_1: float, angka_2: float) -> float:
    return angka_1 ** angka_2

def main():
    print("=== Kalkulator ===")
    print("1.tambah")
    print("2.kurang")
    print("3.kali")
    print("4.bagi")
    print("5.pangkat")

    pilihan = input("Masukkan operator (1/2/3/4/5): ")
    angka_1 = float(input("Masukkan angka 1 : "))
    angka_2 = float(input("Masukkan angka 2 : "))

    if pilihan == "1":
        hasil = tambah(angka_1, angka_2)

    elif pilihan == "2":
        hasil = kurang(angka_1, angka_2)

    elif pilihan == "3":
        hasil = kali(angka_1, angka_2)

    elif pilihan == "4":
        hasil = bagi(angka_1, angka_2)
    
    elif pilihan == "5":
        hasil = pangkat(angka_1, angka_2)

    else:
        print("Syntax Error")

    print(f"hasilnya adalah : {hasil}")

if __name__ == "__main__":
    main()
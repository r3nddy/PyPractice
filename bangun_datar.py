import math

def luas_lingkaran(radius: float)  -> float:
    return  math.pi * radius ** 2

def luas_persegi_panjang(panjang: float, lebar) -> float:
    return panjang * lebar

def luas_segitiga(alas: float, tinggi: float) -> float:
    return 0.5 * alas * tinggi

def luas_layang_layang(diagonal_1: float, diagonal_2: float) -> float:
    return 0.5 * diagonal_1 * diagonal_2

def main():
  
    menu: dict = {
        "1" : "lingkaran",
        "2" : "persegi panjang",
        "3" : "segitiga",
        "4" : "layang layang"
    }
     
    print("Program menghitung luas bangun datar")

    for key, value in menu.items():
        print(f"{key}.{value}")

    pilihan = input("Masukkan bangun ruang : (1/2/3/4)")

    

if __name__ == "__main__":
    main()
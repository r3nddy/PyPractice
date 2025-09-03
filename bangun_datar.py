import math

def luas_lingkaran(radius: float)  -> float:
    return  math.pi * radius ** 2


def main():
    radius = float(input("Masukkan jari jari (cm): "))
    hasil = luas_lingkaran(radius)
    print(f"hasilnya : {hasil:.2f} cm2")

if __name__ == "__main__":
    main()
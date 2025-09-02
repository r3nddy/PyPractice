def prime(n: int) -> bool:
    if n <= 1:
        return False
    for i in range(2, n):
        if n % i == 0:
            return False
    return True
 
def main():
    angka = int(input("Masukkan angka: "))
    if prime(angka):
        print(f"{angka} adalah bilangan prima")
    else:
        print(f"{angka} bukan bilangan prima")

if __name__ == "__main__":
    main()
def grade(nilai: int)->str:
    if 80 <= nilai <= 100:
        return "A"
    if 70 <= nilai < 80:
        return "B"
    if 60 <= nilai < 70:
        return "C"
    if 50 <= nilai < 60:
        return "D"
    if 0 <= nilai < 50:
        return "E"
    else:
        return "Nilai tidak Valid"
    
def main():
    while True:
        print("=== program menentukan grade dari nilai mahasiswa")
        nilai = int(input("Masukkan nilai anda: "))

        print(f"Nilai Anda: {grade(nilai)}")
        break

if __name__ == "__main__":
    main()
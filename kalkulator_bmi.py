def hitung_bmi(berat, tinggi_cm):
    return berat / (tinggi_cm ** 2)

def category(bmi):
    if bmi < 18.5:
        return "Kurus"
    elif bmi < 25:
        return "Normal"
    elif bmi < 30:
        return "Kelebihan berat badan"
    else:
        return "Obesitas"
    
def main():
    berat = float(input("Masukkan berat badan (kg): "))
    tinggi_cm = float(input("Masukkan tinggi badan (cm): "))
    tinggi_m = tinggi_cm / 100

    bmi = hitung_bmi(berat, tinggi_m)
    diagnosa = category(bmi)

    print(f"BMI anda: {bmi:.2f} -> {diagnosa}")


if __name__ == "__main__":
    main()
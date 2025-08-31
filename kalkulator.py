angka_1 = float(input("Masukkan angka 1 : "))
angka_2 = float(input("Masukkan angka 2 : "))
operand = str(input("Masukkan operandnya: "))

if operand == "+":
    print(f"hasil: {angka_1} + {angka_2} = { angka_1 + angka_2 }")

elif operand == "-":
    print(f"hasil: {angka_1} - {angka_2} = { angka_1 - angka_2}")

elif operand == "*":
    print(f"hasil : {angka_1} * {angka_2} = { angka_1 * angka_2}")

elif operand == "/":
    print(f"hasil : {angka_1} * {angka_2} = { angka_1 / angka_2}")
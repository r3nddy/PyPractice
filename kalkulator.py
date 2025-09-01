angka_1 = float(input("Masukkan angka 1 : "))
angka_2 = float(input("Masukkan angka 2 : "))
operator = str(input("Masukkan operandnya: "))

if operator == "+":
 print(angka_1 + angka_2)
elif operator == "-":
 print(angka_1 - angka_2)
elif operator == "*":
 print(angka_1 * angka_2)
elif operator == "/":
 print(angka_1 / angka_2)
else:
 print("Syntax error")
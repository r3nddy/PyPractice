angka_rahasia = 8

print("Tebak angka antara 1 sampai 10!")

tebakan = int(input("Masukkan angka tebakan : "))

if tebakan == angka_rahasia:
    print("Selamat! Kamu menebak dengan benar ")
elif tebakan < angka_rahasia:
    print("Terlalu kecil!")
else:
    print("Terlalu besar!")

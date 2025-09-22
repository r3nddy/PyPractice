espresso_nama = "Espresso"
espresso_harga = 15000

americano_nama = "Americano"
americano_harga = 18000

cappuccino_nama = "Cappuccino"
cappuccino_harga = 22000

latte_nama = "Latte"
latte_harga = 23000

total_pesanan = 0


print("=== Daftar Menu ===")
print("+----+---------------+---------------+")
print("| No | Nama          | Harga         |")
print("+----+---------------+---------------+")
print("| 1  | Espresso      | Rp15.000      |")
print("| 2  | Americano     | Rp18.000      |")
print("| 3  | Cappuccino    | Rp22.000      | <- Promo Diskon 10%!!!")
print("| 4  | Latte         | Rp23.000      |")
print("+----+---------------+---------------+")


while True:
    pilihan = int(input("Pilih Menu : "))

    if pilihan == 1:
        jumlah = int(input("Jumlah pesanan: "))
        harga_pesanan = espresso_harga * jumlah
        total_pesanan += harga_pesanan
        print(f"Anda memesan {jumlah} {espresso_nama} (Rp{harga_pesanan})")

    elif pilihan == 2:
        jumlah = int(input("Jumlah pesanan: "))
        harga_pesanan = americano_harga * jumlah
        total_pesanan += harga_pesanan
        print(f"Anda memesan {jumlah} {americano_nama} (Rp{harga_pesanan})")

    elif pilihan == 3:
        jumlah = int(input("Jumlah pesanan: "))
        harga_pesanan = cappuccino_harga * jumlah

        #diskon 10%
        diskon = int(harga_pesanan * 0.1)
        harga_diskon = harga_pesanan - diskon

        total_pesanan += harga_diskon
        print(f"Anda memesan {jumlah} {cappuccino_nama} (Rp{harga_diskon}, Anda mendapatkan diskon 10%)")

    elif pilihan == 4:
        jumlah = int(input("Jumlah pesanan: "))
        harga_pesanan = latte_harga * jumlah
        total_pesanan += harga_pesanan
        print(f"Anda memesan {jumlah} {latte_nama} (Rp{harga_pesanan})")
    else:
        print("Pilihan tidak valid.")
        continue

    lagi = input("Apakah Anda ingin memesan lagi? (y/n): ").lower()
    if lagi != "y":
        break

print(f"\nTotal yang harus dibayar: Rp{total_pesanan}")
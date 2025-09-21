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
print("| 1  | Espresso      | Rp 15000      |")
print("| 2  | Americano     | Rp 18000      |")
print("| 3  | Cappuccino    | Rp 22000      | <- Promo Diskon 10%!!!")
print("| 4  | Latte         | Rp 23000      |")
print("+----+---------------+---------------+")
print("| 0  | Selesai       |               |")
print("+----+---------------+---------------+")


while True:
    pilihan = int(input("Pilih Menu : "))

    if pilihan == 0:
        break

    elif pilihan == 1:
        jumlah = int(input("Jumlah pesanan: "))
        harga_pesanan = espresso_harga * jumlah
        total_pesanan += harga_pesanan
        print(f"Anda memesan {jumlah} {espresso_nama} (Rp {harga_pesanan})")

    elif pilihan == 2:
        jumlah = int(input("Jumlah pesanan: "))
        harga_pesanan = americano_harga * jumlah
        total_pesanan += harga_pesanan
        print(f"Anda memesan {jumlah} {americano_nama} (Rp {harga_pesanan})")

    elif pilihan == 3:
        jumlah = int(input("Jumlah pesanan: "))
        harga_pesanan = cappuccino_harga * jumlah

        #diskon 10%
        diskon = int(harga_pesanan * 0.1)
        harga_diskon = harga_pesanan - diskon

        total_pesanan += harga_diskon
        print(f"Anda memesan {jumlah} {cappuccino_nama} (Rp {harga_diskon}, Anda mendapatkan diskon 10%)")

    elif pilihan == 4:
        jumlah = int(input("Jumlah pesanan: "))
        harga_pesanan = latte_harga * jumlah
        total_pesanan += harga_pesanan
        print(f"Anda memesan {jumlah} {latte_nama} (Rp {harga_pesanan})")
    else:
        print("Pilihan tidak valid.")

print(f"\nTotal yang harus dibayar: Rp {total_pesanan}")

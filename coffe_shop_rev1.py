# Simpan menu dengan variabel terpisah
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
print(f"1. {espresso_nama} : Rp {espresso_harga}")
print(f"2. {americano_nama} : Rp {americano_harga}")
print(f"3. {cappuccino_nama} : Rp {cappuccino_harga}")
print(f"4. {latte_nama} : Rp {latte_harga}")
print("0. Selesai")

while True:
    pilihan = int(input("Pilih Menu : "))

    if pilihan == 0:
        break
    elif pilihan == 1:
        jumlah = int(input("Jumlah pesanan: "))
        subtotal = espresso_harga * jumlah
        total_pesanan += subtotal
        print(f"Anda memesan {jumlah} {espresso_nama} (Rp {subtotal})")
    elif pilihan == 2:
        jumlah = int(input("Jumlah pesanan: "))
        subtotal = americano_harga * jumlah
        total_pesanan += subtotal
        print(f"Anda memesan {jumlah} {americano_nama} (Rp {subtotal})")
    elif pilihan == 3:
        jumlah = int(input("Jumlah pesanan: "))
        subtotal = cappuccino_harga * jumlah
        total_pesanan += subtotal
        print(f"Anda memesan {jumlah} {cappuccino_nama} (Rp {subtotal})")
    elif pilihan == 4:
        jumlah = int(input("Jumlah pesanan: "))
        subtotal = latte_harga * jumlah
        total_pesanan += subtotal
        print(f"Anda memesan {jumlah} {latte_nama} (Rp {subtotal})")
    else:
        print("Pilihan tidak valid.")

print(f"\nTotal yang harus dibayar: Rp {total_pesanan}")

menu = {
    1: {"nama": "Espresso", "harga": 15000},
    2: {"nama": "Americano", "harga": 18000},
    3: {"nama": "Cappuccino", "harga": 22000},
    4: {"nama": "Latte", "harga": 23000}
}

pesanan = []
total_pesanan = 0

def menampilkan_menu():
    print("=== Daftar menu ===")
    for key, item in menu.items():
        print(f"{key}. {item["nama"]} : Rp {item["harga"]}")
    print("0.selesai")
    print("1")

while True:
    menampilkan_menu()
    pilihan = int(input("Pilih Menu : "))

    if pilihan == 0:
        break

    elif pilihan == 1:
        
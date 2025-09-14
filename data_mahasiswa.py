# Program menyimpan data mahasiswa sederhana

def tambah_mahasiswa(data: list) -> None:
    """Fungsi untuk menambah data mahasiswa ke dalam list."""
    nama = input("Masukkan nama mahasiswa: ")
    nim = input("Masukkan NIM: ")
    jurusan = input("Masukkan jurusan: ")

    mahasiswa = {
        "nama": nama,
        "nim": nim,
        "jurusan": jurusan
    }
    data.append(mahasiswa)
    print("Data mahasiswa berhasil ditambahkan!\n")


def tampilkan_mahasiswa(data: list) -> None:
    """Fungsi untuk menampilkan semua data mahasiswa."""
    if not data:
        print("Belum ada data mahasiswa.\n")
    else:
        print("Daftar Data Mahasiswa:")
        for i, mhs in enumerate(data, start=1):
            print(f"{i}. Nama: {mhs['nama']}, NIM: {mhs['nim']}, Jurusan: {mhs['jurusan']}")
        print()


def main():
    data_mahasiswa = []
    
    while True:
        print("=== Menu Data Mahasiswa ===")
        print("1. Tambah Data Mahasiswa")
        print("2. Lihat Data Mahasiswa")
        print("3. Keluar")
        pilihan = input("Pilih menu: ")

        if pilihan == "1":
            tambah_mahasiswa(data_mahasiswa)
        elif pilihan == "2":
            tampilkan_mahasiswa(data_mahasiswa)
        elif pilihan == "3":
            print("Program selesai.")
            break
        else:
            print("Pilihan tidak valid!\n")


if __name__ == "__main__":
    main()

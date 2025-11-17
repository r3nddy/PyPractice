import json
import os
from datetime import datetime
from tabulate import tabulate
import random
import requests
import time
from prettytable import PrettyTable
import sys
import pwinput

# ==================== FILE DATABASE JSON ====================
DB_FILE = "crypto_data.json"

# ==================== VARIABEL GLOBAL ====================
current_user = None
current_level = None
db = {}

# ==================== KONFIGURASI API COINGECKO ====================
CRYPTO_IDS = ['bitcoin', 'ethereum', 'binancecoin', 'solana', 'cardano', 'ripple', 'dogecoin', 'matic-network']
VS_CURRENCY = 'usd'

CRYPTO_DISPLAY_MAP = {
    'bitcoin': {'name': 'Bitcoin', 'symbol': 'BTC'},
    'ethereum': {'name': 'Ethereum', 'symbol': 'ETH'},
    'binancecoin': {'name': 'BNB', 'symbol': 'BNB'},
    'solana': {'name': 'Solana', 'symbol': 'SOL'},
    'cardano': {'name': 'Cardano', 'symbol': 'ADA'},
    'ripple': {'name': 'XRP', 'symbol': 'XRP'},
    'dogecoin': {'name': 'Dogecoin', 'symbol': 'DOGE'},
    'matic-network': {'name': 'Polygon', 'symbol': 'MATIC'},
}

# ==================== STRUKTUR DATABASE DEFAULT ====================
DEFAULT_DB = {
    "users": {
        "rendy": {
            "password": "123456",
            "level": "admin",
            "join_date": "2024-01-01 09:00:00",
            "wallets": {
                "USDT": 10000.00,
                "BTC": 0.5,
                "ETH": 2.0,
                "BNB": 10.0
            }
        }
    },
    "market_prices": {
        "BTC": 43500.00,
        "ETH": 2280.00,
        "BNB": 315.50,
        "SOL": 98.75,
        "ADA": 0.52,
        "XRP": 0.61,
        "DOGE": 0.087,
        "MATIC": 0.89
    },
    "local_coins":[],
    "orders": [],
    "transactions": []
}

# ==================== ANIMATIONS ====================

def blockchain_loading():
    """Loading bar dengan tema blockchain"""
    print("\n")
    print("    ⛓️  Menghubungkan ke Blockchain...")
    print()
    
    for i in range(101):
        filled = int(20 * i / 100)
        bar = '█' * filled + '░' * (20 - filled)
        sys.stdout.write(f'\r    [{bar}] {i}%')
        sys.stdout.flush()
        time.sleep(0.03)
    
    print("\n")
    print("    🔐 Verifikasi Kredensial...")
    time.sleep(1)
    print("    ✅ Koneksi Berhasil!\n")
    time.sleep(0.5)

def verification_animation():
    """Animasi verifikasi"""
    steps = [
        "🔍 Memeriksa Username",
        "🔐 Validasi Password",
        "⛓️  Verifikasi Blockchain",
        "🛡️  Checking Security",
        "✅ Authentication Success"
    ]
    
    print()
    for step in steps:
        print(f"    {step}", end="")
        for _ in range(3):
            sys.stdout.write('.')
            sys.stdout.flush()
            time.sleep(0.2)
        print(" ✓")
        time.sleep(0.3)
    print()

def countdown_timer(seconds):
    """Countdown timer untuk lockout"""
    print("\n")
    for remaining in range(seconds, 0, -1):
        mins, secs = divmod(remaining, 60)
        timer = f'{mins:02d}:{secs:02d}'
        sys.stdout.write(f'\r    ⏳ Menunggu: {timer} ')
        sys.stdout.flush()
        time.sleep(1)
    print("\n")

# ==================== DATABASE FUNCTIONS ====================

def load_database():
    """Load database dari file JSON"""
    global db
    if os.path.exists(DB_FILE):
        with open(DB_FILE, 'r') as f:
            db = json.load(f)
    else:
        db = DEFAULT_DB.copy()
        save_database()
    return db

def save_database():
    """Simpan database ke file JSON"""
    with open(DB_FILE, 'w') as f:
        json.dump(db, f, indent=4)

# ==================== UI FUNCTIONS ====================

def clear_screen():
    """Clear terminal screen"""
    os.system('cls' if os.name == 'nt' else 'clear')

def print_modern_header():
    """Header dengan format PrettyTable"""
    clear_screen()
    print("\n")
    
    now = datetime.now()
    
    main_table = PrettyTable()
    main_table.field_names = ["CRYPTO TRADING TERMINAL - v2.0 💎"]
    main_table.add_row([f"📅 {now.strftime('%A, %d %B %Y')} | ⏰ {now.strftime('%H:%M:%S')}"])
    main_table.align["CRYPTO TRADING TERMINAL - v2.0 💎"] = "c"
    
    print(main_table)
    
    if current_user:
        user_info = PrettyTable()
        user_info.field_names = ["USER INFO"]
        user_info.add_row([f"👤 {current_user} | 🎖️  {current_level.upper()}"])
        print(user_info)
    
    print()

def pause():
    """Pause dan tunggu user menekan Enter"""
    input("\n    [Tekan Enter untuk melanjutkan...]")

# ==================== API FUNCTIONS ====================

def get_crypto_prices_from_api():
    """Mengambil data harga kripto real-time dari API CoinGecko"""
    ids_string = ",".join(CRYPTO_IDS)
    url = f"https://api.coingecko.com/api/v3/simple/price"
    params = {
        'ids': ids_string,
        'vs_currencies': VS_CURRENCY,
        'include_24hr_change': 'true',
        'include_last_updated_at': 'true'
    }
    
    try:
        print("🔄 Mengambil data harga real-time dari CoinGecko...")
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"⚠️ Error saat mengambil data dari API: {e}")
        print("📊 Menggunakan data harga terakhir dari database...")
        return None

def update_market_prices_from_api():
    """Update harga pasar di database dengan data real-time dari API"""
    api_data = get_crypto_prices_from_api()
    
    if api_data:
        updated = False
        for crypto_id, data in api_data.items():
            symbol = CRYPTO_DISPLAY_MAP.get(crypto_id, {}).get('symbol', '')
            if symbol:
                price = data.get(VS_CURRENCY, 0.0)
                if price > 0:
                    db["market_prices"][symbol] = price
                    updated = True
        
        if updated:
            save_database()
            print("✓ Harga pasar berhasil diperbarui dari API!")
            return True
    
    return False

def format_price_change(change):
    """Format perubahan harga dengan warna"""
    if change > 0:
        return f"+{change:.2f}%"
    else:
        return f"{change:.2f}%"
    
# ==================== CRUD FUNCTIONS ====================

def manage_local_coins():
    """Menu manajemen koin lokal (CRUD)"""
    while True:
        clear_screen()
        print_modern_header()
        
        # Buat tabel menu CRUD
        table = PrettyTable()
        table.field_names = ["No", "Menu CRUD Koin Lokal"]
        table.align["No"] = "c"
        table.align["Menu CRUD Koin Lokal"] = "l"
        table.hrules = 1
        
        table.add_row(["1", "➕ Tambah Koin Baru (Create)"])
        table.add_row(["2", "✏️  Update Harga Koin (Update)"])
        table.add_row(["3", "🗑️  Hapus Koin (Delete)"])
        table.add_row(["4", "🔄 Reset 24h Change"])
        table.add_row(["0", "🔙 Kembali ke Menu Utama"])
        
        print(table)
        
        choice = input("\n    🎯 Pilih menu: ").strip()
        
        if choice == "1":
            add_local_coin()
        elif choice == "2":
            update_local_coin()
        elif choice == "3":
            delete_local_coin()
        elif choice == "4":
            reset_24h_change()
        elif choice == "0":
            break
        else:
            print("\n    ✗ Pilihan tidak valid!")
            pause()


def add_local_coin():
    """Tambah koin lokal baru"""
    clear_screen()
    print_modern_header()
    print("=== TAMBAH KOIN LOKAL BARU ===\n")
    
    try:
        name = input("    Nama Koin: ").strip()
        if not name:
            print("\n    ✗ Nama koin tidak boleh kosong!")
            pause()
            return
        
        symbol = input("    Symbol (misal: ABC): ").upper().strip()
        if not symbol:
            print("\n    ✗ Symbol tidak boleh kosong!")
            pause()
            return
        
        # Cek apakah symbol sudah ada
        existing_symbols = [coin["symbol"] for coin in db.get("local_coins", [])]
        if symbol in existing_symbols or symbol in db["market_prices"]:
            print(f"\n    ✗ Symbol {symbol} sudah ada!")
            pause()
            return
        
        price = float(input("    Harga Awal (USD): $"))
        if price <= 0:
            print("\n    ✗ Harga harus lebih dari 0!")
            pause()
            return
        
        description = input("    Deskripsi (opsional): ").strip()
        
        # Konfirmasi
        print(f"\n{'='*50}")
        print("KONFIRMASI KOIN BARU:")
        print(f"Nama      : {name}")
        print(f"Symbol    : {symbol}")
        print(f"Harga     : ${price:,.4f}")
        print(f"Deskripsi : {description if description else '-'}")
        print(f"{'='*50}")
        
        confirm = input("\n    Tambahkan koin ini? (y/n): ").lower()
        
        if confirm == 'y':
            current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            
            new_coin = {
                "name": name,
                "symbol": symbol,
                "price": price,
                "price_24h_ago": price,
                "description": description,
                "created_by": current_user,
                "created_date": current_time,
                "last_updated": current_time
            }
            
            if "local_coins" not in db:
                db["local_coins"] = []
            
            db["local_coins"].append(new_coin)
            db["market_prices"][symbol] = price
            
            save_database()
            print(f"\n    ✓ Koin {name} ({symbol}) berhasil ditambahkan!")
        else:
            print("\n    ✗ Penambahan koin dibatalkan")
            
    except ValueError:
        print("\n    ✗ Input harga tidak valid!")
    except Exception as e:
        print(f"\n    ✗ Terjadi error: {e}")
    
    pause()


def update_local_coin():
    """Update harga koin lokal"""
    clear_screen()
    print_modern_header()
    print("=== UPDATE HARGA KOIN LOKAL ===\n")
    
    if not db.get("local_coins"):
        print("    Belum ada koin lokal yang dapat diupdate.")
        pause()
        return
    
    # Tampilkan daftar koin lokal
    print("Koin Lokal yang Tersedia:\n")
    for i, coin in enumerate(db["local_coins"], 1):
        current_price = coin.get("price", 0)
        print(f"    {i}. {coin['symbol']:6s} - {coin['name']:15s} ${current_price:>10,.4f}")
    
    print()
    symbol = input("    Masukkan symbol koin yang akan diupdate: ").upper().strip()
    
    # Cari koin
    coin_found = None
    for coin in db["local_coins"]:
        if coin["symbol"] == symbol:
            coin_found = coin
            break
    
    if not coin_found:
        print(f"\n    ✗ Koin dengan symbol {symbol} tidak ditemukan!")
        pause()
        return
    
    try:
        current_price = coin_found.get("price", 0)
        price_24h_ago = coin_found.get("price_24h_ago", current_price)
        
        print(f"\n{'='*50}")
        print(f"Koin          : {coin_found['name']} ({symbol})")
        print(f"Harga Saat Ini: ${current_price:,.4f}")
        print(f"Harga 24h Lalu: ${price_24h_ago:,.4f}")
        print(f"{'='*50}\n")
        
        new_price = float(input("    Harga baru (USD): $"))
        
        if new_price <= 0:
            print("\n    ✗ Harga harus lebih dari 0!")
            pause()
            return
        
        # Preview perubahan
        price_diff = new_price - current_price
        price_diff_pct = ((new_price - current_price) / current_price) * 100 if current_price > 0 else 0
        
        if price_24h_ago > 0:
            new_change_24h = ((new_price - price_24h_ago) / price_24h_ago) * 100
        else:
            new_change_24h = 0.0
        
        print(f"\n{'='*50}")
        print("PREVIEW PERUBAHAN:")
        print(f"Harga Lama       : ${current_price:,.4f}")
        print(f"Harga Baru       : ${new_price:,.4f}")
        print(f"Selisih          : ${price_diff:+,.4f} ({price_diff_pct:+.2f}%)")
        print(f"24h Change Baru  : {new_change_24h:+.2f}%")
        print(f"{'='*50}")
        
        confirm = input("\n    Konfirmasi update? (y/n): ").lower()
        
        if confirm == 'y':
            current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            
            old_price = coin_found["price"]
            coin_found["price"] = new_price
            coin_found["last_updated"] = current_time
            
            # Update di market_prices
            db["market_prices"][symbol] = new_price
            
            save_database()
            
            print(f"\n    ✓ Harga {coin_found['name']} ({symbol}) berhasil diupdate!")
            print(f"      Harga: ${old_price:,.4f} → ${new_price:,.4f}")
            print(f"      24h Change: {new_change_24h:+.2f}%")
        else:
            print("\n    ✗ Update dibatalkan")
            
    except ValueError:
        print("\n    ✗ Input harga tidak valid!")
    except Exception as e:
        print(f"\n    ✗ Terjadi error: {e}")
    
    pause()


def delete_local_coin():
    """Hapus koin lokal"""
    clear_screen()
    print_modern_header()
    print("=== HAPUS KOIN LOKAL ===\n")
    
    if not db.get("local_coins"):
        print("    Belum ada koin lokal yang dapat dihapus.")
        pause()
        return
    
    # Tampilkan daftar koin lokal
    print("Koin Lokal yang Tersedia:\n")
    for i, coin in enumerate(db["local_coins"], 1):
        print(f"    {i}. {coin['symbol']:6s} - {coin['name']:15s} ${coin.get('price', 0):>10,.4f}")
    
    print()
    symbol = input("    Masukkan symbol koin yang akan dihapus: ").upper().strip()
    
    # Cari koin
    coin_found = None
    coin_index = -1
    for i, coin in enumerate(db["local_coins"]):
        if coin["symbol"] == symbol:
            coin_found = coin
            coin_index = i
            break
    
    if not coin_found:
        print(f"\n    ✗ Koin dengan symbol {symbol} tidak ditemukan!")
        pause()
        return
    
    # Konfirmasi penghapusan
    print(f"\n{'='*50}")
    print(f"KONFIRMASI HAPUS:")
    print(f"Nama        : {coin_found['name']}")
    print(f"Symbol      : {coin_found['symbol']}")
    print(f"Harga       : ${coin_found.get('price', 0):,.4f}")
    print(f"Dibuat oleh : {coin_found.get('created_by', '-')}")
    print(f"{'='*50}")
    
    confirm = input("\n    Yakin ingin menghapus koin ini? (y/n): ").lower()
    
    if confirm == 'y':
        # Hapus dari local_coins
        db["local_coins"].pop(coin_index)
        
        # Hapus dari market_prices
        if symbol in db["market_prices"]:
            del db["market_prices"][symbol]
        
        save_database()
        print(f"\n    ✓ Koin {coin_found['name']} ({symbol}) berhasil dihapus!")
    else:
        print("\n    ✗ Penghapusan dibatalkan")
    
    pause()


def reset_24h_change():
    """Reset 24h change koin lokal"""
    clear_screen()
    print_modern_header()
    print("=== RESET 24H CHANGE ===\n")
    
    if not db.get("local_coins"):
        print("    Belum ada koin lokal.")
        pause()
        return
    
    print("Fitur ini akan me-reset 24h change dengan")
    print("mengupdate 'price_24h_ago' ke harga saat ini.\n")
    
    # Tampilkan koin lokal
    print("Koin Lokal:\n")
    for i, coin in enumerate(db["local_coins"], 1):
        current_price = coin.get("price", 0)
        price_24h_ago = coin.get("price_24h_ago", current_price)
        
        if price_24h_ago > 0:
            change = ((current_price - price_24h_ago) / price_24h_ago) * 100
        else:
            change = 0.0
        
        print(f"    {i}. {coin['symbol']:6s} - {coin['name']:15s} ${current_price:>10,.4f} ({change:+.2f}%)")
    
    print("\nOpsi:")
    print("    1. Reset semua koin")
    print("    2. Reset satu koin")
    print("    0. Batal")
    
    choice = input("\n    Pilih: ").strip()
    
    if choice == "1":
        confirm = input("\n    Reset semua koin? (y/n): ").lower()
        if confirm == 'y':
            for coin in db["local_coins"]:
                coin["price_24h_ago"] = coin.get("price", 0)
            save_database()
            print("\n    ✓ Semua koin berhasil di-reset!")
            print("      Sekarang 24h change = 0% untuk semua koin lokal")
        else:
            print("\n    ✗ Dibatalkan")
            
    elif choice == "2":
        symbol = input("\n    Symbol koin: ").upper().strip()
        coin_found = None
        for coin in db["local_coins"]:
            if coin["symbol"] == symbol:
                coin_found = coin
                break
        
        if coin_found:
            old_24h = coin_found.get("price_24h_ago", 0)
            coin_found["price_24h_ago"] = coin_found.get("price", 0)
            save_database()
            print(f"\n    ✓ {symbol} berhasil di-reset!")
            print(f"      price_24h_ago: ${old_24h:,.4f} → ${coin_found['price']:,.4f}")
        else:
            print(f"\n    ✗ Koin {symbol} tidak ditemukan!")
    
    pause()

# ==================== AUTH FUNCTIONS ====================

def register():
    """Registrasi user baru dengan validasi sederhana"""
    try:
        clear_screen()
        print_modern_header()
        
        # Header registrasi
        reg_header = PrettyTable()
        reg_header.field_names = ["📝 FORM REGISTRASI"]
        reg_header.add_row(["Buat akun baru untuk mengakses sistem"])
        print(reg_header)
        print()
        
        # Input Username
        while True:
            try:
                username = input("    👤 Username : ").lower().strip()
                
                if not username or username == "":
                    print("    ❌ Username tidak boleh kosong!\n")
                    continue
                if len(username) < 4:
                    print("    ❌ Username minimal 4 karakter!\n")
                    continue
                if username in db["users"]:
                    print("    ❌ Username sudah digunakan! Pilih yang lain.\n")
                    continue
                print("    ✅ Username tersedia!")
                break
            except KeyboardInterrupt:
                print("\n    ⚠️  Input dibatalkan")
                pause()
                return
        
        # Input Password dengan pwinput (masked)
        while True:
            try:
                password = pwinput.pwinput(prompt="    🔒 Password : ", mask="*")
                
                if not password or password.strip() == "":
                    print("    ❌ Password tidak boleh kosong!\n")
                    continue
                if len(password) < 6:
                    print("    ❌ Password minimal 6 karakter!\n")
                    continue
                
                print("    ✅ Password diterima!")
                
                confirm_pass = pwinput.pwinput(prompt="    🔒 Konfirmasi: ", mask="*")
                if password != confirm_pass:
                    print("    ❌ Password tidak cocok! Coba lagi.\n")
                    continue
                print("    ✅ Password confirmed!")
                break
            except KeyboardInterrupt:
                print("\n    ⚠️  Input dibatalkan")
                pause()
                return
        
        # Pilih Level Akses
        print()
        level_table = PrettyTable()
        level_table.field_names = ["NO", "LEVEL AKSES", "HAK AKSES"]
        level_table.add_row(["1", "User (Trader)", "✅ Trading, ✅ Wallet, ❌ CRUD Koin"])
        level_table.add_row(["2", "Admin", "✅ CRUD Koin, ❌ Trading, ❌ Wallet"])
        level_table.align["NO"] = "c"
        level_table.align["LEVEL AKSES"] = "l"
        level_table.align["HAK AKSES"] = "l"
        level_table.align["NO"] = "c"
        level_table.align["LEVEL AKSES"] = "l"
        print(level_table)
        print()
        
        while True:
            try:
                level_choice = input("    Pilihan [1/2]: ").strip()
                if level_choice == "1" or level_choice == "":
                    level = "user"
                    print("    ✅ Level: User")
                    break
                elif level_choice == "2":
                    level = "admin"
                    print("    ✅ Level: Admin")
                    break
                else:
                    print("    ❌ Pilihan tidak valid!")
            except KeyboardInterrupt:
                print("\n    ⚠️  Input dibatalkan")
                pause()
                return
        
        print()
        
        # Proses registrasi dengan loading
        process_table = PrettyTable()
        process_table.field_names = ["STATUS"]
        process_table.add_row(["🔄 Memproses registrasi..."])
        print(process_table)
        time.sleep(1)
        
        # Simpan user ke database
        # ✅ PERBEDAAN: Admin tidak dapat wallet, User dapat wallet
        if level == "admin":
            wallets = {}  # Admin tidak punya wallet
            bonus_msg = "Tidak ada wallet (Admin mode)"
        else:
            wallets = {
                "USDT": 10000.00,  # Bonus awal untuk user
                "BTC": 0.0,
                "ETH": 0.0,
                "BNB": 0.0
            }
            bonus_msg = "Bonus USDT $10,000 telah ditambahkan!"

        # Simpan user ke database
        db["users"][username] = {
            'password': password,
            'level': level,
            'join_date': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'wallets': wallets
        }
        
        save_database()
        
        # Loading animation
        print()
        for i in range(101):
            filled = int(20 * i / 100)
            bar = '█' * filled + '░' * (20 - filled)
            sys.stdout.write(f'\r    [{bar}] {i}%')
            sys.stdout.flush()
            time.sleep(0.02)
        
        print("\n")
        
        # Success message
        clear_screen()
        print_modern_header()
        
        success_box = PrettyTable()
        success_box.field_names = ["✅ REGISTRASI BERHASIL"]
        success_box.add_row([f"Selamat datang, {username}! 🎉"])
        success_box.add_row(["Akun Anda telah dibuat"])
        success_box.add_row([bonus_msg])  # ✅ PAKAI VARIABEL bonus_msg
        success_box.add_row(["Silakan login untuk melanjutkan"])
        print(success_box)
        
        # Detail akun
        print()
        detail_table = PrettyTable()
        detail_table.field_names = ["INFORMASI AKUN", "DATA"]
        detail_table.add_row(["👤 Username", username])
        detail_table.add_row(["🎖️  Level", level.upper()])

        # ✅ TAMPILKAN BONUS HANYA UNTUK USER
        if level == "user":
            detail_table.add_row(["💰 Bonus USDT", "$10,000.00"])
        else:
            detail_table.add_row(["💰 Wallet", "Tidak tersedia (Admin)"])
            
        detail_table.add_row(["📅 Tanggal Bergabung", db["users"][username]['join_date']])
        
        detail_table.align["INFORMASI AKUN"] = "l"
        detail_table.align["DATA"] = "l"
        print(detail_table)
        
        # Tips
        print()
        tips = PrettyTable()
        tips.field_names = ["💡 TIPS KEAMANAN"]
        tips.add_row(["Simpan kredensial Anda dengan aman!"])
        print(tips)
        
        pause()
        
    except KeyboardInterrupt:
        print("\n\n    ⚠️  Registrasi dibatalkan")
        pause()
    except Exception as e:
        print(f"\n    ❌ Error saat registrasi: {e}")
        print("    Registrasi gagal. Silakan coba lagi.")
        pause()

def login():
    """Login user dengan validasi dan security features"""
    try:
        global current_user, current_level
        clear_screen()
        print_modern_header()
        
        # Header login
        login_header = PrettyTable()
        login_header.field_names = ["🔐 HALAMAN LOGIN"]
        login_header.add_row(["Masukkan kredensial untuk melanjutkan"])
        print(login_header)
        print()
        
        percobaan = 0
        berhasil = False
        
        while percobaan < 3 and not berhasil:
            try:
                username = input("    👤 Username: ").lower().strip()
                
                if not username or username == "":
                    print("    ❌ Username tidak boleh kosong!\n")
                    continue
                
                password = pwinput.pwinput(prompt="    🔒 Password: ", mask="*")
                
                # PERBAIKAN: Hapus strip() dari password, biarkan apa adanya
                if not password:
                    print("    ❌ Password tidak boleh kosong!\n")
                    continue
                
                print()
                
                # Validasi login - bandingkan langsung tanpa modifikasi
                if username in db["users"] and password == db["users"][username]['password']:
                    current_user = username
                    current_level = db["users"][username]['level']
                    berhasil = True
                    
                    # Login berhasil - Animasi loading
                    blockchain_loading()
                    
                    # Animasi verifikasi
                    verification_animation()
                    
                    time.sleep(0.5)
                    return True
                    
                else:
                    percobaan += 1
                    sisa = 3 - percobaan
                    if sisa > 0:
                        print(f"    ❌ Username atau password salah! Sisa percobaan: {sisa}\n")
                    else:
                        print("    🚫 Username atau password salah 3 kali!")
                        print("    ⏳ Silakan tunggu 10 detik sebelum mencoba lagi.")
                        
                        # Countdown 10 detik (ganti dengan 300 untuk 5 menit)
                        countdown_timer(10)
                        
                        print("    ✅ Waktu tunggu selesai. Anda bisa mencoba login kembali.")
                        time.sleep(2)
                        return False
                        
            except KeyboardInterrupt:
                print("\n    ⚠️  Login dibatalkan")
                pause()
                return False
            except Exception as e:
                print(f"    ❌ Error saat login: {e}")
                percobaan += 1
        
        return berhasil
        
    except KeyboardInterrupt:
        print("\n\n    ⚠️  Login dibatalkan")
        pause()
        return False
    except Exception as e:
        print(f"\n    ❌ Error pada fungsi login: {e}")
        pause()
        return False

def logout():
    """Logout dan hapus sesi"""
    global current_user, current_level
    
    clear_screen()
    print_modern_header()
    
    logout_box = PrettyTable()
    logout_box.field_names = ["🔓 LOGOUT"]
    logout_box.add_row(["✓ Sesi API dihapus"])
    logout_box.add_row([f"✓ Logout berhasil. Sampai jumpa, {current_user}!"])
    print(logout_box)
    
    current_user = None
    current_level = None
    pause()

# ==================== MENU FUNCTIONS ====================

def print_auth_menu():
    """Menu login/register"""
    menu = PrettyTable()
    menu.field_names = ["NO", "MENU", "KETERANGAN"]
    menu.add_row(["1", "🔐 LOGIN", "Masuk ke akun Anda"])
    menu.add_row(["2", "📝 REGISTER", "Buat akun baru"])
    menu.add_row(["3", "❌ EXIT", "Keluar dari aplikasi"])
    
    menu.align["NO"] = "c"
    menu.align["MENU"] = "l"
    menu.align["KETERANGAN"] = "l"
    
    print(menu)
    print()


def main_menu():
    """Tampilkan menu utama trading - berbeda untuk admin dan user"""
    clear_screen()
    print_modern_header()
    
    # Buat tabel menggunakan PrettyTable
    table = PrettyTable()
    table.field_names = ["No", "Pilihan Menu"]
    
    # Set alignment
    table.align["No"] = "c"
    table.align["Pilihan Menu"] = "l"
    table.hrules = 1
    
    # Set width kolom
    table.max_width["Pilihan Menu"] = 40
    
    # ✅ MENU UNTUK ADMIN
    if current_level == "admin":
        table.add_row(["1", "📊 Lihat Harga Pasar (Live)"])
        table.add_row(["2", "⚙️  Listing Koin Baru (CRUD)"])
        table.add_row(["3", "📜 Lihat Semua Transaksi (All Users)"])
        table.add_row(["0", "🚪 Keluar & Hapus Sesi"])
    
    # ✅ MENU UNTUK USER
    else:
        table.add_row(["1", "📊 Lihat Harga Pasar (Live)"])
        table.add_row(["2", "💼 Exchange & Wallet"])
        table.add_row(["3", "💰 BUY "])
        table.add_row(["4", "💸 SELL "])
        table.add_row(["5", "📜 Lihat Riwayat Transaksi Saya"])
        table.add_row(["0", "🚪 Keluar & Hapus Sesi"])

    print(table)


# ==================== MARKET FUNCTIONS ====================

def view_market_prices():
    """Lihat harga pasar crypto dengan data real-time"""
    while True:
        clear_screen()
        print_modern_header()
        
        last_updated_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        print("==============================================")
        print("   HARGA PASAR CRYPTOCURRENCY (REAL-TIME)")
        print("==============================================")
        print(f"Data dari: CoinGecko API | Mata Uang: USD")
        print(f"Update Terakhir: {last_updated_time}\n")
        
        # Ambil data real-time dari API
        api_data = get_crypto_prices_from_api()
        
        table_data = []
        
        if api_data:
            for i, (crypto_id, data) in enumerate(api_data.items(), 1):
                display_info = CRYPTO_DISPLAY_MAP.get(crypto_id, {'name': crypto_id.capitalize(), 'symbol': 'N/A'})
                
                name = display_info['name']
                symbol = display_info['symbol']
                price = data.get(VS_CURRENCY, 0.0)
                change_24h = data.get(f'{VS_CURRENCY}_24h_change', 0.0)
                
                if symbol != 'N/A':
                    db["market_prices"][symbol] = price
                
                change_str = format_price_change(change_24h)
                
                table_data.append([
                    i,
                    name,
                    symbol,
                    f"${price:,.4f}",
                    change_str
                ])
            
            save_database()
        else:
            for i, (symbol, price) in enumerate(db["market_prices"].items(), 1):
                name = symbol
                for crypto_id, info in CRYPTO_DISPLAY_MAP.items():
                    if info['symbol'] == symbol:
                        name = info['name']
                        break
                
                change = random.uniform(-10, 10)
                change_str = format_price_change(change)
                
                table_data.append([
                    i,
                    name,
                    symbol,
                    f"${price:,.4f}",
                    change_str + " (simulasi)"
                ])
        
                # ✅ TAMBAHKAN KOIN LOKAL # bagian ini ada 2 tabulate perlu di revisi
        for coin in db.get("local_coins", []):
            current_price = coin.get("price", 0)
            price_24h_ago = coin.get("price_24h_ago", current_price)
            
            if price_24h_ago > 0:
                change_24h = ((current_price - price_24h_ago) / price_24h_ago) * 100
                change_str = format_price_change(change_24h)
            else:
                change_str = "0.00%"
            
            table_data.append([
                len(table_data) + 1,
                coin["name"],
                coin["symbol"],
                f"${current_price:,.4f}",
                change_str + " (Lokal)"
            ])
        
        print(tabulate(table_data, 
                      headers=["No", "Nama", "Simbol", "Harga (USD)", "24h Change"],
                      tablefmt="grid"))
        
        print("\n" + "="*46)
        print("1. Refresh Manual")
        print("2. Auto-Refresh (30 detik)")
        print("0. Kembali ke Menu Utama")
        print("="*46)
        
        choice = input("\nPilih menu: ").strip()
        
        if choice == "1":
            continue
        elif choice == "2":
            auto_refresh_prices()
            break
        elif choice == "0":
            break
        else:
            print("\n✗ Pilihan tidak valid!")
            time.sleep(1)

def auto_refresh_prices():
    """Auto-refresh harga setiap 30 detik"""
    try:
        refresh_count = 0
        while True:
            clear_screen()
            print_modern_header()
            
            last_updated_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            
            print("==============================================")
            print("   AUTO-REFRESH MODE (Tekan Ctrl+C untuk Stop)")
            print("==============================================")
            print(f"Update Terakhir: {last_updated_time}")
            print(f"Refresh ke-{refresh_count + 1}\n")
            
            api_data = get_crypto_prices_from_api()
            
            table_data = []
            
            if api_data:
                for i, (crypto_id, data) in enumerate(api_data.items(), 1):
                    display_info = CRYPTO_DISPLAY_MAP.get(crypto_id, {'name': crypto_id.capitalize(), 'symbol': 'N/A'})
                    
                    name = display_info['name']
                    symbol = display_info['symbol']
                    price = data.get(VS_CURRENCY, 0.0)
                    change_24h = data.get(f'{VS_CURRENCY}_24h_change', 0.0)
                    
                    if symbol != 'N/A':
                        db["market_prices"][symbol] = price
                    
                    change_str = format_price_change(change_24h)
                    
                    table_data.append([
                        i,
                        name,
                        symbol,
                        f"${price:,.4f}",
                        change_str
                    ])
                
                save_database()
            

                        # ✅ TAMBAHKAN KOIN LOKAL # perlu di revisi
            for coin in db.get("local_coins", []):
                current_price = coin.get("price", 0)
                price_24h_ago = coin.get("price_24h_ago", current_price)
                
                if price_24h_ago > 0:
                    change_24h = ((current_price - price_24h_ago) / price_24h_ago) * 100
                    change_str = format_price_change(change_24h)
                else:
                    change_str = "0.00%"
                
                table_data.append([
                    len(table_data) + 1,
                    coin["name"],
                    coin["symbol"],
                    f"${current_price:,.4f}",
                    change_str + " (Lokal)"
                ])
            
            print(tabulate(table_data, 
                          headers=["No", "Nama", "Simbol", "Harga (USD)", "24h Change"],
                          tablefmt="grid"))
            
            print("\nMenunggu 30 detik untuk refresh berikutnya...")
            print("Tekan Ctrl+C untuk kembali ke menu")
            
            time.sleep(30)
            refresh_count += 1
            
    except KeyboardInterrupt:
        print("\n\n✓ Auto-refresh dihentikan")
        pause()

# ==================== WALLET FUNCTIONS ====================

def get_wallet():
    """Ambil wallet user saat ini"""
    return db["users"][current_user]["wallets"]

def deposit_usdt():
    """Deposit USDT ke wallet"""
    print("\n=== DEPOSIT USDT ===")
    try:
        amount = float(input("Jumlah USDT: $"))
        if amount > 0:
            wallet = get_wallet()
            wallet["USDT"] = wallet.get("USDT", 0) + amount
            save_database()
            print(f"\n✓ Berhasil deposit ${amount:,.2f} USDT")
        else:
            print("\n✗ Jumlah harus lebih dari 0")
    except ValueError:
        print("\n✗ Input tidak valid!")
    
    pause()
    view_wallet()

def withdraw():
    """Withdraw dari wallet"""
    print("\n=== WITHDRAW ===")
    
    wallet = get_wallet()
    crypto = input("Aset yang ingin di-withdraw: ").upper().strip()
    
    if crypto not in wallet:
        print(f"\n✗ Anda tidak memiliki {crypto}")
        pause()
        return
    
    try:
        amount = float(input(f"Jumlah {crypto}: "))
        
        if amount <= 0:
            print("\n✗ Jumlah harus lebih dari 0")
        elif amount > wallet[crypto]:
            print(f"\n✗ Saldo tidak cukup! Saldo Anda: {wallet[crypto]:.8f} {crypto}")
        else:
            wallet[crypto] -= amount
            save_database()
            print(f"\n✓ Berhasil withdraw {amount:.8f} {crypto}")
    except ValueError:
        print("\n✗ Input tidak valid!")
    
    pause()
    view_wallet()

def view_wallet():
    """Lihat wallet dan saldo"""
    clear_screen()
    print_modern_header()
    print("=== EXCHANGE & WALLET ===\n")
    
    wallet = get_wallet()
    
    table_data = []
    total_usd = 0
    
    for i, (crypto, balance) in enumerate(wallet.items(), 1):
        if crypto == "USDT":
            value_usd = balance
        else:
            price = db["market_prices"].get(crypto, 0)
            value_usd = balance * price
        
        total_usd += value_usd
        
        table_data.append([
            i,
            crypto,
            f"{balance:.8f}",
            f"${value_usd:,.2f}"
        ])
    
    print(tabulate(table_data,
                  headers=["No", "Aset", "Saldo", "Nilai (USD)"],
                  tablefmt="grid"))
    
    print(f"\n{'='*50}")
    print(f"Total Portfolio: ${total_usd:,.2f}")
    print(f"{'='*50}")
    
    print("\n1. Deposit USDT")
    print("2. Withdraw")
    print("0. Kembali")
    
    choice = input("\nPilih menu: ").strip()
    
    if choice == "1":
        deposit_usdt()
    elif choice == "2":
        withdraw()

# ==================== ORDER FUNCTIONS ====================

def create_buy_order():
    """Buat order beli dengan tampilan market prices yang menarik"""
    clear_screen()
    print_modern_header()
    
    # Header
    header = PrettyTable()
    header.field_names = ["💰 BUY ORDER - INSTANT PURCHASE 💰"]
    header.add_row(["Beli cryptocurrency dengan harga pasar terkini"])
    print(header)
    print()
    
    # Update harga dari API
    print("🔄 Mengambil data harga real-time dari CoinGecko...")
    update_result = update_market_prices_from_api()
    if update_result:
        print("✓ Harga pasar berhasil diperbarui dari API!\n")
    else:
        print("⚠️ Menggunakan harga terakhir dari database\n")
    
    # Tampilkan harga pasar dengan PrettyTable
    market_table = PrettyTable()
    market_table.field_names = ["No", "Crypto", "Symbol", "Price (USD)", "Status"]
    market_table.hrules = 1 
    
    # Tambahkan crypto dari API
    coin_list = []
    for i, (symbol, price) in enumerate(list(db["market_prices"].items())[:8], 1):
        # Cari nama lengkap
        crypto_name = symbol
        for crypto_id, info in CRYPTO_DISPLAY_MAP.items():
            if info['symbol'] == symbol:
                crypto_name = info['name']
                break
        
        market_table.add_row([
            i,
            crypto_name,
            symbol,
            f"${price:,.4f}",
            "🟢 Live"
        ])
        coin_list.append(symbol)
    
    # Tambahkan koin lokal
    for coin in db.get("local_coins", []):
        i += 1
        market_table.add_row([
            i,
            coin["name"],
            coin["symbol"],
            f"${coin.get('price', 0):,.4f}",
            "🔵 Local"
        ])
        coin_list.append(coin["symbol"])
    
    market_table.align["No"] = "c"
    market_table.align["Crypto"] = "l"
    market_table.align["Symbol"] = "c"
    market_table.align["Price (USD)"] = "r"
    market_table.align["Status"] = "c"
    
    print(market_table)
    print()
    
    # Info Wallet
    wallet = get_wallet()
    usdt_balance = wallet.get("USDT", 0)
    
    wallet_info = PrettyTable()
    wallet_info.field_names = ["💼 YOUR WALLET"]
    wallet_info.hrules = 1
    wallet_info.add_row([f"USDT Balance: ${usdt_balance:,.2f}"])
    print(wallet_info)
    print()
    
    # Input
    print("─" * 60)
    crypto = input(" 🪙  Crypto yang ingin dibeli (Symbol): ").upper().strip()
    
    if crypto not in coin_list:
        print(f"\n❌ {crypto} tidak tersedia di pasar")
        pause()
        return
    
    try:
        amount = float(input(f"📦 Jumlah {crypto}: "))
        
        if amount <= 0:
            print("\n❌ Jumlah harus lebih dari 0!")
            pause()
            return
        
        price = db["market_prices"].get(crypto, 0)
        total_cost = amount * price
        
        # Preview Order dengan PrettyTable
        print()
        preview = PrettyTable()
        preview.field_names = ["📋 ORDER SUMMARY", ""]
        preview.add_row(["Crypto", crypto])
        preview.add_row(["Amount", f"{amount:.8f} {crypto}"])
        preview.add_row(["Price", f"${price:,.4f}"])
        preview.add_row(["─────────", "─────────"])
        preview.add_row(["💳 Total Cost", f"${total_cost:,.2f} USDT"])
        preview.add_row(["💰 Your Balance", f"${usdt_balance:,.2f} USDT"])
        
        if total_cost <= usdt_balance:
            remaining = usdt_balance - total_cost
            preview.add_row(["✅ Remaining", f"${remaining:,.2f} USDT"])
        else:
            deficit = total_cost - usdt_balance
            preview.add_row(["❌ Deficit", f"${deficit:,.2f} USDT"])
        
        preview.align["📋 ORDER SUMMARY"] = "l"
        preview.hrules = 1 
        preview.align[""] = "r"
        print(preview)
        print()
        
        # Validasi saldo
        if total_cost > usdt_balance:
            error = PrettyTable()
            error.field_names = ["❌ INSUFFICIENT BALANCE"]
            error.hrules = 1
            error.add_row([f"You need ${total_cost - usdt_balance:,.2f} more USDT"])
            error.add_row(["Please deposit or reduce amount"])
            print(error)
            pause()
            return
        
        # Konfirmasi
        confirm = input("✅ Konfirmasi order BUY? (y/n): ").lower()
        
        if confirm == 'y':
            # Eksekusi order
            wallet["USDT"] -= total_cost
            wallet[crypto] = wallet.get(crypto, 0) + amount
            
            transaction = {
                "id": len(db["transactions"]) + 1,
                "user": current_user,
                "type": "BUY",
                "crypto": crypto,
                "amount": amount,
                "price": price,
                "total": total_cost,
                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "status": "COMPLETED"
            }
            
            db["transactions"].append(transaction)
            save_database()
            
            # Success message
            print()
            success = PrettyTable()
            success.field_names = ["✅ ORDER EXECUTED SUCCESSFULLY"]
            success.hrules = 1
            success.add_row([f"Bought {amount:.8f} {crypto}"])
            success.add_row([f"Total: ${total_cost:,.2f} USDT"])
            success.add_row([f"Transaction ID: #{transaction['id']}"])
            print(success)
        else:
            print()
            cancel = PrettyTable()
            cancel.field_names = ["❌ ORDER CANCELLED"]
            cancel.hrules = 1
            cancel.add_row(["Transaction has been cancelled"])
            print(cancel)
            
    except ValueError:
        print("\n❌ Input tidak valid!")
    except Exception as e:
        print(f"\n❌ Error: {e}")
    
    pause()

def create_sell_order():
    """Buat order jual dengan tampilan portfolio yang menarik"""
    clear_screen()
    print_modern_header()
    
    # Header
    header = PrettyTable()
    header.field_names = ["💸 SELL ORDER - INSTANT SELL 💸"]
    header.add_row(["Jual cryptocurrency Anda dengan harga pasar terkini"])
    print(header)
    print()
    
    # Update harga dari API
    print("🔄 Mengambil data harga real-time dari CoinGecko...")
    update_result = update_market_prices_from_api()
    if update_result:
        print("✓ Harga pasar berhasil diperbarui dari API!\n")
    else:
        print("⚠️ Menggunakan harga terakhir dari database\n")
    
    wallet = get_wallet()
    
    # Tampilkan portfolio (aset yang dimiliki)
    portfolio_table = PrettyTable()
    portfolio_table.field_names = ["No", "Crypto", "Your Balance", "Current Price", "Total Value"]
    portfolio_table.hrules = 1
    
    available_cryptos = []
    portfolio_items = []
    
    for crypto, balance in wallet.items():
        if crypto != "USDT" and balance > 0:
            price = db["market_prices"].get(crypto, 0)
            total_value = balance * price
            portfolio_items.append((crypto, balance, price, total_value))
            available_cryptos.append(crypto)
    
    if not available_cryptos:
        print("❌ Anda tidak memiliki cryptocurrency untuk dijual")
        print("💡 Silakan beli terlebih dahulu di menu BUY\n")
        pause()
        return
    
    # Sort by total value (highest first)
    portfolio_items.sort(key=lambda x: x[3], reverse=True)
    
    for i, (crypto, balance, price, total_value) in enumerate(portfolio_items, 1):
        portfolio_table.add_row([
            i,
            crypto,
            f"{balance:.8f}",
            f"${price:,.4f}",
            f"${total_value:,.2f}"
        ])
    
    portfolio_table.align["No"] = "c"
    portfolio_table.align["Crypto"] = "c"
    portfolio_table.align["Your Balance"] = "r"
    portfolio_table.align["Current Price"] = "r"
    portfolio_table.align["Total Value"] = "r"
    
    print(portfolio_table)
    
    # Total portfolio value
    total_crypto_value = sum(item[3] for item in portfolio_items)
    usdt_balance = wallet.get("USDT", 0)
    total_portfolio = total_crypto_value + usdt_balance
    
    print()
    summary = PrettyTable()
    summary.field_names = ["💼 PORTFOLIO SUMMARY", "VALUE"]
    summary.hrules = 1 
    summary.add_row(["Crypto Assets", f"${total_crypto_value:,.2f}"])
    summary.add_row(["USDT Balance", f"${usdt_balance:,.2f}"])
    summary.add_row(["─────────────", "─────────────"])
    summary.add_row(["💰 Total Portfolio", f"${total_portfolio:,.2f}"])
    summary.align["💼 PORTFOLIO SUMMARY"] = "l"
    summary.align["VALUE"] = "r"
    print(summary)
    print()
    
    # Input
    print("─" * 60)
    crypto = input("🪙 Crypto yang ingin dijual (Symbol): ").upper().strip()
    
    if crypto not in available_cryptos:
        print(f"\n❌ Anda tidak memiliki {crypto} atau saldo 0")
        pause()
        return
    
    try:
        current_balance = wallet[crypto]
        print(f"📦 Saldo {crypto} Anda: {current_balance:.8f}")
        
        amount = float(input(f"📦 Jumlah {crypto} yang dijual: "))
        
        if amount <= 0:
            print("\n❌ Jumlah harus lebih dari 0!")
            pause()
            return
        
        if amount > current_balance:
            print(f"\n❌ Saldo tidak cukup! Maksimal: {current_balance:.8f} {crypto}")
            pause()
            return
        
        price = db["market_prices"].get(crypto, 0)
        total_receive = amount * price
        
        # Preview Order dengan PrettyTable
        print()
        preview = PrettyTable()
        preview.field_names = ["📋 SELL ORDER SUMMARY", ""]
        preview.hrules = 1 
        preview.add_row(["Crypto", crypto])
        preview.add_row(["Amount to Sell", f"{amount:.8f} {crypto}"])
        preview.add_row(["Current Price", f"${price:,.4f}"])
        preview.add_row(["─────────────", "─────────────"])
        preview.add_row(["💵 You Will Receive", f"${total_receive:,.2f} USDT"])
        preview.add_row(["📊 Remaining Balance", f"{current_balance - amount:.8f} {crypto}"])
        preview.add_row(["💰 New USDT Balance", f"${usdt_balance + total_receive:,.2f}"])
        
        preview.align["📋 SELL ORDER SUMMARY"] = "l"
        preview.align[""] = "r"
        print(preview)
        print()
        
        # Konfirmasi
        confirm = input("✅ Konfirmasi order SELL? (y/n): ").lower()
        
        if confirm == 'y':
            # Eksekusi order
            wallet[crypto] -= amount
            wallet["USDT"] = wallet.get("USDT", 0) + total_receive
            
            transaction = {
                "id": len(db["transactions"]) + 1,
                "user": current_user,
                "type": "SELL",
                "crypto": crypto,
                "amount": amount,
                "price": price,
                "total": total_receive,
                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "status": "COMPLETED"
            }
            
            db["transactions"].append(transaction)
            save_database()
            
            # Success message
            print()
            success = PrettyTable()
            success.field_names = ["✅ ORDER EXECUTED SUCCESSFULLY"]
            success.hrules = 1
            success.add_row([f"Sold {amount:.8f} {crypto}"])
            success.add_row([f"Received: ${total_receive:,.2f} USDT"])
            success.add_row([f"Transaction ID: #{transaction['id']}"])
            print(success)
        else:
            print()
            cancel = PrettyTable()
            cancel.field_names = ["❌ ORDER CANCELLED"]
            cancel.hrules = 1
            cancel.add_row(["Transaction has been cancelled"])
            print(cancel)
            
    except ValueError:
        print("\n❌ Input tidak valid!")
    except Exception as e:
        print(f"\n❌ Error: {e}")
    
    pause()

def view_transaction_history():
    """Lihat riwayat transaksi - Admin lihat semua, User lihat miliknya"""
    clear_screen()
    print_modern_header()
    
    # ✅ ADMIN: Lihat semua transaksi
    if current_level == "admin":
        print("=== SEMUA RIWAYAT TRANSAKSI (ALL USERS) ===\n")
        
        if not db["transactions"]:
            print("    📭 Belum ada transaksi dari semua user")
        else:
            table_data = []
            for trans in reversed(db["transactions"][-50:]):  # 50 transaksi terakhir
                table_data.append([
                    trans["id"],
                    trans["user"],  # Tampilkan username
                    trans["timestamp"],
                    trans["type"],
                    trans["crypto"],
                    f"{trans['amount']:.8f}",
                    f"${trans['price']:,.4f}",
                    f"${trans['total']:,.2f}",
                    trans["status"]
                ])
            
            print(tabulate(table_data,
                          headers=["ID", "User", "Waktu", "Type", "Crypto", "Amount", "Price", "Total", "Status"],
                          tablefmt="grid"))
            
            print(f"\n📊 Total Transaksi: {len(db['transactions'])}")
    
    # ✅ USER: Lihat transaksi miliknya sendiri
    else:
        print("=== RIWAYAT TRANSAKSI SAYA ===\n")
        
        user_transactions = [t for t in db["transactions"] 
                           if t["user"] == current_user]
        
        if not user_transactions:
            print("    📭 Belum ada transaksi")
        else:
            table_data = []
            for trans in reversed(user_transactions[-20:]):  # 20 transaksi terakhir
                table_data.append([
                    trans["id"],
                    trans["timestamp"],
                    trans["type"],
                    trans["crypto"],
                    f"{trans['amount']:.8f}",
                    f"${trans['price']:,.4f}",
                    f"${trans['total']:,.2f}",
                    trans["status"]
                ])
            
            print(tabulate(table_data,
                          headers=["ID", "Waktu", "Type", "Crypto", "Amount", "Price", "Total", "Status"],
                          tablefmt="grid"))
            
            print(f"\n📊 Total Transaksi Anda: {len(user_transactions)}")
    
    pause()

# ==================== MAIN PROGRAM ====================

def run_trading_menu():
    """Menu trading setelah login"""
    # Update harga dari API saat pertama login
    print("\n🔄 Memperbarui harga pasar dari CoinGecko API...")
    update_market_prices_from_api()
    time.sleep(2)
    
    while True:
        main_menu()
        choice = input("\n    🎯 Pilih menu: ").strip()
        
        # ✅ MENU ADMIN
        if current_level == "admin":
            if choice == "1":
                view_market_prices()
            elif choice == "2":
                manage_local_coins()
            elif choice == "3":
                view_transaction_history()
            elif choice == "0":
                logout()
                break
            else:
                print("\n    ❌ Pilihan tidak valid!")
                pause()
        
        # ✅ MENU USER
        else:
            if choice == "1":
                view_market_prices()
            elif choice == "2":
                view_wallet()
            elif choice == "3":
                create_buy_order()
            elif choice == "4":
                create_sell_order()
            elif choice == "5":
                view_transaction_history()
            elif choice == "0":
                logout()
                break
            else:
                print("\n    ❌ Pilihan tidak valid!")
                pause()

def main():
    """Program utama"""
    global current_user, current_level
    
    # Load database
    load_database()
    
    while True:
        try:
            print_modern_header()
            print_auth_menu()
            
            choice = input("    🎯 Pilih Menu [1-3]: ").strip()
            
            if choice == '1':
                if login():
                    # Success message
                    success = PrettyTable()
                    success.field_names = ["✅ LOGIN BERHASIL"]
                    success.add_row([f"Selamat datang! Login sebagai {current_level.upper()}"])
                    print()
                    print(success)
                    time.sleep(2)
                    
                    # Masuk ke menu trading
                    run_trading_menu()
                    
            elif choice == '2':
                register()
                
            elif choice == '3':
                clear_screen()
                print_modern_header()
                
                exit_box = PrettyTable()
                exit_box.field_names = ["👋 TERIMA KASIH"]
                exit_box.add_row(["Terima kasih telah menggunakan"])
                exit_box.add_row(["Crypto Trading Terminal v2.0"])
                exit_box.add_row(["🪙 Stay Safe, Trade Smart! 🪙"])
                print(exit_box)
                print()
                
                time.sleep(1)
                break
                
            else:
                error = PrettyTable()
                error.field_names = ["⚠️ ERROR"]
                error.add_row(["Pilihan tidak valid! Silakan pilih 1-3"])
                print()
                print(error)
                time.sleep(1.5)
                
        except KeyboardInterrupt:
            print("\n\n    ⚠️  Program dihentikan oleh user")
            print("    👋 Goodbye!\n")
            break
        except Exception as e:
            error_table = PrettyTable()
            error_table.field_names = ["❌ ERROR"]
            error_table.add_row([f"Terjadi kesalahan: {e}"])
            print()
            print(error_table)
            time.sleep(2)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n    ⚠️  Program terminated by user")
        print("    👋 Goodbye!\n")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ Terjadi error: {e}")
        pause()
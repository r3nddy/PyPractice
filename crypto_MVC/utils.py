"""
Utils: Helper Functions & Animations
Fungsi bantuan dan animasi
"""

import os
import sys
import time
from config import MIN_USERNAME_LENGTH, MIN_PASSWORD_LENGTH


# ==================== HELPER FUNCTIONS ====================

def clear_screen():
    """Clear terminal screen"""
    os.system('cls' if os.name == 'nt' else 'clear')


def pause():
    """Pause dan tunggu user menekan Enter"""
    input("\n    [Tekan Enter untuk melanjutkan...]")


def format_price_change(change):
    """Format perubahan harga dengan tanda"""
    if change > 0:
        return f"+{change:.2f}%"
    else:
        return f"{change:.2f}%"


def validate_username(username):
    """Validasi username"""
    if not username or username.strip() == "":
        return False, "Username tidak boleh kosong"
    
    if len(username) < MIN_USERNAME_LENGTH:
        return False, f"Username minimal {MIN_USERNAME_LENGTH} karakter"
    
    return True, "Valid"


def validate_password(password):
    """Validasi password"""
    if not password or password.strip() == "":
        return False, "Password tidak boleh kosong"
    
    if len(password) < MIN_PASSWORD_LENGTH:
        return False, f"Password minimal {MIN_PASSWORD_LENGTH} karakter"
    
    return True, "Valid"


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


def progress_bar(message="Processing", duration=1):
    """Progress bar generik"""
    print()
    for i in range(101):
        filled = int(20 * i / 100)
        bar = '█' * filled + '░' * (20 - filled)
        sys.stdout.write(f'\r    {message}: [{bar}] {i}%')
        sys.stdout.flush()
        time.sleep(duration / 100)
    print("\n")
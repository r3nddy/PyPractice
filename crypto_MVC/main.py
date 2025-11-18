"""
Main Entry Point
Crypto Trading Terminal v2.0
"""

import sys
import time
from prettytable import PrettyTable

from config import SESSION
from database import load_database
from auth import login, register, logout
from menu import print_header, print_auth_menu, main_menu
from trading import (
    view_market_prices, 
    create_buy_order, 
    create_sell_order,
    view_wallet,
    manage_local_coins,
    view_transaction_history,
    update_market_prices_from_api
)
from utils import clear_screen, pause


def run_trading_menu():
    """Menu trading setelah login"""
    # Update harga dari API saat pertama login
    print("\n🔄 Memperbarui harga pasar dari CoinGecko API...")
    update_market_prices_from_api()
    time.sleep(2)
    
    while True:
        main_menu()
        choice = input("\n    🎯 Pilih menu: ").strip()
        
        # MENU ADMIN
        if SESSION['current_level'] == "admin":
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
        
        # MENU USER
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
    # Load database
    load_database()
    
    while True:
        try:
            print_header()
            print_auth_menu()
            
            choice = input("    🎯 Pilih Menu [1-3]: ").strip()
            
            if choice == '1':
                if login():
                    # Success message
                    success = PrettyTable()
                    success.field_names = ["✅ LOGIN BERHASIL"]
                    success.add_row([f"Selamat datang! Login sebagai {SESSION['current_level'].upper()}"])
                    print()
                    print(success)
                    time.sleep(2)
                    
                    # Masuk ke menu trading
                    run_trading_menu()
                    
            elif choice == '2':
                register()
                
            elif choice == '3':
                clear_screen()
                print_header()
                
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
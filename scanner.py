import sys
import argparse
from colorama import Fore, Style, init

# initialisation de colorama pour l'affichage coloré [cite: 34, 74]
init(autoreset=True)

def main():
    print(f"{Fore.CYAN}{Style.BRIGHT}=== XYBERSCAN v1.0 - Communauté Xyberclan ==={Style.RESET_ALL}")
    
    # configuration de l'argument URL 
    parser = argparse.ArgumentParser(description="Scanner de vulnérabilités web")
    parser.add_argument("url", help="L'URL du site à scanner (ex: https://monsite.com)")
    args = parser.parse_args()
    
    print(f"[*] Analyse lancée pour : {args.url}...")
    
    # Emplacement futur pour l'appel des differents modules 
    # - modules/headers.py
    # - modules/ssl_check.py
    # - modules/ports.py
    # - modules/sensitive.py

if __name__ == "__main__":
    main()
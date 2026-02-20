import subprocess
import sys

def install_if_missing(packages):
    for package, import_name in packages.items():
        try:
            __import__(import_name)
        except ImportError:
            print(f"Installing {package}...")
            result = subprocess.run(
                [sys.executable, "-m", "pip", "install", package],
                capture_output=True, text=True
            )
            if result.returncode != 0:
                print(f"Failed to install {package}. Error:\n{result.stderr}")
                sys.exit(1)

install_if_missing({
    "msoffcrypto-tool": "msoffcrypto",
    "pandas": "pandas",
    "openpyxl": "openpyxl",
    "pyperclip": "pyperclip",
})

import msoffcrypto
import io
import pandas as pd
import pyperclip
import time
import os
from datetime import datetime                                    # NEW

OUTDATED_DAYS = 90                                              # NEW

def load_encrypted_excel(filepath, password_file='encryption_pass.txt'):
    """Decrypt and load Excel file"""
    script_dir = os.path.dirname(os.path.abspath(__file__))
    password_path = os.path.join(script_dir, password_file)
    
    with open(password_path, 'r') as f:
        password = f.read().strip()
    
    decrypted = io.BytesIO()
    with open(filepath, 'rb') as f:
        file = msoffcrypto.OfficeFile(f)
        file.load_key(password=password)
        file.decrypt(decrypted)
    
    decrypted.seek(0)
    return pd.read_excel(decrypted)

def search(df, query):
    """Find matching entries"""
    q = query.lower()
    matches = []
    
    for idx, row in df.iterrows():
        if q in str(row['Service / Website']).lower() or q in str(row['Username']).lower():
            matches.append({
                'index': idx,
                'service': row['Service / Website'],
                'username': row['Username'],
                'password': row['Password'],
                'timestamp': row['Timestamp']
            })
    
    return matches

def check_outdated(timestamp) -> str | None:                    # NEW
    """Return a warning string if the password is older than OUTDATED_DAYS, else None."""
    try:
        last_updated = pd.to_datetime(timestamp)
        days_old = (datetime.now() - last_updated).days
        if days_old >= OUTDATED_DAYS:
            return f"⚠ Password last updated {days_old} days ago. Consider updating it."
    except Exception:
        return "⚠ Could not parse timestamp. Please verify this entry."
    return None

def display_and_copy(match, df):
    """Show entry details and copy password"""
    os.system('cls' if os.name == 'nt' else 'clear')
    print("=" * 50)
    
    row = df.iloc[match['index']]
    for col, val in row.items():
        if col == 'Timestamp':                                  # NEW
            continue                                            # NEW
        if pd.notna(val) and str(val).strip():
            display = '*' * len(str(val)) if 'password' in col.lower() else val
            print(f"{col}: {display}")
    
    print("=" * 50)

    warning = check_outdated(match['timestamp'])
    if warning:
        print(f"\n{warning}")

    pyperclip.copy(match['password'])
    print("\n✓ Password copied to clipboard!")
    time.sleep(5)

if __name__ == "__main__":
    df = load_encrypted_excel('C:\\Users\\JM\\Desktop\\Treasury\\Passwords.xlsx')
    
    query = input("Service: ")
    results = search(df, query)
    
    if not results:
        print("No matches found.")
        exit()
    
    for i, match in enumerate(results, 1):
        print(f"{i}. {match['service']} ({match['username']})")
    
    if len(results) == 1:
        selected = results[0]
    else:
        choice = int(input(f"\nSelect (1-{len(results)}): ")) - 1
        selected = results[choice]
    
    display_and_copy(selected, df)
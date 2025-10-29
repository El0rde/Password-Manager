import msoffcrypto
import io
import pandas as pd
import pyperclip

# Decrypt the file
decrypted = io.BytesIO()

with open('encryption_pass.txt', 'r') as f:
    content = f.read()

with open('C:\\Users\\LENOVO T14\\Desktop\\College\\Passwords.xlsx', 'rb') as f:
    file = msoffcrypto.OfficeFile(f)
    file.load_key(password=content)  
    file.decrypt(decrypted)


decrypted.seek(0)
df = pd.read_excel(decrypted)
print("✓ File loaded successfully! \033c")

def search(query):
    """Search for matching query"""
    query_lower = query.lower()

    matches = []

    for index, row in df.iterrows():
        service = str(row['Service / Website'])
        username = str(row['Username'])

        if query_lower in service.lower() or query_lower in username.lower():
            matches.append({
                'index': index,
                "service": service,
                "username": row['Username'],
                'password': row['Password'],
                'time': row['Timestamp']
            })
            
    return matches

def show_contents(selected, df):
    if selected is None:
        return

    # Show details and copy password
    print("\033c" + "="*50)

    row = df.iloc[selected['index']]

    for column in df.columns:
        value = row[column]

        if pd.notna(value) and str(value).strip() != '':
            if 'password' in column.lower():
                display_value = '*' * len(str(value))
            else:
                display_value = value
            
            print(f"{column}: {display_value}")
            if column == 'Password':
                print('')

            if column == 'Timestamp':
                # if time 
                pass

    print("="*50)
    pyperclip.copy(selected['password'])
    # print("\n✓ Password copied to clipboard!")

if __name__ == "__main__":
    search_query = input("Service: ")
    results = search(search_query)

    if len(results) == 0:
        print("No matches found.")
    else:
        for i, match in enumerate(results, 1):
            print(f"{i}. {match['service']} ({match['username']})")

        if len(results) == 1:
            selected = results[0]
        else:
            choice = input(f"\nSelect (1-{len(results)}): ")
            selected = results[int(choice) - 1]

        show_contents(selected, df)

        


# ==================================================

# Print Columns
# print("\nYour columns are:")
# for i, col in enumerate(df.columns, 1):
#     print(f"  {i}. {col}")


# print("\n" + "="*50)
# print("Example entry (first row):")
# print("="*50)
# for col in df.columns:
#     if pd.notna(df[col][0]):
#         if (col == "Password"):
#             pyperclip.copy(df[col][0])
#             print("\n✓ Password copied to clipboard!")
#         else:
#             print(f"{col}: {df[col][0]}")

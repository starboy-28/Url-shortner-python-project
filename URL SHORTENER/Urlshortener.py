import sqlite3
import string
import random

# Create a SQLite database to store URL mappings
conn = sqlite3.connect("url_shortener.db")
cursor = conn.cursor()

# Create a table to store the mappings
cursor.execute('''CREATE TABLE IF NOT EXISTS url_map (
                  id INTEGER PRIMARY KEY AUTOINCREMENT,
                  short_code TEXT UNIQUE,
                  long_url TEXT
               )''')

# Function to generate a random short code
def generate_short_code():
    characters = string.ascii_letters + string.digits
    short_code = ''.join(random.choice(characters) for _ in range(6))
    return short_code

# Function to shorten a URL
def shorten_url(long_url):
    cursor.execute("INSERT OR IGNORE INTO url_map (short_code, long_url) VALUES (?, ?)", (generate_short_code(), long_url))
    conn.commit()

# Function to expand a short URL
def expand_url(short_code):
    cursor.execute("SELECT long_url FROM url_map WHERE short_code = ?", (short_code,))
    result = cursor.fetchone()
    if result:
        return result[0]
    else:
        return None

# Main program
if __name__ == "__main__":
    while True:
        print("1. Shorten URL")
        print("2. Expand URL")
        print("3. Exit")
        choice = input("Enter your choice: ")

        if choice == "1":
            long_url = input("Enter the long URL: ")
            shorten_url(long_url)
            print("Shortened URL: http://yourshortener.com/" + generate_short_code())
        elif choice == "2":
            short_code = input("Enter the short code: ")
            long_url = expand_url(short_code)
            if long_url:
                print("Long URL: " + long_url)
            else:
                print("URL not found.")
        elif choice == "3":
            conn.close()
            break
        else:
            print("Invalid choice. Please try again.")


import sqlite3

DATABASE = 'database.db'

# Function to insert links into the redirects table
def add_links():
    links = [
        {
            "dest_link": f"https://example{num}.com",
            "custom_link": f"custom{num}"
        } for num in range(1, 31)
    ]

    with sqlite3.connect(DATABASE) as conn:
        cursor = conn.cursor()
        for link in links:
            try:
                cursor.execute(
                    'INSERT INTO redirects (dest_link, custom_link) VALUES (?, ?)',
                    (link["dest_link"], link["custom_link"])
                )
            except sqlite3.IntegrityError:
                print(f"Custom link {link['custom_link']} already exists.")
        conn.commit()
        print(f"Added {len(links)} links to the database.")

if __name__ == "__main__":
    add_links()

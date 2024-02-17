import os
import sqlite3
import shutil
from rsa import newkeys
from pathlib import Path

def create_database(db_path: str) -> bool:
    """
    Create a SQLite database with the necessary table.
    """
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        cursor.execute('''CREATE TABLE IF NOT EXISTS keys (
                            id INTEGER PRIMARY KEY,
                            keypart TEXT
                          )''')

        conn.commit()
        conn.close()
        return True
    except Exception as e:
        print(f"Error creating database: {e}")
        return False

def create_keychain(re_create: bool, keychain_dir: str, db_filename: str) -> bool:
    """
    Create a keychain directory and keys database if they don't exist.
    """
    try:
        if re_create and os.path.exists(keychain_dir):
            shutil.rmtree(keychain_dir)

        os.makedirs(keychain_dir)

        db_path = os.path.join(keychain_dir, f"{db_filename}.db")
        return create_database(db_path)
    except Exception as e:
        print(f"Error creating keychain: {e}")
        return False

def generate_keys(key_size: int, re_create: bool, db_filename: str = "keys") -> bool:
    """
    Generate RSA keys and store them in the database.
    """
    try:
        home_dir = str(Path.home())
        keychain_dir = os.path.join(home_dir, ".keychain")

        if create_keychain(re_create, keychain_dir, db_filename):
            db_path = os.path.join(keychain_dir, f"{db_filename}.db")

            public_key, private_key = newkeys(key_size)

            conn = sqlite3.connect(db_path)
            cursor = conn.cursor()

            # Insert keys into the database
            cursor.execute("INSERT INTO keys (id, keypart) VALUES (?, ?)", (1, str(public_key.n)))
            cursor.execute("INSERT INTO keys (id, keypart) VALUES (?, ?)", (2, str(public_key.e)))
            cursor.execute("INSERT INTO keys (id, keypart) VALUES (?, ?)", (3, str(private_key.d)))
            cursor.execute("INSERT INTO keys (id, keypart) VALUES (?, ?)", (4, str(private_key.p)))
            cursor.execute("INSERT INTO keys (id, keypart) VALUES (?, ?)", (5, str(private_key.q)))

            conn.commit()
            conn.close()
            return True
        else:
            return False
    except Exception as e:
        print(f"Error generating keys: {e}")
        return False

import os
import sqlite3
from pathlib import Path
from rsa import PublicKey, PrivateKey, encrypt, decrypt
from typing import Union

def load_public_key(db_filename: str = "keys") -> Union[PublicKey, None]:
    """
    Load the public key from the database.
    """
    try:
        home_dir = str(Path.home())
        db_path = os.path.join(home_dir, ".keychain", f"{db_filename}.db")
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        cursor.execute("SELECT keypart FROM keys WHERE id = 1")
        n = int(cursor.fetchone()[0])

        cursor.execute("SELECT keypart FROM keys WHERE id = 2")
        e = int(cursor.fetchone()[0])

        conn.close()

        public_key = PublicKey(n, e)
        return public_key
    except Exception as e:
        print(f"Error loading public key: {e}")
        return None

def load_private_key(db_filename: str = "keys") -> Union[PrivateKey, None]:
    """
    Load the private key from the database.
    """
    try:
        home_dir = str(Path.home())
        db_path = os.path.join(home_dir, ".keychain", f"{db_filename}.db")
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        cursor.execute("SELECT keypart FROM keys WHERE id = 1")
        n = int(cursor.fetchone()[0])

        cursor.execute("SELECT keypart FROM keys WHERE id = 2")
        e = int(cursor.fetchone()[0])

        cursor.execute("SELECT keypart FROM keys WHERE id = 3")
        d = int(cursor.fetchone()[0])

        cursor.execute("SELECT keypart FROM keys WHERE id = 4")
        p = int(cursor.fetchone()[0])

        cursor.execute("SELECT keypart FROM keys WHERE id = 5")
        q = int(cursor.fetchone()[0])

        conn.close()

        private_key = PrivateKey(n, e, d, p, q)
        return private_key
    except Exception as e:
        print(f"Error loading private key: {e}")
        return None

def encrypt_message(message: str, db_filename: str = "keys") -> Union[bytes, None]:
    """
    Encrypt a message using the public key.
    """
    try:
        public_key = load_public_key(db_filename)
        if public_key:
            encrypted_message = encrypt(message.encode('utf-8'), public_key)
            return encrypted_message
        else:
            return None
    except Exception as e:
        print(f"Error encrypting message: {e}")
        return None

def decrypt_message(encrypted_message: bytes, db_filename: str = "keys") -> Union[str, None]:
    """
    Decrypt a message using the private key.
    """
    try:
        private_key = load_private_key(db_filename)
        if private_key:
            decrypted_message = decrypt(encrypted_message, private_key)
            return decrypted_message.decode('utf-8')
        else:
            return None
    except Exception as e:
        print(f"Error decrypting message: {e}")
        return None

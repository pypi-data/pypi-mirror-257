# pysqlitecrypto_rsa

This package provides functionality for managing RSA keys and encrypting/decrypting messages using SQLite databases.

## Functions Available for Import

### Keychain Operations

#### `generate_keys(key_size: int, re_create: bool, db_filename: str = "keys") -> bool`

Generates RSA keys and stores them in an SQLite database.

- `key_size`: The size of the RSA keys to be generated.
- `re_create`: Whether to recreate the keychain directory and database if they already exist.
- `db_filename`: The name of the database file. Defaults to "keys".

### Encryption Operations

#### `encrypt_message(message: str, db_filename: str = "keys") -> Union[bytes, None]`

Encrypts a message using the public key stored in the specified database.

- `message`: The message to be encrypted.
- `db_filename`: The name of the database file. Defaults to "keys".

#### `decrypt_message(encrypted_message: bytes, db_filename: str = "keys") -> Union[str, None]`

Decrypts an encrypted message using the private key stored in the specified database.

- `encrypted_message`: The encrypted message to be decrypted.
- `db_filename`: The name of the database file. Defaults to "keys".

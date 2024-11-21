import socket

# Fungsi untuk enkripsi dan dekripsi RSA sederhana
def rsa_encrypt(message, public_key):
    n, e = public_key
    return [pow(ord(char), e, n) for char in message]

def rsa_decrypt(encrypted_message, private_key):
    n, d = private_key
    return ''.join([chr(pow(char, d, n)) for char in encrypted_message])

# Fungsi untuk dekripsi DES
def des_decrypt(encrypted_message, key):
    return bytes([byte ^ key[i % len(key)] for i, byte in enumerate(encrypted_message)])

# RSA Keys (contoh sederhana)
PUBLIC_KEY = (3233, 17)  # (n, e)
PRIVATE_KEY = (3233, 2753)  # (n, d)

HOST = '127.0.0.1'
PORT = 65432

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen()
    print("Server is listening...")

    conn, addr = s.accept()
    with conn:
        print(f"Connection from: {addr}")

        # Menerima DES Key yang terenkripsi menggunakan RSA
        encrypted_des_key = conn.recv(1024)
        encrypted_des_key = eval(encrypted_des_key.decode())  # Convert string back to list

        # Dekripsi DES Key
        des_key = rsa_decrypt(encrypted_des_key, PRIVATE_KEY).encode()
        print(f"Decrypted DES key: {des_key}")

        # Menerima pesan terenkripsi
        encrypted_message = conn.recv(1024)
        print(f"Encrypted message received: {encrypted_message}")

        # Dekripsi pesan
        decrypted_message = des_decrypt(encrypted_message, des_key)
        print(f"Decrypted message: {decrypted_message.decode()}")

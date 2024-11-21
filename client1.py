import socket

# Fungsi untuk enkripsi dan dekripsi RSA sederhana
def rsa_encrypt(message, public_key):
    n, e = public_key
    return [pow(ord(char), e, n) for char in message]

def rsa_decrypt(encrypted_message, private_key):
    n, d = private_key
    return ''.join([chr(pow(char, d, n)) for char in encrypted_message])

# Fungsi untuk enkripsi DES
def des_encrypt(message, key):
    return bytes([byte ^ key[i % len(key)] for i, byte in enumerate(message)])

# RSA Public Key dari server
PUBLIC_KEY = (3233, 17)  # (n, e)

HOST = '127.0.0.1'
PORT = 65432

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    
    # Generate DES Key
    des_key = "halodunia".encode()

    # Enkripsi DES Key menggunakan RSA
    encrypted_des_key = rsa_encrypt(des_key.decode(), PUBLIC_KEY)
    s.send(str(encrypted_des_key).encode())
    print(f"Encrypted DES key sent: {encrypted_des_key}")

    # Input pesan dari pengguna
    message = input("Enter a message to send: ").encode()

    # Enkripsi pesan menggunakan DES
    encrypted_message = des_encrypt(message, des_key)
    s.send(encrypted_message)
    print(f"Encrypted message to send: {encrypted_message}")
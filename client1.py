import socket

# RSA Public Key (Server)
PUBLIC_KEY = (3233, 17)  # (n, e)

# Fungsi untuk enkripsi RSA
def rsa_encrypt(message, public_key):
    n, e = public_key
    return [pow(char, e, n) for char in message]

# Fungsi untuk enkripsi DES
def des_encrypt(message, key):
    return bytes([byte ^ key[i % len(key)] for i, byte in enumerate(message)])

# Konfigurasi client
HOST = '127.0.0.1'
PORT = 65432

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    print("Connected to the server.")
    
    # Generate DES key
    des_key = b"halodunia"  # DES key (8 bytes)
    
    # Enkripsi dan kirimkan kunci DES menggunakan RSA
    encrypted_des_key = rsa_encrypt(des_key, PUBLIC_KEY)
    s.send(str(encrypted_des_key).encode())
    print(f"DES key sent: {encrypted_des_key}")
    
    # Percakapan tanpa determinasi
    while True:
        message = input("Enter your message: ").encode()
        encrypted_message = des_encrypt(message, des_key)
        s.send(encrypted_message)
        
        encrypted_response = s.recv(1024)
        response = bytes([byte ^ des_key[i % len(des_key)] for i, byte in enumerate(encrypted_response)])
        print(f"Server: {response.decode()}")

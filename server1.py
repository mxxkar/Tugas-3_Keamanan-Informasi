import socket
from threading import Thread

# RSA Keys (Server)
PRIVATE_KEY = (3233, 2753)  # (n, d)
PUBLIC_KEY = (3233, 17)  # (n, e)

# Fungsi untuk dekripsi RSA
def rsa_decrypt(encrypted_message, private_key):
    n, d = private_key
    return bytes([pow(char, d, n) for char in encrypted_message])

# Fungsi untuk dekripsi DES
def des_decrypt(encrypted_message, key):
    return bytes([byte ^ key[i % len(key)] for i, byte in enumerate(encrypted_message)])

# Fungsi untuk menangani koneksi klien
def handle_client(client_socket):
    print("Client connected.")
    
    # Menerima dan mendekripsi kunci DES
    encrypted_des_key = eval(client_socket.recv(1024).decode())  # Terima kunci DES terenkripsi
    des_key = rsa_decrypt(encrypted_des_key, PRIVATE_KEY)
    print(f"DES key received: {des_key}")
    
    # Percakapan tanpa determinasi
    while True:
        encrypted_message = client_socket.recv(1024)
        if not encrypted_message:
            break
        decrypted_message = des_decrypt(encrypted_message, des_key)
        print(f"Client: {decrypted_message.decode()}")
        
        # Kirim balasan (terenkripsi dengan DES)
        response = input("Enter your reply: ").encode()
        encrypted_response = bytes([byte ^ des_key[i % len(des_key)] for i, byte in enumerate(response)])
        client_socket.send(encrypted_response)
    
    client_socket.close()
    print("Client disconnected.")

# Konfigurasi server
HOST = '127.0.0.1'
PORT = 65432

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))
server.listen(5)
print("Server is listening...")

while True:
    client_socket, addr = server.accept()
    Thread(target=handle_client, args=(client_socket,)).start()

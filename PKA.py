import socket
import time
import struct

# RSA Helper Function
def rsa_encrypt(message, key):
    e_or_d, n = key
    # Pad message to ensure proper size for encryption
    message_bytes = message.encode('utf-8')
    encrypted_message = [pow(byte, e_or_d, n) for byte in message_bytes]
    return encrypted_message

def rsa_decrypt(cipher, key):
    d, n = key
    decrypted_message = ''.join([chr(pow(char, d, n)) for char in cipher])
    return decrypted_message

# PKA Server Key
pka_public_key = (7, 143)  # {e, n}
pka_private_key = (103, 143)  # {d, n}

# Public Keys A and B
public_keys = {
    "A": (7, 143),  # Public key A
    "B": (11, 143)  # Public key B
}

# PKA Server Implementation
def pka_server():
    # Start server socket
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('127.0.0.1', 65432))
    server_socket.listen(5)
    print("PKA Server running...")

    while True:
        conn, addr = server_socket.accept()
        print(f"Connection received from {addr}")

        # Receive request from client
        request = conn.recv(1024).decode()
        print(f"Request received: {request}")

        # Parse request 
        if request.startswith("REQUEST_KEY:"):
            requested_id = request.split(":")[1]
            if requested_id in public_keys:
                # Return the public key for the requested ID
                pub_key = public_keys[requested_id]
                response = f"Public Key for {requested_id}: {pub_key}"
                
                # Encrypt the response with PKA's private key
                encrypted_response = rsa_encrypt(response, pka_private_key)
                print(f"Sending encrypted response: {encrypted_response}")
                
                # Send encrypted response (encoding as byte data)
                encrypted_response_bytes = struct.pack(f'{len(encrypted_response)}I', *encrypted_response)
                conn.send(encrypted_response_bytes)
            else:
                conn.send("ERROR: Unknown ID".encode())
        else:
            conn.send("ERROR: Invalid Request".encode())

        conn.close()

# Run PKA server
if __name__ == "__main__":
    pka_server()

from cryptography.hazmat.primitives.asymmetric import dh
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes

# Sinh cặp khóa phía client từ tham số DH
def generate_client_key_pair(parameters):
    private_key = parameters.generate_private_key()
    public_key = private_key.public_key()
    return private_key, public_key

# Tính khóa bí mật chia sẻ (shared secret)
def derive_shared_secret(private_key, server_public_key):
    shared_key = private_key.exchange(server_public_key)
    return shared_key

def main():
    # Tải public key của server từ file
    with open("server_public_key.pem", "rb") as f:
        server_public_key = serialization.load_pem_public_key(f.read())

    # Lấy tham số DH từ public key của server
    parameters = server_public_key.public_numbers().parameter_numbers
    parameter_numbers = dh.DHParameterNumbers(
        p=parameters.p,
        g=parameters.g
    )
    parameters = parameter_numbers.parameters()

    # Sinh cặp khóa client và tính shared secret
    private_key, public_key = generate_client_key_pair(parameters)
    shared_secret = derive_shared_secret(private_key, server_public_key)

    print("Shared Secret:", shared_secret.hex())

if __name__ == "__main__":
    main()

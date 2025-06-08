from Crypto.Hash import SHA3_256

def sha3(message):
    sha_hash = SHA3_256.new()
    sha_hash.update(message)
    return sha_hash.digest()

def main():
    text = input("Nhập chuỗi văn bản: ").encode('utf-8')
    hashed_text = sha3(text)
    print("Chuỗi văn bản đã nhập:", text.decode('utf-8'))
    print("SHA-3 Hash:", hashed_text.hex())

if __name__ == "__main__":
    main()

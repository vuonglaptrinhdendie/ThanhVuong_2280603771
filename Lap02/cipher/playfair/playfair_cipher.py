class PlayFairCipher:
    def __init__(self):
        pass

    def create_playfair_matrix(self, key):
        key = key.replace("J", "I").upper()
        key_set = []
        for char in key:
            if char not in key_set and char.isalpha():
                key_set.append(char)

        alphabet = "ABCDEFGHIKLMNOPQRSTUVWXYZ"
        for letter in alphabet:
            if letter not in key_set:
                key_set.append(letter)

        matrix = [key_set[i:i + 5] for i in range(0, 25, 5)]
        return matrix

    def find_letter_coords(self, matrix, letter):
        for row in range(5):
            for col in range(5):
                if matrix[row][col] == letter:
                    return row, col
        return None, None

    def playfair_encrypt(self, plain_text, key):
        matrix = self.create_playfair_matrix(key)
        plain_text = plain_text.replace("J", "I").upper()
        plain_text = ''.join([c for c in plain_text if c.isalpha()])

        # Chuẩn hóa văn bản thành các cặp
        pairs = []
        i = 0
        while i < len(plain_text):
            a = plain_text[i]
            b = ''
            if i + 1 < len(plain_text):
                b = plain_text[i + 1]
                if a == b:
                    b = 'X'
                    i += 1
                else:
                    i += 2
            else:
                b = 'X'
                i += 1
            pairs.append((a, b))

        encrypted_text = ''
        for a, b in pairs:
            row1, col1 = self.find_letter_coords(matrix, a)
            row2, col2 = self.find_letter_coords(matrix, b)
            if row1 == row2:
                encrypted_text += matrix[row1][(col1 + 1) % 5]
                encrypted_text += matrix[row2][(col2 + 1) % 5]
            elif col1 == col2:
                encrypted_text += matrix[(row1 + 1) % 5][col1]
                encrypted_text += matrix[(row2 + 1) % 5][col2]
            else:
                encrypted_text += matrix[row1][col2]
                encrypted_text += matrix[row2][col1]

        return encrypted_text

    def playfair_decrypt(self, cipher_text, key):
        matrix = self.create_playfair_matrix(key)
        cipher_text = cipher_text.upper()
        cipher_text = ''.join([c for c in cipher_text if c.isalpha()])

        decrypted_text = ''
        for i in range(0, len(cipher_text), 2):
            a = cipher_text[i]
            b = cipher_text[i + 1]
            row1, col1 = self.find_letter_coords(matrix, a)
            row2, col2 = self.find_letter_coords(matrix, b)
            if row1 == row2:
                decrypted_text += matrix[row1][(col1 - 1) % 5]
                decrypted_text += matrix[row2][(col2 - 1) % 5]
            elif col1 == col2:
                decrypted_text += matrix[(row1 - 1) % 5][col1]
                decrypted_text += matrix[(row2 - 1) % 5][col2]
            else:
                decrypted_text += matrix[row1][col2]
                decrypted_text += matrix[row2][col1]

        return decrypted_text
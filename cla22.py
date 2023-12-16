# file name: ola9.py
# Seyde Martinez
# November 30, 2023
# This lab is intended to create a Caesar chiper in which each character in the plaintext message is shifted a number of positions. 

ALPHABET = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', ' ']

def main():
    plaintext = input("Enter the message you want to encode: ")
    key= int(input("Enter the key: "))
    print(f"Encoding message '{plaintext}' with key {key}.")

    cipher = generate_cipher(key)
    
    encoded = encode_message(plaintext, cipher)
    print(f"Encoded:{encoded}")
    
    decoded = decode_message(encoded, cipher)
    print(f"Decoded:{decoded}")

def generate_cipher(key):
    key = key % len(ALPHABET)
    cipher = ALPHABET[-key:] + ALPHABET[:-key]
    return cipher

def encode_message(plaintext, cipher):
    encoded_message = ''
    for char in plaintext:
        if char.lower() in ALPHABET:
            index = ALPHABET.index(char.lower())
            encoded_char = cipher[index]
            if char.isupper():
                encoded_char = encoded_char.lower()
            encoded_message += encoded_char
        else:
            encoded_message += char
    return encoded_message

def decode_message(encoded_message, cipher):
    decoded_message = ''
    for char in encoded_message:
        if char.lower() in cipher:
            index = cipher.index(char.lower())
            decoded_char = ALPHABET[index]
            if char.isupper():
                decoded_char = decoded_char.lower()
            decoded_message += decoded_char
        else:
            decoded_message += char
    return decoded_message
        

main()       
    
    
    
    
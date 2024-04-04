import random

## VARS ##

subs = ['#@', 'jj', '11', 'Yd', '}T', ')E', 'AV', 'O ', 'c/', '}5', 'I1', '#d', 'oz', '2k', '$!', '3E', 'iv', 'R@', ' D', 'tT', '22', ">'", 'W ', 'p-', "s'", '-$', '>o', 'eP', '|D', '33', '|1', 'rv', 'y[', 'W&', 'SN', '5m', 'MD', 'MV', '44', 'U+', '55', 'Y:', 'p*', 'zN', '|t', '1i', 'Xb', 'g;', 's~', 'c6', 'fT', 'JF', '(C', 'u.', '66', '77', 'D2', '88', 'Ru', 'YF', '[d', ';_', 'R|', '`)', 'P<', '%t', 'Wa', 'G"', 'XU', 'Bd', ']8', 'wd', '!b', '3t', '99', 'kM', 'o6', 'm<', 'WR', '5t', '[c', '"|', 'Ac', 'v:', 'x[', 'XM', 'a!', 'Dq', 'u9', '}=', 'Km', 'VD', '.K', '2}', ']q']
characters = ['2', '8', '\\', '`', "'", 'Z', '#', '1', ';', 'D', '5', 'j', 'M', '&', 'n', ']', 'i', 'X', '6', 'C', 'p', '3', 'v', '{', 's', '0', 'B', 'T', '.', 'f', '/', '^', 't', 'U', 'N', 'u', ':', 'J', '[', 'P', ')', 'H', '}', '>', 'I', 'b', 'Q', 'w', 'F', '=', '*', 'W', ',', 'e', 'x', 'h', 'V', 'S', '4', 'k', '7', 'A', 'G', 'l', 'r', '-', 'a', '(', 'R', 'y', 'g', '9', 'c', 'Y', '<', 'L', '%', '?', '"', '$', '|', '+', 'o', 'z', 'O', 'E', '@', '~', 'K', ' ', '_', 'm', 'q', 'd', '!']
defualt = "01010010010101110110110100110101011111000101001001100011010110110110101001101010010100100101011101101010011010100101001001010111"

## ENC FUNCS ##

def string_to_binary_byte_data(string):
    byte_data = string.encode('ascii')    
    binary_byte_data = ''.join(format(byte, '08b') for byte in byte_data)
    return binary_byte_data

def binary_byte_data_to_string(binary_byte_data):
    byte_chunks = [binary_byte_data[i:i+8] for i in range(0, len(binary_byte_data), 8)]
    byte_data = bytes(int(chunk, 2) for chunk in byte_chunks)
    decoded_string = byte_data.decode('ascii')
    return decoded_string

def calculate_byte_data_size(byte_data):
    size_in_bits = len(byte_data) * 8
    padding = (int((128-(size_in_bits % 128)) / 8)) if (int((128-(size_in_bits % 128)) / 8)) != 16 else 128
    return size_in_bits, padding

def xor(binary, key):
    return ''.join(str(int(bit1) ^ int(bit2)) for bit1, bit2 in zip(binary, key))

def enc(string):
    string = "".join([characters[(len(characters)-1)-characters.index(i)] for i in string])
    new_string = "".join([subs[characters.index(i)] for i in string])
    new_string = "".join([characters[(len(characters)-1)-characters.index(i)] for i in new_string])
    return new_string

def dec(string):
    string = "".join([characters[(len(characters)-1)-characters.index(i)] for i in string])
    new_string = "".join([characters[subs.index(i)] for i in ([string[i:i+2] for i in range(0, len(string), 2)])])
    string = "".join([characters[(len(characters)-1)-characters.index(i)] for i in new_string])
    return string

def pad(string, padding):
    if padding != 0:
        string = string[-1] + string
        while padding > 1:
            add_char = random.choice(characters)
            if add_char != string[0]:
                padding -= 1
                string += add_char
    return string

def de_pad(string):
    orig = string
    last_letter = string[0]
    last_index = string.rfind(last_letter)
    string = string[:last_index+1][1:]
    if string.strip() != "": return string
    else: return orig

def rep(binary):
    byte_data = bytes(int(binary[i:i+8], 2) for i in range(0, len(binary), 8))
    hex_data = byte_data.hex()[::-1]
    string = "".join([characters[(len(characters)-1)-characters.index(i)] for i in hex_data])
    return string

def de_rep(text):
    text = "".join([characters[(len(characters)-1)-characters.index(i)] for i in text])
    hex_data = text[::-1]
    byte_data = bytes.fromhex(hex_data)
    binary_byte_data = ''.join(format(byte, '08b') for byte in byte_data)
    return binary_byte_data

def casper_enc(text, password):
    ciphered_text = enc(text)[::-1]
    initial_size, padding = calculate_byte_data_size(ciphered_text)
    padded_text = pad(ciphered_text, padding)
    encrypted_padded_text = "".join([characters[(len(characters)-1)-characters.index(i)] for i in padded_text])
    new_size = initial_size + (8*padding)
    key = key_gen(password, new_size)
    binary_data = string_to_binary_byte_data(encrypted_padded_text)
    binary_data = xor(binary_data, key)
    binary_data = xor(binary_data, key[::-1])
    defualt_com = defualt
    while len(defualt_com) != len(binary_data):
        defualt_com = defualt_com[::-1] + defualt
    binary_data = xor(binary_data, defualt_com)
    binary_data = xor(binary_data[::-1], key)
    binary_data = binary_data[::-1]
    output = rep(binary_data)
    return output

## DEC FUNCS

def casper_dec(text, password):
    if text[0] == "'" and text[-1] == "'": text = text[1:][:-1]
    binary_data = de_rep(text)
    key = key_gen(password, len(binary_data))
    binary_data = binary_data[::-1]
    binary_data = xor(binary_data, key)[::-1]
    defualt_com = defualt
    while len(defualt_com) != len(binary_data):
        defualt_com = defualt_com[::-1] + defualt
    binary_data = xor(binary_data, defualt_com)
    binary_data = xor(binary_data, key[::-1])
    binary_data = xor(binary_data, key)
    cipher_text = binary_byte_data_to_string(binary_data)
    cipher_text = "".join([characters[(len(characters)-1)-characters.index(i)] for i in cipher_text])
    cipher_text = de_pad(cipher_text)
    #print(cipher_text)
    final = dec(cipher_text[::-1])
    return final

## KEY GEN ##

def ceaser(string, size):
    new_string = "".join([characters[(characters.index(i)+size)%len(characters)] for i in string])
    return new_string

def key_gen(string, size):
    for i in string:
        string = ceaser(string, characters.index(i))
    string = enc(string + string[::-1])
    key_size, _ = calculate_byte_data_size(string)
    string_list = [characters.index(i) for i in string]
    string = "".join([characters[i] for i in sorted(string_list)])
    if key_size > size:
        new_string = string[:(len(string))-int((key_size - size) / 8)]
    elif key_size < size:
        while calculate_byte_data_size(string)[0] < size:
            string = enc(string)
        if calculate_byte_data_size(string)[0] > size:
            string = string[:(len(string))-int((calculate_byte_data_size(string)[0] - size) / 8)]
        new_string = string
    else:
        new_string = string
    binary = string_to_binary_byte_data(new_string[::-1])
    defualt_com = defualt
    while len(defualt_com) != len(binary):
        defualt_com = defualt_com[::-1] + defualt
    binary = xor(binary, defualt_com)
    return binary

while 1:
    text_to_encrypt = input("text to encrypt (empty to skip): ")
    if text_to_encrypt.strip() not in ["", None, False]:
        encryption_key = input("key for encryption (string): ")
        print("\nOUTPUT:\n"+casper_enc(text_to_encrypt, encryption_key)+"\n")

    try:
        text_to_decrypt = input("text to decrypt (empty to skip): ")
        if text_to_decrypt.strip() not in ["", None, False]:
            decryption_key = input("key for encryption (string): ")
            print("\nOUTPUT:\n"+casper_dec(text_to_decrypt, decryption_key)+"\n")
    except: print("\nOUTPUT:\nwrong decryption key\n")

import random
import base64

## VASRS ##

#subs = ['#@', 'jj', '11', 'Yd', '}T', ')E', 'AV', 'O ', 'c/', '}5', 'I1', '#d', 'oz', '2k', '$!', '3E', 'iv', 'R@', ' D', 'tT', '22', ">'", 'W ', 'p-', "s'", '-$', '>o', 'eP', '|D', '33', '|1', 'rv', 'y[', 'W&', 'SN', '5m', 'MD', 'MV', '44', 'U+', '55', 'Y:', 'p*', 'zN', '|t', '1i', 'Xb', 'g;', 's~', 'c6', 'fT', 'JF', '(C', 'u.', '66', '77', 'D2', '88', 'Ru', 'YF', '[d', ';_', 'R|', '`)', 'P<', '%t', 'Wa', 'G"', 'XU', 'Bd', ']8', 'wd', '!b', '3t', '99', 'kM', 'o6', 'm<', 'WR', '5t', '[c', '"|', 'Ac', 'v:', 'x[', 'XM', 'a!', 'Dq', 'u9', '}=', 'Km', 'VD', '.K', '2}', ']q']
subs = ['/2', "'8", '%\\', '_`', "$'", 'KZ', 'r#', 'O1', 's;', '"D', 'Q5', '~j', '-M', 'g&', 'Zn', 'h]', '4i', '8X', 'L6', 'SC', 'zp', '[3', 'Gv', '}{', 'Ws', 'R0', ',B', '7T', '#.', 'xf', '|/', '2^', 'yt', ' U', 'uN', 'cu', 'j:', '3J', 'Y[', '.P', 'F)', '@H', '>}', 'A>', 'TI', '=b', 'VQ', '{w', 'IF', ']=', 'U*', 'nW', 'J,', 'le', 'Dx', 'mh', 'pV', 'eS', 'o4', 'kk', '^7', 'fA', '9G', '`l', ')r', '+-', '5a', '?(', 'dR', 'By', ';g', 'E9', 'Hc', '\\Y', 'b<', 'aL', ':%', '(?', 'N"', '*$', 'M|', 'C+', '6o', '1z', '0O', '<E', 'i@', 'w~', 'vK', '! ', 'q_', 'tm', '&q', 'Pd', 'X!'][::-1]
characters = ['2', '8', '\\', '`', "'", 'Z', '#', '1', ';', 'D', '5', 'j', 'M', '&', 'n', ']', 'i', 'X', '6', 'C', 'p', '3', 'v', '{', 's', '0', 'B', 'T', '.', 'f', '/', '^', 't', 'U', 'N', 'u', ':', 'J', '[', 'P', ')', 'H', '}', '>', 'I', 'b', 'Q', 'w', 'F', '=', '*', 'W', ',', 'e', 'x', 'h', 'V', 'S', '4', 'k', '7', 'A', 'G', 'l', 'r', '-', 'a', '(', 'R', 'y', 'g', '9', 'c', 'Y', '<', 'L', '%', '?', '"', '$', '|', '+', 'o', 'z', 'O', 'E', '@', '~', 'K', ' ', '_', 'm', 'q', 'd', '!']
defualt = "01010010010101110110110100110101011111000101001001100011010110110110101001101010010100100101011101101010011010100101001001010111"

## ENC FUNCS ##

def reorder_list_with_value(input_list, value):
    hash_value = sum([(sum([int(characters.index(i))**2 for i in value+value[::-1]])*len(value))**((characters.index(i)+10)//10) for i in [i[0] for i in subs]])*sum([int(i)*10 for i in list(defualt)])
    sorted_list = sorted(input_list, key=lambda x: hash_value*(characters.index(x[(0 if len(x)==1 or characters.index(x[0]) <= (len(characters)-1)//2 else 1)])**2))
    return sorted_list

def replace(string):
    string = string.split("##R")
    for i in range(1, (0 if len(string) < 0 else len(string))):
        seg = string[i]
        try:
            code = chr(int(seg.split("##")[0]))
            new = code + "##".join(seg.split("##")[1:])
            string.pop(i)
            string.insert(i, new)
        except:
            new = "##R" + seg
            string.pop(i)
            string.insert(i, new)
    string = "".join(string)
    if r"Ä" in string: string = string.replace(r"Ä", r"─")
    if r"À" in string: string = string.replace(r"À", r"└")
    if r"Ã" in string: string = string.replace(r"Ã", r"├")
    if r"³" in string: string = string.replace(r"³", r"│")
    return string

def safe(msg):
    msg = msg.strip("\n")
    for i in msg:
        if i not in characters: msg = msg.replace(i, f"##R{str(ord(i))}##")
    msg = "".join([i for i in msg if i in characters])
    return msg

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
    padding = (int((128-(size_in_bits % 128)) / 8)) if (int((128-(size_in_bits % 128)) / 8)) != 16 else 16
    return size_in_bits, padding

def xor(binary, key):
    return ''.join(str(int(bit1) ^ int(bit2)) for bit1, bit2 in zip(binary, key))

def gen_table(key, char_list):
    temp_c = "".join([i for i in char_list if i not in key])
    string = key + "".join(temp_c)
    table = []
    first = []
    for i in range(0, len(temp_c)+len(key)):
        if string[0] not in first:
            table.append(string)
            first.append(string[0])
        string = (string[1:] + string[0])
    return table

def table_enc(text, key):
    global characters
    prev = ""
    if len(text) > 90:
        while len(text) > 90:
            key += "1"
            add = table_enc(text[:90], key)
            prev += add
            text = text[90:]
    key = characters[-1] + key + characters[0] + characters[(characters.index(key[0])//2)]
    while len(key) < len(text): key = key + key[::-1]
    new_key = "".join([key[i] for i in range(0, len(key)-1) if key[i] not in key[:i]])
    for i in range((len(key)-len(new_key))):
        for b in characters:
            if b not in new_key:
                new_key += b
                break
    key = new_key
    if len(key)%2==0: key = key[::-1]
    while len(key) > len(text): key = key[::-1][:-1]
    table = gen_table(key, characters)
    indexes = [i[0] for i in table]
    for i in characters:
        if i not in indexes: indexes.append(i)
    result = ""
    for i in range(len(key)):
        ychar = text[i]
        xchar = key[i]
        row = table[(indexes.index(ychar)+i)%(len(indexes))]
        add_char = row[(characters.index(xchar)-i)%(len(characters))]
        result += add_char
    return prev + result[::-1]

def table_dec(cipher, key):
    global characters
    prev = ""
    if len(cipher) > 90:
        while len(cipher) > 90:
            key += "1"
            add = table_dec(cipher[:90], key)
            prev += add
            cipher = cipher[90:]
    key = characters[-1] + key + characters[0] + characters[(characters.index(key[0])//2)]
    cipher = cipher[::-1]
    while len(key) < len(cipher): key = key + key[::-1]
    new_key = "".join([key[i] for i in range(0, len(key)-1) if key[i] not in key[:i]])
    for i in range((len(key)-len(new_key))):
        for b in characters:
            if b not in new_key:
                new_key += b
                break
    key = new_key
    if len(key)%2==0: key = key[::-1]
    while len(key) > len(cipher): key = key[::-1][:-1]
    table = gen_table(key, characters)
    indexes = [i[0] for i in table]
    for i in characters:
        if i not in indexes: indexes.append(i)
    result = ""
    for i in range(len(key)):
        xchar = key[i]
        val = (characters.index(xchar)-i)%(len(characters))
        for row in table:
            if row[val] == cipher[i]:
                srow = row
                break
        ychar = indexes[(table.index(srow)-i)%(len(characters))]
        result += ychar
    return prev + result

def rail_cipher(text, mode):
    alpha = characters[::-1]
    cipher_text = "".join([alpha[::-1][(len(alpha)-1)-alpha.index(i)] for i in text])
    cipher_text = text
    first = "".join([cipher_text[i] for i in range(0, len(cipher_text), 2)])
    second = "".join([cipher_text[i] for i in range(1, len(cipher_text), 2)])
    first = [alpha[(alpha.index(i)+(mode*(len(second)-1)**2))%(len(alpha))] for i in first]
    second = [alpha[(alpha.index(i)+(mode*(len(first)+1)**2))%(len(alpha))] for i in second]
    third = [i for i in first]
    for i in range(0, len(second)): third[i] = third[i]+second[i]
    cipher_text = "".join(third)
    return cipher_text

def enc(string):
    string = "".join([characters[(len(characters)-1)-characters.index(i)] for i in string])
    new_string = "".join([subs[[i[0] for i in subs].index(o)][1] for o in string])
    new_string = "".join([characters[(len(characters)-1)-characters.index(i)] for i in new_string])
    new_string = rail_cipher(rail_cipher(new_string, 1), 1)
    return new_string

def dec(string):
    string = rail_cipher(rail_cipher(string, -1), -1)
    string = "".join([characters[(len(characters)-1)-characters.index(i)] for i in string])
    #new_string = "".join([characters[subs.index(i)] for i in ([string[i:i+2] for i in range(0, len(string), 2)])]) for duel sub list
    new_string = "".join([subs[[i[1] for i in subs].index(o)][0] for o in string])
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
    #hex_data = byte_data.hex()[::-1]   ## converted to use bas364 cuz smaller. to revert, uncomment this and dec equivelant, comment out line below and get rid of text = "b'" + text in de_rep, also remove [::-1] finr after hex_data at the end of the line 2 below
    hex_data = str(base64.b64encode(byte_data))[2:]
    string = "".join([characters[(len(characters)-1)-characters.index(i)] for i in hex_data[::-1]])
    return string

def de_rep(text):
    text = "".join([characters[(len(characters)-1)-characters.index(i)] for i in text])
    hex_data = text[::-1]
    text = "b'" + text
    #byte_data = bytes.fromhex(hex_data) ## uncomment this too
    byte_data = base64.b64decode(hex_data)
    binary_byte_data = ''.join(format(byte, '08b') for byte in byte_data)
    return binary_byte_data

def sort_val(password):
    global subs, characters, defualt
    ts, tc, td = (subs, characters, defualt)
    subs = reorder_list_with_value(subs, password)
    characters = reorder_list_with_value(characters, password[::-1])
    defualt = ("".join(["1" if int(i)<5 else "0" for i in (str((int(defualt)*(((sum([((len(characters)-1)-characters.index(i))**2 for i in password]))+3)**3))))])[::-1])[:len(defualt)]
    return (ts, tc, td)

def casper_enc(text, password, length=9000):
    text = safe(text)
    prev = ""
    if len(text) > length:
        while len(text) > length:
            password += "1"
            prev += table_enc(casper_enc(enc(text[:length]), enc(password)), password[::-1])
            text = text[length:]
    global subs, characters, defualt
    ts, tc, td = (subs, characters, defualt)
    subs, characters, defualt = sort_val(enc(password))
    text = text + characters[:11][random.randint(0, 10)]
    text = table_enc(text, password)
    ciphered_text = enc(text)[::-1]
    initial_size, padding = calculate_byte_data_size(ciphered_text)
    padded_text = pad(ciphered_text, padding)
    padded_text = padded_text[0]+ceaser(ciphered_text[:-1], sum([characters.index(i) for i in padded_text[len(ciphered_text)+1:]]))+padded_text[len(ciphered_text):]
    padded_text = ceaser(padded_text[0], characters.index(subs[0][0])+characters.index(padded_text[-1])) + padded_text[1:]
    padded_text = ceaser(padded_text[:-2], (characters.index(padded_text[-2])+characters.index(padded_text[-1]))) + ceaser(padded_text[-2], characters.index(subs[0][1])) + ceaser(padded_text[-1], characters.index(subs[1][0]))
    encrypted_padded_text = ("".join([characters[(len(characters)-1)-characters.index(i)] for i in padded_text]))
    encrypted_padded_text = rail_cipher(encrypted_padded_text, 1)
    new_size = initial_size + (8*padding)
    key = key_gen(password, new_size)
    binary_data = string_to_binary_byte_data(encrypted_padded_text)
    binary_data = xor(binary_data, key)
    binary_data = xor(binary_data, key[-8:] + key[8:][:-8] + key[:8])
    binary_data = xor(binary_data[-8:] + binary_data[8:][:-8] + binary_data[:8], key)
    binary_data = xor(binary_data, key[::-1])
    defualt_com = defualt
    while len(defualt_com) != len(binary_data): defualt_com = defualt_com[::-1] + defualt
    binary_data = xor(binary_data, defualt_com)
    binary_data = xor(binary_data[::-1], key)
    new_key = [sum([int(b) for b in i]) for i in [key[i:i+8] for i in range(0, len(key), 8)]]
    new_key = [new_key[i]*new_key[(i+1)%(len(new_key)-1)] for i in new_key]
    new_key = enc("".join([characters[i%(len(characters)-1)] for i in new_key]))
    new_key = string_to_binary_byte_data(new_key)
    binary_data = xor(binary_data, new_key)
    binary_data = binary_data[::-1]
    output = rep(binary_data)
    output = ceaser(output[:4], characters.index(subs[2][1])+(characters.index(output[-1])*2)) + output[4:]
    output = table_enc(output, password)
    subs, characters, defualt = (ts, tc, td)
    return "|" + prev + output + "|"

## DEC FUNCS ##

def dec_length(start_length):
    return len(casper_enc(("".join(["a" for i in range(start_length)])), "a", start_length+1))

def casper_dec(text, password, length=12015):
    text = text[1:][:-1]
    prev = ""
    if len(text) > length:
        while len(text) > length:
            password += "1"
            prev += dec(casper_dec(table_dec(text[:length], password[::-1]), enc(password)))
            text = text[length:]
    global subs, characters, defualt
    ts, tc, td = (subs, characters, defualt)
    subs, characters, defualt = sort_val(enc(password))
    text = table_dec(text, password)
    text = ceaser(text[:4], -1*(characters.index(subs[2][1])+(characters.index(text[-1])*2))) + text[4:]
    binary_data = de_rep(text)
    key = key_gen(password, len(binary_data))
    binary_data = binary_data[::-1]
    new_key = [sum([int(b) for b in i]) for i in [key[i:i+8] for i in range(0, len(key), 8)]]
    new_key = [new_key[i]*new_key[(i+1)%(len(new_key)-1)] for i in new_key]
    new_key = enc("".join([characters[i%(len(characters)-1)] for i in new_key]))
    new_key = string_to_binary_byte_data(new_key)
    binary_data = xor(binary_data, new_key)
    binary_data = xor(binary_data, key)[::-1]
    defualt_com = defualt
    while len(defualt_com) != len(binary_data): defualt_com = defualt_com[::-1] + defualt
    binary_data = xor(binary_data, defualt_com)
    binary_data = xor(binary_data, key[::-1])
    binary_data = xor(binary_data, key)
    binary_data = binary_data[-8:] + binary_data[8:][:-8] + binary_data[:8]
    binary_data = xor(binary_data, key[-8:] + key[8:][:-8] + key[:8])
    binary_data = xor(binary_data, key)
    cipher_text = binary_byte_data_to_string(binary_data)
    cipher_text = rail_cipher(cipher_text, -1)
    cipher_text = ("".join([characters[(len(characters)-1)-characters.index(i)] for i in cipher_text]))
    cipher_text = ceaser(cipher_text[:-2], -1*(characters.index((ceaser(cipher_text[-2], -1*(characters.index(subs[0][1])))))+characters.index((ceaser(cipher_text[-1], -1*(characters.index(subs[1][0]))))))) + (ceaser(cipher_text[-2], -1*(characters.index(subs[0][1])))) + (ceaser(cipher_text[-1], -1*(characters.index(subs[1][0]))))
    cipher_text = ceaser(cipher_text[0], -1*(characters.index(subs[0][0])+characters.index(cipher_text[-1]))) + cipher_text[1:]
    cipher_text = cipher_text[0]+ceaser(cipher_text[1:].replace(cipher_text.split(cipher_text[0])[-1], "")[:-1], (-1*sum([characters.index(i) for i in (cipher_text.split(cipher_text[0])[-1])])))+cipher_text[0]+cipher_text.split(cipher_text[0])[-1]
    cipher_text = de_pad(cipher_text)
    final = dec(cipher_text[::-1])
    final = table_dec(final, password)[:-1]
    subs, characters, defualt = (ts, tc, td)
    return replace(prev + final)

## KEY GEN ##

def ceaser(string, size):
    new_string = "".join([characters[(characters.index(i)+size)%len(characters)] for i in string])
    return new_string

def key_gen(string, size):
    for i in string: string = ceaser(string, characters.index(i))
    string = "".join([ceaser(i, characters.index(i)) for i in string[::-1]])
    string = enc(string + string[::-1])
    key_size, _ = calculate_byte_data_size(string)
    string_list = [characters.index(i) for i in string]
    string = "".join([characters[i] for i in (sorted(string_list, key=lambda x: ([i[0] for i in subs]).index(x) if x in [i[0] for i in subs] else len([i[0] for i in subs])))])
    if key_size > size:
        new_string = string[:(len(string))-int((key_size - size) / 8)]
    elif key_size < size:
        while calculate_byte_data_size(string)[0] < size:
            string = enc(string) + string[::-1]
            string = enc(string)
        if calculate_byte_data_size(string)[0] > size:
            string = string[:(len(string))-int((calculate_byte_data_size(string)[0] - size) / 8)]
        new_string = string
    else:
        new_string = string
    binary = string_to_binary_byte_data(new_string[::-1])
    defualt_com = defualt[::-1]
    while len(defualt_com) != len(binary):
        defualt_com = defualt_com[::-1] + defualt
    binary = xor(binary, defualt_com)
    kstring = ""
    for i in range(0, len(binary), 4):
        total = "011"+binary[i:(i+4)]
        decimal_value = int(total, 2)
        ascii_character = chr(decimal_value)
        kstring += ascii_character
    print("\nKEY:\n"+kstring)
    return binary

while 1:
    text_to_encrypt = input("text to encrypt (empty to skip): ")
    if text_to_encrypt.strip() not in ["", None, False]:
        encryption_key = input("key for encryption (string): ")
        if encryption_key.strip() != "":
            print("\nOUTPUT:\n"+casper_enc(text_to_encrypt, encryption_key)+"\n")
    try:
        text_to_decrypt = input("text to decrypt (empty to skip): ")
        if text_to_decrypt.strip() not in ["", None, False]:
            decryption_key = input("key for encryption (string): ")
            if decryption_key.strip() != "":
                print("\nOUTPUT:\n"+casper_dec(text_to_decrypt, decryption_key)+"\n")
    except Exception as e:
        subs = ['/2', "'8", '%\\', '_`', "$'", 'KZ', 'r#', 'O1', 's;', '"D', 'Q5', '~j', '-M', 'g&', 'Zn', 'h]', '4i', '8X', 'L6', 'SC', 'zp', '[3', 'Gv', '}{', 'Ws', 'R0', ',B', '7T', '#.', 'xf', '|/', '2^', 'yt', ' U', 'uN', 'cu', 'j:', '3J', 'Y[', '.P', 'F)', '@H', '>}', 'A>', 'TI', '=b', 'VQ', '{w', 'IF', ']=', 'U*', 'nW', 'J,', 'le', 'Dx', 'mh', 'pV', 'eS', 'o4', 'kk', '^7', 'fA', '9G', '`l', ')r', '+-', '5a', '?(', 'dR', 'By', ';g', 'E9', 'Hc', '\\Y', 'b<', 'aL', ':%', '(?', 'N"', '*$', 'M|', 'C+', '6o', '1z', '0O', '<E', 'i@', 'w~', 'vK', '! ', 'q_', 'tm', '&q', 'Pd', 'X!'][::-1]
        characters = ['2', '8', '\\', '`', "'", 'Z', '#', '1', ';', 'D', '5', 'j', 'M', '&', 'n', ']', 'i', 'X', '6', 'C', 'p', '3', 'v', '{', 's', '0', 'B', 'T', '.', 'f', '/', '^', 't', 'U', 'N', 'u', ':', 'J', '[', 'P', ')', 'H', '}', '>', 'I', 'b', 'Q', 'w', 'F', '=', '*', 'W', ',', 'e', 'x', 'h', 'V', 'S', '4', 'k', '7', 'A', 'G', 'l', 'r', '-', 'a', '(', 'R', 'y', 'g', '9', 'c', 'Y', '<', 'L', '%', '?', '"', '$', '|', '+', 'o', 'z', 'O', 'E', '@', '~', 'K', ' ', '_', 'm', 'q', 'd', '!']
        defualt = "01010010010101110110110100110101011111000101001001100011010110110110101001101010010100100101011101101010011010100101001001010111"
        print(f"\nOUTPUT:\nwrong decryption key\n{e}")


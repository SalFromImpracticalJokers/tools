import ctypes
import os
import random
import time
import gc

# compile with (windows) "g++ -O3 -march=native -funroll-loops -shared -o encryption.dll CASPER_2.cpp -static -static-libgcc -static-libstdc++"
# (linux) "g++ -O3 -march=native -funroll-loops -shared -fPIC -o encryption.so CASPER_2.cpp"

class Encryptor:
    def __init__(self, default_salt=b"2891"):
        if os.name == "nt":
            lib_path = os.path.abspath("./encryption.dll")
        else:
            lib_path = os.path.abspath("./encryption.so")
        
        self.encryption_lib = ctypes.CDLL(lib_path)

        self.encryption_lib.encrypt.argtypes = [
            ctypes.POINTER(ctypes.c_ubyte),
            ctypes.c_size_t,
            ctypes.POINTER(ctypes.c_ubyte),
            ctypes.c_size_t,
            ctypes.POINTER(ctypes.c_ubyte)
        ]
        
        self.encryption_lib.encrypt.restype = None

        self.encryption_lib.create_key.argtypes = [
            ctypes.POINTER(ctypes.c_ubyte),
            ctypes.c_size_t,
            ctypes.c_size_t,
            ctypes.POINTER(ctypes.c_ubyte)
        ]
        
        self.encryption_lib.create_key.restype = None
        
        self.encryption_lib.gen_bytes.argtypes = [
            ctypes.POINTER(ctypes.c_ubyte),
            ctypes.c_size_t
        ]
        
        self.encryption_lib.gen_bytes.retypes = None
        
        self.encryption_lib.binary_rotate.argtypes = [
            ctypes.POINTER(ctypes.c_uint8), 
            ctypes.c_size_t, 
            ctypes.c_int, 
            ctypes.POINTER(ctypes.c_uint8),
            ctypes.c_int
        ]
        
        self.encryption_lib.binary_rotate.retypes = None
        
        self.encryption_lib.substitute_bytes.argtypes = [
            ctypes.POINTER(ctypes.c_uint8), 
            ctypes.c_size_t, 
            ctypes.POINTER(ctypes.c_uint8),
            ctypes.POINTER(ctypes.c_uint8),
            ctypes.c_int
        ]
        
        self.encryption_lib.substitute_bytes.retypes = None
        
        self.prototype_output_data = (ctypes.c_ubyte * 256)()
        self.default_salt = default_salt
        self.keys = []
        self.fake_keys = [self.create_key(self.gen_random_bytes(256)) for i in range(random.randint(5, 11))]
        self.machine_code = (os.name + str(os.cpu_count())).encode()
        #self.machine_code = (os.name + str(2)).encode()
        self.default_seed = self.machine_code + self.machine_code[::-1] + self.default_salt
        self.default_key = self.create_key(self.default_seed, 256)
        
    def get_output_array(self, size):
        # get factor of 256 then multiply precomputed 256 bit array by that to quickly make an output array of the correct size
        new_array = ctypes.cast(ctypes.create_string_buffer(ctypes.sizeof(self.prototype_output_data)), ctypes.POINTER(ctypes.c_ubyte * 256)).contents
        return new_array
        
    def add_key(self, key):
        self.keys.append(self.xor_encrypt(key, self.binary_rotate(self.default_key, (len(self.keys)+1)*len(self.machine_code))))
        
    def export_keys(self, loc=False):
        if (not loc and type(loc) != int): return [self.xor_encrypt(key, self.binary_rotate(self.default_key, (index+1)*len(self.machine_code))) for index, key in enumerate(self.keys)]
        elif type(loc) == int and (loc >= 0 and loc < len(self.keys)): return self.xor_encrypt(self.keys[loc], self.binary_rotate(self.default_key, (loc+1)*len(self.machine_code)))
        else: raise IndexError("list index out of range")
        
    def gen_random_bytes(self, length: int = 0) -> bytes:
        if length == 0: return b""
        output_data = (ctypes.c_ubyte * length)()
        
        self.encryption_lib.gen_bytes(
            output_data,
            length
        )
        output_data = self.binary_rotate(output_data, random.randint(1, 127))

        return bytes(output_data)[:length]
        
    def create_key(self, passphrase: str = "", key_length: int = 256) -> bytes:
        passphrase = bytearray(passphrase)
        passphrase.extend(self.default_salt)
        passphrase = bytes(passphrase)
        input_length = len(passphrase)
        output_data = (ctypes.c_ubyte * key_length)()
        
        self.encryption_lib.create_key(
            (ctypes.c_ubyte * input_length).from_buffer_copy(passphrase),
            input_length,
            key_length,
            output_data
        )
        output_data = self.binary_rotate(output_data, 127)

        return bytes(output_data)[:key_length]
        
    def substitute(self, data, key) -> bytes:
        data_length = len(data)
        key_length = len(key)
        
        output_data = (ctypes.c_ubyte * data_length)()
        self.encryption_lib.substitute_bytes(
            (ctypes.c_ubyte * data_length).from_buffer_copy(data),
            data_length,
            output_data,
            (ctypes.c_ubyte * key_length).from_buffer_copy(key),
            os.cpu_count()
        )
        return bytes(output_data)
        
    def add_padding(self, data, key, mode=False):
        padding_length = (256-(len(data)%256))-1
        padding = bytearray()
        last_byte = bytes([data[-1]])
        last_byte_val = last_byte[0]
        
        while len(padding) < padding_length:
            generated = self.gen_random_bytes(padding_length - len(padding))

            for byte in generated:
                if byte != last_byte_val:
                    padding.append(byte)
        
        if not mode: return last_byte + data + bytes(padding)
        else: return bytes(padding)
    
    def remove_padding(self, data):
        padding_byte = data[0]
        
        padding_index = len(data) - 1
        while padding_index >= 0 and data[padding_index] != padding_byte:
            padding_index -= 1
        
        return data[:padding_index + 1][1:]
        
    def casper_enc(self, data, key=None, mode=False) -> bytes:
        if (not mode and type(mode) != int) or (mode != 0 and mode != 1): raise ValueError("no 'mode=' argument provided for encryption (1) or decryption (0)")
        if mode == 1:
            padding = self.add_padding(data, key, mode=1)
            pad_len = len(padding)
            part1 = self.xor_encrypt(data, bytes((padding[i%pad_len]+key[i])%256 for i in range(20))+key[20:])
            part1 = self.xor_encrypt(bytes([len(padding)]), self.binary_rotate(bytes([key[-1]]), key[1])) + part1
            part2 = self.xor_encrypt(padding, key)
            return part1 + part2
        else:
            data_length = len(data)
            padding_length = self.xor_encrypt(bytes([data[0]]), self.binary_rotate(bytes([key[-1]]), key[1]))[0]
            part1 = data[:(data_length-padding_length)][1:]
            part2 = data[(data_length-padding_length):]
            decrypted_padding = self.xor_encrypt(part2, key)
            pad_len = len(decrypted_padding)
            decrypted_data = self.xor_encrypt(part1, bytes((decrypted_padding[i%pad_len]+key[i])%256 for i in range(20))+key[20:])
            return decrypted_data
                
    def xor_enc(self, data, key=None) -> bytes:
        key += self.xor_encrypt(self.default_salt, key)
        data_length = len(data)
        shifts = [(i//10)+1 for i in key]
        rotates = b"".join(list(self.binary_rotate(key, i) for i in shifts))
        key += rotates
        return self.xor_encrypt(data, key)

    def xor_encrypt(self, input_data: bytes, key: bytes) -> bytes:
        input_length = len(input_data)
        key_length = len(key)

        output_data = (ctypes.c_ubyte * input_length)()
        self.encryption_lib.encrypt(
            (ctypes.c_ubyte * input_length).from_buffer_copy(input_data),
            input_length,
            (ctypes.c_ubyte * key_length).from_buffer_copy(key),
            key_length,
            output_data,
            os.cpu_count()
        )
        return bytes(output_data)

    def binary_rotate(self, input_data: bytes, shift: int) -> bytes:
        input_bytearray = bytearray(input_data)
        
        output_bytearray = bytearray(len(input_data))

        input_ptr = (ctypes.c_uint8 * len(input_bytearray)).from_buffer(input_bytearray)
        output_ptr = (ctypes.c_uint8 * len(output_bytearray)).from_buffer(output_bytearray)

        self.encryption_lib.binary_rotate(
            input_ptr,
            len(input_bytearray),
            shift,
            output_ptr,
            os.cpu_count()
        )

        # Convert the output bytearray back to bytes and return
        return bytes(output_bytearray)
        
    def garbage_collect(self):
        gc.collect()

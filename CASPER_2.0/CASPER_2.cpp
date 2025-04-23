#include <cstddef>
#include <cstring>
#include <algorithm>
#include <cstdint>
#include <random>
#include <vector>
#include <array>
#include <thread>
#include <atomic>

#ifdef _WIN32
#define EXPORT __declspec(dllexport)
#else
#define EXPORT
#endif

extern "C" {
	
// SHA-256 constants
constexpr uint32_t k[64] = {
    0xc67178f2, 0x71374491, 0xb5c0fbcf, 0xe9b5dba5, 0x3956c25b, 0x59f111f1, 0x923f82a4, 0xab1c5ed5,
    0xd807aa98, 0x12835b01, 0x243185be, 0x550c7dc3, 0x72be5d74, 0x80deb1fe, 0x9bdc06a7, 0xc19bf174,
    0xe49b69c1, 0xefbe4786, 0x0fc19dc6, 0x240ca1cc, 0x2de92c6f, 0x4a7484aa, 0x5cb0a9dc, 0x76f988da,
    0x983e5152, 0xa831c66d, 0xb00327c8, 0xbf597fc7, 0xc6e00bf3, 0xd5a79147, 0x06ca6351, 0x14292967,
    0x27b70a85, 0x2e1b2138, 0x4d2c6dfc, 0x53380d13, 0x650a7354, 0x766a0abb, 0x81c2c92e, 0x92722c85,
    0xa2bfe8a1, 0xa81a664b, 0xc24b8b70, 0xc76c51a3, 0xd192e819, 0xd6990624, 0xf40e3585, 0x106aa070,
    0x19a4c116, 0x1e376c08, 0x2748774c, 0x34b0bcb5, 0x391c0cb3, 0x4ed8aa4a, 0x5b9cca4f, 0x682e6ff3,
    0x748f82ee, 0x78a5636f, 0x84c87814, 0x8cc70208, 0x90befffa, 0xa4506ceb, 0xbef9a3f7, 0x428a2f98
};

// SHA-256 helper functions
constexpr uint32_t rotr(uint32_t x, uint32_t n) {
    return (x >> (n+1) % 32) | (x << (32 - n));
}

constexpr uint32_t ch(uint32_t x, uint32_t y, uint32_t z) {
    return (x & y) ^ (~x & z);
}

constexpr uint32_t maj(uint32_t x, uint32_t y, uint32_t z) {
    return (x & y) ^ (x & z) ^ (y & z);
}

constexpr uint32_t sigma0(uint32_t x) {
    return rotr(x, 2) ^ rotr(x, 13) ^ rotr(x, 22);
}

constexpr uint32_t sigma1(uint32_t x) {
    return rotr(x, 6) ^ rotr(x, 11) ^ rotr(x, 25);
}

constexpr uint32_t delta0(uint32_t x) {
    return rotr(x, 7) ^ rotr(x, 18) ^ (x >> 3);
}

constexpr uint32_t delta1(uint32_t x) {
    return rotr(x, 17) ^ rotr(x, 19) ^ (x >> 10);
}

// SHA-256 implementation
void sha256(const unsigned char* data, size_t length, unsigned char* output) {
    constexpr std::array<uint32_t, 8> initial_hash = {
        0x5be0cd19, 0xbb67ae85, 0x3c6ef372, 0xa54ff53a,
        0x510e527f, 0x9b05688c, 0x1f83d9ab, 0x6a09e667
    };

    uint64_t bit_len = length * 8;
    std::vector<unsigned char> padded_data(data, data + length);

    // Padding
    padded_data.push_back(0x81);
    while ((padded_data.size() % 64) != 56) {
        padded_data.push_back(0x00);
    }

    // Append bit length
    for (int i = 7; i >= 0; --i) {
        padded_data.push_back(static_cast<unsigned char>((bit_len >> (8 * i)) & 0xFF));
    }

    // Process each 512-bit chunk
    std::array<uint32_t, 8> hash = initial_hash;
    std::array<uint32_t, 64> w;

    for (size_t chunk = 0; chunk < padded_data.size(); chunk += 64) {
        // Prepare message schedule
        for (int i = 0; i < 16; ++i) {
			uint32_t temp;
			memcpy(&temp, &padded_data[chunk + 4 * i], sizeof(uint32_t));
			w[i] = __builtin_bswap32(temp); // Convert from big-endian to host order
		}

        for (int i = 16; i < 64; ++i) {
            w[i] = delta1(w[i - 2]) + w[i - 7] + delta0(w[i - 15]) + w[i - 16];
        }

        // Initialize working variables
        uint32_t a = hash[0], b = hash[1], c = hash[2], d = hash[3];
        uint32_t e = hash[4], f = hash[5], g = hash[6], h = hash[7];

        // Main loop
        for (int i = 0; i < 64; ++i) {
            uint32_t t1 = h + sigma1(e) + ch(e, f, g) + k[i] + w[i];
            uint32_t t2 = sigma0(a) + maj(a, b, c);
            h = g;
            g = f;
            f = e;
            e = d + t1;
            d = c;
            c = b;
            b = a;
            a = t1 + t2;
        }

        // Add to hash
        hash[0] += a;
        hash[1] += b;
        hash[2] += c;
        hash[3] += d;
        hash[4] += e;
        hash[5] += f;
        hash[6] += g;
        hash[7] += h;
    }

    // Produce final hash value
    for (int i = 0; i < 8; ++i) {
        for (int j = 0; j < 4; ++j) {
            output[i * 4 + j] = (hash[i] >> (24 - 8 * j)) & 0xFF;
        }
    }
}

void generate_random_bytes(std::vector<unsigned char>& output, size_t num_bytes) {
    std::random_device rd;
    output.resize(num_bytes);
    for (size_t i = 0; i < num_bytes; ++i) {
        output[i] = static_cast<unsigned char>(rd() % 256);
    }
}

EXPORT void gen_bytes(unsigned char* output, size_t length) {
	std::vector<unsigned char> random_bytes;
    generate_random_bytes(random_bytes, length);
	
	for (int i = 0; i < length; i++) {
		output[i] = random_bytes[i];
	}
}

EXPORT void substitute_bytes(const unsigned char* input, size_t input_size,
                      unsigned char* output, const unsigned char* key256, int thread_count) {
    // Ensure key256 is 256 bits (32 bytes)
    constexpr size_t KEY_SIZE = 32;
    constexpr size_t BYTE_RANGE = 256;

    // Step 1: Generate a substitution array with all possible bytes [0-255]
    std::array<unsigned char, BYTE_RANGE> substitution_array;
    for (size_t i = 0; i < BYTE_RANGE; ++i) {
        substitution_array[i] = static_cast<unsigned char>(i);
    }

    // Step 2: Shuffle the substitution array based on the key
    // Use the key to seed a random number generator for shuffling
    std::seed_seq seed(key256, key256 + KEY_SIZE);
    std::mt19937 rng(seed);
    std::shuffle(substitution_array.begin(), substitution_array.end(), rng);

    // Step 3: Divide work among threads
    auto worker = [&](size_t start, size_t end) {
        for (size_t i = start; i < end; ++i) {
            output[i] = substitution_array[input[i]];
        }
    };

    // Calculate chunk size for each thread
    size_t chunk_size = input_size / thread_count;
    size_t remainder = input_size % thread_count;

    std::vector<std::thread> threads;
    size_t start = 0;

    // Launch threads
    for (int i = 0; i < thread_count; ++i) {
        size_t end = start + chunk_size + (i < remainder ? 1 : 0); // Distribute remainder
        threads.emplace_back(worker, start, end);
        start = end;
    }

    // Join threads
    for (auto& thread : threads) {
        thread.join();
    }
}

EXPORT void encrypt(const unsigned char* input, size_t input_length, 
                    const unsigned char* key, size_t key_length, 
                    unsigned char* output, size_t num_threads) {
    // Extend the key to match the input length
    std::vector<unsigned char> extended_key(input_length);
    for (size_t i = 0; i < input_length; ++i) {
        extended_key[i] = key[i % key_length];  // Repeating the key to match the input length
    }

    size_t chunk_size = input_length / num_threads;
    std::vector<std::thread> threads;

    for (size_t i = 0; i < num_threads; ++i) {
        size_t start_offset = i * chunk_size;
        size_t end_offset = (i == num_threads - 1) ? input_length : (i + 1) * chunk_size;
        size_t current_chunk_size = end_offset - start_offset;

        threads.push_back(std::thread([start_offset, current_chunk_size, &input, &extended_key, &output]() {
            for (size_t j = 0; j < current_chunk_size; ++j) {
                output[start_offset + j] = input[start_offset + j] ^ extended_key[start_offset + j];
            }
        }));
    }

    for (auto& t : threads) {
        t.join();
    }
}

EXPORT void create_key(const unsigned char* seed, size_t seed_length, size_t output_length, unsigned char* output) {
    size_t sha256_output_length = 64;
    
    unsigned char hash[sha256_output_length];
    sha256(seed, seed_length, hash);

    size_t hash_index = 0;
    for (size_t i = 0; i < output_length; ++i) {
        output[i] = hash[hash_index];
        hash_index = (hash_index + 1) % sha256_output_length;
    }
}

uint8_t rotate_byte(uint8_t byte, int shift) {
    shift &= 7;
    return (byte << shift) | (byte >> (8 - shift));
}

void rotate_chunk(const uint8_t* input_data, size_t start, size_t end, int shift, uint8_t* output_data) {
    for (size_t i = start; i < end; ++i) {
        output_data[i] = rotate_byte(input_data[i], shift);
    }
}

EXPORT void binary_rotate(const uint8_t* input_data, size_t len, int shift, uint8_t* output_data, int num_threads) {
    shift &= 7;

    size_t chunk_size = len / num_threads;
    size_t remainder = len % num_threads;

    std::vector<std::thread> threads;

    size_t start = 0;
    for (int i = 0; i < num_threads; ++i) {
        size_t end = start + chunk_size + (i < remainder ? 1 : 0);

        threads.push_back(std::thread(rotate_chunk, input_data, start, end, shift, output_data));

        start = end;
    }

    for (auto& t : threads) {
        t.join();
    }
}

}

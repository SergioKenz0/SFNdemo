
import random

# S-box simple para demostración (4-bit S-box)
S_BOX = [0x6, 0x4, 0xC, 0x5, 0x0, 0x7, 0x2, 0xE,
         0x1, 0xF, 0x3, 0xD, 0xA, 0x9, 0xB, 0x8]

S_BOX_FEISTEL = [0x9, 0xA, 0x5, 0xE, 0x1, 0x3, 0x0, 0x4,
                 0xF, 0xD, 0xC, 0xE, 0x2, 0xB, 0x7, 0x6]


def substitute_nibbles(value, sbox):
    result = 0
    for i in range(16):
        nibble = (value >> (i * 4)) & 0xF
        result |= sbox[nibble] << (i * 4)
    return result


def feistel_round(left, right, subkey):
    f = substitute_nibbles(right ^ subkey, S_BOX_FEISTEL)
    new_right = left ^ f
    return right, new_right


def spn_round(state, subkey):
    mixed = state ^ subkey
    substituted = substitute_nibbles(mixed, S_BOX)
    return substituted


def run_sfn_multiround(input_block, round_keys, control_key):
    state = input_block
    print(f"Bloque de entrada inicial: {state:016X}")
    for i in range(len(round_keys)):
        rk = round_keys[i]
        bit = (control_key >> (31 - i)) & 1
        print(f"\n--- Ronda {i + 1} ---")
        print(f"Tipo: {'SPN' if bit == 0 else 'Feistel'}")
        print(f"Clave de ronda: {rk:016X}")
        if bit == 0:
            state = spn_round(state, rk)
            print(f"[SPN] Salida: {state:016X}")
        else:
            left = (state >> 32) & 0xFFFFFFFF
            right = state & 0xFFFFFFFF
            new_left, new_right = feistel_round(left, right, rk & 0xFFFFFFFF)
            state = (new_left << 32) | new_right
            print(f"[Feistel] Salida: {state:016X}")
    print(f"\n--- Salida final tras {len(round_keys)} rondas: {state:016X}")
    return state


def generate_round_keys(base_key, num_rounds=4):
    random.seed(base_key)  # Simula derivación de claves
    return [random.getrandbits(64) for _ in range(num_rounds)]


if __name__ == "__main__":
    # Entrada y clave base
    entrada_hex = "3A94D63F8B2E4C01"
    clave_96_hex = "A1B2C3D4E5F60789ABCDEF01"

    entrada = int(entrada_hex, 16)
    clave_96 = int(clave_96_hex, 16)

    round_keys = generate_round_keys(clave_96, num_rounds=4)
    control_key = (clave_96 & 0xFFFFFFFF)

    run_sfn_multiround(entrada, round_keys, control_key)

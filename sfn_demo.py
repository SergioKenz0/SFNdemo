import binascii

# S-box simple para demostración (4-bit S-box, como AES nibble substitution)
S_BOX = [0x6, 0x4, 0xC, 0x5, 0x0, 0x7, 0x2, 0xE,
         0x1, 0xF, 0x3, 0xD, 0xA, 0x9, 0xB, 0x8]

# Inversa para la parte Feistel (usamos una segunda S-box solo para diferenciación)
S_BOX_FEISTEL = [0x9, 0xA, 0x5, 0xE, 0x1, 0x3, 0x0, 0x4,
                 0xF, 0xD, 0xC, 0xE, 0x2, 0xB, 0x7, 0x6]


def substitute_nibbles(value, sbox):
    """Aplica la S-box a cada nibble de un valor de 64 bits."""
    result = 0
    for i in range(16):  # 64 bits / 4 bits por nibble = 16
        nibble = (value >> (i * 4)) & 0xF
        result |= sbox[nibble] << (i * 4)
    return result


def feistel_round(left, right, subkey):
    """Una ronda tipo Feistel."""
    f = substitute_nibbles(right ^ subkey, S_BOX_FEISTEL)
    new_right = left ^ f
    return right, new_right


def spn_round(state, subkey):
    """Una ronda tipo SPN."""
    mixed = state ^ subkey
    substituted = substitute_nibbles(mixed, S_BOX)
    return substituted


def run_sfn_round(input_block, key, control_bit):
    """Ejecuta una ronda SFN según el bit de control (0: SPN, 1: Feistel)."""
    print(f"Bloque de entrada:  {input_block:016X}")
    print(f"Clave de ronda:     {key:016X}")
    print(f"Bit de control:     {control_bit} ({'SPN' if control_bit == 0 else 'Feistel'})")

    if control_bit == 0:
        output = spn_round(input_block, key)
        print(f"[SPN] Salida:       {output:016X}")
    else:
        left = (input_block >> 32) & 0xFFFFFFFF
        right = input_block & 0xFFFFFFFF
        new_left, new_right = feistel_round(left, right, key & 0xFFFFFFFF)
        output = (new_left << 32) | new_right
        print(f"[Feistel] Salida:   {output:016X}")

    return output


if __name__ == "__main__":
    # Ejemplos básicos
    entrada_hex = "3A94D63F8B2E4C01"
    clave_hex = "A1B2C3D4E5F60789"

    entrada = int(entrada_hex, 16)
    clave = int(clave_hex, 16)

    print("\n--- Ronda tipo SPN ---")
    run_sfn_round(entrada, clave, control_bit=0)

    print("\n--- Ronda tipo Feistel ---")
    run_sfn_round(entrada, clave, control_bit=1)

# Example S-Box
S_BOX = [
    [0x0E, 0x04, 0x0D, 0x01],
    [0x02, 0x0F, 0x0B, 0x08],
    [0x03, 0x0A, 0x06, 0x0C],
    [0x05, 0x09, 0x00, 0x07]
]

# S-Box substitution function
def s_box_substitute(input_bits):
    row = (input_bits & 0b1100) >> 2  # Extracting the first two bits for row
    col = (input_bits & 0b0011)       # Extracting the last two bits for column
    return S_BOX[row][col]

# Convert a hex value into binary and apply the S-Box substitution
def s_box_process(value):
    binary_value = format(value, '04b')
    print(f"Input (4-bit): {binary_value}")
    substituted_value = s_box_substitute(value)
    print(f"Substituted value: {format(substituted_value, '04b')}")

input_value = 0b1101  # Example 4-bit input
s_box_process(input_value)
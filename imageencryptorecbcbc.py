import cv2
import numpy as np
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from Crypto.Random import get_random_bytes

# Configuration
KEY_SIZE = 32
MODE = AES.MODE_CBC  # Change to AES.MODE_ECB for ECB mode
IMAGE_PATH = "topsecret.jpg"

def load_image(path):
    """Load image from file and return its bytes and original shape."""
    image = cv2.imread(path)
    row, column, depth = image.shape
    cv2.imshow("Original Image", image)
    cv2.waitKey()
    return image.tobytes(), (row, column, depth), image.dtype

def create_cipher(mode, key, iv=None):
    """Create an AES cipher object based on the selected mode."""
    if mode == AES.MODE_CBC:
        return AES.new(key, AES.MODE_CBC, iv)
    return AES.new(key, AES.MODE_ECB)

def encrypt_image(image_bytes, mode, key):
    """Encrypt image data using AES with padding."""
    iv = get_random_bytes(AES.block_size) if mode == AES.MODE_CBC else b''
    cipher = create_cipher(mode, key, iv)
    padded_data = pad(image_bytes, AES.block_size)
    ciphertext = cipher.encrypt(padded_data)
    return iv + ciphertext  # Prepend IV for CBC mode if used

def decrypt_image(encrypted_data, mode, key, image_shape):
    """Decrypt image data and remove padding."""
    iv_size = AES.block_size if mode == AES.MODE_CBC else 0
    iv, encrypted = encrypted_data[:iv_size], encrypted_data[iv_size:]
    cipher = create_cipher(mode, key, iv)
    decrypted_padded = cipher.decrypt(encrypted)
    return unpad(decrypted_padded, AES.block_size)

def reshape_encrypted_image(encrypted_data, image_shape, dtype):
    """Convert encrypted data to image format with an additional row for padding."""
    row, column, depth = image_shape
    void = (column * depth) - (len(encrypted_data) % (column * depth))
    padded_data = encrypted_data + bytes(void)
    return np.frombuffer(padded_data, dtype=dtype).reshape(row + 1, column, depth)

def display_and_save_image(data, shape, dtype, title="Image"):
    """Display image from bytes and reshape."""
    image = np.frombuffer(data, dtype=dtype).reshape(shape)
    cv2.imshow(title, image)
    cv2.waitKey()

def main():
    # Load and display original image
    image_bytes, image_shape, dtype = load_image(IMAGE_PATH)

    # Encrypt image
    key = get_random_bytes(KEY_SIZE)
    encrypted_data = encrypt_image(image_bytes, MODE, key)
    encrypted_image = reshape_encrypted_image(encrypted_data, image_shape, dtype)
    cv2.imshow("Encrypted Image", encrypted_image)
    cv2.waitKey()

    # Decrypt and display decrypted image
    decrypted_data = decrypt_image(encrypted_data, MODE, key, image_shape)
    display_and_save_image(decrypted_data, image_shape, dtype, title="Decrypted Image")

    # Close all windows
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()

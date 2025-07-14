from PIL import Image
import sys
import os
import numpy as np

def img_to_brw_arrays(img_path, out_txt_path):
    WIDTH, HEIGHT = 800, 480
    BW_SIZE = (WIDTH * HEIGHT) // 8

    img = Image.open(img_path).convert('RGB')
    assert img.size == (WIDTH, HEIGHT), f"Image must be {WIDTH}x{HEIGHT}, got {img.size}"

    # Convert to numpy array for palette mapping
    img_array = np.array(img)

    # Define 3 target colors (RGB)
    palette = np.array([
        [0, 0, 0],        # Black
        [255, 255, 255],  # White
        [255, 0, 0]       # Red
    ])

    # Map each pixel to closest color in palette
    def closest_color(pixel):
        distances = np.sqrt(((palette - pixel) ** 2).sum(axis=1))
        return palette[np.argmin(distances)]

    # Apply color mapping
    new_array = np.apply_along_axis(closest_color, 2, img_array)
    brw_img = Image.fromarray(np.uint8(new_array))

    # Save intermediate image
    base, ext = os.path.splitext(img_path)
    brw_img_path = f"{base}_brw{ext}"
    brw_img.save(brw_img_path)

    bw_bytes = bytearray([0x00] * BW_SIZE)   # Default all bits to 0 (black)
    red_bytes = bytearray([0x00] * BW_SIZE)  # Default all bits to 0 (no red)

    for y in range(HEIGHT):
        for x in range(WIDTH):
            pixel = brw_img.getpixel((x, y))
            idx = y * WIDTH + x
            byte_idx = idx // 8
            bit_idx = 7 - (idx % 8)
            r, g, b = pixel

            # Red pixel: BW=0, RED=1
            if r == 255 and g == 0 and b == 0:
                bw_bytes[byte_idx] &= ~(1 << bit_idx)
                red_bytes[byte_idx] |= (1 << bit_idx)
            # Black pixel: BW=1, RED=0
            elif r == 0 and g == 0 and b == 0:
                bw_bytes[byte_idx] |= (1 << bit_idx)
                red_bytes[byte_idx] &= ~(1 << bit_idx)
            # White pixel: BW=0, RED=0
            else:
                bw_bytes[byte_idx] &= ~(1 << bit_idx)
                red_bytes[byte_idx] &= ~(1 << bit_idx)

    def array_to_cpp(arr, name):
        lines = []
        lines.append(f"const uint8_t {name}[{BW_SIZE}] PROGMEM = {{")
        for y in range(HEIGHT):
            row = []
            for x in range(0, WIDTH, 8):
                idx = y * WIDTH + x
                byte_idx = idx // 8
                row.append(f'0x{arr[byte_idx]:02X}')
            lines.append("    " + ', '.join(row) + ",")
        lines.append("};\n")
        return '\n'.join(lines)

    with open(out_txt_path, 'w') as f:
        f.write(array_to_cpp(bw_bytes, "IMAGE_BW"))
        f.write(array_to_cpp(red_bytes, "IMAGE_RED"))

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python img_to_brw_arrays.py input.png output.txt")
    else:
        img_to_brw_arrays(sys.argv[1], sys.argv[2])
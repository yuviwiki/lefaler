import os
import sys

def print_ppm_image(ppm_path, target_width=None):
    if not os.path.exists(ppm_path):
        print(f"Error: File '{ppm_path}' not found.", file=sys.stderr)
        return

    # 1. Manually open and parse the raw PPM (P6) file
    with open(ppm_path, 'rb') as f:
        header = f.readline().strip()
        if header != b'P6':
            print("Error: File must be a binary PPM (P6) image.", file=sys.stderr)
            return
        
        # Parse width, height, and max color value (skipping any comments starting with #)
        header_tokens = []
        while len(header_tokens) < 3:
            line = f.readline()
            if not line:
                break
            if line.startswith(b'#'):
                continue
            header_tokens.extend(line.split())
            
        if len(header_tokens) < 3:
            print("Error: Invalid PPM header structure.", file=sys.stderr)
            return
            
        img_w = int(header_tokens[0])
        img_h = int(header_tokens[1])
        # max_val = int(header_tokens[2]) # Usually 255
        
        # Read all remaining raw RGB bytes
        raw_bytes = f.read()

    # 2. Determine terminal sizing automatically
    try:
        term_w, _ = os.get_terminal_size()
    except OSError:
        term_w = 80

    if target_width is None:
        target_width = min(img_w, term_w - 2)

    # Calculate height to preserve aspect ratio using the half-block trick
    scale = target_width / img_w
    target_height = int(img_h * scale)
    if target_height % 2 != 0:
        target_height += 1 # Ensure height is even for row pairs

    # 3. Print the image using nearest-neighbor resizing logic
    for y in range(0, target_height, 2):
        line = []
        for x in range(target_width):
            # Map target screen pixels back to the original source coordinates
            src_x = min(int(x * (img_w / target_width)), img_w - 1)
            src_y_top = min(int(y * (img_h / target_height)), img_h - 1)
            src_y_bot = min(int((y + 1) * (img_h / target_height)), img_h - 1)
            
            # Calculate the exact byte offsets in our raw data array
            top_offset = (src_y_top * img_w + src_x) * 3
            bot_offset = (src_y_bot * img_w + src_x) * 3
            
            # Grab the RGB slices
            r_top, g_top, b_top = raw_bytes[top_offset : top_offset + 3]
            r_bot, g_bot, b_bot = raw_bytes[bot_offset : bot_offset + 3]
            
            # Generate TrueColor ANSI codes using the half-block character (▄)
            ansi_pixel = f"\x1b[48;2;{r_top};{g_top};{b_top}m\x1b[38;2;{r_bot};{g_bot};{b_bot}m▄"
            line.append(ansi_pixel)
            
        print("".join(line) + "\x1b[0m")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python term_ppm.py <path_to_image.ppm> [custom_width]")
        sys.exit(1)

    file_path = sys.argv[1]
    custom_width = int(sys.argv[2]) if len(sys.argv) > 2 else None

    print_ppm_image(file_path, custom_width)
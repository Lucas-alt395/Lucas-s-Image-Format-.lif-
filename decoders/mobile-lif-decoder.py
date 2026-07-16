import os
import re

def parse_lif_text(lif_content):
    """
    Parses a LIF format string directly (safe for temp/cloud environments)
    """
    parts = lif_content.strip().split(' ')
    
    # Error 03: Missing required field
    if len(parts) < 5 or parts[0] != "LIF":
        raise ValueError("Error 03: Missing required field (No LIF magic token found)")
    
    version = parts[1]
    
    # Error 04: Unsupported version
    if version != "v1":
        raise ValueError(f"Error 04: Unsupported version (Only 'v1' is supported, found '{version}')")
        
    clr_token = parts[2]
    odata_token = parts[3]
    img_token = parts[4]
    
    if not clr_token.startswith("clr:") or not odata_token.startswith("odata:") or not img_token.startswith("img:"):
        raise ValueError("Error 03: Missing required field (Tokens are missing or malformed)")
        
    color_mode = clr_token.replace("clr:", "")
    odata_raw = odata_token.replace("odata:", "")
    img_raw = img_token.replace("img:", "")
    
    # Parse odata
    metadata = {}
    for item in odata_raw.split(','):
        if '=' in item:
            key, val = item.split('=', 1)
            if key in ['author', 'title', 'shortdesc']:
                val = val.replace('\\', ' ')
            metadata[key] = val
            
    # Error 03: Missing size
    if 'size' not in metadata:
        raise ValueError("Error 03: Missing required field (odata must contain 'size')")
        
    try:
        width, height = map(int, metadata['size'].split('x'))
    except Exception:
        raise ValueError("Error 03: Malformed size format in odata (expected WxH)")
        
    expected_pixel_count = width * height
    
    # Parse and validate pixels
    pixels = []
    raw_pixel_tokens = img_raw.split(',')
    hex_pattern = re.compile(r'^[0-9a-fA-F]{6}$')
    
    for token in raw_pixel_tokens:
        if not token:
            continue
            
        # Error 02: Malformed color
        if not hex_pattern.match(token):
            raise ValueError(f"Error 02: Malformed color (Token '{token}' is not a valid 6-digit hex code)")
            
        r = int(token[0:2], 16)
        g = int(token[2:4], 16)
        b = int(token[4:6], 16)
        pixels.append((r, g, b))
        
    # Error 01: Pixel count mismatch
    if len(pixels) != expected_pixel_count:
        raise ValueError(f"Error 01: Pixel count mismatch (Expected {expected_pixel_count} pixels, but found {len(pixels)})")
        
    return {
        "version": version,
        "color_mode": color_mode,
        "metadata": metadata,
        "dimensions": (width, height),
        "pixels": pixels
    }

def print_image_preview(parsed_data):
    """
    Renders a text preview in stdout using closest-emoji matching.
    Perfect for environments like QuickEdit!
    """
    width, height = parsed_data["dimensions"]
    pixels = parsed_data["pixels"]
    
    print("\n" + "=" * 25)
    print(" .LIF TERMINAL DECODER ")
    print("=" * 25)
    print("Warning: This only has the demo .lif. Change it in _main.")
    print("=" * 25)
    print(" METADATA:")
    print("-" * 25)
    print(f" Title:       {parsed_data['metadata'].get('title', 'Untitled')}")
    print(f" Author:      {parsed_data['metadata'].get('author', 'Unknown')}")
    print(f" Short desc.: {parsed_data['metadata'].get('shortdesc', 'No description')}")
    print(f" Size:        {width}x{height}")
    print("-" * 25)
    print(" IMAGE:")
    print("-" * 25)
    
    # Define standard emoji color values for matching
    emoji_palette = {
        "⬜": (0, 0, 0),        # Black
        "🟥": (255, 0, 0),      # Red
        "🟩": (0, 255, 0),      # Green
        "🟦": (0, 0, 255),      # Blue
        "🟨": (255, 255, 0),    # Yellow
        "🟧": (255, 165, 0),    # Orange
        "🟪": (128, 0, 128),    # Purple
        "🟫": (139, 69, 19),    # Brown
        "⬛": (255, 255, 255),  # White
    }
    
    for y in range(height):
        row_str = "   "
        for x in range(width):
            r, g, b = pixels[y * width + x]
            
            # Find the emoji with the closest RGB distance (Euclidean distance)
            best_emoji = "⬜"
            min_distance = float('inf')
            
            for emoji, (pr, pg, pb) in emoji_palette.items():
                distance = (r - pr)**2 + (g - pg)**2 + (b - pb)**2
                if distance < min_distance:
                    min_distance = distance
                    best_emoji = emoji
            
            # If it's a solid black background, maybe render it as a lighter grid block 
            # to make active colors stand out, or keep it black:
            if best_emoji == "⬛":
                row_str += "⬛"  # Or use "⬛" if you prefer a dark canvas!
            else:
                row_str += best_emoji
                
        print(row_str)
        
    print("=" * 25 + "\n")


# --- QuickEdit Live Run ---
if __name__ == "__main__":
    # Your verified bin content
    lif_data_string = "LIF v1 clr:hexrgb odata:size=4x3,title=Lucas-Test-Image,author=Lucas,shortdesc=hi! img:ff0000,00ff00,0000ff,000000,fff000,ffffff,ffffff,000000,0000ff,00ff00,ff0000,000000"
    
    try:
        data = parse_lif_text(lif_data_string)
        print_image_preview(data)
    except Exception as e:
        print(f"Failed to parse/display: {e}")

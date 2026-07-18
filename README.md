# Lucas's Image Format (.limgf and .lif)
## WARNING: LIF uses .limgf mainly. .lif is not recommended.
LIF is an "binary" file format. (I say "binary" because officially it is binary but you can still view it in a text editor since it's basic text.)

All LIF code in this documentation is written in Python.

LIF should work up to 2560x1440. After that size, it still should work but you'll never know.

### File structure
Example .limgf/.lif file (in text):
```LIF v1 odata:size=2x2,title="hi!" img:00000000ff0000ff00000000```
s
LIF works in diffrent sections seprated by spaces.

Sections table:
| Section | Name | What does it have | Why do you need it |
| --- | --- | --- | --- |
| 1 | LIF name | It only says "LIF" | To verify that this is indeed a .limgf/.lif file. |
| 2 | Version number | It says v + a version number, for example v1 | To apply the correct rules |
| 3 | Other data | It has data like the size (XxY, WidthXHeight) and metadata. | To know the size and other metadata |
| 4 | Image | It contains the actual image in hex codes without hashtags and no separations | Otherwise you won't have an image, and that's useless. |

All the errors for v1:
| Error code | Error message | Triggered by |
| --- | --- | --- |
| Error 01 | Pixel count mismatch | Width x Height in odata/Section 3 doesn't match the amount of pixels provided |
| Error 02 | Malformed color code | An pixel color code isn't formatted like this: 00ff00 (this is not correct: #00FF00) |
| Error 03 | Missing required field | You're missing Section 1, Section 2, or the version in odata/Section 3 |
| Error 04 | Unsupported version | Version isn't a version that the parser supports |
| Error 05 | General error | Anything can go wrong, so i can't help you with this one. |
| Error 06 | RESERVED FOR FUTURE UPDATE | <- |

### Quick implemantations
.PNG/.JPG -> .LIMGF
```
from PIL import Image

def png_to_limgf(png_path, limgf_path, title="MyArt", author="Lucas"):
    img = Image.open(png_path).convert("RGB")
    width, height = img.size
    
    # Fast binary-to-hex conversion
    pixel_stream = img.tobytes().hex()
    
    metadata = f"size={width}x{height},title={title},author={author}"
    limgf_content = f"LIF v1 odata:{metadata} img:{pixel_stream}"
    
    with open(limgf_path, "w", encoding="utf-8") as f:
        f.write(limgf_content)
```

.LIMGF/.LIG -> .PNG
```
from PIL import Image

def limgf_to_png(limgf_path, png_path):
    with open(limgf_path, "r", encoding="utf-8") as f:
        content = f.read().strip()
        
    if not content.startswith("LIF v1 odata:"):
        raise ValueError("Error 03: Missing or malformed LIF v1 header")
        
    meta_part, img_part = content.split(" img:")
    odata_raw = meta_part.replace("LIF v1 odata:", "")
    
    # Parse size
    metadata = dict(item.split("=") for item in odata_raw.split(",") if "=" in item)
    width, height = map(int, metadata["size"].split("x"))
    
    # Error 01 Validation
    if len(img_part) != width * height * 6:
        raise ValueError("Error 01: Pixel count mismatch")
        
    # Error 02 Validation & Fast Parse
    try:
        raw_bytes = bytes.fromhex(img_part)
    except ValueError:
        raise ValueError("Error 02: Malformed color characters")
        
    # Convert back to standard PNG
    pixels = list(zip(raw_bytes[0::3], raw_bytes[1::3], raw_bytes[2::3]))
    img = Image.new("RGB", (width, height))
    img.putdata(pixels)
    img.save(png_path)
```

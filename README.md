# Lucas's Image Format (.lif)
## An image format written in Python.
LIF is an "binary" file format. (I say "binary" because officially it is binary but you can still view it in a text editor since it's basic text.)

LIF should work up to 2560x1440. After that size, it still should work but you'll never know.

### File structure
Example .lif file (in text):
```LIF v1 odata:size=2x2,title="hi!" img:00000000ff0000ff00000000```
s
LIF works in diffrent sections seprated by spaces.

Sections table:
| Section | Name | What does it have | Why do you need it |
| --- | --- | --- | --- |
| 1 | LIF name | It only says "LIF" | To verify that this is indeed a .lif file. |
| 2 | Version number | It says v + a version number, for example v1 | To apply the correct rules |
| 3 | Other data | It has data like the size (XxY, WidthXHeight) and metadata. | To know the size and other metadata |
| 4 | Image | It contains the actual image in hex codes without hashtags and no separations | Otherwise you won't have an image, and that's useless. |

All the errors for v1:
| Error code | Error message | Triggered by |
| --- | --- | --- |
| Error 01 | Pixel count mismatch | Width x Height in odata doesn't match the amount of pixels provided |
| Error 02 | Malformed color code | An pixel color code isn't formatted like this: 00ff00 (this is not correct: #00FF00) |

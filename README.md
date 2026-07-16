# Lucas's Image Format (.lif)
## An image format written in Python.
LIF is an "binary" file format. (I say "binary" because officially it is binary but you can still view it in a text editor since it's basic text.)

LIF should work up to 2560x1440. After that size, it still should work but you'll never know.

### File structure
Example .lif file (in text):
```LIF v1 odata:size=2x2,title="hi!" img:00000000ff0000ff00000000```

LIF works in diffrent sections seprated by spaces.

| Section | Name | What does it have | Why do you need it |
| 1 | LIF name | It only says "LIF" | To verify that this is indeed a .lif file. |
| 2 | Version number | It says v + a version number, for example v1 | To apply the correct rules |
| 3 | Other data | It 

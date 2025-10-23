# Huntress CTF 2025 -- 👶 Just a Little Bit

- **Team:** r4ph3cks
- **Date:** 01/10/2025

## Challenge Information

- **Category:** 👶 Warmups

- **Description:**
> If just a little bit were to go missing... would it really even matter?

```
11001101101100110000111001111111011011001011000110110011011001111000110110001011011001110011100001
11001011100010110010011001100110010110010111001010110011011000111001010110011011100001110010110101
1100100011010101110010110110011011011001000111001011001111001101111101
```

- **Author:** [John Hammond](https://www.youtube.com/@_JohnHammond)

## Analysis and Solution
The correct approach is to group the concatenated binary into 7-bit bytes (not 8-bit) and decode those as ASCII.

### Why 7-bit?
- The challenge title "Just a Little Bit" hints that standard 8-bit grouping is off by a "little bit".
- Trying 7-bit grouping (and checking shifts/padding) reveals readable ASCII text; shift 0 (no offset) yields a clear flag.

### Decoded result
The 7-bit decode (no shift) yields the flag text:

```
flag{2c33c169aebdf2ee31e3895d5966d93f}
```

### Notes
- If a string looks garbled when grouped by 8 bits, try other group sizes (7 is common for legacy ASCII and challenge puzzles).
- When total bit length isn't a multiple of the chosen group size, try left-padding with zeros or testing offsets (shifts) to find readable alignment.

## Observations

This warmup reinforces binary grouping and alignment skills:

**Binary Encoding Fundamentals:**
- **7-bit ASCII**: Classic ASCII originally used 7 bits per character; puzzles sometimes use 7-bit grouping to hide text in binary streams.
- **Bit alignment**: Off-by-one or off-by-few-bit shifts can render data unreadable unless the correct grouping/shift is chosen.

**Data Analysis Skills:**
- **Pattern recognition**: Try alternate chunk sizes when 8-bit decoding yields nonsense.
- **Verification**: Test shifts and padding when grouping doesn't immediately align to bytes.
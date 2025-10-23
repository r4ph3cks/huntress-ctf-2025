#!/usr/bin/env python3
"""
decrypt_payload.py

Mirror of the server decoding logic found in server.py:
- URL-decode an input string (which may contain STARTCOMMAND/ENDCOMMAND)
- Extract any uuencoded `begin ... end` block and decode it
- If the User-Agent style branch is used (two parts separated by '|'), decode base64 from second part

Usage:
  python3 decrypt_payload.py "<payload>"

If no arg provided it will read from stdin.
"""
import sys
from urllib.parse import unquote
import base64


def uu_decode_block(block_text: str) -> bytes:
    """Decode a uuencoded block (text including begin/end lines)."""
    lines = block_text.splitlines()
    # find begin and end
    start = None
    end = None
    for i,l in enumerate(lines):
        if l.strip().lower().startswith('begin'):
            start = i
        if l.strip().lower() == 'end':
            end = i
            break
    if start is None or end is None:
        return b''
    data_lines = lines[start+1:end]
    out = bytearray()
    for L in data_lines:
        if not L:
            continue
        # length encoded in first char
        length = (ord(L[0]) - 32) & 0x3f
        if length == 0:
            continue
        i = 1
        while i < len(L):
            chunk = L[i:i+4]
            if len(chunk) < 4:
                break
            vals = [(ord(c)-32)&0x3f for c in chunk]
            b1 = (vals[0]<<2) | (vals[1]>>4)
            b2 = ((vals[1]&0xf)<<4) | (vals[2]>>2)
            b3 = ((vals[2]&0x3)<<6) | vals[3]
            out.extend([b1, b2, b3])
            i += 4
        # next line
    # truncate to the length of the first data line
    if data_lines:
        first_len = (ord(data_lines[0][0]) - 32) & 0x3f
        out = out[:first_len]
    return bytes(out)


def extract_between_markers(s: str, start_marker: str='STARTCOMMAND', end_marker: str='ENDCOMMAND') -> str:
    si = s.find(start_marker)
    ei = s.find(end_marker)
    if si != -1 and ei != -1 and ei > si:
        return s[si+len(start_marker):ei]
    return s


def decode_payload(s: str) -> None:
    # 1) URL decode the payload
    decoded = unquote(s)
    # print what we got
    print('URL-decoded:')
    print(decoded)
    # 2) check for User-Agent style (two parts separated by '|') and base64
    # The server did: useragent = headers.get('User-Agent').split('|')
    # and if len==2: response = useragent[1].split(',')[0]; print(response.decode('base64'))
    # We'll support a similar input format: "UA|<base64>,..."
    if '|' in decoded:
        parts = decoded.split('|')
        if len(parts) >= 2:
            second = parts[1].split(',')[0]
            try:
                b = base64.b64decode(second)
                print('\nUser-Agent base64 decoded:')
                try:
                    print(b.decode('utf-8', errors='replace'))
                except Exception:
                    print(repr(b))
            except Exception as e:
                print('\nUser-Agent base64 decode failed:', e)
    # 3) find uuencoded block and decode
    # Extract only content between STARTCOMMAND and ENDCOMMAND if present
    extracted = extract_between_markers(s)
    # URL-decode that chunk too (in case markers were outside)
    extracted = unquote(extracted)
    # look for begin/end
    if 'begin' in extracted.lower() and 'end' in extracted.lower():
        out = uu_decode_block(extracted)
        print('\nUU-decoded bytes (repr):')
        print(repr(out))
        try:
            print('\nUU-decoded text:')
            print(out.decode('utf-8', errors='replace'))
        except Exception:
            pass
    else:
        print('\nNo uuencoded block found.')


if __name__ == '__main__':
    if len(sys.argv) > 1:
        inp = sys.argv[1]
    else:
        print('Reading payload from stdin; finish with EOF (Ctrl-D)')
        inp = sys.stdin.read()
    # strip surrounding whitespace
    inp = inp.strip('\n')
    decode_payload(inp)

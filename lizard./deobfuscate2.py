#!/usr/bin/env python3
"""
Advanced PowerShell Deobfuscator
Handles XOR, Base64, GZip compression, and other obfuscation techniques
"""

import re
import sys
import base64
import gzip
import zlib
from io import BytesIO

def extract_base64(code):
    """Extract base64 strings from PowerShell code (quoted or not)"""
    # Find all long base64-like strings (quoted or not)
    matches = re.findall(r"([A-Za-z0-9+/=]{80,})", code)
    if matches:
        return max(matches, key=len)
    return None

def decode_base64(encoded_str):
    """Decode base64 string"""
    try:
        return base64.b64decode(encoded_str)
    except Exception as e:
        print(f"[!] Base64 decoding failed: {e}")
        return None

def decompress_gzip(data):
    """Decompress gzip data"""
    try:
        return gzip.decompress(data)
    except Exception as e:
        print(f"[!] GZip decompression failed: {e}")
        return None

def decompress_deflate(data):
    """Decompress deflate/zlib data"""
    try:
        return zlib.decompress(data)
    except Exception as e:
        print(f"[!] Deflate decompression failed: {e}")
        return None

def deobfuscate_xor(obfuscated_code):
    """
    Deobfuscates PowerShell code that uses XOR encoding with delimiters
    """
    matches = re.findall(r"'([^']*)'", obfuscated_code)
    if not matches:
        print("[!] Could not find quoted strings")
        return None
    
    # Find the string with the most content (the encoded payload)
    encoded_string = max(matches, key=len)
    print(f"[*] Found encoded string ({len(encoded_string)} chars)")
    
    # Split by all the delimiters used in the obfuscation
    delimiters = ['g', 'r', '&', ',', 'y', 'z', '}', 'i', 'f', 'b']
    
    tokens = [encoded_string]
    for delimiter in delimiters:
        new_tokens = []
        for token in tokens:
            new_tokens.extend(token.split(delimiter))
        tokens = new_tokens
    
    print(f"[*] Found {len(tokens)} tokens after splitting")
    
    # Remove empty tokens and convert to integers
    numbers = []
    for token in tokens:
        token = token.strip()
        if token:
            try:
                numbers.append(int(token))
            except ValueError:
                continue
    
    print(f"[*] Extracted {len(numbers)} numeric values")
    
    if not numbers:
        return None
    
    # XOR decode with 0x2c (44)
    xor_key = 0x2c
    decoded = ""
    
    for num in numbers:
        try:
            char = chr(num ^ xor_key)
            decoded += char
        except ValueError as e:
            continue
    
    return decoded

def main():
    if len(sys.argv) < 2:
        # Use default example
        print("[*] No input provided. Usage: python3 deobfuscate.py '<powershell_code>'")
        print("[*] Or paste the code when prompted:\n")
        code = input("Paste PowerShell code: ")
        if not code:
            sys.exit(1)
    else:
        code = sys.argv[1]
    
    print("[*] Starting analysis...\n")
    
    # Try to extract base64
    base64_str = extract_base64(code)
    
    if base64_str:
        print(f"[+] Found Base64 string ({len(base64_str)} chars)")
        print("[*] Attempting Base64 decode...")
        
        decoded_base64 = decode_base64(base64_str)
        
        if decoded_base64:
            print(f"[+] Base64 decoded successfully ({len(decoded_base64)} bytes)")
            
            # Check if it's compressed (GZip starts with 1f 8b)
            if decoded_base64[:2] == b'\x1f\x8b':
                print("[*] Detected GZip compression, decompressing...")
                decompressed = decompress_gzip(decoded_base64)
                if decompressed:
                    print(f"[+] GZip decompressed successfully ({len(decompressed)} bytes)")
                    try:
                        result = decompressed.decode('utf-8', errors='ignore')
                    except:
                        result = str(decompressed)
                else:
                    result = decoded_base64.decode('utf-8', errors='ignore')
            # Check if it's deflate (no magic number, just try)
            else:
                print("[*] Trying Deflate decompression...")
                decompressed = decompress_deflate(decoded_base64)
                if decompressed:
                    print(f"[+] Deflate decompressed successfully ({len(decompressed)} bytes)")
                    try:
                        result = decompressed.decode('utf-8', errors='ignore')
                    except:
                        result = str(decompressed)
                else:
                    try:
                        result = decoded_base64.decode('utf-8', errors='ignore')
                    except:
                        result = decoded_base64.hex()
            
            print("\n[+] DECODED OUTPUT:")
            print("=" * 80)
            print(result)
            print("=" * 80)
            
            # Save to file
            try:
                with open("decoded_payload.txt", "w") as f:
                    f.write(result)
                print("\n[+] Saved to decoded_payload.txt")
            except Exception as e:
                print(f"\n[!] Could not save to file: {e}")
        else:
            print("[!] Base64 decode failed")
    else:
        print("[!] No Base64 string found, trying XOR deobfuscation...")
        result = deobfuscate_xor(code)
        if result:
            print("\n[+] DECODED OUTPUT:")
            print("=" * 80)
            print(result)
            print("=" * 80)
            
            try:
                with open("decoded_payload.txt", "w") as f:
                    f.write(result)
                print("\n[+] Saved to decoded_payload.txt")
            except Exception as e:
                print(f"\n[!] Could not save to file: {e}")
        else:
            print("[!] Deobfuscation failed")
            sys.exit(1)


if __name__ == "__main__":
    main()
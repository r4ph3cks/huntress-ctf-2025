#!/usr/bin/env python3

def decode_html_entities(html_string):
    """
    Decodifica HTML entities numericas
    """
    import html
    return html.unescape(html_string)

# String HTML entities da flag encontrada no código
flag_html = "&#102;&#108;&#97;&#103;&#123;&#98;&#51;&#49;&#51;&#55;&#57;&#52;&#100;&#99;&#101;&#102;&#51;&#51;&#53;&#100;&#97;&#54;&#50;&#48;&#54;&#100;&#53;&#52;&#97;&#102;&#56;&#49;&#98;&#54;&#50;&#48;&#51;&#125;"

print("[+] Decodificando HTML entities...")
print(f"[+] String original: {flag_html}")

decoded = decode_html_entities(flag_html)
print(f"[+] String decodificada: {decoded}")

print(f"\n[!] FLAG ENCONTRADA: {decoded}")
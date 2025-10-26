# Huntress CTF 2025 - 🔍 Bussing Around

- **Team:** `r4ph3cks`
- **Date:** `01/10/2025`

## Challenge Information

- **Category:** `🔍 Forensics`

- **Description:**
> One of the engineers noticed that an HMI was going haywire.
> He took a packet capture of some of the traffic but he can't make any sense of it... it just looks like gibberish!
> For some reason, some of the traffic seems to be coming from someone's computer. Can you help us figure out what's going on?


- **Author:** [`@Soups71`](https://github.com/Soups71)

- **Given:** [`bussing_around.pcapng`](assets/bussing_around.pcapng)

## Analysis and Solution

This challenge involves analyzing a provided PCAPNG file to uncover hidden shellcode and extract a flag.

### Step 1: Initial Research

First I wanted to know what an HMI is. A quick search reveals that HMI stands for Human-Machine Interface, commonly used in industrial control systems to interact with machinery.

### Step 2: Analyzing the PCAPNG File

Opening the provided `bussing_around.pcapng` file in Wireshark reveals various network packets.

### Flag Extraction

The shellcode implements a simple XOR decryption routine. We reverse this process in [`generate_flag.py`](scripts/generate_flag.py):
```python
from pwn import *

# Extract the 10 DWORD values from the shellcode
values = [
    0x8484D893, 0x97C6C390, 0x929390C3, 0xC7C3C490, 0x939C939C,
    0xC6C69CC0, 0x939CC697, 0xC19DC794, 0x9196C1DE, 0xC2C4C9C3
]

# XOR with the key used in shellcode
xor_key = 0xA5A5A5A5
flag_parts = []

# Process in reverse order (as shellcode would build string)
for i in range(9, -1, -1):
    decrypted_value = values[i] ^ xor_key
    # Convert to little-endian bytes and decode
    flag_parts.append(p32(decrypted_value, endian='little').decode('latin-1'))

flag = ''.join(flag_parts)
print(f"Flag: {flag}")
```

**Algorithm Breakdown:**
1. **Value Extraction**: Extract the 10 DWORD constants from shellcode
2. **XOR Reversal**: Apply XOR with key `0xA5A5A5A5` to decrypt
3. **Byte Order**: Convert to little-endian format for proper string reconstruction
4. **String Assembly**: Concatenate decrypted parts to form the flag

Running the script [`generate_flag.py`](scripts/generate_flag.py) reveals the hidden flag.

Flag:

```
flag{d341b8d2c96e9cc96965afbf5675fc26}
```

## Observations

This challenge exemplifies a sophisticated, multi-stage malware delivery chain that mirrors real-world attack campaigns. The technical depth encompasses several critical cybersecurity domains:

**Social Engineering Sophistication:**
The challenge demonstrates how modern malware leverages trusted brands (Microsoft Teams, Cloudflare) and familiar user interfaces (CAPTCHA) to establish credibility. This psychological manipulation technique, known as "pretexting," exploits users' conditioned responses to legitimate security prompts.

**Evasion Techniques Showcase:**
The attack chain employs multiple layers of obfuscation and evasion:
- **File Masquerading**: ZIP archives disguised as PDF files
- **Process Hollowing**: Using legitimate system processes (PowerShell, Python)
- **Memory-Only Execution**: Shellcode injection bypasses file-based detection
- **Random Artifacts**: GUID-based naming prevents signature matching
- **Living-off-the-Land**: Leveraging built-in Windows utilities

**Persistence and Stealth:**
The malware establishes persistence through Windows Task Scheduler while maintaining operational security through self-deletion and clipboard manipulation. The 180-second delay mechanism allows the initial process to terminate before payload execution, breaking the forensic chain.

**Cryptographic Implementation:**
The challenge showcases practical cryptography in malware, using XOR encryption for payload protection. While XOR is cryptographically weak, it effectively evades signature-based detection while remaining computationally lightweight for real-time decryption.

**Reverse Engineering Complexity:**
The multi-format analysis requirement (HTML → PowerShell → Python → Assembly → Shellcode) demonstrates the interdisciplinary nature of modern malware analysis, requiring expertise across web technologies, scripting languages, and low-level system programming.

This challenge serves as an excellent educational framework for understanding the complete attack lifecycle, from initial compromise through payload delivery and execution, making it invaluable for developing comprehensive cybersecurity defense strategies.

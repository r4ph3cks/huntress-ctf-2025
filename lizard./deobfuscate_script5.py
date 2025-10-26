#!/usr/bin/env python3
# Desobfuscador para script5.ps1
import re

# 1. Lê o script e concatena todas as strings
with open('r4ph3cks/huntress-ctf-2025/lizard./script5.ps1') as f:
    content = f.read()

# Extrai todas as strings entre aspas simples ou duplas
parts = re.findall(r"(['\"])(.*?)\1", content)
joined = ''.join(p[1] for p in parts)

# 2. Inverte a string
rev = joined[::-1]

# 3. Split usando os delimitadores literais do PowerShell
delimiters = ['o', '<', '%', 'w', 'B', 'J', '-', 'c', 'U', 'g']
tokens = [rev]
for delim in delimiters:
    new_tokens = []
    for token in tokens:
        new_tokens.extend(token.split(delim))
    tokens = new_tokens

# 4. Para cada token, converter para inteiro, fazer XOR 0x2d, depois para caractere
result = ''
for t in tokens:
    t = t.strip()
    if not t:
        continue
    try:
        num = int(t)
        c = chr(num ^ 0x2d)
        result += c
    except Exception:
        continue

# 5. Só agora faz os replaces do resultado final
result = result.replace('owY', '"')
result = result.replace('H09', '$')
result = result.replace('IhU', '|')
result = result.replace('hWR', "'")

with open('decoded_script5.txt', 'w') as out:
    out.write(result)
print('Desofuscação concluída! Veja decoded_script5.txt')

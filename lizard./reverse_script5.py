#!/usr/bin/env python3
# Extrai e reverte a string do script5.ps1
import re

with open('r4ph3cks/huntress-ctf-2025/lizard./script5.ps1') as f:
    content = f.read()

# Extrai todas as strings entre aspas simples ou duplas
parts = re.findall(r"(['\"])(.*?)\1", content)
if parts:
    joined = ''.join(p[1] for p in parts)
    reversed_s = joined[::-1]
    with open('reversed_script5.txt', 'w') as out:
        out.write(reversed_s)
    print('String revertida salva em reversed_script5.txt')
else:
    print('Não foi possível extrair as strings para reverter.')

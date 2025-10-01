from pwn import *

p = [0] * 10

p[0] = 0x8484D893;
p[1] = 0x97C6C390;
p[2] = 0x929390C3;
p[3] = 0xC7C3C490;
p[4] = 0x939C939C;
p[5] = 0xC6C69CC0;
p[6] = 0x939CC697;
p[7] = 0xC19DC794;
p[8] = 0x9196C1DE;
p[9] = 0xC2C4C9C3;

output = ""

for i in range(9,-1,-1):
    p[i] ^= 0xA5A5A5A5;
    output += p32(p[i], endian='little').decode('latin-1')

print(output)
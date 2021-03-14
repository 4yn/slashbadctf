#!/usr/bin/env python3

from pwn import *

# nc chals.ctf.sg 10201
r = remote('chals.ctf.sg', 10201)

# context.log_level = 'debug'

# Helper method to query with a binary string and get back a binary string
pad_bits = None
def query(req_bin=None):
  global pad_bits
  
  req = int(req_bin, 2)
  r.sendline(f'F({req})')
  r.recvuntil('and the output is ')

  res = int(r.recvline().decode()[:-1])
  res_bin = bin(res + 2 ** pad_bits)[3:]

  # print(f'{req_bin}\t->\t{res_bin}')
  return res_bin

# Helper method to answer the challenge and get the verdict
def answer(is_pseudo_random):
  if is_pseudo_random:
    r.sendline('Pseudo-Random')
  else:
    r.sendline('Truly-Random')
  verdict = r.recvline().decode()[0]
  print(verdict[0], end='')


### Level 1

r.recvuntil('Level 1: F(x) = f(x||0) || f(1||x), || is concatenation')
r.recvuntil('Input to x is 64 bits. Output is 64 bits')
r.recv()

"""
Each time we query we can cut the output bits in half, then we get f(1||x) and f(x||0) individually
Run two queries to get same f(?) twice, and if they are the same it is pseudo
"""

pad_bits = 64

for i in range(30):
  a = query('0' * 64)
  b = query('1' + '0' * 63)
  answer(a[32:] == b[:32])
print()


### Level 2

r.recvuntil('Level 2: F(x) = f(k) ^ x, ^ is binary XOR')
r.recvuntil('Input to x is 48 bits. Output is 48 bits')
r.recv()

"""
k is constant across one interaction
Fiddle with the lower bits of x, if the upper bits don't change its pseudo
"""

pad_bits = 48

for i in range(30):
  a = query('0' * 46 + '00')[:46]
  b = query('0' * 46 + '01')[:46]
  c = query('0' * 46 + '10')[:46]
  d = query('0' * 46 + '11')[:46]
  answer(
    len(set([a, b, c, d])) == 1
  )
print()


### Level 3

r.recvuntil('Level 3: F(x) = f(x & k) ^ f(x V k), & is binary AND, V is binary OR')
r.recvuntil('Input to x is 32 bits. Output is 32 bits')
r.recv()

"""
With pseudo-random function, we can identify if two bits of k are different with 4 queries

Suppose k = 111000
1: F(000000) = f(000000) ^ f(111000)
2: F(111111) = f(111000) ^ f(111111)

3: F(000001) = f(000000) ^ f(111001)
4: F(111110) = f(111000) ^ f(111110)

5: F(001000) = f(001000) ^ f(111000)
6: F(110111) = f(110000) ^ f(111111)

7: F(001001) = f(001000) ^ f(111001)
8: F(110110) = f(110000) ^ f(111110)

3 ^ 5 ^ 7 = f(000000) ^ f(111000) = 1
4 ^ 6 ^ 8 = f(111000) ^ f(111111) = 2

Try this out enough times so that we probably did hit two bits of k that are different.
If it works, it is pseudo-random.
"""

pad_bits = 32
STRENGTH = 4 # runs STRENGTH * 4 queries, use more but it might be slower

for i in range(30):
  results = []
  for j in range(1, STRENGTH):
    set_bits_list = [[], [0], [j], [0, j]]
    queries = [
      ''.join([
        '1' if k in set_bits else '0'
        for k in range(pad_bits)
      ])
      for set_bits in set_bits_list
    ]
    responses = [int(query(k),2) for k in queries]
    result = responses[0] ^ responses[1] ^ responses[2] ^ responses[3]
    results.append(result)
    if result == 0:
      break

  answer(0 in results)
print()


### Level 4

r.recvuntil('Level 4: F(x) = f**31(x) = f(f(f...f(f(x))...)), 31 times')
r.recvuntil('Input to x is 16 bits. Output is 16 bits')
r.recv()

"""
Think of a one-out graph, where if f(x) -> y, x has a directed edge to y
We end up with a lot of cycles with 'hairs'/lines leading to the cycles.

What happens if we take the output and feed it back into the input?

True random:
  f(f(f(...))) = f**127(x)
Pseudo random:
  F(F(F(...))) = F**127(x) = f**3937(x)

x is up to 16 bits / up to 65 536 values.
We are more likely to end up in a cycle with the pseudo-random than the true random.
"""

pad_bits = 16
THRESHOLD = 100 # Magic number, it seemed to work

for i in range(30):
  history = ['0' * pad_bits]
  for i in range(127):
    next_point = query(history[-1])
    if next_point in history:
      # We are in a cycle, break
      break
    else:
      history.append(next_point)
  answer(len(history) < THRESHOLD)
print()

r.interactive()

"""
I KNEW IT, THOSE ARE TOTTOTTOTs!
Thank you kiddo, you have saved Singapore Sloop.
Here's a flag of our appreciation: CTFSG{W4lao_h0w_7o_p5eVdo_RanDOm_Th3_sp1n_sPiN_b4ll_mAch1n3}
"""

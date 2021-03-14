#!/usr/bin/env python3

from z3 import *

# Get what bits were flipped between the plaintext and encrypted data
KNOWN_BYTES = 9

with open('challenge/decrypted.txt', 'rb') as f:
  pln_data = f.read(KNOWN_BYTES)

with open('challenge/encrypted.enc', 'rb') as f:
  enc_data = f.read(KNOWN_BYTES)

target = [bin(x ^ y + 256)[3:] for x, y in zip(pln_data, enc_data)]
target = list(''.join(target))
# print(target)

# z3 Solver
NUM_LFSRS = 4
KEYS = [8, 8, 24, 24]
SUM_KEYS = 64
TAPS = [96, 195, 1310720, 589824]
TAPS_INVERTED = [[5, 6], [0, 1, 6, 7], [18, 20], [16, 19]]

s = Solver()

# Seed the LFSRs
seed = [BitVec(f'seed_{i}', 1) for i in range(SUM_KEYS)]
lfsrs = [
  seed[0:8][::-1],
  seed[8:16][::-1],
  seed[16:40][::-1],
  seed[40:64][::-1]
]

# Iterate through the cipher
def twister(x):
  a, b, c, d = x
  return (
    # a != b and c
    ((a ^ b) & c) | 
    # not b or c and d
    (((~b) | c) & d)
  )

for target_bit_idx, target_bit in enumerate(target):
  # Propagate each LFSR
  new_bits = []
  for lfsr_idx, (lfsr, taps) in enumerate(zip(lfsrs, TAPS_INVERTED)):
    new_bit = BitVec(f'lfsr_{lfsr_idx}_{target_bit_idx}', 1)

    # Propagate this bit
    new_bit_value = 0
    for tap in taps:
      # Do feedback
      new_bit_value = new_bit_value ^ lfsr[- tap - 1]
    s.add(new_bit == new_bit_value)

    # Push to back of lfsr
    lfsr.append(new_bit)

    # For twister
    new_bits.append(new_bit)
  
  # Assert target
  s.add(target_bit == twister(new_bits))

print(s.check())

model = s.model()

# Get back the seed
seed_bits = [
  None for i in range(SUM_KEYS)
]

for var in model.decls():
  if 'seed' in var.name():
    _, _, bit_idx = var.name().partition('_')
    seed_bits[int(bit_idx)] = model[var]

# There will be some None.
# Turns out it does not affect the cipher because its already out of range for the LFSR.
print(seed_bits)

recovered_seed = int(''.join([
  '1' if i == 1 else '0'
  for i in seed_bits[::-1]
]), 2)

print('recovered key', recovered_seed)

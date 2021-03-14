#!/usr/bin/env python3

from pwn import *

# context.log_level = 'debug'

LEN_GRIC = 10
LEN_CHECKSUM = 17
CHECKSUM_CHARS = list('ABCDEFGHJKLMRTXYZ')
  
# r = process(['python3', './challenge/server.py'])
# nc chals.ctf.sg 10101
r = remote('chals.ctf.sg', 10101)

# Initialize blank coefficient array and checksum mapping  
coefficients = [None for _ in range(LEN_GRIC)]
checksums = [None for _ in range(LEN_CHECKSUM)]

# Blank line to skip to first 'How may I help you?'
r.clean(timeout=0.1)
r.sendline(' ')

# Helper methods for pwntools
def to_menu():
  # Skip to the menu
  r.recvuntil('How may I help you?')

# run_query()               -> 0000000000
# run_query((0, 1))         -> 1000000000
# run_query((0, 2))         -> 2000000000
# run_query((1, 1))         -> 0100000000
# run_query((0, 1), (1, 2)) -> 1200000000
def run_query(*nonzero_digits):
  query_digits = ['0' for i in range(LEN_GRIC)]
  for index, digit in nonzero_digits:
    query_digits[index] = f'{digit}'
  query = ''.join(query_digits)
  print(query)

  to_menu()
  r.sendline('G')
  r.sendline(f'G{query}')
  r.recvuntil('Your GRIC is ')
  data = r.recvline().decode()
  return data[-2]

# Get the checksum for all zeros
checksums[0] = run_query()

# Find the first coefficient that is not 0
first_nonzero = None
for i in range(10):
  one_checksum = run_query((i, 1))
  if one_checksum != checksums[0]:
    # Without loss of generality, let this coefficient be 1
    # This works because the modulus 17 is prime
    coefficients[i] = 1
    checksums[1] = one_checksum
    first_nonzero = i
    break
  else:
    coefficients[i] = 0

# Find the checksums letters for sum of 2 to 9
for d in range(2, 10):
  two_to_nine_checksum = run_query((first_nonzero, d))
  checksums[d] = two_to_nine_checksum

# Iterate through the remaining digits
# We only have enough queries to find out the second last digit
deferred_digits = [] # [(index, checksum)]
for i in range(first_nonzero + 1, LEN_GRIC):
  other_checksum = run_query((i, 1))

  if other_checksum in checksums:
    # We have seen this checksum before, we can find the coefficient
    coefficients[i] = checksums.index(other_checksum)
    
    if None in checksums and coefficients[i] != 0:
      # We know the coefficients of two digits
      # Combine them (like with Diophantine equations) to find the checksum of 10 to 16
      second_nonzero = i

      first_coefficient = coefficients[0] # Its 1 anyways
      second_coefficient = coefficients[second_nonzero]

      for first_digit in range(1, 10):
        for second_digit in range(1, 10):
          candidate_checksum = (
            first_coefficient * first_digit + second_coefficient * second_digit
          ) % LEN_CHECKSUM

          if checksums[candidate_checksum] is None:
            # We don't know the letter for this checksum, run a query to find out
            checksums[candidate_checksum] = run_query((first_nonzero, first_digit), (second_nonzero, second_digit))

          if len(list(filter(lambda x: x is None, checksums))) == 1:
            # One last checksum left, we dentify by elimination
            last_checksum = list(set(CHECKSUM_CHARS) - set(filter(lambda x: x is not None, checksums)))[0]
            last_checksum_idx = checksums.index(None)
            checksums[last_checksum_idx] = last_checksum

      # By now we will know every checksum
      # If there are any previous 
  else:
    # We have not yet seen this checksum, and therefore cannot find its coefficient
    # The coefficient is probably in the 10-16 range
    # Store the value and process it later
    deferred_digits.append((i, other_checksum))

for deferred_index, deferred_checksum in deferred_digits:
  coefficients[deferred_index] = checksums.index(deferred_checksum)

# Pray hard that the last coefficient is 0
# We will be right 1/17 times anyways
# coefficients[-1] = 0

def calculate_checksum(gric):
  digit_values = [
    int(digit) * coefficient
    for digit, coefficient in zip(gric, coefficients)
  ]
  checksum_value = sum(digit_values)
  checksum_character = checksums[checksum_value % LEN_CHECKSUM]
  return checksum_character

# Try to answer the server
to_menu()
r.sendline('C')
for _ in range(100):
  print('.', end='')
  r.recvuntil('letter of G')
  challenge = list(r.recvline().decode('utf8')[:-2])
  checksum = calculate_checksum(challenge)
  r.sendline(checksum)
print()

r.interactive()

"""
Wow you did it. Congratulations! Here flag!
CTFSG{NRIC_m3meS_F0R_GRIC_7eENs}
"""

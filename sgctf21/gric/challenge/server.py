#!/usr/local/bin/python3

import sys
import random

LEN_GRIC = 10  # For whoever

constants = [0] * LEN_GRIC
sbox = list('ABCDEFGHJKLMRTXYZ')


def setup():
    global constants, sbox
    constants = [random.randint(0, 17) for x in range(LEN_GRIC)]
    random.shuffle(sbox)


def get_checksum(n):
    return sbox[sum(map(lambda x: int(x[0]) * int(x[1]), zip(n, constants))) % len(sbox)]


def oracle():
    sys.stdout.write("What GRIC do you want to get the last digit for?\n")
    sys.stdout.flush()  # Everyone is fun to flush
    b = input()

    if (b[0] != 'G' or len(b) != LEN_GRIC+1):
        sys.stdout.write("Not a valid GRIC\n")
        sys.stdout.flush()  # Everyone is fun to flush
        return

    for i in range(1, LEN_GRIC+1):
        try:
            int(b[i])
        except:
            sys.stdout.write(f"Not a valid GRIC.\n")
            sys.stdout.flush()  # Everyone is fun to flush
            return

    sys.stdout.write(f"Your GRIC is {b}{get_checksum(b[1:])}\n")
    sys.stdout.flush()  # Everyone is fun to flush


def challenge():
    sys.stdout.write("Welcome to the challenge. Answer all 100 outputs correctly and you will get the flag\n")
    sys.stdout.flush()  # Everyone is fun to flush

    for i in range(100):
        a = "".join([str(random.randint(0, 9)) for x in range(LEN_GRIC)])
        sys.stdout.write(f"What is the checksum letter of G{a}?\n")
        sys.stdout.flush()  # Everyone is fun to flush
        resp = input()[0]

        if resp != get_checksum(a):
            sys.stdout.write("Nope, that is the wrong answer. Goodbye!\n")
            sys.stdout.flush()  # Everyone is fun to flush
            exit(0)
        else:
            sys.stdout.write(f"Good job! Only {99 - i} more to go!\n")
            sys.stdout.flush()  # Everyone is fun to flush

    sys.stdout.write("Wow you did it. Congratulations! Here flag!\n")
    sys.stdout.write("<CENSORED>\n")
    sys.stdout.flush()  # Everyone is fun to flush
    exit(0)


def print_help():
    sys.stdout.write("Welcome to the (proof of concept) GRIC checker.\n")
    sys.stdout.write("How may I help you?\n")
    sys.stdout.write("(A)bout GRIC\n")
    sys.stdout.write("(C)hallenge this proof of concept\n")
    sys.stdout.write("(G)et checksum for a given GRIC number\n")
    sys.stdout.write("(H)elp\n")
    sys.stdout.write("(Q)uit\n\n")
    sys.stdout.flush()  # Everyone is fun to flush


def print_about():
    sys.stdout.write("Introducing GRIC: A revolutionary personal identification system designed for the global world.\n")
    sys.stdout.write("We recognise the importance of having a system where everyone can be identified by a unique designation.\n")
    sys.stdout.write("In many countries, individuals are not being tracked by the government because they are not registered.\n")
    sys.stdout.write("As such, we realise a national level identity number is perhaps not a best solution.\n")
    sys.stdout.write("That's why we created GRIC.\n")
    sys.stdout.write("There will not be any need for your passports anymore. You can now travel with your 10 digit GRIC!\n")
    sys.stdout.write("GRIC will take care of that, by being the all-in-one travel and licensing document.\n")
    sys.stdout.write("Support GRIC, and support making the world more globalized today.\n")
    sys.stdout.flush()  # Everyone is fun to flush


def main():
    setup()
    print_help()
    oracle_limit = 25

    while True:
        a = input()[0]

        if a == 'A':
            print_about()
        elif a == 'H':
            print_help()
        elif a == 'Q':
            sys.stdout.write("Goodbye!\n")
            sys.stdout.flush()  # Everyone is fun to flush
            exit(0)
        elif a == 'C':
            challenge()
        elif a == 'G':
            sys.stdout.write(f"You can ask the oracle {oracle_limit} more times\n")
            sys.stdout.flush()  # Everyone is fun to flush
            if oracle_limit == 0:
                sys.stdout.write("You are out of oracle tries. Goodbye\n")
                sys.stdout.flush()  # Everyone is fun to flush
                exit(0)
            oracle()
            oracle_limit -= 1

        sys.stdout.write("How may I help you?\n\n")
        sys.stdout.flush()  # Everyone is fun to flush


if __name__ == '__main__':
    main()

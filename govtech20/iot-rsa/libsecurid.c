/*
From https://seclists.org/bugtraq/2000/Dec/459

Sample SecurID Token Emulator with Token Secret Import
From: "I.C. Wiener" <icwiener () MAILRU COM>
Date: Thu, 21 Dec 2000 16:12:15 -0800
Sample SecurID Token Emulator with Token Secret Import

We have performed some cryptoanalysis and let's just say we do have
grounds to believe that this algorithm is easily breakable.
Once again, security of the cipher should be based entirely on the
secrecy of the key, not the algorithm.


Least Significant First byte order is assumed
/*

/* (c) 1999-3001 I.C. Wiener */

#ifdef _MSC_VER
    #pragma intrinsic           (_lrotr, _lrotl)
#else /* GCC or CC */
    #define __int64             long long
    #define __forceinline       __inline__
    #define _lrotr(x, n)        ((((unsigned long)(x)) >> ((int) ((n) & 31))) | (((unsigned long)(x)) << ((int) ((-(n)) & 31))))
    #define _lrotl(x, n)        ((((unsigned long)(x)) << ((int) ((n) & 31))) | (((unsigned long)(x)) >> ((int) ((-(n)) & 31))))
#endif

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>


#define ror32(x, n)             _lrotr (x, n)
#define rol32(x, n)             _lrotl (x, n)
#define bswap32(x)              (rol32 ((unsigned long)(x), 8) & 0x00ff00ff | ror32 ((unsigned long)(x), 8) & 0xff00ff00)

static __forceinline unsigned char      ror8 (const unsigned char x, const int n) { return (x >> (n & 7)) | (x << ((-n) & 7)); }
static __forceinline unsigned __int64   rol64 (const unsigned __int64 x, const int n) { return (x << (n & 63)) | (x >> ((-n) & 63)); }
static __forceinline unsigned __int64   bswap64 (const unsigned __int64 x) { unsigned long a = (unsigned long) x, b = (unsigned long) (x >> 32); return (((unsigned __int64) bswap32 (a)) << 32) | bswap32(b); }

typedef union _OCTET
{
    unsigned __int64            Q[1];
    unsigned long               D[2];
    unsigned short              W[4];
    unsigned char               B[8];
}   OCTET;

void securid_expand_key_to_4_bit_per_byte (const OCTET source, char *target)
{
    int     i;

    for (i = 0; i < 8; i++)
    {
        target[i*2  ] = source.B[i] >> 4;
        target[i*2+1] = source.B[i] & 0x0F;
    }
}

void securid_expand_data_to_1_bit_per_byte (const OCTET source, char *target)
{
    int     i, j, k;

    for (i = 0, k = 0; i < 8; i++) for (j = 7; j >= 0; j--) target[k++] = (source.B[i] >> j) & 1;
}

void securid_reassemble_64_bit_from_64_byte (const unsigned char *source, OCTET *target)
{
    int     i = 0, j, k = 0;

    for (target->Q[0] = 0; i < 8; i++) for (j = 7; j >= 0; j--) target->B[i] |= source[k++] << j;
}

void securid_permute_data (OCTET *data, const OCTET key)
{
    unsigned char       bit_data[128];
    unsigned char       hex_key[16];

    unsigned long       i, k, b, m, bit;
    unsigned char       j;
    unsigned char       *hkw, *permuted_bit;

    memset (bit_data, 0, sizeof (bit_data));

    securid_expand_data_to_1_bit_per_byte (*data, bit_data);
    securid_expand_key_to_4_bit_per_byte (key, hex_key);

    for (bit = 32, hkw = hex_key, m = 0; bit <= 32; hkw += 8, bit -= 32)
    {
        permuted_bit = bit_data + 64 + bit;
        for (k = 0, b = 28; k < 8; k++, b -= 4)
        {
            for (j = hkw[k]; j; j--)
            {
                bit_data[(bit + b + m + 4) & 0x3F] = bit_data[m];
                m = (m + 1) & 0x3F;
            }

            for (i = 0; i < 4; i++)
            {
                permuted_bit[b + i] |= bit_data[(bit + b + m + i) & 0x3F];
            }
        }
    }

    securid_reassemble_64_bit_from_64_byte (bit_data + 64, data);
}

void securid_do_4_rounds (OCTET *data, OCTET *key)
{
    unsigned char       round, i, j;
    unsigned char       t;

    for (round = 0; round < 4; round++)
    {
        for (i = 0; i < 8; i++)
        {
            for (j = 0; j < 8; j++)
            {
                if ((((key->B[i] >> (j ^ 7)) ^ (data->B[0] >> 7)) & 1) != 0)
                {
                    t = data->B[4];
                    data->B[4] = 100 - data->B[0];
                    data->B[0] = t;
                }
                else
                {
                    data->B[0] = (unsigned char) (ror8 ((unsigned char) (ror8 (data->B[0], 1) - 1), 1) - 1) ^ data->B[4];
                }
                data->Q[0] = bswap64 (rol64 (bswap64 (data->Q[0]), 1));
            }
        }
        key->Q[0] ^= data->Q[0];
    }
}

void securid_convert_to_decimal (OCTET *data, const OCTET key)
{
    unsigned long       i;
    unsigned char       c, hi, lo;

    c = (key.B[7] & 0x0F) % 5;

    for (i = 0; i < 8; i++)
    {
        hi = data->B[i] >>   4;
        lo = data->B[i] & 0x0F;
        c = (c + (key.B[i] >>   4)) % 5; if (hi > 9) data->B[i] = ((hi = (hi - (c + 1) * 2) % 10) << 4) | lo;
        c = (c + (key.B[i] & 0x0F)) % 5; if (lo > 9) data->B[i] = (lo = ((lo - (c + 1) * 2) % 10)) | (hi << 4);
    }
}

void securid_hash_data (OCTET *data, OCTET key, unsigned char convert_to_decimal)
{
    securid_permute_data (data, key); // data bits are permuted depending on the key
    securid_do_4_rounds (data, &key); // key changes as well
    securid_permute_data (data, key); // final permutation is based on the new key
    if (convert_to_decimal)
        securid_convert_to_decimal (data, key); // decimal conversion depends on the key too
}

void securid_hash_time (unsigned long time, OCTET *hash, OCTET key)
{
    hash->B[0] = (unsigned char) (time >> 16);
    hash->B[1] = (unsigned char) (time >> 8);
    hash->B[2] = (unsigned char) time;
    hash->B[3] = (unsigned char) time;
    hash->B[4] = (unsigned char) (time >> 16);
    hash->B[5] = (unsigned char) (time >> 8);
    hash->B[6] = (unsigned char) time;
    hash->B[7] = (unsigned char) time;

    securid_hash_data (hash, key, 1);
}

unsigned long long securid_hash(unsigned long long key, unsigned long msg)
{
    OCTET hash, key_oct;
    key_oct.Q[0] = key;
    securid_hash_time (msg, &hash, key_oct);
    return hash.Q[0];
}

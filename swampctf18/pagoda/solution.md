# Pagoda 1,2,3 - SwampCTF 2018 (499/500/500)

## Intro

Pagoda consists three crypto challenges, each with a task description, some hint in a journal form and finally the encoded message in the form of:

```
   ---------   ---------   ---   ---   ---   ---                   ---------   ---------
   ---   ---   ---   ---   ---   ---   ---   ---                   ---------   ---------
   ---   ---   ---   ---   ---------   ---------                   ---   ---            
   ---   ---   ---   ---   ---------   ---   ---                   ---------            
   ---   ---   ---   ---   ---   ---   ---------                   ---   ---   ---------
   ---   ---   ---   ---   ---   ---   ---------   ..(cont'd)...   ---   ---   ---------
```

Each 'chunk' has two vertical bars, 6 characters tall. Each row may or may not be joined in the middle, effectively encoding 6 bits of data. Even more curious is the ending 'chunk' which has no vertical bar but looks something similar to the `=` sign, which in b64 indicates to discard 2 bits of information. 

On examining all three encoded messages:

- text1 contains 87 data chunks and 1 `=`

( 87 * 6 bits - 2 extra bits) / 8 bits per byte = 65 bytes of data

- text2 contains 92 data chunks and no `=`

( 92 * 6 bits - 0 extra bits) / 8 bits per byte = 69 bytes of data

- text3 contains 63 data chunks and 1 `=`

( 63 * 6 bits - 2 extra bits) / 8 bits per byte = 47 bytes of data

Integer values of bytes are found, thus pointing towards an encoding pattern alike base64. Now the primary task is to identify the mapping of 'chunks' to values from 0 to 63.

## Trigrams and Hexagrams

Looking forward, Pagoda3.txt mentions 'the eight trigrams'. Some google-fu teaches us that [Trigrams](https://en.wikipedia.org/wiki/Bagua) consist three lines which are either solid or broken into two pieces, and are later stacked on top of each other. Their counterparts are [Hexagrams](https://en.wikipedia.org/wiki/Hexagram_(I_Ching)), which involves ordered pairings of the eight trigrams to form stacks of 6 lines, creating 64 unique symbols. Consulting their order, each hexagram was historically given a [value](https://en.wikipedia.org/wiki/List_of_hexagrams_of_the_I_Ching) from 1 to 64 under the ["King Wen" sequence](https://en.wikipedia.org/wiki/King_Wen_sequence), with the zero spot being taken by a yin-yang symbol.

_Jackpot._

## Parsing Hexagrams

Hexagrams are read from bottom to top and some more googling can reveal [multiple](http://www.cfcl.com/ching/) [lists](https://en.wikibooks.org/wiki/I_Ching/The_64_Hexagrams) which with some multiple-cursor magic in sublime can be formatted into a nice map to use to decode hexagrams. I encountered the former list first and used its method of reading broken lines from bottom to top to get the dictionary for decoding data:

```python
hexagram_dict = {	
		"------":1
		"      ":2,
		"-   - ":3,
		" -   -":4, 
		# ... ... 
		"- - - ":63,
		" - - -":64
	}
```

On closer examination the mapping of hexagrams to integers ranges from 1 to 64, but base64 encoding needs integers from 0 to 63. This is resolved by subtracting 1 from each hexagram value (especially since the yin-yang symbol didn't pop up here anyways and there now is no '0' character).

## Pagoda 1 (499)

> Thank Bog I've finally gotten to somplace that has a recognizable structure. After walking for days through this mire and muck, I'm happy to find a hummock. But what is this building, some kind of Asian pagoda? What waits inside for me?
>
> -=Created By: hachinijuku=-
> 
> [Pagoda1.txt](challenge/Pagoda1.txt) [text1.html](challenge/text1.html)

To decode text1:

1. Parse each hexagram from the text

```python
with open('./challenge/text1.txt') as f:
    data = f.readlines()

hexagram_dict = {
	# whatever should be here
}

for chunk_id in range((len(data[0])-1)/12):
	this_hexagram = ""
	for row in range(6):
		this_hexagram = data[row][chunk_id*12+6] + this_hexagram
	"""
	E.g. for first hexagram:
	
	---------
	---   ---
	---   ---
	---   ---
	---   ---
	---   ---
	this_hexagram = '     -'
	"""
	# To continue ...
```

2. Map it to its "I Ching" value subtracted by one

```python
for chunk_id in range((len(data[0])-1)/12):
	# Continued ...
	hexagram_value = hexagram_dict[this_hexagram]-1
	"""
	E.g. for first hexagram:
	hexagram_value = hexagram_dict['     -'] - 1
				   = 23 - 1
				   = 22
	"""
	# To continue ...
```

3. Convert the integers to a 6-bit binary string and concatenate

```python
bytestring = []

for chunk_id in range((len(data[0])-1)/12):
	# Continued ...
	bytestring.append('{:06b}'.format(hexagram_value))

bytestring = "".join(bytestring)
# 0101100101101111011101010010 ... ... 00111100
```

4. Decode it into ascii.

```python
def binToAscii(x):
	return "".join([chr(int(x[i:i+8],2)) for i in range(0,len(x),8)])

print binToAscii(bytestring)
# You have done well in Pagoda 1 flag{bmV4dDogU3RyYW5nZXIgVGhpbmdz}<
```

### [Full Solution](pagoda1_solve.py)

## Pagoda 2 (500)

> After having decoded the symbol sequence of the first Pagoda I feel like I'm ready for any new challenge that might be thrust upon me. 
>
> But wait, what's this I seen in Pagoda 2?
>
> -=Created By: hachinijuku=-
>
>[Pagoda2.txt](challenge/Pagoda2.txt) [text2.html](challenge/text2.html)

Decoding text2 with the same approach as in Pagoda 1 gives no feasible results. However, the challenge prompt mentions 'what's this I seen [..] ?'. Inspecting [Pagoda2.txt](challenge/Pagoda2.txt), the text mentions

> ... reflections on the surface of the water.

Use the same approach in Pagoda1, except reflect each hexagram vertically:

```python
for chunk_id in range((len(data[0])-1)/12):
	this_hexagram = ""
	for row in range(6):
		this_hexagram = this_hexagram + data[row][chunk_id*12+6] # Order swapped!
	# ... ...

# ... ...
print binToAscii(bytestring)
# The secrets of the second Pagoda are yours flag{QnJvdGhlciBvZiBOdXdh}
```

### [Full Solution](pagoda2_solve.py)

## Pagoda 3 (500)

> I approach the final pagoda with renewed confidence.
> 
> Not broken but, *Hint:* these problems must be solved in Sequence. Consult flag 2 to get it right.
> 
> -=Created By: hachinijuku=-
> 
> [Pagoda3.txt](challenge/Pagoda3.txt) [text3.html](challenge/text3.html)

Pagoda 1 and Pagoda 2 approaches don't work for this text file either.

On reading [Pagoda3.txt](challenge/Pagoda3.txt), it mentions:

> ... statue found in the middle of the floor. ...
>
> ... "He who devised the eight trigrams." ...

A quick google tells us that the trigrams are attributed to "Fu Xi". Further searching shows us that there is more than one way to map hexagrams to numbers [other than the "King Wen" sequence](https://en.wikipedia.org/wiki/King_Wen_sequence#Other_hexagram_sequences):

> Binary sequence, also known as [Fu Xi](https://en.wikipedia.org/wiki/Fuxi) sequence or Shao Yong sequence

Yes, its just binary.

After attempting various ways to map solid and broken lines to binary, assigning solid lines as `1` and broken lines as `0` gives valid ascii and the flag.

```python
for chunk_id in range((len(data[0])-1)/12):
	this_hexagram_binary = ""
	for row in range(6):
		if data[row][chunk_id*12+6] == '-':
			this_hexagram_binary = '1' + this_hexagram_binary
		else:
			this_hexagram_binary = '0' + this_hexagram_binary
	bytestring.append(this_hexagram_binary)
	# ... ...

# ... ...
print binToAscii(bytestring)
# K'an above, Li below flag{QWxyZWFkeSBGb3JkaW5n}3
```

### [Full Solution](pagoda3_solve.py)
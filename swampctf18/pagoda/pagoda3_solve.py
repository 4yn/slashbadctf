with open('./challenge/text3.txt') as f:
    data = f.readlines()

bytestring = []

for chunk_id in range((len(data[0])-1)/12):
	this_hexagram_binary = ""
	for row in range(6):
		if data[row][chunk_id*12+6] == '-':
			this_hexagram_binary = '1' + this_hexagram_binary
		else:
			this_hexagram_binary = '0' + this_hexagram_binary
	bytestring.append(this_hexagram_binary)

bytestring = "".join(bytestring)
print bytestring

def binToAscii(x):
	return "".join([chr(int(x[i:i+8],2)) for i in range(0,len(x),8)])

print binToAscii(bytestring)
# K'an above, Li below flag{QWxyZWFkeSBGb3JkaW5n}3
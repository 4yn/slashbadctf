with open('./challenge/text2.txt') as f:
    data = f.readlines()

hexagram_dict = {
	"------":1,		"      ":2,		"-   - ":3,		" -   -":4,		"--- - ":5,		" - ---":6,		" -    ":7,		"    - ":8,	
	"--- --":9,		"-- ---":10,	"---   ":11,	"   ---":12,	"- ----":13,	"---- -":14,	"  -   ":15,	"   -  ":16,	
	"-  -- ":17,	" --  -":18,	"--    ":19,	"    --":20,	"-  - -":21,	"- -  -":22,	"     -":23,	"-     ":24,	
	"-  ---":25,	"---  -":26,	"-    -":27,	" ---- ":28,	" -  - ":29,	"- -- -":30,	"  --- ":31,	" ---  ":32,	
	"  ----":33,	"----  ":34,	"   - -":35,	"- -   ":36,	"- - --":37,	"-- - -":38,	"  - - ":39,	" - -  ":40,	
	"--   -":41,	"-   --":42,	"----- ":43,	" -----":44,	"   -- ":45,	" --   ":46,	" - -- ":47,	" -- - ":48,	
	"- --- ":49,	" --- -":50,	"-  -  ":51,	"  -  -":52,	"  - --":53,	"-- -  ":54,	"- --  ":55,	"  -- -":56,	
	" -- --":57,	"-- -- ":58,	" -  --":59,	"--  - ":60,	"--  --":61,	"  --  ":62,	"- - - ":63,	" - - -":64}

bytestring = []

for chunk_id in range((len(data[0])-1)/12):
	this_hexagram = ""
	for row in range(6):
		this_hexagram = this_hexagram + data[row][chunk_id*12+6]
	hexagram_value = hexagram_dict[this_hexagram]-1
	bytestring.append('{:06b}'.format(hexagram_value))

bytestring = "".join(bytestring)
print bytestring

def binToAscii(x):
	return "".join([chr(int(x[i:i+8],2)) for i in range(0,len(x),8)])

print binToAscii(bytestring)
# The secrets of the second Pagoda are yours flag{QnJvdGhlciBvZiBOdXdh}
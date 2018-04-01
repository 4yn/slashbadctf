import pickle
import math
import json

d = pickle.load( open( "challenge/Orb_of_Light_p2_SaveCormyr/page_of_numbers.p", "rb" ) )

p = []

for i in d:

	vxy = i[2] * math.cos(i[3])
	vz = i[2] * math.sin(i[3])
	t = vz / 9.81 * 2

	dr = vxy * t
	dx = dr * math.cos(i[4] - math.pi)
	dy = dr * math.sin(i[4] - math.pi)

	x = int(i[0] + dx)
	y = int(i[1] + dy)

	# print "x: " + str(x) + "\ty: " + str(y)
	p.append([x,y])

f = open('orb2_coordinates.txt', 'w')

f.write(json.dumps(p))
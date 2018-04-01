import pickle
import math
import json

d = pickle.load( open( "challenge/Orb_of_Light_p2_SaveCormyr/examples.p", "rb" ) )

for i in d[:10]:
	dx = 0.0 + i[1][1] - i[0][0]
	dy = 0.0 + i[1][0] - i[0][1]
	dr = math.sqrt(dx*dx + dy*dy) 
	dt = math.atan2(dy,dx) + math.pi

	vxy = i[0][2] * math.cos(i[0][3])
	vz = i[0][2] * math.sin(i[0][3])
	t = vz / 9.81 * 2

	print "dx: " + str(dx) + "\tdy: " + str(dy) + "\tdr: " + str(dr) + "\t" + str(t * vxy) + "\tdt: " + str(dt) + " \t " + str(i[0][4])

print 

for pt in d[:10]:
	i = pt[0][:]

	vxy = i[2] * math.cos(i[3])
	vz = i[2] * math.sin(i[3])
	t = vz / 9.81 * 2

	dr = vxy * t
	dx = dr * math.cos(i[4] - math.pi)
	dy = dr * math.sin(i[4] - math.pi)

	x = i[0] + dx
	y = i[1] + dy

	print "x: " + str(x) + "\t" + str(pt[1][1]) + "\ty: " + str(y) + "\t" + str(pt[1][0])
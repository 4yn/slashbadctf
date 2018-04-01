from PIL import Image

images = []
for i in range(6400):
	ims.append(".challenge/Orb_of_Light_p3_disjunction/all_frags/fragment-" + str(i).zfill(5) + ".png")

flag = Image.new("RGB", (800, 800))

for index, file in enumerate(ims):
  img = Image.open(file)
  x = (index % 80) * 10
  y = (index / 80) * 10
  w, h = img.size
  flag.paste(img, (x, y, x + w, y + h))

flag.save('orb3_flag.png')

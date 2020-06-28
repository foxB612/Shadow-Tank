import sys
import getopt
from PIL import Image
import numpy as np

def resize(img1, img2):
	w1, h1 = img1.size
	w2, h2 = img2.size
	if w2 < w1 and h2 < h1:
		img1 = img1.resize([w2, h2])
	else:
		img2 = img2.resize([w1, h1])
	return img1, img2

def RGB2Gray(bmp):
	r,g,b = np.split(bmp, 3, axis=2)
	t = r * 0.299 + g * 0.587 + b * 0.114
	gray = np.array(t, dtype=np.uint8).squeeze(2)
	return gray

def RGBA2Gray(bmp):
	r,g,b,a = np.split(bmp, 4, axis=2)
	t = r * 0.299 + g * 0.587 + b * 0.114
	gray = np.array(t, dtype=np.uint8).squeeze(2)
	return gray

def process(g1, g2):
	for i in range(len(g1)):
		for j in range(len(g1[i])):
			while g1[i][j] < g2[i][j]:
				g1 = g1 * 0.9 + 255 * 0.1
				g2 = g2 * 0.9
	g1 = np.array(g1, dtype=np.uint8)
	g2 = np.array(g2, dtype=np.uint8)
	return g1, g2

def main(path1, path2, outputPath):
	try:
		img1 = Image.open(path1)
		img2 = Image.open(path2)
	except FileNotFoundError as e:
		print(e)
		return

	img1, img2 = resize(img1, img2)

	bmp1 = np.array(img1)
	bmp2 = np.array(img2)

	if bmp1.shape[-1] == 4:
		g1 = RGBA2Gray(bmp1)
		g2 = RGBA2Gray(bmp2)
	else:
		g1 = RGB2Gray(bmp1)
		g2 = RGB2Gray(bmp2)

	g1, g2 = process(g1, g2)

	alpha = 255 - (g1 - g2)
	color = np.divide(g2, alpha / 255, out=np.zeros(g2.shape), where=alpha!=0)
	color = np.array(color, dtype=np.uint8)
	o = np.stack([color, color, color, alpha], axis=2)
	out = Image.fromarray(o, mode="RGBA")
	out.save(outputPath)
	print("Image", outputPath, "generated.")



if not len(sys.argv) == 4:
	print("Use: ShadowTank.py <inputfile1> <inputfile2> <outputfile>")
	sys.exit(2)
try:
	main(sys.argv[1], sys.argv[2], sys.argv[3])
except Exception as e:
	print(e)
		




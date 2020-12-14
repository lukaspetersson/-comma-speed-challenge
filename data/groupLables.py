inFile = open("train.txt", "r")
outFile = open("train-grouped.txt", "w")

for x in inFile:
	num = float(x)
	outLable = 0
	if num > 25:
		outLable = 30
	elif num > 20:
		outLable = 25
	elif num > 15:
		outLable = 20
	elif num > 10:
		outLable = 15
	elif num > 5:
		outLable = 10
	elif num > 2:
		outLable = 5
	else:
		outLable = 0
	outFile.write(str(outLable) + "\n")
outFile.close()
print("done")

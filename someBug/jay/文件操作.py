import os
import re
import time

#dirPath ='D:\\workspace\\python\\someBug\\'
dirPath ='D:\\workspace\\python\\someBug\\jay\\mp3\\'
def changename_jay(dirPath):	
	names = os.listdir(dirPath)
	print(os.listdir(dirPath))
	a = re.compile(r'\D+')
	for n in names:
		#print(n) 17603505519
		if '.' in n:
			ns = n.split('.')
			print(ns[0],ns[1])
			if ns[1] == 'mp3':
				nc = a.findall(ns[0])
				print(nc)
				if len(nc) > 0 :
					os.rename(f'{dirPath}{ns[0]}.mp3',f'{dirPath}周杰伦-{nc[0]}.mp3')
				if len(nc) == 0:
					os.rename(f'{dirPath}{ns[0]}.mp3',f'{dirPath}周杰伦-{ns[0]}.mp3')

changename_jay(dirPath)






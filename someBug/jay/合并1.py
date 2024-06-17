import requests
import re
import json
import pprint
import os
import subprocess

path1= 'D:\\workspace\\python\\someBug\\jay'

filenames = os.listdir(path1)
#print(filenames)

def mp3addmp4(jay_name):
	print(f'开始合并{jay_name}音视频')
	cmd = f'ffmpeg -i {jay_name}.mp4 -i {jay_name}.mp3 -c:v copy -c:a aac -strict experimental {jay_name}_lich.mp4'
	subprocess.Popen(cmd,shell=True)
	print(f'{jay_name}_lich.mp4 处理完成')
'''
cmd = 'ffmpeg -y -i video.mp4 -i audio.mp3 -c:v copy -c:a aac -strict experimental mew_video.mp4'
subprocess.Popen(cmd,shell=True)

command = f'ffmpeg -i{video_name}.mp4 -i {video_name}.mp3 -c:v copy -c:a aac -strict experimental {video_name}.mp4'
subprocess.Popen(command,shell=True)

'''	
for f in filenames:
	if 'mp3' in f:
		f_f = f.split('.') 
		jay_name=f_f[0] 
		mp3addmp4(jay_name) 

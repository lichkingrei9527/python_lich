import requests
import re
import json
import pprint


"""
def get_response(html_url):
	'''发送请求'''
	headers = {
		'referer':'https://www.bilibili.com/',
		'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36 Edg/108.0.1462.42'
	}
	response = requests.get(url=html_url,headers=headers)

	return response



def get_videoinfo(html_url,i):
	response = get_response(html_url)
	#title = re.findall('<h1 title="(.*?)" class="video-title tit">',response.text)[0]
	title = ''
	try:
		title = re.findall('<div title="(.*?)" class="tag-link bgm-link">',response.text)[0]
	except:	
		print('titleNotFind')
#	finally:
#		print('go on')
	title = str(i) + title

	

	html_data = re.findall('<script>window.__playinfo__=(.*?)</script>',response.text)[0]
	jsonData = json.loads(html_data)
	audio_url = jsonData['data']['dash']['audio'][0]['baseUrl']
	video_url = jsonData['data']['dash']['video'][0]['baseUrl']

	videoinfo = [title,audio_url,video_url]
	print(videoinfo[0])
	return videoinfo

def saveJay(videoinfo):
	audio_content = get_response(videoinfo[1]).content
	video_content = get_response(videoinfo[2]).content
	with open(videoinfo[0] + '.mp3',mode='wb') as f:
		f.write(audio_content)
	with open(videoinfo[0] + '.mp4',mode='wb') as f:
		f.write(video_content)
	print(videoinfo[0]+'  视频内存保存完成')	

#videoinfo = get_videoinfo(url)
#saveJay(videoinfo)

i=35
#url = 'https://www.bilibili.com/video/BV1Dh41167W4/?p=' + str(i)

while i<198:
	url = 'https://www.bilibili.com/video/BV1Dh41167W4/?p=' + str(i)
	videoinfo = get_videoinfo(url,i)
	saveJay(videoinfo)
	print('第'+ str(i)+ '首完成')
	i = i + 1
	
"""


def get_response(html_url):
	'''发送请求'''
	headers = {
		'referer':'https://www.bilibili.com/',
		'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36 Edg/108.0.1462.42'
	}
	response = requests.get(url=html_url,headers=headers)

	return response



def get_videoinfo(html_url,i):
	response = get_response(html_url)
	#title = re.findall('<h1 title="(.*?)" class="video-title tit">',response.text)[0]
	title = ''
	try:
		#title = re.findall('<div title="(.*?)" class="tag-link bgm-link">',response.text)[0]
		title = re.findall('<title data-vue-meta="true">(.*?)</title>',response.text)[0]
	except:	
		print('titleNotFind')
#	finally:
#		print('go on')
	title = str(i) + title

	

	html_data = re.findall('<script>window.__playinfo__=(.*?)</script>',response.text)[0]
	jsonData = json.loads(html_data)
	audio_url = jsonData['data']['dash']['audio'][0]['baseUrl']
	video_url = jsonData['data']['dash']['video'][0]['baseUrl']

	videoinfo = [title,audio_url,video_url]
	print(videoinfo[0])
	return videoinfo

def saveJay(videoinfo):
	print('开始保存' + videoinfo[0])
	audio_content = get_response(videoinfo[1]).content
	video_content = get_response(videoinfo[2]).content
	with open(videoinfo[0] + '.mp3',mode='wb') as f:
		f.write(audio_content)
	with open(videoinfo[0] + '.mp4',mode='wb') as f:
		f.write(video_content)
	print(videoinfo[0]+'  视频内存保存完成')	

#videoinfo = get_videoinfo(url)
#saveJay(videoinfo)

i=1
#url = 'https://www.bilibili.com/video/BV1Dh41167W4/?p=' + str(i)

while i<8:
	#url = 'https://www.bilibili.com/video/BV1Dh41167W4/?p=' + str(i)
	#url = 'https://www.bilibili.com/video/BV1j7411w7GK?p=' + str(i)
	url = 'https://www.bilibili.com/video/BV1bE41127s6?p='  + str(i)
	url = 'https://www.bilibili.com/video/BV1TP4y1w7T9?p='  + str(i)
	videoinfo = get_videoinfo(url,i)
	saveJay(videoinfo)
	print('第'+ str(i)+ '首完成')
	i = i + 1

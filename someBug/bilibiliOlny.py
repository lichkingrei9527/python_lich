import requests
import re
import json
import pprint









def get_response(html_url):
	'''发送请求'''
	headers = {
		'referer':'https://www.bilibili.com/',
		'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36 Edg/108.0.1462.42'
	}
	response = requests.get(url=html_url,headers=headers)

	return response



def get_videoinfo(html_url):
	response = get_response(html_url)
	#title = re.findall('<h1 title="(.*?)" class="video-title tit">',response.text)[0]
	#title = 'test'
	#title = re.findall('<div title="(.*?)" class="tag-link bgm-link">',response.text)[0]
	title = re.findall('<title data-vue-meta="true">(.*?)</title>',response.text)[0]
	
	html_data = re.findall('<script>window.__playinfo__=(.*?)</script>',response.text)[0]
	print(title)

	jsonData = json.loads(html_data)
	print(jsonData)
	audio_url = jsonData['data']['dash']['audio'][0]['baseUrl']
	video_url = jsonData['data']['dash']['video'][0]['baseUrl']

	videoinfo = [title[0],audio_url,video_url]
	#print(videoinfo)
	return videoinfo

def saveJay(videoinfo):
	audio_content = get_response(videoinfo[1]).content
	video_content = get_response(videoinfo[2]).content
	print("开始保存视频")
	#with open(videoinfo[0] + '.mp3',mode='wb') as f:
	with open('lzy.mp3', mode='wb') as f:
		f.write(audio_content)
	#with open(videoinfo[0] + '.mp4',mode='wb') as f:
	#	f.write(video_content)
	print(videoinfo[0]+'  视频内存保存完成')	

#videoinfo = get_videoinfo(url)
#saveJay(videoinfo)

'''
i=194
#url = 'https://www.bilibili.com/video/BV1Dh41167W4/?p=' + str(i)

while i<198:
	url = 'https://www.bilibili.com/video/BV1Dh41167W4/?p=' + str(i)
	videoinfo = get_videoinfo(url)
	saveJay(videoinfo)
	i = i + 1
	print('第'+ str(i)+ '首完成')
'''
#url = 'https://www.bilibili.com/video/BV1j7411w7GK?p=3'
#url = 'https://www.bilibili.com/video/BV1Dh41167W4/?p=11'
url = 'https://www.bilibili.com/video/BV1qT42197uX/?spm_id_from=333.788'

videoinfo = get_videoinfo(url)
#saveJay(videoinfo)


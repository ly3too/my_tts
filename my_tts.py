#!/usr/bin/python3

import requests
import json
import sys
import io
import base64
import vlc # vlc player needed
import time

class BaiduRest:
	def __init__(self, cu_id, api_key, api_secert):
		# token认证的url
		self.token_url = "https://openapi.baidu.com/oauth/2.0/token"
		# 语音合成的resturl
		self.getvoice_url = "http://tsn.baidu.com/text2audio"
		# 语音识别的resturl
		self.upvoice_url = 'http://vop.baidu.com/server_api'
		self.cu_id = cu_id
		self.getToken(api_key, api_secert)
		return

	def getToken(self, api_key, api_secert):
		# 1.获取token
		data={'grant_type':'client_credentials','client_id':api_key,'client_secret':api_secert}
		r=requests.post(self.token_url,data=data)
		Token=json.loads(r.text)
		self.token_str = Token['access_token']


	def getVoice(self, text, filename, per, speed):
		# 2. 向Rest接口提交数据
		data={'tex':text,'lan':'zh','cuid':self.cu_id,'ctp':1,'tok':self.token_str, 'per':per, 'spd' : speed}
		r=requests.post(self.getvoice_url,data=data,stream=True)
		voice_fp = open(filename,'wb')
		voice_fp.write(r.raw.read())
		# for chunk in r.iter_content(chunk_size=1024):
			# voice_fp.write(chunk)
		voice_fp.close()


	def getText(self, filename):
		# 2. 向Rest接口提交数据
		data = {"format":"wav","rate":16000, "channel":1,"token":self.token_str,"cuid":self.cu_id,"lan":"zh"}
		# 语音的一些参数
		wav_fp = open(filename,'rb')
		voice_data = wav_fp.read()
		data['len'] = len(voice_data)
		data['speech'] = base64.b64encode(voice_data).decode('utf-8')
		post_data = json.dumps(data)
		r=requests.post(self.upvoice_url,data=bytes(post_data,encoding="utf-8"))
		# 3.处理返回数据
		return r.text
		
	def play(self, filename):
		# play it
		import vlc
		player = vlc.MediaPlayer(file_name)
		player.play();
		while player.get_state() != vlc.State.Ended:
			time.sleep(0.5);
		print("done playing")


if __name__ == "__main__":
	#api_key和api_secrett 等存放在 conf.json
	
	api_key = ""
	api_secret = ""
	file_name = ""
	per = ""
	speed = ""
	
	with open("./conf.json") as json_file:
		json_data = json.load(json_file)
		api_key = json_data["api_key"]
		api_secret = json_data["api_secret"]
		file_name = json_data["file_name"]
		per = json_data["per"]
		speed = json_data["speed"]
		

	if (len(sys.argv) < 2):
		print ("useage: \n"
				"    {} text1 text2 ...".format(sys.argv[0]))
		exit()
	
	# 初始化
	bdr = BaiduRest("test_tts", api_key, api_secret)
	
	for idx in range(1, len(sys.argv)):
		bdr.getVoice(sys.argv[idx], file_name, per, speed)
		bdr.play(file_name)

	
	
   

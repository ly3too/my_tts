# A simple Chinese Text to speech script using baidu TTS REST api
## 一个简单的中文语音合成脚本， 使用百度的 REST API
- similar to Mac's say 

## prerequest
- install vlc player

```shell
sudo apt-get install vlc
```

- install python3 and required librarys

```shell
python3 -m pip install -r requirements.txt
```

## configuration
- write a conf.json file in the same directory as file "say"

```shell
cp conf_sample.json conf.json
```

- replace the key and secret of yours, which can be obtained from baidu [here](http://ai.baidu.com/tech/speech/tts).

```
"api_key" : "your api key",
"api_secret" : "your api secret",
"file_name" : "out.mp3", temp file used to save data
"per" : 0, person from 0 to 5, to choose the voice type
"speed" : 4
```

## usage

```shell
./say text1 text2 ... 
```
you can link it to bin directory
```shell 
ln -s `pwd`/say ~/.local/bin/say

# now you can call say
say text1 text2 ...
```


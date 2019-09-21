import requests
import re
import json
import jsonpath

# 搜索
api = 'http://music.taihe.com/search'
data = {
    'key':'薛之谦'
}

# 获取歌手的页面内容
resp = requests.get(api,params=data)
html = resp.text
# print(html)

# 获取歌曲id
# 解析网页内容
song_ids = re.findall(r'data-playdata="(.+?)"',html)
# print(song_ids)
numbers = re.findall(r'\d+',song_ids[0])
# print(numbers)
for i in numbers:
    url = 'http://musicapi.taihe.com/v1/restserver/ting?method=baidu.ting.song.playAAC&format=jsonp&callback=jQuery17204900046242283971_1569043878329&songid=%s&from=web&_=1569043880839'% i
    # 请求：获取mp3文件地址
    response = requests.get(url)
    data = response.text
    # print(data)

    #第一种提取方式
    content = re.findall(r'\((.*)\)',data)[0]
    # print(content)
    content = json.loads(content)
    # print(content)
    #
    # # 获取歌曲信息
    # mp3_name = content['songinfo']['title']
    # print(mp3_name)
    # mp3_url = content['bitrate']['file_link']
    # print(mp3_url)

    # 第二种提取方式
    mp3_name = jsonpath.jsonpath(content,"$..title")[0]
    mp3_url = jsonpath.jsonpath(content,'$..file_link')[0]
    print(mp3_name)
    # 数据保存
    response_song = requests.get(mp3_url)
    with open(r'D:\start\新建文件夹\%s.mp3'%mp3_name,'wb') as f:
        f.write(response_song.content)

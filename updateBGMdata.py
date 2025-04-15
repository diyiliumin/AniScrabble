import requests
from bs4 import BeautifulSoup
import pandas as pd
import matplotlib.pyplot as plt
import urllib.request, urllib.error
from matplotlib.font_manager import FontProperties
import json
import time
import random

# 定义一个函数来获取和解析页面
def get_anime_info(url):
    response = askURL(url)
    #print(response)
    soup = BeautifulSoup(response, 'html.parser')
    tips = soup.select('#browserItemList a.l')
    data = []
    for tip in tips:
        text = tip.get_text().strip()
        if text:  # 确保文本不为空
            data.append(text)    
            addlist(text)
    return data

# 定义一个函数来收集所有页面的数据，并解析日期
def collect_data(base_url):
    all_data = []
    i = 1
    while i < 100:
        url = f"{base_url}&page={i}"
        print(f"Fetching data from {url}")
        data = get_anime_info(url)
        i += 1
        print(i)
        sleep_time = random.uniform(0, 1)
        time.sleep(sleep_time)
        if not data:  # 如果没有数据，停止循环
            print('No data found, stopping the loop.')
            break

    all_data.extend(data)
    return all_data

def addlist(text):
    # 遍历字符串的每个字符
    for char in text:
        if char == ' ':
            break;
        parts = text.split()
        cleantext = parts[0]  # 返回第一个元素    
        if char in anilist:
            if cleantext not in anilist[char]:
                anilist[char].append(cleantext)
        else:
            anilist[char] = [cleantext]  # 新建一个空列表作为默认值
            


def askURL(url):
    head = {  # 模拟浏览器头部信息，向豆瓣服务器发送消息
        "User-Agent": "Mozilla / 5.0(Windows NT 10.0; Win64; x64) AppleWebKit / 537.36(KHTML, like Gecko) Chrome / 80.0.3987.122  Safari / 537.36"
    }
    # 用户代理，表示告诉豆瓣服务器，我们是什么类型的机器、浏览器（本质上是告诉浏览器，我们可以接收什么水平的文件内容）

    request = urllib.request.Request(url, headers=head)
    html = ""
    try:
        response = urllib.request.urlopen(request)
        html = response.read().decode("utf-8")
    except urllib.error.URLError as e:
        if hasattr(e, "code"):
            print(e.code)
        if hasattr(e, "reason"):
            print(e.reason)
            
    return html

base_url = 'https://bgm.tv/anime/browser/?sort=collects'

anilist = {}

print (collect_data(base_url))
print (anilist)

keys_to_remove = [key for key, value in anilist.items() if len(value) == 1]
for key in keys_to_remove:
    del anilist[key]

# 将字典转换为 JSON 格式
anilist_json = json.dumps(anilist,ensure_ascii=False,indent=4)

# 写入到 anilist.js 文件
with open("anilist.js", "w",encoding='utf-8') as js_file:
    js_file.write("const anilist = " + anilist_json + ";")
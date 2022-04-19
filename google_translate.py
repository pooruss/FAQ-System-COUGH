# ！/usr/bin/python3
# -*- coding: utf-8 -*-
import requests
import re
import csv

def translated_content(text, target_language):
    headers = {
        "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
        # "accept-language": "en,zh-CN;q=0.9,zh;q=0.8",
        "content-type": "application/x-www-form-urlencoded;charset=UTF-8",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.66 Safari/537.36"
    }
    # 请求url
    url = "https://translate.google.cn/_/TranslateWebserverUi/data/batchexecute?rpcids=MkEWBc&f.sid=4441787135986856753&bl=boq_translate-webserver_20220119.07_p0&hl=zh-CN&soc-app=1&soc-platform=1&soc-device=1&_reqid=849580&rt=c"
    # 数据参数
    from_data = {
        "f.req": r"""[[["MkEWBc","[[\"{}\",\"auto\",\"{}\",true],[null]]",null,"generic"]]]""".format(text, target_language)
    }
    try:
        r = requests.post(url, headers=headers, data=from_data, timeout=60)
        if r.status_code == 200:
        # 正则匹配结果
            response = re.findall(r',\[\[\\"(.*?)\\"', r.text)[1]
        else:
            response = re.findall(r',\[\[\\"(.*?)\\"', r.text)[1]
        return response
    except Exception as e:
        print(e)
        return False

# 翻译各个国家语言
def translation_from_google(inputs):
    for input_text in inputs:
        for i in ['en', 'zh', 'fr', 'ja', 'nl', 'es']:
            response = translated_content(input_text, i)
            try:
                print(input_text + '\t' + response)
            except:
                print (response)


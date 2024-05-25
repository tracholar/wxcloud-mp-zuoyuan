# coding:utf-8
import requests as rq
import time

body = {
  "Content": "测试中文",
  "ToUserName": 'me',
  "FromUserName": "you",
  "CreateTime": int(time.time())
}


rsp = rq.post('http://127.0.0.1/api/wx', json=body)
print(rsp.text)
# coding:utf-8
import requests as rq
import time

body = {
  "Content": "为什么花儿这么红",
  "ToUserName": 'me',
  'MsgType': 'text',
  "FromUserName": "you",
  "CreateTime": int(time.time())
}


rsp = rq.post('http://127.0.0.1/api/wx', json=body)
print(rsp.text)
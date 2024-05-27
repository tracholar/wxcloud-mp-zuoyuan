# coding:utf-8
import requests as rq
import time

body = {
  "Content": "小兔子的笑话",
  "ToUserName": 'me',
  'MsgType': 'event',
  'Event': 'subscribe',
  "FromUserName": "you",
  "CreateTime": int(time.time())
}


rsp = rq.post('http://127.0.0.1/api/wx', json=body)
print(rsp.text)
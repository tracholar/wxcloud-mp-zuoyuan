# coding:utf-8
import requests as rq
import time

body = {
  "Content": "ilovetracholar",
  "ToUserName": 'me',
  "FromUserName": "you",
  "CreateTime": int(time.time())
}


rsp = rq.post('http://127.0.0.1/api/wx/msg', json=body)
print(rsp.text)
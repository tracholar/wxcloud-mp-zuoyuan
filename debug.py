# coding:utf-8
import requests as rq
import time

body = {
  "Content": "北京天气",
  "ToUserName": 'me',
  'MsgType': 'text',
  'Event': 'subscribe',
  "FromUserName": "you",
  "CreateTime": int(time.time())
}

import re
pat = u'^(.+)天气$'
print(re.match(pat, u'北京天气'))

rsp = rq.post('http://127.0.0.1/api/wx', json=body)
print(rsp.text)
# coding:utf-8
import requests as rq

body = '''
{
  "signature": "ilovetracholar",
  "timestamp": 1716626952,
  "nonce": "rwerwer",
  "echostr": "test"
}
'''

rsp = rq.post('http://127.0.0.1/api/wx/test', data=body, headers = {'content-type': 'text/json'})
print(rsp.content)
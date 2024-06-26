from datetime import datetime
from flask import render_template, request, jsonify
from run import app
from wxcloudrun.dao import delete_counterbyid, query_counterbyid, insert_counter, update_counterbyid
from wxcloudrun.model import Counters
from wxcloudrun.response import make_succ_empty_response, make_succ_response, make_err_response
from wxcloudrun.spark_ai_api import chat

import time
import xmltodict
import logging
import re

logger = logging.getLogger(__name__)


@app.route('/')
def index():
    """
    :return: 返回index页面
    """
    return render_template('index.html')


@app.route('/api/count', methods=['POST'])
def count():
    """
    :return:计数结果/清除结果
    """

    # 获取请求体参数
    params = request.get_json()

    # 检查action参数
    if 'action' not in params:
        return make_err_response('缺少action参数')

    # 按照不同的action的值，进行不同的操作
    action = params['action']

    # 执行自增操作
    if action == 'inc':
        counter = query_counterbyid(1)
        if counter is None:
            counter = Counters()
            counter.id = 1
            counter.count = 1
            counter.created_at = datetime.now()
            counter.updated_at = datetime.now()
            insert_counter(counter)
        else:
            counter.id = 1
            counter.count += 1
            counter.updated_at = datetime.now()
            update_counterbyid(counter)
        return make_succ_response(counter.count)

    # 执行清0操作
    elif action == 'clear':
        delete_counterbyid(1)
        return make_succ_empty_response()

    # action参数错误
    else:
        return make_err_response('action参数错误')


@app.route('/api/count', methods=['GET'])
def get_count():
    """
    :return: 计数的值
    """
    counter = Counters.query.filter(Counters.id == 1).first()
    return make_succ_response(0) if counter is None else make_succ_response(counter.count)


@app.route('/api/wx', methods=['GET'])
def wx_check():
    import hashlib
    from config import wx_token

    signature = request.args.get('signature')
    timestamp = request.args.get('timestamp')
    nonce = request.args.get('nonce')
    echostr = request.args.get('echostr')

    token = wx_token

    list = [token, timestamp, nonce]
    list.sort()
    sha1 = hashlib.sha1()
    map(sha1.update, list)
    hashcode = sha1.hexdigest()
    logger.info("handle/GET func: hashcode: %s, signature: %s", hashcode, signature)
    if hashcode == signature:
        return echostr
    else:
        return ""


@app.route('/api/wx', methods=['POST'])
def wx_handler():
    req = request.get_json()
    logger.debug("req: %s", req)

    if 'action' in req and req['action'] == 'CheckContainerPath':
        return ''
    else:
        return handler_msg(req)


def handler_weather(req):
    content = req['Content']
    logger.info('get weather for %s', content)

    return u'晴'


handler_map = {
    u'^(.+)天气$': handler_weather
}


def handler_msg(req):
    to_user = req['ToUserName']
    from_user = req['FromUserName']
    msg_type = req['MsgType'] if 'MsgType' in req else 'text'
    ret_content = ''

    if msg_type == 'text':
        content = req['Content']

        matched = False
        for pat, handler in handler_map.items():
            if re.match(pat, content):
                ret_content = handler(req)
                matched = True
                break

        if not matched:
            ret_content = chat("请在100字以内回复我。" + content)
    elif msg_type == 'event':
        event = req['Event']
        if event == 'subscribe':
            ret_content = u'欢迎订阅！已经接入大模型，可以输入任意文字进行对话！'
        else:
            ret_content = u'不支持的事件' + event
    else:
        ret_content = u"不支持消息类型" + msg_type
    msg = {
        'ToUserName': from_user,
        'FromUserName': to_user,
        'CreateTime': int(time.time()),
        'MsgType': 'text',
        'Content': ret_content
    }

    logger.debug("rsp: %s", msg)
    return jsonify(msg)

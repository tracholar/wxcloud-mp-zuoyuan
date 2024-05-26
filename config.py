import os
import logging

# 是否开启debug模式
DEBUG = bool(os.environ.get('DEBUG', 'true'))
logfmt = '[%(asctime)s] {%(pathname)s:%(lineno)d} %(levelname)s - %(message)s'
if DEBUG:
    logging.basicConfig(level=logging.DEBUG, format=logfmt)
else:
    logging.basicConfig(level=logging.INFO, format=logfmt)

logging.info('DEBU: %s', DEBUG)

# 读取数据库环境变量
username = os.environ.get("MYSQL_USERNAME", 'root')
password = os.environ.get("MYSQL_PASSWORD", 'root')
db_address = os.environ.get("MYSQL_ADDRESS", '127.0.0.1:3306')

wx_token = 'ilovetracholar'

import requests
import configparser
import subprocess
import platform
import time
import functools
import traceback
import sys
from functools import wraps
import logging
from logging.handlers import RotatingFileHandler
import base64

# 设置日志
log_file = r'C:\Users\Zenith\work\auto_campus_login\login_campus.log'
logging.basicConfig(
    handlers=[RotatingFileHandler(log_file, maxBytes=100000, backupCount=5)],
    level=logging.INFO,
    format='[%(asctime)s] %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

def print_error(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            logging.error(f"Error in {func.__name__}: {str(e)}")
            logging.error("Traceback:")
            logging.error(traceback.format_exc())
    return wrapper

def encode_password(password):
    """
    校园网登录界面前端使用 base64 对密码进行编码。
    是的, 他们就是这么干的, 用http传输明文密码。
    """
    password_bytes = password.encode('utf-8')
    encoded_bytes = base64.b64encode(password_bytes)
    encoded_password = encoded_bytes.decode('utf-8')
    
    return encoded_password

headers = {
    'Accept': 'application/json, text/javascript, */*; q=0.01',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'zh-CN,zh;q=0.9',
    'Connection': 'keep-alive',
    'Content-Type': 'application/x-www-form-urlencoded',
    'Host': '10.102.250.13',
    'Origin': 'http://10.102.250.13',
    'Referer': 'http://10.102.250.13/',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36'
}

@print_error
def check_login_status():
    url = 'http://10.102.250.13/index.php/index/init?_=1722522235609'
    response = requests.get(url, headers=headers)
    return response.json()['status'] == 1

@print_error
def login(username, password_crypt):
    url = 'http://10.102.250.13/index.php/index/login'
    data = {
        'username': username,
        'domain': 'fudan',
        'password': password_crypt,
        'enablemacauth': '0'
    }
    requests.post(url, headers=headers, data=data)

@print_error
def read_config(config_file='config.ini', *keys):
    config = configparser.ConfigParser()
    config.read(config_file)
    return tuple(config.get('Credentials', key) for key in keys)

@print_error
def is_connected_to_wifi(ssid):
    system = platform.system()
    if system == "Windows":
        try:
            # 使用 CREATE_NO_WINDOW 标志来防止显示控制台窗口
            output = subprocess.check_output(
                ["netsh", "wlan", "show", "interfaces"],
                creationflags=subprocess.CREATE_NO_WINDOW
            ).decode("utf-8", errors="ignore")
            return ssid in output
        except subprocess.CalledProcessError:
            return False
    elif system == "Darwin":  # macOS
        try:
            output = subprocess.check_output(
                ["/System/Library/PrivateFrameworks/Apple80211.framework/Versions/Current/Resources/airport", "-I"]
            ).decode("utf-8", errors="ignore")
            return f' SSID: {ssid}' in output
        except subprocess.CalledProcessError:
            return False
    else:
        raise OSError("Unsupported operating system")

def main():
    username, password = read_config('config.ini', 'username', 'password')
    password_crypt = encode_password(password)
    is_connect = False
    while True:
        new_is_connect = is_connected_to_wifi("iFudan.stu")
        if new_is_connect != is_connect:
            is_connect = new_is_connect
            logging.info(f'Connected to iFudan.stu: {is_connect}')
        if is_connect:
            is_login = check_login_status()
            if not is_login:
                logging.info('Try to login')
                login(username, password_crypt)
                logging.info('Login success')
        time.sleep(5)

if __name__ == '__main__':
    main()
#!/usr/bin/env python
# coding:utf-8

import json
import re
import os
import requests
from bs4 import BeautifulSoup

configs = []
headers = {'X-Requested-With': 'XMLHttpRequest',
           'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) '
           'Chrome/56.0.2924.87 Safari/537.36'}

def freessr():
    """ parse website：https://freessr.xyz """
    try:
        url = "http://freessr.xyz"
        response = requests.get(url, headers=headers).text
        bs = BeautifulSoup(response, 'lxml').find('div', class_="row").get_text().strip()
    except Exception as e:
        print(e)

    else:
        server = re.findall(r"(?<=服务器地址:)\S+", bs)
        server_port = re.findall(r"(?<=端口:)\d+", bs)
        password = re.findall(r"(?<=密码:)[a-zA-Z0-9.]+", bs)
        method = re.findall(r"(?<=加密方式:)\S+", bs)

        accounts = []
        for i, value in enumerate(server):
            account = {
                "server": value,
                "server_port": server_port[i],
                "password": password[i],
                "method": method[i],
                "remarks": "",
                "timeout": 5
            }
            accounts.append(account)
        configs.extend(accounts)


def main():
    """ 程序入口 """
    freessr()
    #parse_ishadow()
    # parse_kejiss()      # 这个网站挂了

    gui_config = {
        "configs": configs,
        "strategy":"com.shadowsocks.strategy.ha",
        "index": -1,
        "global": "false",
        "enabled": "true",
        "shareOverLan": "false",
        "isDefault": "false",
        "localPort": 1080,
        "pacUrl": "null",
        "useOnlinePac": "false",
        "secureLocalPac": "true",
        "availabilityStatistics": "false",
        "autoCheckUpdate": "false",
        "checkPreRelease": "false",
        "isVerboseLogging": "false",
        "logViewer": {
            "topMost": "false",
            "wrapText": "false",
            "toolbarShown": "false",
            "Font": "Consolas, 9.75pt",
            "BackgroundColor": "Black",
            "TextColor": "White"
        },
        "proxy": {
            "useProxy": "false",
            "proxyType": 0,
            "proxyServer": "",
            "proxyPort": 0,
            "proxyTimeout": 3
        },
        "hotkey": {
            "SwitchSystemProxy": "",
            "SwitchSystemProxyMode": "",
            "SwitchAllowLan": "",
            "ShowLogs": "",
            "ServerMoveUp": "",
            "ServerMoveDown": ""
        }}

    try:
        result = json.dumps(gui_config)
        path = r"/local/sdb/python/temp/gui-config.json"  # gui-config.json path
        with open(path, "w+") as f:
            f.write(result)
    except Exception as e:
        print(">>  Generate gui-config.json failed")
        print(">>  " + e)
    else:
        print(">>  Generate gui-config.json successful")


if __name__ == "__main__":
    configs = []
    main()
    #os.system("taskkill -f -t -im Shadowsocks.exe")
    #os.system("start e:\software\shadowsocks\Shadowsocks-4.0.4\Shadowsocks.exe")      
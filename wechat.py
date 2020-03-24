#coding:utf-8
import requests
import json
import time
from openpyxl import Workbook
from bs4 import BeautifulSoup

def Get_url():
    _offset = 0
    while (1):
        _offset += 10
        url = "https://mp.weixin.qq.com/mp/profile_ext?action=home&__biz=MzU3MDkxNzczNw==&scene=126&bizpsid=0#wechat_redirect" #对应的公众号全用
        headers = {
            "Cookie": "wxuin=2587046413; devicetype=android-22; version=26070333; lang=zh_CN; pass_ticket=YHveKi9JhV16VDItcgvnUcWSLb7yewFuJkmgvMNXi1lIqmgz6Ss4DKNFwG4MJbaL; wap_sid2=CI3kzNEJElxCUF9uYUxVRVhaVEdsS0VQaVhlcmZZQnAxVzdkbHJ6YUxLLXlTa2ZIODYyWlctT3Z5OGpYNVFKb3BqaFlSWWdtcVFON1lWeVViMHFSUWthcDM4RHJ5eDBFQUFBfjC0p+LzBTgNQJVO",
            "User-Agent": "Mozilla/5.0 (Linux; Android 5.1.1; OPPO R11 Build/NMF26X; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/74.0.3729.136 Mobile Safari/537.36 MicroMessenger/6.7.3.1360(0x26070333) NetType/WIFI Language/zh_CN Process/toolsmp"
        }
        params = {
            "action": "getmsg",
            "__biz": 'MzU3MDkxNzczNw==',  ####公众号唯一
            "f": "json",
            "offset": _offset,  ####页面偏移
            "count": "10",
            "is_ok": "1",
            "scene": "126",
            "uin": '777',
            "key": '777',
            "pass_ticket": 'YHveKi9JhV16VDItcgvnUcWSLb7yewFuJkmgvMNXi1lIqmgz6Ss4DKNFwG4MJbaL',  ####票据
            "wxtoken": "",
            "appmsg_token": '1053_nifDnAqVomOzN8QVsiWn5-udqs8NELEkHtjZrQ~~',  ####票据
            "x5": "0",
        }
        proxies = {
            "https": None,
            "http": None,
        }
        res = requests.get(url, headers=headers, params=params, proxies=proxies, timeout=3)
        data = json.loads(res.text)
        msg_list = eval(data.get("general_msg_list")).get("list", [])
        mess = []
        for i in msg_list:
            u_m = {}
            u_m['title'] = i["app_msg_ext_info"]["title"]
            u_m['datetime'] = i['comm_msg_info']['datetime']
            u_m['url'] = i["app_msg_ext_info"]["content_url"]
            mess.append(u_m)

        if 1 == data.get("can_msg_continue"):
            time.sleep(5)
            continue
        else:
            print("爬取完毕")
            return(mess)


def Get_message(m_list):
    for m in m_list:
        hds = {
            'heads': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36'}
        text = requests.get(m['url'],
                            headers=hds).text  # .text#replace('\n', '').replace('\r', '').replace(' ', '')
        soup = BeautifulSoup(text, 'html.parser')
        data = soup.find(('section', {'data-role': 'paragraph'})).text
        m['message'] = data
        time.sleep(2)
    return m_list

def store(m_list):
    wb = Workbook()
    ws = wb.create_sheet(title = '远川科技评论')
    ws.append(['标题', '发布时间', '地址', '正文'])
    for m in m_list:
        ws.append([m[0],m[1],m[2],m[3]])
    save_path = '远川评论.xlsx'
    wb.save(save_path)



if __name__ == '__main__':
    '''
    应用VX（PC版），用fiddler/burp(proxifier)全都无法获得 VX（PC版）的HTTP请求页面，有哪位大佬知道正确设置方法，望告知
    '''

    url = Get_url()
    message = Get_message(url)
    store(message)
import re
import requests
import json
import time
import os
from datetime import datetime, timedelta, timezone
from requests.models import ContentDecodingError

def push(content,checktype):
    url = 'https://wxpusher.zjiecode.com/api/send/message'
    data = {"appToken":'AT_uSvGG61heMNaTPvsxoWZ4zzh7vyzPv0a',
        "content":content,
        "summary":checktype,
        "contentType":1,
        "uids":['UID_Sdl7m3U2euWtYjVxFr92nHsT7nlr'], 
        "verifyPay":'false'}
    resp = requests.post(url = url,json=data)

    return resp.text

def getTimes():
    TZ = timezone(timedelta(hours=8), name='Asia/Shanghai')
    times_now = datetime.utcnow().replace(tzinfo=timezone.utc).astimezone(TZ).strftime('%Y-%m-%d %H:%M:%S')
    return times_now


def amsz():
    try:

        url = f'https://webapi.qmai.cn/web/catering/integral/sign/signIn'
        headers = {'Host': 'webapi.qmai.cn' ,
        'Connection': 'keep-alive' ,
        'content-type': 'application/json' ,
        'Qm-From': 'wechat',
        'Qm-User-Token': 'CXs5cdLX3czWzr_gAcyUkvBoUacIPWjddSBcoyuo31ZjQ0UMKwtfjZ4Kffde2vH4ml5fkSUyP2INWwq3WUt9xQ' ,
        'Qm-From-Type': 'catering' ,
        'Accept': 'v=1.0' ,
        'Accept-Encoding': 'gzip' ,
        'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 17_4 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 MicroMessenger/8.0.46(0x18002e2c) NetType/WIFI Language/zh_CN', 
        'Referer': 'https://servicewechat.com/wx0ea382a771798601/193/page-frame.html'}

        data = {
        "mobilePhone" : "13612533440",
        "activityId" : "827230712196247553",
        "appid" : "wx0ea382a771798601",
        "userName" : "微信用户"
        }

        res = requests.post(url=url,headers=headers,json=data).text
        resjson = json.loads(res)
        message,status = resjson['message'],resjson['status']
        if '今天已签到' in message or status:
            print(f'阿嫲手作签到成功')

            print(res)

            infourl =f'https://webapi.qmai.cn/web/catering/crm/points-info'

            headers = {'Host': 'webapi.qmai.cn' ,
                    'Connection': 'keep-alive' ,
                    'content-type': 'application/json' ,
                    'Qm-From': 'wechat' ,
                    'Qm-User-Token':'CXs5cdLX3czWzr_gAcyUkvBoUacIPWjddSBcoyuo31ZjQ0UMKwtfjZ4Kffde2vH4ml5fkSUyP2INWwq3WUt9xQ',
                    'Qm-From-Type': 'catering'  ,
                    'Accept-Encoding': 'gzip' ,
                    'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 17_4 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 MicroMessenger/8.0.46(0x18002e2c) NetType/WIFI Language/zh_CN' ,
                    'Referer': 'https://servicewechat.com/wx0ea382a771798601/193/page-frame.html'}
            data ={"appid" : "wx0ea382a771798601"}
            res = requests.post(url=infourl,headers=headers,json=data).text
            resjson = json.loads(res)
            totalPoints = resjson['data']['totalPoints']
            print(res)
            push(f'{getTimes()}\n\nstatus:{message}\n\ntotalPoints:{totalPoints}','阿嫲手作签到')
    except Exception as e:
        push(f'{e}','阿嫲手作签到出错')


def dp():
    url = f'https://a.zhimatech.com/restful/mall/3536/checkInRecord'

    headers ={'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 17_4 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 MicroMessenger/8.0.49(0x18003134) NetType/WIFI Language/zh_CN',
    'Authorization': f'Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzdWIiOiIzMjAyNjcxIiwiZ3VhcmQiOiJtZW1iZXIiLCJtYWxsX2lkIjoiMzUzNiIsImlzcyI6Imh0dHBzOi8vYS56aGltYXRlY2guY29tL3Jlc3RmdWwvbWVtYmVyL3gvdG9rZW4iLCJleHAiOjQwOTI1OTkzNDksImlhdCI6MTcxNzUxOTU3NywiYXBwX2lkIjoid3hiNzMwOWQxNzU3YzY1OGExIn0._YOb9z7W-D-4LG4H0cmBkjo-QSTw8GCEiZUn967oPUs'}
    # body = {'longitude':'0','latitude':'0'}
    res =requests.post(url=url,headers=headers,json={}).text
    jss = json.loads(res)
    msg = jss['msg']
    push(f'{getTimes()}\n\n{msg}','东平保利')


if __name__ =='__main__':
    try:
        amsz()
        dp()
    except Exception as e:
        print(e)


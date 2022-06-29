# -*- coding: utf-8 -*-

# This code shows an example of text translation from English to Simplified-Chinese.
# This code runs on Python 2.7.x and Python 3.x.
# You may install `requests` to run this code: pip install requests
# Please refer to `https://api.fanyi.baidu.com/doc/21` for complete api document

import requests
import random
import json
from hashlib import md5

# Generate salt and sign
def make_md5(s, encoding='utf-8'):
    return md5(s.encode(encoding)).hexdigest()

def baiduTranslate(f,t,q):
    # Set your own appid/appkey.
    appid = '20220628001259188'
    appkey = 'c8FbTwsW9QoG_7fzS8o5'

    # For list of language codes, please refer to `https://api.fanyi.baidu.com/doc/21`
    from_lang = f
    to_lang =  t

    endpoint = 'http://api.fanyi.baidu.com'
    path = '/api/trans/vip/translate'
    url = endpoint + path

    query = q


    salt = random.randint(32768, 65536)
    sign = make_md5(appid + query + str(salt) + appkey)

    # Build request
    headers = {'Content-Type': 'application/x-www-form-urlencoded'}
    payload = {'appid': appid, 'q': query, 'from': from_lang, 'to': to_lang, 'salt': salt, 'sign': sign}

    # Send request
    r = requests.post(url, params=payload, headers=headers)
    result = r.json()

    # Show response
    temp=result['trans_result'][0]['dst']
    return temp

if __name__ == '__main__':
    print(baiduTranslate('zh','en','为深入贯彻习总书记“疫情要防住、经济要稳住、发展要安全”的重要指示精神，全面落实全国稳住经济大盘电视电话会议部署要求，高效统筹疫情防控和经济社会发展，以更强的紧迫感、更高的主动性抢抓当前关键时间窗口，进一步推进知识产权政策实施提速增效，促进经济平稳健康发展'))

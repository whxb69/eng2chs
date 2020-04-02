# -*- coding:utf-8 -*-
import cgitb
import urllib.request
import urllib.error
import execjs
import re
import time
from eng2chs import readip
from eng2chs import getip
import requests
import socket
from fake_useragent import UserAgent
import traceback
from retrying import retry

cgitb.enable()

'''
主要功能类为tfunction。
使用时在顶端添加 from m_trans import tfunction
建立tfunction实例,使用trans函数,输入参数为需要翻译的内容。
返回结果即为翻译结果。

    exp:    


'''

try:
    ua = UserAgent()
except:
    ua = UserAgent()


class Py4Js:
    def __init__(self):
        self.ctx = execjs.compile("""
        function TL(a) {
        var k = "";                                                                                                                                                                         
        var b = 406644;
        var b1 = 3293161072;

        var jd = ".";
        var $b = "+-a^+6";
        var Zb = "+-3^+b+-f";

        for (var e = [], f = 0, g = 0; g < a.length; g++) {
            var m = a.charCodeAt(g);
            128 > m ? e[f++] = m : (2048 > m ? e[f++] = m >> 6 | 192 : (55296 == (m & 64512) && g + 1 < a.length && 56320 == (a.charCodeAt(g + 1) & 64512) ? (m = 65536 + ((m & 1023) << 10) + (a.charCodeAt(++g) & 1023),
            e[f++] = m >> 18 | 240,
            e[f++] = m >> 12 & 63 | 128) : e[f++] = m >> 12 | 224,
            e[f++] = m >> 6 & 63 | 128),
            e[f++] = m & 63 | 128)
        }
        a = b;
        for (f = 0; f < e.length; f++) a += e[f],
        a = RL(a, $b);
        a = RL(a, Zb);
        a ^= b1 || 0;
        0 > a && (a = (a & 2147483647) + 2147483648);
        a %= 1E6;
        return a.toString() + jd + (a ^ b)
    };

    function RL(a, b) {
        var t = "a";
        var Yb = "+";
        for (var c = 0; c < b.length - 2; c += 3) {
            var d = b.charAt(c + 2),
            d = d >= t ? d.charCodeAt(0) - 87 : Number(d),
            d = b.charAt(c + 1) == Yb ? a >>> d: a << d;
            a = b.charAt(c) == Yb ? a + d & 4294967295 : a ^ d
        }
        return a
    }
    """)

    def getTk(self, text):
        return self.ctx.call("TL", text)


class tfunction():
    def __init__(self):
        self.js = Py4Js()

    def trans(self, temp, pro=1, mode='e2c'):
        if not isinstance(temp, str):
            return 'content should be str'

        js = self.js

        num = int(len(temp) / 4500) + 1
        results = [temp[i*4500:(i+1)*4500] for i in range(num)]
        reslist = [''] * len(results)
        alllist = []
        pat_w = re.compile('\w')
        for i in range(len(results)):
            flag = pat_w.match(results[i][-1])
            if flag:
                pat_ws = re.compile("[^\w\s']")
                bpoint = pat_ws.search(results[i+1]).regs[0][1]
                results[i] = results[i] + ' ' + results[i+1][:bpoint]
                results[i+1] = results[i+1][bpoint:]


        for index,result in enumerate(results):
            tk = js.getTk(result)
            content = urllib.parse.quote(result)
            socket.setdefaulttimeout(20)

            if mode == 'e2c':
                url = "https://translate.google.cn/translate_a/single?client=t" \
                      "&sl=en&tl=zh-CN&hl=zh-CN&dt=at&dt=bd&dt=ex&dt=ld&dt=md&dt=qca" \
                      "&dt=rw&dt=rm&dt=ss&dt=t&ie=UTF-8&oe=UTF-8&clearbtn=1&otf=1&pc=1" \
                      "&srcrom=0&ssel=0&tsel=0&kc=2&tk=%s&q=%s" % (tk, content)

            elif mode == 'c2e':
                url = "https://translate.google.cn/translate_a/single?client=t" \
                      "&sl=zh-CN&tl=en&hl=zh-CN&dt=at&dt=bd&dt=ex&dt=ld&dt=md&dt=qca" \
                      "&dt=rw&dt=rm&dt=ss&dt=t&ie=UTF-8&oe=UTF-8&clearbtn=1&otf=1&ssel=0" \
                      "&tsel=3&kc=2&tk=%s&q=%s" % (tk, content)
            headers = {'User-Agent': ua.random}
            try:
                if pro == 1:
                    response = self.req(url)
                else:
                    response = requests.get(url=url, headers=headers, allow_redirects=False)

                if response.status_code == 200:
                    results[index] = response.text
                    # k = k + 1
                    response.close()
                if response.status_code == 302:
                    print('reaponse 302 2秒后继续')
                    getip.get_ip()
                    time.sleep(2)
                    return self.trans(temp, pro, mode)
            except:
                print(traceback.print_exc())
                return self.trans(temp, pro, mode)

            res = self.setres(results[index].replace('null',"'null'"))
            tres_l = res[0]
            reslist[index] = ''
            for t in tres_l:
                if t[0] != 'null':
                    reslist[index] += t[0]
                    alllist.append(t[0])


        return ('').join(reslist),alllist

    @retry(stop_max_attempt_number=3)
    def getproxy(self):
        return readip.readip()

    @retry(stop_max_attempt_number=5)
    def req(self, url):
        proxies = self.getproxy()
        headers = {'User-Agent': ua.random}
        response = requests.get(url=url, headers=headers, allow_redirects=False, timeout=2)
        return response

    def setres(self,inputs):
        try:
            return eval(inputs)
        except NameError as e:
            key = re.compile("'\w+'").search(e.args[0]).group().strip("\\'")
            inputs_n = inputs.replace(key,"'%s'"%key)
            return self.setres(inputs_n)


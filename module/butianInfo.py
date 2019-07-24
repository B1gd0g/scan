# -- coding: utf-8 --
from module import printc
from module import tool
import re,time,random
try:
    import requests
except:
    msg1="[-] 您还没有安装requests依赖包,请使用 pip install requests安装"
    printc.printf(msg1,'red')
try:
    import json
except:
    msg1="[-] 您还没有安装json依赖包,请使用 pip install json安装"
    printc.printf(msg1,'red')

def get_src_name(url,page):
    index  = page.split("-")
    index1 = int(index[0]) #抓取开始页
    index2 = int(index[1]) #抓取结束页
    #获取company_name和company_id时的请求头
    headers={
            "Accept":"application/json, text/javascript, */*; q=0.01",
            'Accept-Encoding': 'gzip,deflate',
            "Accept-Language":"zh-CN,zh;q=0.9",
            "Connection":"keep-alive",
            "Content-Length":"14",
            "Content-Type":"application/x-www-form-urlencoded; charset=UTF-8",
            "Cookie":"__guid=66782632.3287965366713424400.1557370637004.574; btlc_ba52447ea424004a7da412b344e5e41a=6a5e25bf5c72acfece861fc7be289c9993d9b5da0cb4589e46af2333e47e91c0; PHPSESSID=8okmbhj4elrs2kc3o4c15n9hc3; __DC_monitor_count=31; __DC_sid=66782632.2355515763036458500.1563936908835.0845; __q__=1563936909201; __DC_gid=66782632.539342110.1557370637005.1563936912059.173",
            "Host":"www.butian.net",
            "Origin":"https://www.butian.net",
            "Referer":"https://www.butian.net/Reward/plan",
            "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.81 Safari/537.36",
            "X-Requested-With":"XMLHttpRequest"}
    #请求https://www.butian.net/Loo/submit?cid=62111时的请求头
    headers_company_url ={
            "Accept"          : "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3",
            "Accept-Encoding" : "gzip, deflate, br",
            "Accept-Language" : "zh-CN,zh;q=0.9",
            "Cache-Control"   : "max-age=0",
            "Connection"      : "keep-alive",
            "Cookie"          : "__guid=66782632.3287965366713424400.1557370637004.574; btlc_ba52447ea424004a7da412b344e5e41a=6a5e25bf5c72acfece861fc7be289c9993d9b5da0cb4589e46af2333e47e91c0; PHPSESSID=8okmbhj4elrs2kc3o4c15n9hc3; __DC_monitor_count=31; __DC_sid=66782632.2355515763036458500.1563936908835.0845; __q__=1563936909201; __DC_gid=66782632.539342110.1557370637005.1563936912059.173",
            "Host"            : "www.butian.net",
            "Upgrade-Insecure-Requests": "1",
            "User-Agent"      : "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.142 Safari/537.36"
}
    try:
        # for p in range(1,int(page)+1):
        for p in range(index1,index2+1):
            sleep_time1 =  random.uniform(1.1,3.4) # 停止请求几秒钟,防止被禁止ip
            data    = {"s":1,"p":p}
            res     = requests.post(url=url,data=data,headers=headers)#请求获取cid和名字
            content = res.content
            # print(type(content))
            # print(content)
            content=json.loads(content)
            msg1="++++++++++++++++++++++++++++++++++第{p}页++++++++++++++++++++++++++++++++++++++++++".format(p=p)
            title1  = "Website"
            t1_len  = 15
            title2  = "ID"
            t2_len  = 2
            title3  = "Name"
            t3_len  = 15
            printc.printf(msg1,'yellow')
            tool.setSheetTitle(t1_len,title1,t2_len,title2,t3_len,title3) # 打印标题
            for i in content['data']["list"]:
                company_id     = i["company_id"]
                company_name   = i["company_name"]
                try:
                    url2 = "https://www.butian.net/Loo/submit?cid={company_id}".format(company_id=company_id)
                    res2 = requests.get(url=url2,headers=headers_company_url)
                    p    = "value=\"((http://|https://|www.|[a-z]+)[.\w-]+\.[a-z]+)\""
                    company_url = re.findall(p,str(res2.text),re.S)[0][0]
                    sleep_time2 =  random.uniform(1.1,3.2) # 停止请求几秒钟,防止被禁止ip
                    time.sleep(sleep_time2)
                except :
                    msg = "[-] {url2} 请求失败!请检查原因".format(url2=url2)
                    printc.printf(msg,'red')
                    pass
                #line0   = tool.setStr2SameLen(8,""," ") + str("企业名字") + tool.setStr2SameLen(8,""," ") + str("|") + tool.setStr2SameLen(8,""," ") + str("企业网站") + tool.setStr2SameLen(8,""," ")
                t1      = company_url
                t2      = company_id
                t3      = company_name
                tool.print2sheet(t1_len,t1,title1,t2_len,t2,title2,t3_len,t3,title3)
            #title1  = tool.setStr2SameLen(8,"","-")
            # msg     =  "名字:"+str(i["company_name"])+"   公司ID:"+str(i["company_id"]+"   公司网址:"+str(company_url))
            # printc.printf(msg,'green')
                time.sleep(sleep_time1)
    except:
        msg3 = "-------------------------------------好像出了一点问题----------------------------------"
        msg4 = "[+] 提示1:请您检查一下URL是否正确!现在仅支持公益SRC提取哦!直接在地址栏中复制的URL有可能不是真正的请求URL哦!您可以F12查看请求URL"
        msg5 = "[+] 提示2:请您登陆补天,F12,并且复制其中的请求头中的cookie,并且改变../scan/module/butianInfo.py文件中header中的cookie选项"
        printc.printf(msg3,'red')
        printc.printf(msg4, 'green')
        printc.printf(msg5, 'green')


        pass
# if __name__=='__main__':
#     url = "https://butian.360.cn/Reward/pub"
#     page = 10
#     get_src_name(url,page)

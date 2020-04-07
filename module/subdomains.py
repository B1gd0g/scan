# -*- coding: utf-8 -*-
import socket,os,threading,queue,time,re,platform
from module import printc,output
from module import tool as tools
#import printc
#from module import printc
try:
    import requests
except:
    msg1="\n[-] 检测到您还没有安装Python3的requests依赖包,请使用 pip install requests 安装\n"
    printc.printf(msg1,'red')
#线程锁        
lock = threading.Lock()
count  = 0  #计数
#获取操作系统信息
systeminfo = platform.platform()
#读取文件每一行并将文件内容存放在列表中
def content2List(add):
    # cwd=os.getcwd()
    dirList=[]
    # Windows 操作系统中 add=cwd+"\\dict\\directory.txt"
    # Linux 操作系统中 add=cwd+"/dict/directory.txt
    f=open(add,"rb")
    for line in f.readlines():
        dirList.append(str(line)[2:-5])
    #print("Length is:"+str(len(dirList)))
    return dirList

#判断是否访问的页面是否存在
def ifExist(res):
    symbol=["404","NOT FOUND","对不起","页面不存在","502BadGateway","403 Forbidden"]
    p="<title>([\W\w]*?)</title>"
    for i in symbol:
        if i in re.findall(p,res)[0]:
            return False
            break
        else:
            return True
#bytes 转化为str
def bytes2str(input):
    if type(input)=="bytes":
        input=bytes.decode(input)
    return input
#删除文件中无用且重复的信息            
def delUseless(add):
    try:
        s=[]
        f=open(add,"r+")
        for i in f.readlines():
            i=i.replace("\n","") 
            s.append(i)
        f.close()
        s=list(set(s))
        with open(add,"w+") as f:
            for i in s:
                f.write(i+"\n")
            f.close()
    except:
        msg1="[-] 是不是路径输错了呢?"
        printc.printf(msg1,"red")
#将爬取的res转化为标准res.text的格式
def change2standard(res):
    try:
        if res.encoding=="ISO-8859-1":
            # res.encoding="utf-8
            result=res.text.encode(res.encoding).decode('GBK')
            #result=res.text.decode(res.encoding).encode("utf8")
        else:
            result=res.text
        return bytes2str(result)
    except:
        if res.encoding=="ISO-8859-1":
            # res.encoding="utf-8
            #result=res.text.decode(res.encoding).encode("gbk")
            result=res.text.encode(res.encoding).decode('utf8')
        else:
            result=res.text
        return bytes2str(result)
#根据标题判断网站是否是可访问的
def isVisible(title):
    flag=["114网址导航","403Forbidden","NotFound","页面不存在","出错","502BadGateway","访问被拒绝","BadRequest"]
    remark=True
    count=0
    for i in flag:
        if str(i) in title:
            remark =False
            break
        # else:
        #     count=count+1
    # if count==len(flag):
    #     remark=True
    return remark

#获取子域名类
class getSubdomainNames(threading.Thread):
    def __init__(self,subdomains,domain1,protocol):
        threading.Thread.__init__(self)
        self.subdomains=subdomains
        self.domain1=domain1
        self.protocol=str(protocol)
        self.p="<title>([\W\w]*?)</title>"
        self.p1="<TITLE>([\W\w]*?)</TITLE>"
    def run(self):
        global lock,count
        domain1=self.domain1
        while not self.subdomains.empty():
            subdomain=self.subdomains.get()
            #domain=httpOrHttps(domain)+"://" +subdomain+"."+domain
            domain=httpOrHttps(self.protocol)+str("://") +str(subdomain)+"."+str(domain1)
            # print(domain)
            #lock.acquire()
            try: 
                res=requests.get(domain,timeout=4)
                result=change2standard(res)
                # print(result)
                # if ifExist(res)==True:
                if (re.findall(self.p,result)):
                    title=(re.findall(self.p,result)[0])
                elif re.findall(self.p1,result):
                    title=(re.findall(self.p1,result)[0])
                else:
                    title=' '
                title=title.replace("\n","")
                title=title.replace("\r","")
                title=title.replace("\t","")
                title=title.replace(" ",'')
                if isVisible(title)==True:
                        lock.acquire()
                        count=count+1
                        msg1="[+] "+tools.setStr2SameLen(30,domain)+title
                        printc.printf(msg1,'green')
                        lock.release()
                else:
                    pass
            except:
                # msg2="[-] "+domain+"不可访问"
                # printc.printf(msg2,'red')
                pass
            #lock.release()
#根据不同的类型选择不同的字典 1 subnames_school 2 subnames_gov 3 subnames_company 0 default subnames ,当然也支持用户自定义字典
def dicJudgeByInput(Input):
    if "Windows" in systeminfo:   
        if Input==1:
            return os.getcwd()+"\dict\subnames_school.txt"
        elif Input==2:
            return os.getcwd()+"\dict\subnames_gov.txt"
            #return os.getcwd().replace("module","\dict\subnames_gov.txt")
        elif Input==3:
            return os.getcwd()+"\dict\subnames_company.txt"
            #return os.getcwd().replace("module","\dict\subnames_company.txt")
        else:
            #return os.getcwd().replace("module","dict\subnames.txt")
            return os.getcwd()+"\dict\subnames.txt" 
    #elif "Linux" in systeminfo:
    elif "Linux" in systeminfo or "Darwin" in systeminfo:
        #print(os.getcwd())
        if Input==1:
            return os.getcwd()+"/dict/subnames_school.txt"
        elif Input==2:
            #return os.getcwd().replace("module","/dict/subnames_gov.txt")
            return os.getcwd()+"/dict/subnames_gov.txt"
        elif Input==3:
            #return os.getcwd().replace("module","/dict/subnames_company.txt")
            return os.getcwd()+"/dict/subnames_company.txt"
        else:
            #return os.getcwd().replace("module","/dict/return os.getcwd()+"/dict/subnames_school.txt"")
            return os.getcwd()+"/dict/subnames.txt"
    else:
        return Input 
#判断网站使用的是http或者https
def httpOrHttps(protocol):
    if protocol=="https":
        protocol="https"
    else:
        protocol="http"
    return protocol
#得到一个队列
def GetQueue(list):
    PortQueue = queue.Queue()
    for p in list:
        PortQueue.put(p)
    return PortQueue
#获取子域名
def getSubdomainName(nThreads,Num,domain,protocol):
    global count
    start_time=time.time()
    add=dicJudgeByInput(Num)
    subdomains=GetQueue(tools.content2List(add))
    ThreadList=[]
    for i in range(0, nThreads):
        t = getSubdomainNames(subdomains,domain,protocol)
        ThreadList.append(t)
    for t in ThreadList:
        t.start()
    for t in ThreadList:
        t.join()
    msg1="[+] Time cost:"+str(time.time()-start_time)+" s"
    msg2="[+] {count} Subdomains have been found".format(count=count)
    printc.printf(msg1,"yellow")
    printc.printf(msg2,"yellow")
#根据用户输入C:\targets.txt   /use/targets.txt   http://www.baidu.com   返回不同字符串或者列表  判断用户输入的是地址还是网址
#简单点讲就是根据用户输入的来决定输出结果是什么
def input2result(s):
    res = s
    if "http" in s:
        res = s
    elif "/"  in s:
        res = tools.content2List(s)
    elif "\\" in s:
        res = tools.content2List(s)
        print("当前是windows")
    return res
'''
缘故:对网站进行资产探测,这个功能产生缘故是有一次工作中遇到了一项任务,是对资产进行一个个复制,然后黏贴到浏览器中,一百多个资产我一个个进行测试,我信奉的原则是,机械重复的动作应该交给程序来做! 2019-8-31 14:49:57
作用:(1)该函数的作用是如果输入一个url然后程序进行探测,如果有效则可返回url以及标题.
    (2)如果请求一个连接进行了跳转,如果有效则打印并标记url进行了跳转
'''
#资产探测类
class URLDetect(threading.Thread):
    def __init__(self,urls,protocol):
        threading.Thread.__init__(self)
        self.urls=urls
        # self.domain1=domain1
        self.protocol=str(protocol)
        self.p="<title>([\W\w]*?)</title>"                     #匹配标题方便打印
        self.p1="<TITLE>([\W\w]*?)</TITLE>"
    def run(self):
        global lock,count
        status_code=title= '0'
        # domain1=self.domain1                                 #类似于baidu.com
        while not self.urls.empty():                           #对用户输入放入资产进行遍历
            url=self.urls.get()                                #类似于baidu.com
            # print(url)
            # domain=httpOrHttps(domain)+"://" +subdomain+"."+domain
            if "http" not in url:
                domain  = self.protocol + "://" + url
                #if "www" not in url:
                    # urls   = "http://www." + urls
                    #domain  = self.protocol + "://www." + url   #拼接成类似于http://www.baidu.com这样的完整域名
            #     else:
            #         domain  = self.protocol + "://" + url       #拼接成类似于http://www.baidu.com这样的完整域名
            else:
                domain  = url                                   #如果原目标中有指定协议则按原协议地址返回
            #domain=httpOrHttps(self.protocol)+str("://") +str(subdomain) 
            try: 
                res          = requests.get(domain,timeout=1,allow_redirects=True)
                lock.acquire()
                status_code  = res.status_code
                result=change2standard(res)
                #这里是用用来匹配网站title,后面可以根据自己的需要添加新的规则
                if (re.findall(self.p,result)):
                    title=(re.findall(self.p,result)[0])
                elif re.findall(self.p1,result):
                    title=(re.findall(self.p1,result)[0])
                else:
                    title=' '
                title=title.replace("\n","")#对title进行去杂
                title=title.replace("\r","")
                title=title.replace("\t","")
                title=title.replace(" ",'')
                #title=title.decode('utf-8')
                #if isVisible(title)==True:
                if status_code == 200:
                        count = count  + 1
                        msg   = "[+] " + tools.setStr2SameLen(30,domain)+title
                        #url status_code title visitable
                        tools.print2sheet(t1_len=25,t1=str(url),title1="URL",t2_len=2,t2="   "+str(status_code),title2="Status",t3_len=1,t3="   Yes",title3="Visitable",t4_len=20,t4=title,title4="Title")
                        # printc.printf(msg,'green')
                else:
                    #msg = "[-] " + " Yes "+domain
                    tools.print2sheet(t1_len=25,t1=str(url),title1="URL",t2_len=2,t2="   "+str(status_code),title2="Status",t3_len=1,t3="   No",title3="Visitable",t4_len=20,t4=title,title4="Title")
                    # printc.printf(msg,'red')
                    pass
                lock.release()
            except:
                # lock.acquire()
                # msg = "[-] " + " No "+domain
                # printc.printf(msg,'red')
                if status_code == 200:
                    tools.print2sheet(t1_len=25,t1=str(url),title1="URL",t2_len=2,t2="   "+str(status_code),title2="Status",t3_len=1,t3="   Yes",title3="Visitable",t4_len=20,t4=title,title4="Title")
                else:
                    #msg = "[-] " + " Yes "+domain
                    tools.print2sheet(t1_len=25,t1=str(url),title1="URL",t2_len=2,t2="   "+str(status_code),title2="Status",t3_len=1,t3="   No",title3="Visitable",t4_len=20,t4=title,title4="Title")
                #lock.release()
                pass
#资产探测函数
def urlDetect(urls,protocol,nThreads=40):
    tools.setSheetTitle(t1_len=25,title1="URL",t2_len=2,title2="Status",t3_len=1,title3="Visitable",t4_len=20,title4="Title")
    start_time     = time.time()
    # print(tools.content2List(urls))
    #因为当与用户输入 baidu.com时input2result无法处理,所以这里捕获一下异常人工进行处理一下,直接给其加上http或者www
    try:
        urls       = tools.input2result(urls)
    except:
        # print("出错啦")
        #msg            = "Please input standard url like http://www.test.com or https://www.test.com"
        # print(msg)
        # if "www" not in urls:
        #     urls   = "{protocol}://www.".format(protocol=protocol) + urls
        # else:
        urls   = "{protocol}://".format(protocol=protocol) + urls  #由于有时 类似  https://www.test.test.com 是不能正常访问的,所以就不手工添加www,先把上面代码注释掉,下次需要的时候再使用(2019-10-24 19:08:46)
    #根据用户输入的不同,执行不同的操作
    if type(urls)  == type([]):
        urls       = GetQueue(urls)
    elif type(urls)== type(""):
        temp       = []
        temp.append(urls)
        urls       = GetQueue(temp)
    ThreadList = []
    for i in range(0, nThreads):
        t = URLDetect(urls,protocol)
        ThreadList.append(t)
    for t in ThreadList:
        t.start()
    for t in ThreadList:
        t.join()
    msg1="[+] Time cost:"+str(time.time()-start_time)+" s"
    msg2="[+] {count} visitable URLs have been found".format(count=count)
    printc.printf(msg1,"yellow")
    printc.printf(msg2,"yellow")    


if __name__=='__main__':
    getSubdomainName(300,1,"ncu.edu.cn","http")


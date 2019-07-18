# coding=utf-8
'''
    该程序主要是实现邮件自动发送的功能,默认是使用QQ邮箱,但是函数内置提供了其他邮箱登录的函数,只要输入相关参数即可实现自定义邮箱发送
'''
import smtplib,time
from email.mime.text import MIMEText
from email.utils import formataddr
sender_ = "1058763824@qq.com"        # 发送人的邮箱
qq_key = "kgdjxqxokdttbdbg"          # qq允许第三方登录的key
receiver = "cyber-security@qq.com"   # 接受方的邮箱
subjectTitle = "您有一封新邮件"       # 邮件的的默认主题
sender_nickname  = "白猫"

def send(senderAddress=None,receiverAddress=None,subjectTitle_=None,emailContent=None,key=None):
    global sender_,receiver,qq_key,subjectTitle
    if receiverAddress != None:
        receiver     = receiverAddress
    if subjectTitle    != None:
        subjectTitle = subjectTitle_
    current_time = time.strftime("%Y-%m-%d %X",time.localtime())
    msg = "[{current_time}] From {sender} To {receiver}".format(current_time=current_time,sender=sender_,receiver=receiver)
    print(msg)
    try:
        ###################邮件内容模块##########################
        msg = MIMEText(emailContent,'plain','utf-8')         # emailContent是邮件的内容
        msg['From']    = formataddr(["白猫",sender_])   # 发件人邮箱
        msg['To']      = formataddr(['收件人昵称',receiver])  # 收件人的邮箱 
        msg['Subject'] = subjectTitle                        # 邮件主题/标题      
        ###################邮件内容模块##########################

        #*******************邮件登录模块*************************
        server = smtplib.SMTP_SSL("smtp.qq.com",465)         #暂时使用QQ邮箱,后期可根据需要重新配置
        server.login(sender_,qq_key)                         #发件人的邮箱账号,以及以及key
        server.sendmail(sender_,[receiver,],msg.as_string()) #发件人的邮箱,接收人的邮箱,邮件内容
        server.quit()                                        #退出                         
        #*******************邮件登录模块*************************

        current_time = time.strftime("%Y-%m-%d %X",time.localtime())
        msg = "[{current_time}] Email sent successfully!".format(current_time=current_time)
        print(msg)
    except Exception as e:
        current_time = time.strftime("%Y-%m-%d %X",time.localtime())
        msg = "[{current_time}] Email did not sent successfully!Please check the reason!".format(current_time=current_time)
        print(msg)
        print(e)
if __name__=='__main__':
    emailContent = """
    
.--.   .--. .-./`)   .---.     .---.                 .-''-.  ,---.  ,---.   .-''-.  .-------.       ____     __   ,-----.    ,---.   .--.    .-''-.   
|  | _/  /  \ .-.')  | ,_|     | ,_|               .'_ _   \ |   /  |   | .'_ _   \ |  _ _   \      \   \   /  /.'  .-,  '.  |    \  |  |  .'_ _   \  
| (`' ) /   / `-' \,-./  )   ,-./  )              / ( ` )   '|  |   |  .'/ ( ` )   '| ( ' )  |       \  _. /  '/ ,-.|  \ _ \ |  ,  \ |  | / ( ` )   ' 
|(_ ()_)     `-'`"`\  '_ '`) \  '_ '`)           . (_ o _)  ||  | _ |  |. (_ o _)  ||(_ o _) /        _( )_ .';  \  '_ /  | :|  |\_ \|  |. (_ o _)  | 
| (_,_)   __ .---.  > (_)  )  > (_)  )           |  (_,_)___||  _( )_  ||  (_,_)___|| (_,_).' __  ___(_ o _)' |  _`,/ \ _/  ||  _( )_\  ||  (_,_)___| 
|  |\ \  |  ||   | (  .  .-' (  .  .-'           '  \   .---.\ (_ o._) /'  \   .---.|  |\ \  |  ||   |(_,_)'  : (  '\_/ \   ;| (_ o _)  |'  \   .---. 
|  | \ `'   /|   |  `-'`-'|___`-'`-'|___          \  `-'    / \ (_,_) /  \  `-'    /|  | \ `'   /|   `-'  /    \ `"/  \  ) / |  (_,_)\  | \  `-'    / 
|  |  \    / |   |   |        \|        \          \       /   \     /    \       / |  |  \    /  \      /      '. \_/``".'  |  |    |  |  \       /  
`--'   `'-'  '---'   `--------``--------`           `'-..-'     `---`      `'-..-'  ''-'   `'-'    `-..-'         '-----'    '--'    '--'   `'-..-'   
                                                                                                                                                      

    """
    send(emailContent=emailContent,subjectTitle_="今天天气不错")
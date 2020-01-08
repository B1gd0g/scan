# -- coding: utf-8 --
import telnetlib,eventlet,time
from module import globalInfo,printc

portsList  =  globalInfo.most_useful_ports() #最常见的一些端口信息
#telnet批量检测函数
def telnet(ip="",port = "",address=''):
	eventlet.monkey_patch()
	time_limit  = 0.2 #设置超时时间为1s
#默认情况下只扫描常见一些端口
	if port=="":
		for port in portsList:
			with eventlet.Timeout(time_limit,False):#请求超过1.5s没响应默认该端口不通
				try:
					tn      =telnetlib.Telnet(ip,port)
					msg     = "[+] {ip}:{port} open [+]".format(ip=ip,port=port)
					print(msg) 
				except Exception as e:
					msg     = "[-] {ip}:{port} close".format(ip=ip,port=port)
					print(msg)
					pass
				finally:
					pass
			msg     = "[-] {ip}:{port} close".format(ip=ip,port=port)
			print(msg)
#当用户指定一些常见的扫描端口时 port=123,122
	elif "," in port:
		ports = port.split(",")
		with eventlet.Timeout(time_limit,False):#请求超过1.5s没响应默认该端口不通
			for port in ports:
				try:
					tn      =telnetlib.Telnet(ip,port)
					msg     = "[+] {ip}:{port} open [+]".format(ip=ip,port=port)
					print(msg)      
				except Exception as e:
					msg     = "[-] {ip}:{port} close".format(ip=ip,port=port)
					print(msg)
					pass
				finally:
					pass
			#程序请求超过设定时间内仍然没有相应默认认为该端口不通
			msg     = "[-] {ip}:{port} close".format(ip=ip,port=port)
			print(msg)
#用户指定一定范围的扫描目标时port=1-1000
	elif "-" in port:
		ports = port.split("-")
		start = int(ports[0])
		end   = int(ports[1])
		ports = port.split(",")
		for port in range(start,end+1):
			with eventlet.Timeout(time_limit,False):#请求超过1.5s没响应默认该端口不通
				try:
					tn      =telnetlib.Telnet(ip,port)
					msg     = "[+] {ip}:{port} open [+]".format(ip=ip,port=port)
					print(msg) 
				except Exception as e:
					msg     = "[-] {ip}:{port} close".format(ip=ip,port=port)
					print(msg)
					pass
				finally:
					pass
			#程序请求超过设定时间内仍然没有相应默认认为该端口不通
			msg     = "[-] {ip}:{port} close".format(ip=ip,port=port)
			print(msg)

#用户只扫描单个目标时
	else:
		with eventlet.Timeout(time_limit,False):#请求超过1.5s没响应默认该端口不通
			try:
				tn      =telnetlib.Telnet(ip,port)
				msg     = "[+] {ip}:{port} open [+]".format(ip=ip,port=port)
				print(msg) 
			except Exception as e:
				msg     = "[-] {ip}:{port} close".format(ip=ip,port=port)
				print(msg)
				pass
			#程序请求超过设定时间内仍然没有相应默认认为该端口不通
			msg     = "[-] {ip}:{port} close".format(ip=ip,port=port)
			print(msg)


if __name__=='__main__':
		telnet("220.181.38.148")
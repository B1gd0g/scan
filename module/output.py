# -- coding: utf-8 --
'''
该模块是自己手工创建并且维护,可能会遇到很多问题,后面会持续维护
'''
import sys,os
#将文
def output(content,fileName):
	root_dir 	= os.getcwd()    							#程序的根目录
	file_add	= os.path.join(root_dir,'output',fileName)  #该出妙在不用人工判断不同平台,比如是Windows还是Linux,程序可以自己判断
	file 		= open(file_add,'a+')
	file.write(str(content) + "\n")
	file.close()
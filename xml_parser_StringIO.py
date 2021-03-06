#!/usr/bin/env python
# -*- coding: UTF-8 -*-
#本脚本完成MRO_XML文件转换为可入库的csv文件
import os,gzip,time,cStringIO
from xml.parsers.expat import ParserCreate
from os.path import join, splitext

#变量声明
d_eNB = {}
d_obj = {}
s = ''
flag = False
output = cStringIO.StringIO()

#Sax解析类
class DefaultSaxHandler(object):
	#处理开始标签
	def start_element(self, name, attrs):
		global d_eNB
		global d_obj
		if name == 'eNB':
			d_eNB = attrs
		elif name == 'object':
			d_obj = attrs
		elif name == 'v':
			output.write(d_eNB['id']+' '+ d_obj['id']+' '+d_obj['MmeUeS1apId']+' '+d_obj['MmeGroupId']+' '+d_obj['MmeCode']+' '+d_obj['TimeStamp']+' ')
		else:
			pass
	#处理中间文本
	def char_data(self, text):
		global d_eNB
		global d_obj
		global flag
		if text[0:1].isnumeric():
			output.write(text)
		elif text.startswith('MR.LteScPlrULQci1'):
			flag = True
			#print(text,flag)
		else:
			pass
	#处理结束标签
	def end_element(self, name):
		global d_eNB
		global d_obj
		if name == 'v':
			output.write('\n')
		else:
			pass

#Sax解析调用
handler = DefaultSaxHandler()
parser = ParserCreate()
parser.StartElementHandler = handler.start_element
parser.EndElementHandler = handler.end_element
parser.CharacterDataHandler = handler.char_data

i = 0	#rowcount
start_time = time.time()
xm = gzip.open('/tmcdata/mro2csv/input31/TD-LTE_MRO_NSN_OMC_234598_20160224060000.xml.gz','rb')
with open('/tmcdata/mro2csv/output31/TD-LTE_MRO_NSN_OMC_234598_20160224060000.csv','w') as t:		#生成csv文件以写入数据
	for line in xm.readlines():
		i += 1
		if i%10000 == 0:
			print('------>%d' % i)
		parser.Parse(line) #解析xml文件内容
		if flag:
			break
	t.writelines(output.getvalue().replace(' \n','\r\n').replace(' ',',').replace('T',' ').replace('NIL',''))	#写入解析后内容
print('文件行计数：%d，处理用时：%f。' % (i,time.time()-start_time))
xm.close()
output.close()
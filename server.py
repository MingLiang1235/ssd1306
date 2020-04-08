#!/usr/bin/python3
#-*- encoding:UTF-8 -*-
#coding=utf-8
#以上保存后在linux内无法直接打开，需要vim :set fileformat=unix来去除\r\n为\n
'''filename： share_memo.py
   perporse:  multiprocessing server and share-memory IPC.Provide weather data.
	Author:   unicoder@sohu.com
	date:	  2020-04-03
	'''

import mmap
import contextlib
import time
import logging
import requests
import random
import time
import socket
import http.client
from bs4 import BeautifulSoup

def get_content(url, data=None):
	header={
		'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
		'Accept-Encoding':'gzip,deflate,sdch',
		'Accept-Language':'zh-CN,zh;q=0.8',
		'Connection':'keep-alive',
		'User-Agent':'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) chrome/43.0.235'
	}
	timeout = random.choice(range(60,190))
	while True:
		try:
			rep = requests.get(url, headers=header, timeout=timeout)
			rep.encoding = 'utf-8'
			break                      #获取一次便中断
		except socket.timeout as e:
			print('3:', e)
			time.sleep(random.choice(range(5,15)))
		except socket.error as e:
			print('4:', e)
			time.sleep(random.choice(range(20,60)))
		except http.client.BadStatusLine as e:
			print('5:',e)
			time.sleep(random.choice(range(30,90)))
		except http.client.IncompleteRead as e:
			time.sleep(random.choice(range(10,19)))
	return rep.text

def get_data(html_text):
	final = []
	bs = BeautifulSoup(html_text, "html.parser")  #创建BeautifulSoup对象
	body = bs.body  #获取Body部分
	data = body.find('div',{'id':'7d'}) #找id为7d的div
	ul = data.find('ul')
	li = ul.find('li')   #找到第一个li（今天）
	temp = []
	#date = li.find('h1').string  #找到日期
	#final.append(date)
	inf = li.find_all('p')  #获取li中所有的p
	final.append(inf[0].string)  #天气状况
	if inf[1].find('span') is None:
		temperature_highest = None #到了傍晚，天气预报没有当天的最高气温，需要加判断语句来输出最低气温
	else:
		temperature_highest = inf[1].find('span').string   #最高气温
	temperature_lowest = inf[1].find('i').string  #最低气温
	final.append(temperature_highest)
	final.append(temperature_lowest)
	return final

#def write_data(data, name):




if __name__ == '__main__':
	logging.basicConfig(filename="/home/pi/Prog/ssd1306/log",filemode="a",format="%(asctime)s-%(name)s-%(message)s",level=logging.INFO)
	url = {
			'北京':'http://www.weather.com.cn/weather/101010100.shtml',
			'三亚':'http://www.weather.com.cn/weather/101310201.shtml',
			'秦皇岛':'http://www.weather.com.cn/weather/101091101.shtml',
			'大连':'http://www.weather.com.cn/weather/10107020102A.shtml',
			'青岛':'http://www.weather.com.cn/weather/101120201.shtml'
			}
	
	

	    
	while True:
		with open("/home/pi/Prog/ssd1306/weather.dat","wb") as f:
			fill = '\x00' * 1024
			fill = fill.encode(encoding = 'utf-8') # turns str to bytes and write to file.
			f.write(fill) # turns str to bytes and write to file.
			f.close()
		with open("/home/pi/Prog/ssd1306/weather.dat",'r+b') as f:   
			with contextlib.closing(mmap.mmap(f.fileno(), 1024, access=mmap.ACCESS_WRITE)) as m:
				#try:
				#	fill = '\x00' * 1024
				#	fill = fill.encode(encoding = 'utf-8') # turns str to bytes
				#	m.seek(0)
				#	m.write(fill)
				#	m.flush()
				#except Exception as err:
				#	logging.warning("?"*10+str(err))
				final = []
				for key, values in url.items():
					html = get_content(values)
					result = get_data(html)
					result.insert(0,key)
					final.append(result)
				#logging.info(str(final))
				outp_s = ''
				for result in final:     #result必得是数列
					s = ''
					for ss in result:
						if ss:               #如果温度没有变化
							s += (ss + ',')  #用逗号分隔
					s = s[0:-1]          #每个城市最后一个逗号去掉，改成空格（下一行实现）
					outp_s += (s + ' ')
				#s = s + str(i)
				try:
					m.seek(0)
					logging.info(outp_s)
					outp_s.rjust(1024, '\x00')
					outp_s = outp_s.encode(encoding = 'utf-8')  #将str类型的s转变为bytes类型。
					m.write(outp_s)
					m.flush()
				except Exception as err:
					logging.warning("!"*10+str(err))
			m.close()
		f.close()
		time.sleep(3600)

#!/usr/bin/python3
#以上保存后在linux内无法直接打开，需要vim :set fileformat=unix来去除\r\n为\n
#-*- encoding:UTF-8 -*-
#coding=utf-8
'''filename： share_memo_client.py
   perporse:  test multiprocessing moudle and share-memory IPC.share memory client is data consumer.
	Author:   unicoder@sohu.com
	date:	  2020-04-03
	'''

import mmap
import contextlib
import time

while True:
	with open("weather.dat","r") as f:
		with contextlib.closing(mmap.mmap(f.fileno(), 1024, access=mmap.ACCESS_READ)) as m:
			s = m.read(1024)
			s = str(s, encoding = 'utf-8').replace('\x00', '')
			print (s)
	time.sleep(0.1)
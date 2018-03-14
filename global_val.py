# -*- coding: utf-8 -*-

import logging
import tkinter.messagebox as messagebox

def _init():#初始化
	global _global_dict
	_global_dict = {}

def set(key,value):
	_global_dict[key] = value


def get(key,defValue=None):
	try:
		return _global_dict[key]
	except KeyError:
		return defValue

def errorEntry(message,err='Error',key=ValueError):
	logging.info(message)
	
	if get('debugFlag') == 'FALSE':
		messagebox.showinfo(err,message)
		try:
			2/0
		except:
			raise key

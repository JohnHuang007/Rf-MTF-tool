#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from tkinter import *
from tkinter import ttk
from tkinter import scrolledtext
from tkinter import filedialog
import tkinter.messagebox as messagebox
import logging,os,time,scriptCmd,global_val,threading

def loadCfg(self):
	logging.info('enter loadCfg')
	cfgfile = filedialog.askopenfilename(filetypes=[("configFile.txt","*.*")])

	# print(dir(rxOnTiming))
	# for child in rxOnTiming.winfo_children():
	# 	print(child)
	# childList = rxTab.winfo_children()[0].winfo_children()
	# childList[0].configure(text='rfeef')
	# child = self.winfo_children()
	# child[0].configure(state='disabled')

	try:
		with open(cfgfile,'r') as f:
			# logging.info('config file open success')
			for winId in ['rxOnTiming','rxOffTiming','txOnTiming','txOffTiming','rxRegsInfo','txRegsInfo']:
				temp = global_val.get(winId)
				temp.delete(*temp.get_children())

			for line in f.readlines():
				tempStr = line.strip()
				cmdStr = ''
				for tempChar in tempStr:
					if tempChar == '#':
						break
					else:
						cmdStr = cmdStr+tempChar
				if cmdStr != '':
					if cmdStr != 'end':
						logging.info('cmdDecoder:'+cmdStr)
						scriptCmd.cmdRun(self,cmdStr)
						# logging.info(cmdStr)
					else:
						pass
	except FileNotFoundError as e:
		logging.info(e)
	except ValueError as e:
		global_val.errorEntry('Uart Open Failed!')
	except NameError as e:
		global_val.errorEntry('ConfigFile Format Error!')
	except:
		logging.info('loadCfg unknown Error')
		

def rx_on(self):
	logging.info('enter rx on')
	cmdStr = 'action=[rx_on]'
	scriptCmd.cmdRun(self,cmdStr)
	time.sleep(1)
	RxOnFlag = 1
	global_val.set('RxOnFlag', RxOnFlag)
	threading.Timer(1,scriptCmd.readFromL1).start()

def rx_off(self):
	logging.info('enter rx off')
	RxOnFlag = 0
	global_val.set('RxOnFlag', RxOnFlag)
	time.sleep(1)
	cmdStr = 'action=[rx_off]'
	scriptCmd.cmdRun(self,cmdStr)

def tx_on(self):
	logging.info('enter tx on')
	cmdStr = 'action=[tx_on]'
	scriptCmd.cmdRun(self,cmdStr)

def tx_off(self):
	logging.info('enter tx off')
	cmdStr = 'action=[tx_off]'
	scriptCmd.cmdRun(self,cmdStr)

def reset(self):
	logging.info('enter reset')
	cmdStr = 'action=[reset]'
	scriptCmd.cmdRun(self,cmdStr)
	RxOnFlag = 0
	global_val.set('RxOnFlag', RxOnFlag)

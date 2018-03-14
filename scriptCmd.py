#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from tkinter import *
from tkinter import ttk
from tkinter import filedialog
from tkinter import scrolledtext
import numpy as np
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import tkinter.messagebox as messagebox
import logging,os,time,serial,threading,ctrlBtn,rfTest,global_val,excelLoad

global timingBeginFlag
timingBeginFlag = False

def cmdRun(self,cmdStr):

	global timingBeginFlag

	cmdKeys = cmdStr.split('=',1)[0]
	cmdValue = cmdStr.split('=',1)[1]

	uartStr = ''

	if cmdKeys == 'reg':

		uartStr = uartStr + '00' # cmdId

		if timingBeginFlag == True:			
			uartStr = uartStr + '01' # cmd operator,regs
		else:
			uartStr = uartStr + '07' # direct write Regs

		# regs write action: tpu/cpu
		if (cmdValue.split('[',1)[1].split(']',1)[0].split(',',3)[0] == 'cpu'):
			uartStr = uartStr + '00' # cpu
		else:
			uartStr = uartStr + '01' # tpu	

		# regs address
		addr = zeroAlignment(cmdValue.split('[',1)[1].split(']',1)[0].split(',',3)[1].split('x',1)[1])
		uartStr = uartStr + addr
		# regs value
		value = zeroAlignment(cmdValue.split('[',1)[1].split(']',1)[0].split(',',3)[2].split('x',1)[1])
		uartStr = uartStr + value
		# regs delay us
		delay = zeroAlignment(cmdValue.split('[',1)[1].split(']',1)[0].split(',',3)[3].split('x',1)[1])
		uartStr = uartStr + delay

		writeToL1(uartStr)
		
		if timingBeginFlag == True:
			global_val.get('timingWin').insert('','end',value=('regs','0x'+addr,'0x'+value,'0x'+delay))
		else:
			global_val.get('RegsRecord').insert('','end',value=('write','0x'+addr,'0x'+value))
	elif cmdKeys == 'gpio':
		uartStr = uartStr + '00' # cmdId
		uartStr = uartStr + '02' # cmd operator,gpio
		# gpio Id
		gpio_name = cmdValue.split('[',1)[1].split(']',1)[0].split(',',2)[0]
		uartStr = uartStr + zeroAlignment(cmdValue.split('[',1)[1].split(']',1)[0].split(',',2)[0].split('@',1)[1],bitsWidth=2)
		# gpio state
		state = zeroAlignment(cmdValue.split('[',1)[1].split(']',1)[0].split(',',2)[1],bitsWidth=2)
		uartStr = uartStr + state
		if state == '00':
			gpio_state = 'Low'
		else:
			gpio_state = 'High'
		# gpio delay us
		delay = zeroAlignment(cmdValue.split('[',1)[1].split(']',1)[0].split(',',2)[2].split('x',1)[1])
		uartStr = uartStr + delay

		writeToL1(uartStr)

		global_val.get('timingWin').insert('','end',value=('Gpio',gpio_name,gpio_state,'0x'+delay))
	elif cmdKeys == 'action':

		uartStr = uartStr + '00' # cmdId
		uartStr = uartStr + '03' # cmd operator,action

		if (cmdValue.split('[',1)[1].split(']',1)[0] == 'rx_on'):
			uartStr = uartStr + '00' # action Id,rx on
			buttonEnList = [0,2,5]
			rfTest.upRxState('on')
		elif (cmdValue.split('[',1)[1].split(']',1)[0] == 'rx_off'):
			uartStr = uartStr + '01' # action Id,rx off
			buttonEnList = [0,1,3,5]
			rfTest.upRxState('off')
		elif (cmdValue.split('[',1)[1].split(']',1)[0] == 'tx_on'):
			uartStr = uartStr + '02' # action Id,rx off
			buttonEnList = [0,4,5]
			rfTest.upTxState('on')
		elif (cmdValue.split('[',1)[1].split(']',1)[0] == 'tx_off'):			
			uartStr = uartStr + '03' # action Id,rx off
			buttonEnList = [0,1,3,5]
			rfTest.upTxState('off')
		elif (cmdValue.split('[',1)[1].split(']',1)[0] == 'reset'):
			uartStr = uartStr + '04' # action Id,reset
			buttonEnList = [0,5]
			rfTest.upTxState('off')
			rfTest.upRxState('off')

		logging.info(cmdValue.split('[',1)[1].split(']',1)[0])

		writeToL1(uartStr)

		for child in self.winfo_children():
			child.configure(state='disabled')
		childButton = self.winfo_children()
		for i in buttonEnList:
			childButton[i].configure(state='enable')
		
		# if global_val.get('timingWin') != None:
		# 	global_val.get('timingWin').insert(INSERT,ctrlBtn.ueState+'\n')
		if (cmdValue.split('[',1)[1].split(']',1)[0] == 'rx_on'):
			RxOnFlag = 1
			global_val.set('RxOnFlag', RxOnFlag)
			threading.Timer(1,readFromL1).start()
		elif (cmdValue.split('[',1)[1].split(']',1)[0] == 'rx_off'):
			RxOnFlag = 0
			global_val.set('RxOnFlag', RxOnFlag)

	elif cmdKeys == 'uart':
		logging.info('open Uart begin')
		try:
			global uartSerPort,uartSerBaudrate
			(uartSerPort,uartSerBaudrate) = (cmdValue.split('[',1)[1].split(']',1)[0].split(',',1)[0],
				cmdValue.split('[',1)[1].split(']',1)[0].split(',',1)[1])
			with serial.Serial(uartSerPort,baudrate=uartSerBaudrate,
				bytesize=8, parity='N', stopbits=1, timeout=1, xonxoff=0, rtscts=0) as ser:
				rfTest.upUartState('open success')
				logging.info('uart open: success')
		except:
			global_val.errorEntry('Uart Open Failed...',key=ValueError)
			
	elif cmdKeys == 'timing_begin':
		uartStr = uartStr + '00' # cmdId
		uartStr = uartStr + '04' # cmd operator, begin

		if (cmdValue.split('[',1)[1].split(']',1)[0] == 'rx_on'):
			uartStr = uartStr + '00' # action Id,rx on
			win = global_val.get('rxOnTiming')
			global_val.set('timingWin', win)
		elif (cmdValue.split('[',1)[1].split(']',1)[0] == 'rx_off'):
			uartStr = uartStr + '01' # action Id,rx off
			win = global_val.get('rxOffTiming')
			global_val.set('timingWin', win)
		elif (cmdValue.split('[',1)[1].split(']',1)[0] == 'tx_on'):
			uartStr = uartStr + '02' # action Id,rx off
			win = global_val.get('txOnTiming')
			global_val.set('timingWin', win)
		elif (cmdValue.split('[',1)[1].split(']',1)[0] == 'tx_off'):
			uartStr = uartStr + '03' # action Id,rx off	
			win = global_val.get('txOffTiming')
			global_val.set('timingWin', win)

		# global timingBeginFlag
		timingBeginFlag = True

		writeToL1(uartStr)
		
	elif cmdKeys == 'timing_end':
		uartStr = uartStr + '00' # cmdId
		uartStr = uartStr + '05' # cmd operator, end

		if (cmdValue.split('[',1)[1].split(']',1)[0] == 'rx_on'):
			uartStr = uartStr + '00' # action Id,rx on
		elif (cmdValue.split('[',1)[1].split(']',1)[0] == 'rx_off'):
			uartStr = uartStr + '01' # action Id,rx off
		elif (cmdValue.split('[',1)[1].split(']',1)[0] == 'tx_on'):
			uartStr = uartStr + '02' # action Id,rx off
		elif (cmdValue.split('[',1)[1].split(']',1)[0] == 'tx_off'):
			uartStr = uartStr + '03' # action Id,rx off	

		# global timingBeginFlag
		timingBeginFlag = False

		writeToL1(uartStr)
	
	elif cmdKeys == 'regsFilePath':
		
		filePath = cmdValue.split('[',1)[1].split(']',1)[0]

		regFilesInfo = global_val.get('regFilesInfo')
		# check this file had been load or not before,
		fileExist = False
		for fileIdx in range(len(regFilesInfo)):
			if filePath == regFilesInfo[fileIdx][0]:
				fileExist = True
				break

		if fileExist == False:
			try:
				regFileInfo = excelLoad.excelLd(filePath)

				if regFileInfo[0] == 0: # fileValid=0
					logging.info('regs file open Success!')
					
					# filePath,sheetIdx,regsOffset
					regFilesInfo.append([regFileInfo[1],regFileInfo[2],regFileInfo[3]])
					global_val.set('regFilesInfo', regFilesInfo)
				else:
					logging.info('regs file open failed!')
			except:
				pass
		
	elif cmdKeys == 'DEBUG':
		
		debugFlag = cmdValue.split('[',1)[1].split(']',1)[0]
		logging.info('debugFlag='+debugFlag)
		global_val.set('debugFlag',debugFlag)

	else:
		logging.info('error one CmdKeys')
		global_val.errorEntry('cmdKeys Error',key=NameError)

def writeToL1(wrStr,timeout=0.1):
	dataStr= ''
	try:
		with serial.Serial(uartSerPort,baudrate=uartSerBaudrate,
			bytesize=8, parity='N', stopbits=1,timeout=timeout,xonxoff=0, rtscts=0) as ser:
			logging.info('uartCmd:'+wrStr)
			wrStr = 'EC+RFTEST=' + wrStr + '\r'

			for idx in range(2):
				ser.write(wrStr.encode('ascii'))
				data = ser.readline()
				if len(data) != 0:
					dataStr = data.decode('ascii').split('\n',1)[0]
					logging.info('Return: '+dataStr)
					break
				else:
					logging.info('AtCmd returned length = 0')

	except ValueError as e:	
		global_val.errorEntry(e,key=ValueError)
	except Exception as e:
		global_val.errorEntry(e,'UartWriteFailed')
	except:
		global_val.errorEntry('Uart Write Failed...')
	finally:
		return dataStr,len(dataStr)

def readFromL1():
	RxOnFlag = global_val.get('RxOnFlag')
	if RxOnFlag == 1:
		uartStr = '0006' # cmd operator, read rx data
		dataStr,data_len=writeToL1(uartStr,1)		
		rxDataPlot(dataStr,data_len)
		threading.Timer(1,readFromL1).start()
	# try:
	# 	with serial.Serial(uartSerPort,baudrate=uartSerBaudrate,
	# 		bytesize=8, parity='N', stopbits=1, timeout=0.01, xonxoff=0, rtscts=0) as ser:
	# 		while RxTmFlag == 1:
	# 			data = ser.readline()
	# 			if len(data) != 0:
	# 				print(data)
	# except Exception as e:
	# 	messagebox.showinfo('UartReadFailed',e)	

def zeroAlignment(inStr,bitsWidth=8):
	if len(inStr) < bitsWidth:
			tempStr = ''
			for i in range(bitsWidth-len(inStr)):
				tempStr = tempStr + '0'
			tempStr = tempStr + inStr
			return tempStr
	else:
		return inStr

def rxDataPlot(dataStr,data_len):
	if data_len != 0:
		dataValue = rxDataSplit(dataStr,8)
		if len(dataValue) == 128:

			qValue = [x&0x000003FF for x in dataValue]
			iValue = [(x>>10)&0x000003FF for x in dataValue]

			adc_vpp = global_val.get('adc_vpp')
			rxTimeIdc = global_val.get('rxTimeIdc')
			rxTimeQdc = global_val.get('rxTimeQdc')
			rxTimePower = global_val.get('rxTimePower')
			rxFreqMax = global_val.get('rxFreqMax')
			fig = global_val.get('fig')

			xValue = np.arange(0,128,1)

			fig.clf()
			iqFig = fig.add_subplot(211)
			iqFig.plot(xValue,iValue,xValue,qValue)
			iqFig.legend(['I','Q'])

			freq = fig.add_subplot(212)	
			sig = [a+b for a,b in zip([x*1j for x in qValue],iValue)]
			SIG = np.fft.fft(sig)
			freq.plot(xValue,SIG)

			fig_Canvas = global_val.get('fig_Canvas')
			fig_Canvas.show()
	else:
		logging.info('rxData length = 0')

def rxDataSplit(str,num=2):
	if len(str) <= num:
		return str
	else:
		tempStr = []
		for i in range(int(len(str)/num)):
			if (str[i] > '9') or (str[i] < '0'):
				return [0] # error
			tempStr.append(int(str[i*num:(i+1)*num].encode("utf-8"),16))
		return tempStr

def strReverse(str):
	tempStr3 = ''
	for u32Idx in range(int(len(str)/8)):
		tempStr = str[u32Idx*8:(u32Idx+1)*8]
		tempStr2 = ''
		for u8Idx in range(4):
			tempStr2 = tempStr2 + tempStr[(4-u8Idx-1)*2:(4-u8Idx)*2]
		tempStr3 = tempStr3 + tempStr2
	return tempStr3


	
	

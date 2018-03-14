#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import global_val

global elementList

def get():
	element = ['AntSw','PA']
	mode = [['Rx','Tx'],['TxOn','TxOff','HighGain','MiddleGain','LowGain']]
	timingProperty = [['RxOn,RxOff','TxOn,TxOff'],['TxOn','TxOff','TxOn','TxOn','TxOn']]

	elementList = [element,mode,timingProperty]

	return element,mode,timingProperty


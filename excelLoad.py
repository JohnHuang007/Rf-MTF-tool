#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import xlrd,scriptCmd

def excelLd(fileNamePath):
	fileValid = -1
	sheetNames = []
	regsOffset = []
	sheetIdx = []

	try:

		rfRegsDef = xlrd.open_workbook(fileNamePath)

		for i in range(len(rfRegsDef._sheet_names)):
			sheetIdx.append(rfRegsDef.sheet_by_index(i))

		for i in range(len(sheetIdx)):

			# 1st line Table names
			sheetNames.append(sheetIdx[i].row_values(0)[5])
			# 2nd line Base address
			baseAddr = sheetIdx[i].row_values(1)[5]

			regsOffset.append({})

			# check row content one by one
			for idx in range(sheetIdx[i].nrows-2):
				tempRow = sheetIdx[i].row_values(idx+2)
				
				if tempRow[0] == 'REGISTER':
					pass
				elif tempRow[0] == 'MNEMONIC':
					pass
				elif tempRow[0] == 'OFFSET':
					tempAddr = hex(int(baseAddr,16)+int(tempRow[5].split('x',1)[1],16))
					regsOffset[i]['0x'+scriptCmd.zeroAlignment(tempAddr.split('x',1)[1])] = idx+2
				elif tempRow[0] == 'Dependency':
					pass
				elif tempRow[0] == 'BITS':
					pass
	except:
		return (fileValid,None,None,None)

	fileValid = 0
	return [fileValid,fileNamePath,sheetNames,regsOffset]
	
def excelRowsRead(fileNamePath,sheetIdx,rowsNum):
	tempXlrd = xlrd.open_workbook(fileNamePath)
	return tempXlrd.sheet_by_index(sheetIdx).row_values(rowsNum)


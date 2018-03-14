#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from tkinter import *
from tkinter import ttk,scrolledtext,Scrollbar,Menu
import numpy as np
import base64
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from pylab import pi
# from icon import img
import tkinter.messagebox as messagebox
import logging,os,time,ctrlBtn,scriptCmd,global_val,matplotlib,excelLoad,stickyEntry,element

class EigenCommRfTest(Frame):
    # def __init__(self, master=None):
    #     Frame.__init__(self, master)  

    def appOpen(self):
        self.grid()
        self.createWidgets()
        self.logCfg()

    def logCfg(self):
        path = os.getcwd() + '/temp'
        if not os.path.isdir(path):
            os.mkdir(path)
        logging.basicConfig(level=logging.INFO,
            filename=path+'/logs_'+time.strftime("%Y%m%d_%H_%M_%S")+'.txt',
            filemode='w')

    def createWidgets(self):
        
        # Uart panel
        # uartPanel = LabelFrame(self,text=' Uart ')
        # Label(uartPanel,text='Port:').grid()
        
        # uartPort = StringVar()
        # portChosen = ttk.Combobox(uartPanel, width=6, textvariable=uartPort) 
        # portChosen['values'] = ('com1', 'com2', 'com3')
        # portChosen.grid(padx=10,pady=10)
        # ttk.Button(uartPanel, text="open",width=8).grid(padx=10,pady=10)

        # Control panel
        ctrlPanel = LabelFrame(self,text=' ControlPanel ')
        ttk.Button(ctrlPanel,text="LoadCfg",width=8,command=lambda: ctrlBtn.loadCfg(ctrlPanel)).grid(padx=10,pady=10)
        ttk.Button(ctrlPanel,text=" rx On ",width=8,command=lambda: ctrlBtn.rx_on(ctrlPanel),state='disabled').grid(padx=10,pady=10)
        ttk.Button(ctrlPanel,text=" rx Off ",width=8,command=lambda: ctrlBtn.rx_off(ctrlPanel),state='disabled').grid(padx=10,pady=10)
        ttk.Button(ctrlPanel,text=" tx On ",width=8,command=lambda: ctrlBtn.tx_on(ctrlPanel),state='disabled').grid(padx=10,pady=10)
        ttk.Button(ctrlPanel,text=" tx Off ",width=8,command=lambda: ctrlBtn.tx_off(ctrlPanel),state='disabled').grid(padx=10,pady=10)
        ttk.Button(ctrlPanel,text=" reset ",width=8,command=lambda: ctrlBtn.reset(ctrlPanel),state='disabled').grid(padx=10,pady=10)

        # status panel
        statusPanel = LabelFrame(self,text=' Status ')
        Label(statusPanel,text='Tx:').grid(column=0, row=1)
        Label(statusPanel,text='           ').grid(column=1, row=1)
        Label(statusPanel,text='Rx:').grid(column=2, row=1)
        Label(statusPanel,text='           ').grid(column=3, row=1)
        Label(statusPanel,text='Uart:').grid(column=4, row=1)
        Label(statusPanel,text='           ').grid(column=5, row=1)

        # Tab control.
        tabControl = ttk.Notebook(self) # Create Tab Control
        # LabelFrame(rxTab,text=' Band ').pack(expand=1, fill="both")
        funcTab = ttk.Frame(tabControl) # Add front-end control tab
        tabControl.add(funcTab, text=' Function ')   
        fecTab = ttk.Frame(tabControl) # Add front-end control tab
        tabControl.add(fecTab, text=' Mapping ')  
        TimingTab = ttk.Frame(tabControl) # Add front-end control tab
        tabControl.add(TimingTab, text=' Timing ')    

        funcCtrl = ttk.Notebook(funcTab) # Create Tab Control
        rxTab = ttk.Frame(funcCtrl)
        funcCtrl.add(rxTab, text=' Rx ') # Add rx tab
        txTab = ttk.Frame(funcCtrl) # Add tx tab
        funcCtrl.add(txTab, text=' Tx ')
        comTab = ttk.Frame(funcCtrl)
        funcCtrl.add(comTab, text=' Com ') # Add common tab
        funcCtrl.grid()

        # rx Tab
        rxTiming = LabelFrame(rxTab,text=' Timing ')
        # OnTiming
        rxOnTiming,vbar1=treeViewBuild(rxTiming,("type","addr","value","delay"),[60,90,90,90],["On type","addr","value","delay"])
        rxOnTiming.configure(height=6)
        rxOnTiming.grid(column=0, row=0,padx=5,pady=5)
        rxOnTiming.bind("<Double-1>",lambda x:rxOnParasUpdata(x,rxOnTiming,rxRegsInfo))
        vbar1.grid(column=1, row=0,sticky=NS)
        
        # rxOnTiming.insert('','end',values=('regs','0x44030000','0x00000000','0x1000'))
        # rxOnTiming.insert('','end',values=('regs','0x4403ffff','0x00000000','0x1000'))
        # rxOnTiming.delete(*rxOnTiming.get_children())

        # offTiming
        rxOffTiming,vbar2=treeViewBuild(rxTiming,("type","addr","value","delay"),[60,90,90,90],["Off type","addr","value","delay"])
        rxOffTiming.configure(height=4)
        rxOffTiming.grid(column=0, row=1,padx=5)
        rxOffTiming.bind("<Double-1>",lambda x:rxOnParasUpdata(x,rxOffTiming,rxRegsInfo))
        vbar2.grid(column=1, row=1,sticky=NS)
        # RegsParas
        rxParas = LabelFrame(rxTab,text=' RegsInfo ')
        rxRegsInfo,vbar3=treeViewBuild(rxParas,("BITS","FIELD","VALUE","DESCRIPTION"),[60,150,60,400],["BITS","FIELD","VALUE","DESCRIPTION"])
        rxRegsInfo.configure(height=4)
        rxRegsInfo.grid(column=0,row=0,padx=5,pady=5)
        vbar3.grid(column=1, row=0,sticky=NS)

        #info
        rxInfo = LabelFrame(rxTab,text=' Info ')
        Label(rxInfo,text=' ADC_Vpp(V): ').grid(column=0, row=0,sticky='W')
        adc_vpp=StringVar()
        adc_vpp.set(3.6)
        adcVpp = Entry(rxInfo,width=6,textvariable=adc_vpp).grid(column=1,row=0,sticky='E')
        Label(rxInfo,text=' ADC_Sample:').grid(column=0, row=1,sticky='W')
        Label(rxInfo,text='7.68MHz').grid(column=1, row=1,sticky='E')
        #freqDomain
        rxFreqDomain = LabelFrame(rxTab,text=' FreqDomain ')
        Label(rxFreqDomain,text=' Max(Hz): ').grid(column=0, row=0)
        rxFreqMax = Label(rxFreqDomain,text=' 0 ').grid(column=1, row=0)
        #TimeDomain
        rxTimeDomain = LabelFrame(rxTab,text=' TimeDomain ')
        Label(rxTimeDomain,text=' IDC(v): ').grid(column=0, row=0,sticky='W')
        Label(rxTimeDomain,text=' QDC(v): ').grid(column=0, row=1,sticky='W')
        Label(rxTimeDomain,text=' Power:'+'\n'+'(dBm)').grid(column=0,row=2,sticky='W')
        rxTimeIdc = Label(rxTimeDomain,text=' 0 ').grid(column=1, row=0,sticky='W')
        rxTimeQdc = Label(rxTimeDomain,text=' 0 ').grid(column=1, row=1,sticky='W')
        rxTimePower = Label(rxTimeDomain,text=' 0 ').grid(column=1, row=2,sticky='W')
        #figure
        fig = Figure(figsize=(7, 3), facecolor='white')
        fig.clf()
        iqFig = fig.add_subplot(211)    # 2 rows, 1 column, top graph
        freq = fig.add_subplot(212)    # 2 rows, 1 column, bottom graph
        # i,q Time domain
        xValues = np.arange(0,2,0.01)
        iValues = np.cos(2*pi*xValues)
        qValues = np.sin(2*pi*xValues)
        # print(np.mean(iValues))
        iqFig.plot(xValues,iValues,xValues,qValues)
        iqFig.legend(['I','Q'])
        # frequency domain
        sig = [a+b for a,b in zip([x*1j for x in qValues],iValues)]
        SIG = np.fft.fft(sig)
        # print(abs(SIG[2]))
        freq.plot(np.arange(0,2,0.01),SIG)
        fig_Canvas = FigureCanvasTkAgg(fig,master=rxTab)
        fig_Canvas.show()
        # rxTab grid        
        rxTiming.grid(column=0,row=0,sticky='WESN',padx=10,pady=10)
        rxParas.grid(column=0,row=1,columnspan=2,sticky='WESN',padx=10)
        fig_Canvas.get_tk_widget().grid(column=1,columnspan=4,row=0,sticky='WSEN',padx=10,pady=10)
        rxInfo.grid(column=2,row=1,sticky='WSEN')
        rxTimeDomain.grid(column=3,row=1,sticky='WSEN')
        rxFreqDomain.grid(column=4,row=1,sticky='WSEN')
        
        # tx Tab
        txTiming = LabelFrame(txTab,text=' Timing ')
        # OnTiming
        txOnTiming,txVbar1=treeViewBuild(txTiming,("type","addr","value","delay"),[60,90,90,90],["On type","addr","value","delay"])
        txOnTiming.configure(height=6)
        txOnTiming.grid(column=0, row=0,padx=5,pady=5)
        txOnTiming.bind("<Double-1>",lambda x:rxOnParasUpdata(x,txOnTiming,txRegsInfo))
        txVbar1.grid(column=1, row=0,sticky=NS)
        # txOnTiming.insert('',1,values=('regs','0x44030000','0x00000000','0x1000'))
        # offTiming
        txOffTiming,txVbar2=treeViewBuild(txTiming,("type","addr","value","delay"),[60,90,90,90],["Off type","addr","value","delay"])
        txOffTiming.configure(height=4)
        txOffTiming.grid(column=0, row=1,padx=5)
        txOffTiming.bind("<Double-1>",lambda x:rxOnParasUpdata(x,txOffTiming,txRegsInfo))
        txVbar2.grid(column=1, row=1,sticky=NS)
        # RegsParas
        txParas = LabelFrame(txTab,text=' Paras ')
        txRegsInfo,txVbar3=treeViewBuild(txParas,("BITS","FIELD","VALUE","DESCRIPTION"),[60,150,60,400],["BITS","FIELD","VALUE","DESCRIPTION"])
        txRegsInfo.configure(height=4)
        txRegsInfo.grid(column=0,row=0,padx=5,pady=5)
        txVbar3.grid(column=1, row=0,sticky=NS)
        txTiming.grid(column=0,row=0,sticky='WESN',padx=10,pady=10)
        txParas.grid(column=0,row=1,sticky='WESN',padx=10)

        # Mapping
        gpioMap,vbar4=treeViewBuild(fecTab,("FEC ID","Func"),[100,200],["GPIO ID","Func"])
        gpioMap.configure(height=6,selectmode='browse')
        gpioMap.bind("<Button-1>",lambda x:leftKey(x,gpioMap))
        gpioMap.bind("<Double-1>",lambda x:treeViewEdit(x,gpioMap,['#2'],mapInd='gpio'))
        gpioIdList = ['FEC@0','FEC@1','FEC@2','FEC@3','FEC@4','FEC@5']
        gpioFuncList = ['PA VM1','PA VM0','PA VEN','ANT SW1','SW VEN','N/A']
        for valuesIdx in range(6):
            gpioMap.insert('','end',values=[gpioIdList[valuesIdx],gpioFuncList[valuesIdx]])

        mipiMap,vbar5=treeViewBuild(fecTab,("Func","Addr","Value"),[120,90,90],["MIPI Func","Addr","Value"])
        mipiMap.configure(height=6,selectmode='browse')
        mipiMap.bind("<Button-1>",lambda x:leftKey(x,mipiMap))
        mipiMap.bind("<Button-3>",lambda x:rightKeyAddDel(x,mipiMap,mapInd=''))
        mipiMap.bind("<KeyPress-Up>",lambda x:upDownKey(x,mipiMap,0))
        mipiMap.bind("<KeyPress-Down>",lambda x:upDownKey(x,mipiMap,1))
        mipiMap.bind("<Double-1>",lambda x:treeViewEdit(x,mipiMap,mapInd='mipi'))
        mipiMap.insert('','end',values=['N/A','N/A','N/A'])
        mipiFuncList = ['N/A']
        mipiRegsList = ['[N/A]=[N/A]']
        vbar5.grid(column=1, row=1,sticky=NS)

        auxDacMap,vbar6=treeViewBuild(fecTab,("power","DacValue"),[100,200],["AptPower","DacValue"])
        auxDacMap.configure(height=6,selectmode='browse')
        auxDacMap.bind("<Button-1>",lambda x:leftKey(x,auxDacMap))
        auxDacMap.bind("<Button-3>",lambda x:rightKeyAddDel(x,auxDacMap))
        auxDacMap.bind("<KeyPress-Up>",lambda x:upDownKey(x,auxDacMap,0))
        auxDacMap.bind("<KeyPress-Down>",lambda x:upDownKey(x,auxDacMap,1))     
        auxDacMap.bind("<Double-1>",lambda x:treeViewEdit(x,auxDacMap))
        auxDacMap.insert('','end',values=['N/A','N/A'])
        vbar6.grid(column=1, row=2,sticky=NS)

        pathCtrl = ttk.Notebook(fecTab) # Create Mapping Path control
        mapPathList,mapPathTableList,pathBandNumList = mapPathAdd(pathCtrl,'Path1')

        mapCtrl = LabelFrame(fecTab,text=' MappingCtrlPanel')
        ttk.Button(mapCtrl,text="addPath",width=12,command=lambda: mapPathAddOne(pathCtrl)).grid(column=0, row=0,padx=5,pady=5,sticky='N')
        ttk.Button(mapCtrl,text="DelPath",width=12,command=lambda: mapPathDelOne(pathCtrl)).grid(column=0, row=1,padx=5,pady=5,sticky='N')
        ttk.Button(mapCtrl,text="UpdToTiming",width=12,command=lambda: updToTimingWin(pathCtrl,pathBandNumList,mapPathTableList,timingPathWin)).grid(column=0, row=2,padx=5,pady=5,sticky='N')

        
        gpioMap.grid(column=0, row=0,padx=5,pady=5,sticky='W')
        mipiMap.grid(column=0, row=1,padx=5,pady=5,sticky='W')
        auxDacMap.grid(column=0, row=2,padx=5,pady=5,sticky='W')
        pathCtrl.grid(column=2, row=0,rowspan=3,padx=5,pady=5,sticky='WSEN')
        mapCtrl.grid(column=3, row=0,rowspan=3,padx=5,pady=5,sticky='WSEN')

        # Timing

        timingCtrl = ttk.Notebook(TimingTab) # Create Mapping Path control
        timingPathWin = timingPathAdd(timingCtrl)
        timingWinList = [[],[],[],[]]
        timingCtrlPanel = LabelFrame(TimingTab,text=' TimingCtrlPanel')
        ttk.Button(timingCtrlPanel,text="GenNvmFile",width=12,command=lambda: timing(pathCtrl)).grid(column=0, row=0,padx=5,pady=5,sticky='N')
        
        timingCtrl.grid(column=0, row=0)
        timingCtrlPanel.grid(column=1, row=0,padx=5,pady=5,sticky='WSEN')

        # ComTab
        # bandFreq
        bandFreqFrame = LabelFrame(comTab,text=' BandFreq ')
        Label(bandFreqFrame,text='Band:').grid(column=0, row=0,sticky='W',padx=5,pady=5)
        bandNumInput = StringVar()
        bandNumOutput = ttk.Combobox(bandFreqFrame,textvariable=bandNumInput,width=15)
        bandNumOutput['values'] = ('band5', 'band8')
        bandNumOutput.grid(column=1, row=0,padx=5,pady=5)
        Label(bandFreqFrame,text='FDD').grid(column=2, row=0,padx=5,pady=5)
        Label(bandFreqFrame,text='Downlink').grid(column=1, row=1,sticky='W',padx=5,pady=5)
        Label(bandFreqFrame,text='Uplink').grid(column=2, row=1,sticky='W',padx=5,pady=5)
        Label(bandFreqFrame,text='Channel:').grid(column=0, row=2,sticky='W',padx=5,pady=5)
        downlinkChannel=StringVar()
        downlinkChannel.set('300')
        Entry(bandFreqFrame,width=17,textvariable=downlinkChannel).grid(column=1, row=2,padx=5,pady=5)
        uplinkChannel=StringVar()
        uplinkChannel.set('18300')
        Entry(bandFreqFrame,width=17,textvariable=uplinkChannel).grid(column=2, row=2,padx=5,pady=5)
        Label(bandFreqFrame,text='Frequency:').grid(column=0, row=3,sticky='W',padx=5,pady=5)
        downlinkFreq=StringVar()
        downlinkFreq.set('2140.0'+' '+'MHz')
        Entry(bandFreqFrame,width=17,textvariable=downlinkFreq).grid(column=1, row=3,padx=5,pady=5)
        uplinkFreq=StringVar()
        uplinkFreq.set('1950.0'+' '+'MHz')
        Entry(bandFreqFrame,width=17,textvariable=uplinkFreq).grid(column=2, row=3,padx=5,pady=5)
        # RxGain
        rxGainFrame = LabelFrame(comTab,text=' RxGain ')
        Label(rxGainFrame,text='Lna:').grid(column=0, row=0,sticky='W',padx=5,pady=5)
        rxLnaGain=StringVar()
        rxLnaGain.set('15')
        Entry(rxGainFrame,width=10,textvariable=rxLnaGain).grid(column=1, row=0,padx=5,pady=5)
        Label(rxGainFrame,text='LnaTune:').grid(column=2, row=0,sticky='W',padx=5,pady=5)
        rxLnaGainTune=StringVar()
        rxLnaGainTune.set('0')
        rxLnaTune = ttk.Combobox(rxGainFrame,textvariable=rxLnaGainTune,width=8)
        rxLnaTune['values'] = ('0', '1')
        rxLnaTune.grid(column=3, row=0,padx=5,pady=5)
        Label(rxGainFrame,text='TIA:').grid(column=0, row=1,sticky='W',padx=5,pady=5)
        rxTiaGain=StringVar()
        rxTiaGain.set('1')
        Entry(rxGainFrame,width=10,textvariable=rxTiaGain).grid(column=1, row=1,padx=5,pady=5)
        Label(rxGainFrame,text='TiaFbGap:').grid(column=2, row=1,sticky='W',padx=5,pady=5)
        rxTiaFbCap=StringVar()
        rxTiaFbCap.set('15')
        Entry(rxGainFrame,width=10,textvariable=rxTiaFbCap).grid(column=3, row=1,padx=5,pady=5)
        Label(rxGainFrame,text='Mixer:').grid(column=0, row=2,sticky='W',padx=5,pady=5)
        rxMixerGain=StringVar()
        rxMixerGain.set('7')
        Entry(rxGainFrame,width=10,textvariable=rxMixerGain).grid(column=1, row=2,padx=5,pady=5)
        Label(rxGainFrame,text='rfBBGain:').grid(column=2, row=2,sticky='W',padx=5,pady=5)
        rxBBGain=StringVar()
        rxBBGain.set('8')
        Entry(rxGainFrame,width=10,textvariable=rxBBGain).grid(column=3, row=2,padx=5,pady=5)
        # TxApc
        txPowerFrame = LabelFrame(comTab,text=' TxPower ')
        Label(txPowerFrame,text='txFilt:').grid(column=0, row=0,sticky='W',padx=5,pady=5)
        txFiltGain=StringVar()
        txFiltGain.set('0')
        Entry(txPowerFrame,width=10,textvariable=txFiltGain).grid(column=1, row=0,padx=5,pady=5)
        Label(txPowerFrame,text='Upc:').grid(column=0, row=1,sticky='W',padx=5,pady=5)
        txUpcGain=StringVar()
        txUpcGain.set('2')
        Entry(txPowerFrame,width=10,textvariable=txUpcGain).grid(column=1, row=1,padx=5,pady=5)
        Label(txPowerFrame,text='PaDriver:').grid(column=0, row=2,sticky='W',padx=5,pady=5)
        txPadrGain=StringVar()
        txPadrGain.set('15')
        Entry(txPowerFrame,width=10,textvariable=txPadrGain).grid(column=1, row=2,padx=5,pady=5)
        # Regs
        regsFrame = LabelFrame(comTab,text=' RegsWrRd ')
        Label(regsFrame,text='Wr:').grid(column=0, row=0,sticky='W',padx=5,pady=5)
        regsWrAddr=StringVar()
        regsWrAddr.set('0x44030000')
        Entry(regsFrame,width=12,textvariable=regsWrAddr).grid(column=1, row=0,padx=5,pady=5)
        regsWrvalue=StringVar()
        regsWrvalue.set('0x00000000')
        Entry(regsFrame,width=12,textvariable=regsWrvalue).grid(column=2, row=0,padx=5,pady=5)
        Label(regsFrame,text='Rd:').grid(column=0, row=1,sticky='W',padx=5,pady=5)
        regsRdAddr=StringVar()
        regsRdAddr.set('0x44030000')
        Entry(regsFrame,width=12,textvariable=regsRdAddr).grid(column=1, row=1,padx=5,pady=5)
        regsRdvalue=StringVar()
        regsRdvalue.set('0x00000000')
        regRdWin = Entry(regsFrame,width=12,textvariable=regsRdvalue,state='disabled').grid(column=2, row=1,padx=5,pady=5)
        ttk.Button(regsFrame,text="Write",command=lambda: regsSend(regsWrAddr.get(),regsWrvalue.get(),'wr',RegsRecord)).grid(column=0,columnspan=2,row=2,padx=5,pady=5,sticky='WSEN')
        ttk.Button(regsFrame,text="Read",command=lambda: regsSend(regsRdAddr.get(),regsRdvalue,'rd',RegsRecord)).grid(column=2,row=2,padx=5,pady=5,sticky='WSEN')
        ttk.Button(regsFrame,text="ClearRegsRecord",command=lambda: clearRegsRecord([RegsRecord,RegsRecordInfo])).grid(column=0,columnspan=3,row=3,padx=5,pady=5,sticky='WSEN')
        #RegsRecord
        regsRecordFrame = LabelFrame(comTab,text=' RegsRecord ')
        RegsRecord,regRecordVbar3=treeViewBuild(regsRecordFrame,("a","b","c"),[80,120,120],["Write/Read","Addr","VALUE"])
        RegsRecord.configure(height=12)
        RegsRecord.bind("<Double-1>",lambda x:rxOnParasUpdata(x,RegsRecord,RegsRecordInfo,mapInd='regsRecord'))
        RegsRecordInfo,regRecordInfoVbar3=treeViewBuild(regsRecordFrame,("BITS","FIELD","VALUE","DESCRIPTION"),[60,150,60,400],["BITS","FIELD","VALUE","DESCRIPTION"])
        RegsRecordInfo.configure(height=12)
        RegsRecord.grid(column=0,row=0,padx=5,pady=5)
        regRecordVbar3.grid(column=1,row=0,padx=5,pady=5,sticky=NS)
        RegsRecordInfo.grid(column=2,columnspan=3,row=0,pady=5)
        regRecordInfoVbar3.grid(column=5,columnspan=3,row=0,pady=5,sticky=NS)

        bandFreqFrame.grid(column=0, row=0,padx=5,pady=5,sticky='WSEN')
        rxGainFrame.grid(column=1, row=0,padx=5,pady=5,sticky='WSEN')
        txPowerFrame.grid(column=2, row=0,padx=5,pady=5,sticky='WSEN')
        regsFrame.grid(column=3, columnspan=2,row=0,padx=5,pady=5,sticky='WSEN')
        regsRecordFrame.grid(column=0, columnspan=4,row=1,padx=5,pady=5,sticky='WSEN')

        # grid
        # uartPanel.grid(column=0, row=0,padx=10,sticky='WNE')
        ctrlPanel.grid(column=0, row=0,padx=10,pady=10,ipady=10,sticky='WSEN')
        statusPanel.grid(column=0,columnspan=2, row=1,padx=10,sticky='WESN')
        tabControl.grid(column=1, row=0,sticky='WNE')
        
        # global
        global_val.set('statePanl',statusPanel)
        global_val.set('rxOnTiming',rxOnTiming)
        global_val.set('rxOffTiming',rxOffTiming)
        global_val.set('txOnTiming',txOnTiming)
        global_val.set('txOffTiming',txOffTiming)
        global_val.set('rxRegsInfo',rxRegsInfo)
        global_val.set('txRegsInfo',txRegsInfo)
        # global_val.set('gpioMap',gpioMap)
        # global_val.set('mipiMap',mipiMap)
        # global_val.set('auxDacMap',auxDacMap)
        global_val.set('mapPathList',mapPathList)
        global_val.set('mapPathTableList',mapPathTableList)
        global_val.set('fig',fig)
        global_val.set('fig_Canvas',fig_Canvas)
        global_val.set('adc_vpp',adc_vpp)
        global_val.set('rxTimeIdc',rxTimeIdc)
        global_val.set('rxTimeQdc',rxTimeQdc)
        global_val.set('rxTimePower',rxTimePower)
        global_val.set('rxFreqMax',rxFreqMax)
        global_val.set('regFilesInfo', [])
        global_val.set('debugFlag','FALSE')
        global_val.set('gpioFuncList',gpioFuncList)
        global_val.set('mipiFuncList',mipiFuncList)
        global_val.set('mipiRegsList',mipiRegsList)
        global_val.set('timingWinList',timingWinList)
        global_val.set('RegsRecord',RegsRecord)
        

def quit():
    RxOnFlag = 0
    global_val.set('RxOnFlag', RxOnFlag)
    app.master.destroy()

def upTxState(state):
    statePanl = global_val.get('statePanl')
    statePanl.winfo_children()[1].configure(text=state)

def upRxState(state):
    statePanl = global_val.get('statePanl')
    statePanl.winfo_children()[3].configure(text=state)

def upUartState(state):
    statePanl = global_val.get('statePanl')
    statePanl.winfo_children()[5].configure(text=state)

def rxOnParasUpdata(event,timingWin,regsWin,mapInd=''):
    regsWin.delete(*regsWin.get_children())

    if mapInd == '':
        if len(timingWin.item(timingWin.selection(),option='values')) != 0:
            if timingWin.item(timingWin.selection(),option='values')[0] == 'regs':
                regsInfoUpdate(regsWin,timingWin.item(timingWin.selection(),option='values')[1],timingWin.item(timingWin.selection(),option='values')[2])
    else:
        if len(timingWin.item(timingWin.selection(),option='values')) != 0:
            regsInfoUpdate(regsWin,timingWin.item(timingWin.selection(),option='values')[1],timingWin.item(timingWin.selection(),option='values')[2])


def regsInfoUpdate(regsWin,regAddr,regValue):

    tempRegAddr = hex(int(regAddr,16))

    regFilesInfo = global_val.get('regFilesInfo')

    for fileIdx in range(len(regFilesInfo)):
        filePath = regFilesInfo[fileIdx][0]
        for sheetIdx in range(len(regFilesInfo[fileIdx][1])):
            if regFilesInfo[fileIdx][2][sheetIdx].get(tempRegAddr,-1) != -1:
                rowNum = regFilesInfo[fileIdx][2][sheetIdx].get(tempRegAddr)
                rowBegin = False
                for rowIdx in range(40):
                    rowValue = excelLoad.excelRowsRead(filePath,sheetIdx,rowNum+rowIdx)

                    # find regs Header
                    if rowBegin == True:
                        if type(rowValue[0]) == float or type(rowValue[0]) == int:
                            column1stValueLow = int(rowValue[0])
                            column1st = int(rowValue[0])
                            bitsValue = hex((int(regValue,16)>>column1stValueLow) & 0x1)
                        elif type(rowValue[0]) == str:
                            if rowValue[0].find(':') != -1:
                                column1stValueHigh = int(rowValue[0].split(':',1)[0]) 
                                column1stValueLow = int(rowValue[0].split(':',1)[1])
                                bitsValue = hex((int(regValue,16) >> column1stValueLow) & ((2**(column1stValueHigh-column1stValueLow+1))-1))
                            else:
                                column1stValueLow = int(rowValue[0])
                                bitsValue = hex((int(regValue,16)>>column1stValueLow) & 0x1)
                            column1st = rowValue[0]
                        else:
                            break

                        regsWin.insert('','end',value=(column1st,rowValue[1],bitsValue,rowValue[5]))

                        # end
                        if column1stValueLow == 0:
                            break
                        else:
                            continue

                    if rowValue[0] == 'BITS':
                        rowBegin = True
                        continue
                    else:
                        continue

def treeViewBuild(frameP,columnsList,widthList,headingList):
    vbar = ttk.Scrollbar(frameP,orient=VERTICAL)
    tempTree = ttk.Treeview(frameP,columns=columnsList,show="headings",yscrollcommand=vbar.set)
    vbar.configure(command=tempTree.yview)
    for i in range(len(columnsList)):
        tempTree.column(columnsList[i],width=widthList[i],anchor='center')
        tempTree.heading(columnsList[i],text=headingList[i])
    
    return tempTree,vbar

def upDownKey(keyword,winMap,upDown):
    pass

def leftKey(event,winMap):
    if global_val.get('testEntry') != None:
        global_val.get('testEntry').destroy()

def rightKeyAddDel(event,winMap,mapInd=''):
    rowId = winMap.identify_row(event.y)
    winMap.focus(rowId)
    context_menu = Menu(winMap,tearoff=0)
    if mapInd == '':
        context_menu.add_command(label="add",command=lambda: treeViewAddOne(winMap,event,mapInd))
        context_menu.add_command(label="del",command=lambda: treeViewDelOne(winMap,event,mapInd))
        context_menu.add_command(label="up",command=lambda: treeViewUpDownOne(winMap,0,mapInd))
        context_menu.add_command(label="down",command=lambda: treeViewUpDownOne(winMap,1,mapInd))
    elif mapInd == 'timing':
        context_menu.add_command(label="up",command=lambda: treeViewUpDownOne(winMap,0,mapInd))
        context_menu.add_command(label="down",command=lambda: treeViewUpDownOne(winMap,1,mapInd))
    context_menu.post(event.x_root,event.y_root)


def treeViewAddOne(winMap,event,mapInd=''):

    rowId = winMap.identify_row(event.y)
    columnId = winMap.identify_column(event.x)

    # 1st row must be at here.
    if winMap.get_children():
        columnNum = len(winMap.item(winMap.get_children()[0],option='values'))

        tempStr = []
        for idx in range(columnNum):
            tempStr.append('N/A')

        if rowId == '':
            winMap.insert('','end',values=tempStr)
        else:
            winMap.insert('',winMap.index(rowId)+1,values=tempStr)

        if mapInd == 'mipi':
            mipiFuncList = global_val.get('mipiFuncList')
            mipiFuncList.append('N/A')
            mipiRegsList = global_val.get('mipiRegsList')
            mipiRegsList.append('[N/A]=[N/A]')

def treeViewDelOne(winMap,event,mapInd=''):

    rowId = winMap.identify_row(event.y)
    
    if rowId != '':
        # onlu delete the focus item.
        tempRowIdx = int(rowId.split('I',1)[1],16)-1
        if len(winMap.get_children()) > 1:
            if mapInd == 'mipi':
                mipiFuncList = global_val.get('mipiFuncList')
                mipiRegsList = global_val.get('mipiRegsList')
                del mipiFuncList[tempRowIdx]
                del mipiRegsList[tempRowIdx]
            winMap.delete(winMap.focus())

def treeViewUpDownOne(winMap,upDown,mapInd=''):
    items = winMap.selection()
    for idx in items:
        if upDown == 0:
            winMap.move(idx,winMap.parent(idx),winMap.index(idx)-1)
        else:
            winMap.move(idx,winMap.parent(idx),winMap.index(idx)+1)


def treeViewEdit(event,winMap,editColumnIdx=[],inputWinType='Entry',mapInd=''):
    
    if global_val.get('testEntry') != None:
        global_val.get('testEntry').destroy()

    rowId = winMap.identify_row(event.y)
    columnId = winMap.identify_column(event.x)

    treeViewUpdInfo = [winMap,columnId,mapInd,rowId]
    global_val.set('treeViewUpdInfo',treeViewUpdInfo)
    
    if rowId != '':
        updateColumn = False
        if editColumnIdx == []:
            updateColumn = True
        
        for idx in range(len(editColumnIdx)):
            if columnId == editColumnIdx[idx]:
                updateColumn = True
                break

        if updateColumn == True:
            x,y,width,height = winMap.bbox(rowId,columnId)
            if inputWinType == 'Entry':
                testEntry = stickyEntry.StickyEntry(winMap, winMap.item(winMap.selection(),option='values')[int(columnId.split('#',1)[1])-1])
                testEntry.place(x=x, y=y,height=height-0.5,width=width+1)
            else: # Mapping Path
                tempValue = StringVar()
                testEntry = ttk.Combobox(winMap,textvariable=tempValue)
                testEntry.insert(0,winMap.item(winMap.selection(),option='values')[int(columnId.split('#',1)[1])-1])
                comboBoxList = mapPath1BoxListGet(winMap,columnId)
                testEntry.config(values=comboBoxList)
                testEntry.focus()
                testEntry.place(x=x, y=y,height=height-0.5,width=width+1)
                testEntry.bind("<Escape>", lambda x: testEntry.destroy())
                testEntry.bind("<<ComboboxSelected>>", lambda x:comboxMapUpd(testEntry,tempValue.get(),columnId))
            global_val.set('testEntry',testEntry)
        

def comboxMapUpd(winMap,function,columnId):
    treeViewMapUpd(function)
    if columnId == '#3':
        mipiFuncList = global_val.get('mipiFuncList')
        tempFuncList = global_val.get('mipiRegsList')
        try:
            mapPathWinUpd('mipiRegsList','',tempFuncList[mipiFuncList.index(function)],function)
        except:
            pass
    winMap.destroy()

def treeViewMapUpd(function):
    treeViewUpdInfo = global_val.get('treeViewUpdInfo')

    if function != '':
        tempList = []
        for editIdx in range(len(treeViewUpdInfo[0].item(treeViewUpdInfo[0].selection(),option='values'))):
            if editIdx != (int(treeViewUpdInfo[1].split('#',1)[1]) - 1):
                tempList.append(treeViewUpdInfo[0].item(treeViewUpdInfo[0].selection(),option='values')[editIdx])
            else:
                lastColumnValue = treeViewUpdInfo[0].item(treeViewUpdInfo[0].selection(),option='values')[editIdx]
                tempList.append(function)
        
        treeViewUpdInfo[0].item(treeViewUpdInfo[0].selection(),values=tempList)

        mapInd = treeViewUpdInfo[2]
        columnId = treeViewUpdInfo[1]
        winMap = treeViewUpdInfo[0]
        tempRowId = treeViewUpdInfo[3]
        rowIdx = int(tempRowId.split('I',1)[1],16)
        if (function != 'N/A') and mapInd != '':
            if mapInd == 'gpio':
                tempFuncList = global_val.get('gpioFuncList')
                eventFlag = 'gpioFunc'
                newText = function
                if tempFuncList[rowIdx-1] != newText:
                    mapPathWinUpd(eventFlag,tempFuncList[rowIdx-1],newText)
                    tempFuncList[rowIdx-1] = newText
            elif mapInd == 'mipi':
                if  (columnId == '#1'):
                    tempFuncList = global_val.get('mipiFuncList')
                    eventFlag = 'mipiFunc'
                    newText = function
                elif (columnId == '#2') or (columnId == '#3'):
                    tempFuncList = global_val.get('mipiRegsList')
                    tempMipiRegsAddr = winMap.item(winMap.selection(),option='values')[1]
                    tempMipiRegsValue = winMap.item(winMap.selection(),option='values')[2]
                    newText = '['+tempMipiRegsAddr+']'+'='+'['+tempMipiRegsValue+']'
                    eventFlag = 'mipiRegsList'
                if tempFuncList[rowIdx-1] != newText:
                    mipiFuncList = global_val.get('mipiFuncList')
                    mapPathWinUpd(eventFlag,tempFuncList[rowIdx-1],newText,mipiFuncList[rowIdx-1])
                    tempFuncList[rowIdx-1] = newText

def mapPathAddOne(parent):
    pass

def regsSend(addr,value,wrRdFlag,winMap):

    if (addr.find('0x') == -1):
        global_val.errorEntry(r'regs address must be included 0x!')
    
    specialFlag = addrSpecialFlagGet(addr,wrRdFlag)

    if wrRdFlag == 'wr':

        if (value.find('0x') == -1):
            tempValue = hex(int(value))
        else:
            tempValue = value

        tempStr = '0007' + specialFlag + scriptCmd.zeroAlignment(addr.split('x',1)[1]) + scriptCmd.zeroAlignment(tempValue.split('x',1)[1]) # direct writ Reg
        dataStr,data_len = scriptCmd.writeToL1(tempStr)
        if dataStr[0:2] == 'ok':
            winMap.insert('','end',values=['write',hex(int(addr,16)),hex(int(tempValue,16))])
    else:# read

        tempStr = '0007' + specialFlag + scriptCmd.zeroAlignment(addr.split('x',1)[1]) + '00000000' # direct writ Reg

        dataStr,data_len = scriptCmd.writeToL1(tempStr)
        tempStr = scriptCmd.strReverse(dataStr)
        if data_len != 0:
            value.set('0x'+tempStr)
            winMap.insert('','end',values=['read',hex(int(addr,16)),'0x'+tempStr])

def clearRegsRecord(winMapList):
    for winId in winMapList:
        winId.delete(*winId.get_children())

def addrSpecialFlagGet(addr,wrRdFlag='wr'):

    if ((int(addr,16) >= int(0x47FC0000)
    and (int(addr,16) < int(0x47FD0000))) == True # RF Seq regs
    or (int(addr,16) >= int(0x46001000)
    and (int(addr,16) < int(0x46002000))) == True): # modem seq regs
        if wrRdFlag == 'wr':
            return '01'
        else:
            return '03'
    else:
        if wrRdFlag == 'wr':
            return '00'
        else:
            return '02'

def mapPathDelOne(parent):
    pass

def mapPathAdd(parent,text='Path1'):
    path1 = ttk.Frame(parent)
    parent.add(path1,text=text)
    Label(path1,text=' BandNum: ').grid(column=0, row=0,padx=5,pady=5)
    path1BandNum=StringVar()
    path1BandNum.set('5,8')
    Entry(path1,width=75,textvariable=path1BandNum).grid(column=1,row=0,sticky='E')
    pathMapping,vbar1=treeViewBuild(path1,("a","b","c","d"),[50,100,100,50],["Element","Mode","Func","Value"])
    pathMapping.configure(height=18,selectmode='browse')
    pathMapping.bind("<Button-3>",lambda x:rightKeyAddDel(x,pathMapping))
    pathMapping.bind("<KeyPress-Up>",lambda x:upDownKey(x,pathMapping,0))
    pathMapping.bind("<KeyPress-Down>",lambda x:upDownKey(x,pathMapping,1))
    pathMapping.bind("<Button-1>",lambda x:leftKey(x,pathMapping))
    pathMapping.bind("<Double-1>",lambda x:treeViewEdit(x,pathMapping,[],'Combobox'))
    pathMapping.insert('','end',values=["AntSw","Rx","ANT SW1","L"])
    pathMapping.insert('','end',values=["AntSw","Tx","ANT SW1","H"])
    pathMapping.insert('','end',values=["PA","TxOn","PA VEN","H"])
    pathMapping.insert('','end',values=["PA","TxOn","SW VEN","H"])
    pathMapping.insert('','end',values=["PA","TxOff","PA VEN","L"])
    pathMapping.insert('','end',values=["PA","TxOff","SW VEN","L"])
    pathMapping.insert('','end',values=["PA","HighGain","PA VM1","L"])
    pathMapping.insert('','end',values=["PA","HighGain","PA VM0","L"])
    pathMapping.insert('','end',values=["PA","MiddleGain","PA VM1","L"])
    pathMapping.insert('','end',values=["PA","MiddleGain","PA VM0","H"])
    pathMapping.insert('','end',values=["PA","LowGain","PA VM1","H"])
    pathMapping.insert('','end',values=["PA","LowGain","PA VM0","H"])
    pathMapping.grid(column=0,columnspan=2,row=1,sticky='WSNE')
    vbar1.grid(column=2, row=1,sticky=NS)
    return [path1],[pathMapping],[path1BandNum]

def timingPathAdd(parent,text='Path1'):

    path = ttk.Frame(parent)
    parent.add(path,text=text)

    Label(path,text=' BandNum: ').grid(column=0, row=0,padx=5,pady=5,sticky='W')
    bandLabel = Label(path,text=' 5,8 ')
    bandLabel.grid(column=1, row=0,padx=5,pady=5,sticky='W')

    rxOnTiming,vbar_1=treeViewBuild(path,("a","b","c"),[150,150,150],['RxOn'+' Func',"Value","Delay(us) SumAll<=10us"])
    rxOnTiming.configure(height=9,selectmode='browse')
    rxOnTiming.bind("<Button-1>",lambda x:leftKey(x,rxOnTiming))
    rxOnTiming.bind("<Button-3>",lambda x:rightKeyAddDel(x,rxOnTiming,mapInd='timing'))
    rxOnTiming.bind("<KeyPress-Up>",lambda x:upDownKey(x,rxOnTiming,0))
    rxOnTiming.bind("<KeyPress-Down>",lambda x:upDownKey(x,rxOnTiming,1))
    rxOnTiming.bind("<Double-1>",lambda x:treeViewEdit(x,rxOnTiming,editColumnIdx=['#3'],mapInd='rxOnTiming'))
    vbar_1.grid(column=2, row=1,sticky=NS)

    rxOffTiming,vbar_2=treeViewBuild(path,("a","b","c"),[150,150,150],['RxOff'+' Func',"Value","Delay(us)"])
    rxOffTiming.configure(height=9,selectmode='browse')
    rxOffTiming.bind("<Button-1>",lambda x:leftKey(x,rxOffTiming))
    rxOffTiming.bind("<KeyPress-Up>",lambda x:upDownKey(x,rxOffTiming,0))
    rxOffTiming.bind("<KeyPress-Down>",lambda x:upDownKey(x,rxOffTiming,1))
    rxOffTiming.bind("<Button-3>",lambda x:rightKeyAddDel(x,rxOffTiming,mapInd='timing'))
    rxOffTiming.bind("<Double-1>",lambda x:treeViewEdit(x,rxOffTiming,editColumnIdx=['#3'],mapInd='rxOffTiming'))
    vbar_2.grid(column=1, row=2,sticky=NS)

    txOnTiming,vbar_3=treeViewBuild(path,("a","b","c"),[150,150,150],['TxOn'+' Func',"Value","Delay(us) SumAll<=5us"])
    txOnTiming.configure(height=9,selectmode='browse')
    txOnTiming.bind("<Button-1>",lambda x:leftKey(x,txOnTiming))
    txOnTiming.bind("<KeyPress-Up>",lambda x:upDownKey(x,txOnTiming,0))
    txOnTiming.bind("<KeyPress-Down>",lambda x:upDownKey(x,txOnTiming,1))
    txOnTiming.bind("<Button-3>",lambda x:rightKeyAddDel(x,txOnTiming,mapInd='timing'))
    txOnTiming.bind("<Double-1>",lambda x:treeViewEdit(x,txOnTiming,editColumnIdx=['#3'],mapInd='txOnTiming'))
    vbar_3.grid(column=4, row=1,sticky=NS)

    txOffTiming,vbar_4=treeViewBuild(path,("a","b","c"),[150,150,150],['TxOff'+' Func',"Value","Delay(us)"])
    txOffTiming.configure(height=9,selectmode='browse')
    txOffTiming.bind("<Button-1>",lambda x:leftKey(x,txOffTiming))
    txOffTiming.bind("<KeyPress-Up>",lambda x:upDownKey(x,txOffTiming,0))
    txOffTiming.bind("<KeyPress-Down>",lambda x:upDownKey(x,txOffTiming,1))
    txOffTiming.bind("<Button-3>",lambda x:rightKeyAddDel(x,txOffTiming,mapInd='timing'))
    txOffTiming.bind("<Double-1>",lambda x:treeViewEdit(x,txOffTiming,editColumnIdx=['#3'],mapInd='txOffTiming'))
    vbar_4.grid(column=4, row=2,sticky=NS)

    rxOnTiming.grid(column=0, columnspan=2,row=1,padx=5,pady=5,sticky='W')
    rxOffTiming.grid(column=0, columnspan=2, row=2,padx=5,pady=5,sticky='W')
    txOnTiming.grid(column=3, row=1,padx=5,pady=5,sticky='W')
    txOffTiming.grid(column=3, row=2,padx=5,pady=5,sticky='W')

    return [rxOnTiming,rxOffTiming,txOnTiming,txOffTiming,bandLabel]

# this function is used to updated mapPath Windows.
def mapPathWinUpd(event,prevText,newText,mipiFunc=''):
    mapPathTableList = global_val.get('mapPathTableList')
    for tableIdx in range(len(mapPathTableList)):
        for child in mapPathTableList[tableIdx].get_children():
            # get current rowId value
            tempValue = []
            for columnIdx in range(len(mapPathTableList[tableIdx].item(child,option='values'))):
                tempValue.append(mapPathTableList[tableIdx].item(child,option='values')[columnIdx])

            if event == 'gpioFunc' or event == 'mipiFunc':
                if tempValue[2] == prevText:
                    tempValue[2] = newText
            elif event == 'mipiRegsList':
                if tempValue[2] == mipiFunc:
                    tempValue[3] = newText

            mapPathTableList[tableIdx].item(child,values=tempValue)

def mapPath1BoxListGet(winMap,columnIdx):

    if columnIdx == '#3':
        gpioFuncList = global_val.get('gpioFuncList')
        mipiFuncList = global_val.get('mipiFuncList')

        return [x for x in gpioFuncList+mipiFuncList if x!='N/A' and x!='']
    elif columnIdx == '#4':
        gpioFuncList = global_val.get('gpioFuncList')
        mipiFuncList = global_val.get('mipiFuncList')
        try:
            gpioFuncList.index(winMap.item(winMap.selection(),option='values')[2])
            return ['L','H']
        except ValueError as e:
            try:
                idx = mipiFuncList.index(winMap.item(winMap.selection(),option='values')[2])
                mipiRegsList = global_val.get('mipiRegsList')
                return  mipiRegsList[idx]
            except:
                return ['N/A']
    elif columnIdx == '#1':
        eleList = element.get()
        return eleList[0]
    elif columnIdx == '#2':
        eleList = element.get()
        modeIdx = eleList[0].index(winMap.item(winMap.selection(),option='values')[0])        
        return eleList[1][modeIdx]

def updToTimingWin(pathParant,pathBandNumList,tableWinList,timingWinList):

    eleList = element.get()

    # clear Timing Win
    # for winId in range(4):
    #     timingWinList[winId].delete(*timingWinList[winId].get_children())

    for tableIdx in range(len(tableWinList)):

        # firstly update BandNum to timingWin
        bandNum = pathBandNumList[tableIdx].get()
        timingWinList[4].config(text=bandNum)

        # secondly update Timing to windows.
        mappingPathFuncList = []
        for child in tableWinList[tableIdx].get_children():
            # get current rowId value
            tempValue = []
            for columnIdx in range(len(tableWinList[tableIdx].item(child,option='values'))):
                tempValue.append(tableWinList[tableIdx].item(child,option='values')[columnIdx])

            mappingPathFuncList.append(tempValue)

        # thirdly add the new one to timing win:
        for funcList in range(len(mappingPathFuncList)):
            try:
                element_id,mode_id,func,value = mappingPathFuncList[funcList][0],mappingPathFuncList[funcList][1],mappingPathFuncList[funcList][2],mappingPathFuncList[funcList][3]
                ele_idx = eleList[0].index(element_id)
                modeIdx = eleList[1][ele_idx].index(mode_id)
                timingPro = eleList[2][ele_idx][modeIdx]
            except ValueError as e:
                global_val.errorEntry('Element Mode Func Setting Error')

            timingIdList = [0,0,0,0]
            if timingPro.find(',') == -1: # only one Timing property
                if timingPro == 'RxOn':
                    timingIdList[0] = 1
                elif timingPro == 'RxOff':
                    timingIdList[1] = 1
                elif timingPro == 'TxOn':
                    timingIdList[2] = 1
                elif timingPro == 'TxOff':
                    timingIdList[3] = 1    
            else:
                for idx in range(timingPro.count(',')+1):
                    tempStr = timingPro.split(',',timingPro.count(','))[idx]

                    if tempStr == 'RxOn':
                        timingIdList[0] = 1
                    elif tempStr == 'RxOff':
                        timingIdList[1] = 1
                    elif tempStr == 'TxOn':
                        timingIdList[2] = 1
                    elif tempStr == 'TxOff':
                        timingIdList[3] = 1  

            for idx in range(len(timingIdList)):
                if timingIdList[idx] == 1:
                    timingWinInsertFlag=True
                    for child in timingWinList[idx].get_children():
                        if timingWinList[idx].item(child,option='values')[0] == func:
                            timingWinInsertFlag = False
                    if timingWinInsertFlag==True:
                        timingWinList[idx].insert('','end',values=[func,value,'0'])

        #lastly, remove non-exist func:
        for idx in range(4):# 4 windows
            for child in timingWinList[idx].get_children():
                removeFlag=True    
                for funcList in range(len(mappingPathFuncList)):
                    if mappingPathFuncList[funcList][2] == timingWinList[idx].item(child,option='values')[0]:
                        removeFlag = False
                        break

                if removeFlag==True:
                    timingWinList[idx].delete(child)

if __name__ == '__main__':
    global_val._init()
    app = EigenCommRfTest()
    app.appOpen()
    app.master.protocol('WM_DELETE_WINDOW', quit)
    app.master.title('EigenComm RF MappingTimingFunction Tool      Version:1.00.00')
    # app.master.iconbitmap('rfTest.ico')
    # tmp = open("tmp.ico","wb+")
    # tmp.write(base64.b64decode(img))
    # tmp.close()
    # app.master.iconbitmap("tmp.ico")
    # os.remove("tmp.ico")

    # print(dir(app.master))
    logging.info('enter main loop')
    upTxState('Off')
    upRxState('Off')
    upUartState('Close')
    app.mainloop()


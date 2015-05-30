#!/usr/bin/env python
# -*- coding: utf-8 -*-




import threading
import time

import OpenRTM_aist
from MPTask import MPTask,GUITask
import MPComp


##
#実行順序の設定ができる実行コンテキストクラス
##
class MultipleOrderedEC(OpenRTM_aist.PeriodicExecutionContext):
  
    def __init__(self):
        OpenRTM_aist.PeriodicExecutionContext.__init__(self)
        self._rtcout = OpenRTM_aist.Manager.instance().getLogbuf("rtobject.mp_ec")
        self.prop = OpenRTM_aist.Manager.instance().getConfig()
        #print OpenRTM_aist.Manager.instance().getConfig()
        self.SetGui = "YES"
        self.FileName = "CompList.conf"
        self.SetGui = self.getProperty(self.prop, "exec_cxt.periodic.gui", self.SetGui)
        #print self.SetGui
        self.FileName = self.getProperty(self.prop, "exec_cxt.periodic.filename", self.FileName)
        #print self.FileName
        self.rs = []
        self.r_num = 0
        self._mutex_del2 = threading.RLock()
        if self.SetGui == "YES":
            self.g_task = GUITask(self)
            self.g_task.activate()

        self.nameList = []
        self.comp_t = []
    ##
    #rtc.confの設定を取得する関数
    ##
    def getProperty(self, prop, key, value):
        
        if  prop.findNode(key) != None:
            #print value
            value = prop.getProperty(key)
        return value
          
    ##
    #
    ##
    def Update_Name(self):
        if self.comp_t == self._comps:
            pass
        else:
            guard2 = OpenRTM_aist.ScopedLock(self._mutex_del2)
            self.comp_t = []
            self.nameList = []
            for i in range(0, len(self._comps)):
                self.comp_t.append(self._comps[i])
                self._comps[i].i_name = self._comps[i]._sm._obj.get_component_profile().instance_name
                #self.nameList.append(self._comps[i]._sm._obj.get_component_profile().instance_name)
            del guard2
    ##
    #コンポーネントの名前取得の関数
    ##
    def getCompName(self, num):
        
        self.Update_Name()
        
        
        #guard2 = OpenRTM_aist.ScopedLock(self._mutex_del2)
        #Name = self._comps[num]._sm._obj.get_component_profile().instance_name
        #del guard2
        #Name = self.nameList[num]
        Name = self._comps[num].i_name
        return Name

    ##
    #コンポーネントの数取得の関数
    ##
    def getCompNum(self):
        return len(self._comps)

    ##
    #コンポーネントのロジック実行の関数
    ##
    def workerComp(self, c):
        sd = c.r in self._comps
        if sd == True:
            
            c.r._sm.worker()
        else:
            
            for i in range(0, len(self._comps)):
                if c.v == self.getCompName(i):
                    c.r = self._comps[i]
                    self._comps[i]._sm.worker()

    ##
    #設定した実行順序のRTCを格納する関数
    ##
    def LoadRules(self):
        for h in range(0, len(self.rs)):
            for i in range(0, len(self.rs[h].ar)):
                for j in range(0, len(self._comps)):
                    
		    #Name = self._comps[j]._sm._obj.get_component_profile().instance_name
		    Name = self.getCompName(j)

                    if Name == self.rs[h].ar[i].name:
			self.rs[h].ar[i].r = self._comps[j]
			
	    for i in range(0, len(self.rs[h].rs)):
		for j in range(0, len(self.rs[h].rs[i].SR)):
		    for k in range(0, len(self.rs[h].rs[i].SR[j])):
			for l in range(0, len(self._comps)):
			    #Name = self._comps[l]._sm._obj.get_component_profile().instance_name
			    Name = self.getCompName(l)
			    if Name == self.rs[h].rs[i].SR[j][k].v:
				self.rs[h].rs[i].SR[j][k].r = self._comps[l]
	
    ##
    #GUIから実行順序の読み込みの関数
    ##
    def LoadRuleGUI(self, RS_d):
        guard = OpenRTM_aist.ScopedLock(self._mutex_del)

        self.rs = []
        self.rs = RS_d

        self.LoadRules()

        del guard
  
    ##
    #ファイルから実行順序の読み込みの関数
    ##
    def LoadRule(self):

	  
        guard = OpenRTM_aist.ScopedLock(self._mutex_del)
	
	
	
	
	for h in range(0, len(self.rs)):
	    self.rs[h].rs = []
	self.rs = []

	MPComp.LoadMainRule(self.rs, self.FileName)

	self.LoadRules()
	

	del guard

    ##
    #スレッド実行関数
    ##
    def svc(self):
        self._rtcout.RTC_TRACE("svc()")
        flag = True
        count_ = 0

        self.LoadRule()
        
    
        
        while flag:
            guard = OpenRTM_aist.ScopedLock(self._mutex_del)
            #self.LoadRules()
            self._worker._cond.acquire()
            while not self._worker._running:
                self._worker._cond.wait()

            t0_ = OpenRTM_aist.Time()

            if self._worker._running:
                
                for i in range(0, len(self.rs)):
		    S = True
		    for j in range(0, len(self.rs[i].ar)):
                        Flag = False
			for k in range(0, len(self._comps)):
			    if self.rs[i].ar[j].r == self._comps[k]:	
				if self.rs[i].ar[j].state == -1:
                                    pass
				else:
                                    if self.rs[i].ar[j].state != self._comps[k]._sm.get_state():
					S = False
                        if Flag == False:
                            for k in range(0, len(self._comps)):
                                if self.getCompName(k) == self.rs[i].ar[j].name:
                                    self.rs[i].ar[j].r = self._comps[k]
                                    if self.rs[i].ar[j].state == -1:
                                        pass
                                    else:
                                        if self.rs[i].ar[j].state != self._comps[k]._sm.get_state():
                                            S = False

		    if S == True:
                        self.r_num = i
			break
		
                if self.r_num < len(self.rs):
                    
		    for i in range(0, len(self.rs[self.r_num].rs)):
						
			if len(self.rs[self.r_num].rs[i].SR) == 0:
                            pass
			elif len(self.rs[self.r_num].rs[i].SR) == 1:
                            
			    for j in range(0, len(self.rs[self.r_num].rs[i].SR[0])):
				self.rs[self.r_num].rs[i].SR[0][j].s = 1
				sd = self.rs[self.r_num].rs[i].SR[0][j].r in self._comps
                                if sd == True:
                                    self.rs[self.r_num].rs[i].SR[0][j].r._sm.worker()
				self.rs[self.r_num].rs[i].SR[0][j].s = 0

			else:
                            
			    p_num = len(self.rs[self.r_num].rs[i].SR)
			    m_task = []
			    for j in range(0, p_num):
				m_task_s = MPTask(self)
				m_task.append(m_task_s)
				for k in range(0, len(self.rs[self.r_num].rs[i].SR[j])):
				    m_task_s.addComp(self.rs[self.r_num].rs[i].SR[j][k],i,j,k)
				m_task_s.activate()
			    for j in range(0, p_num):
				m_task[j].wait()
				m_task[j].close()
				
                
            

            self._worker._cond.release()

            del guard

            t1_ = OpenRTM_aist.Time()

            if count_ > 1000:
                exctm_ = (t1_ - t0_).getTime().toDouble()
                slptm_ = self._period.toDouble() - exctm_
                self._rtcout.RTC_PARANOID("Period:    %f [s]", self._period.toDouble())
                self._rtcout.RTC_PARANOID("Execution: %f [s]", exctm_)
                self._rtcout.RTC_PARANOID("Sleep:     %f [s]", slptm_)

            t2_ = OpenRTM_aist.Time()

            if not self._nowait and self._period.toDouble() > ((t1_ - t0_).getTime().toDouble()):
                if count_ > 1000:
                    self._rtcout.RTC_PARANOID("sleeping...")
                slptm_ = self._period.toDouble() - (t1_ - t0_).getTime().toDouble()
                time.sleep(slptm_)

            if count_ > 1000:
                t3_ = OpenRTM_aist.Time()
                self._rtcout.RTC_PARANOID("Slept:     %f [s]", (t3_ - t2_).getTime().toDouble())
                count_ = 0
            count_ += 1
            flag = self._running
        
        return 0
    

  
  

def MultipleOrderedECInit(manager):
  manager.registerECFactory("MultipleOrderedEC",
                            MultipleOrderedEC,
                            OpenRTM_aist.ECDelete)

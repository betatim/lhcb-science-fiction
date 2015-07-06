from Ganga.GPI import *
import sys
import inspect
import os
local_dir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
print local_dir



#Default for comparisons
eventTypeList = ['13104013']#,'30000000','13104012','13104013','13104015','27165100','27165103','27165175']
for eventType in eventTypeList:
    
#v47r2
#eventType = '13104011'
    if eventType == '30000000':
        Decay='MinBias'
    if eventType == '13104011':
        Decay='Bs_PhiPhi=DecProdCut'
    if eventType == '13104012':
        Decay='Bs_PhiPhi=CDFAmp_DecProdCut'
    if eventType == '13104013':
        Decay='Bs_PhiPhi=CDFAmp_DecProdCut_hpt400'
    if eventType == '13104015':
        Decay='Bs_PhiPhi=flatLT'
    if eventType == '27165100':
        Decay='Dst_D0pi_KSpipi=DecProdCut'
    if eventType == '27165103':
        Decay='Dst_D0pi_KSpipi=TightCut'
    if eventType == '27165175':
        Decay='Dst_D0pi,KSpipi=UPT,DecProdCut'
        
    print eventType,Decay
    Nevts = 2500
    j = Job(application=Gauss(
            version="v47r2",
            optsfile=[File( local_dir + "/Gauss_Option_AfterTaskForce.py")],
            #extraopts= "execute(%s)"%eventType,
            #user_release_area=local_dir + "/../cmt",
            ))
    
    j.outputfiles = [LocalFile("*.sim"),LocalFile("*.root"),LocalFile("*.xml")]
    j.name = Decay+"_Upgrade_AfterTaskForce"
    j.backend = Dirac()
    events = Nevts
    eventsperjob = 50
    j.application.extraopts = "execute("+eventType+");from Gaudi.Configuration import *;ApplicationMgr().EvtMax="+str(events)+";"               
    print j.application.extraopts 
    j.splitter = GaussSplitter(numberOfJobs=int(round(events*1.1/eventsperjob)),
                               eventsPerJob=eventsperjob)
    #j.do_auto_resubmit = True
    print j
    j.prepare()
    print j.name
    j.submit()

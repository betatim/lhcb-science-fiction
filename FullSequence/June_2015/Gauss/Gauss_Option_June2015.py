#Run this script with Gauss v47r2 to reproduce the TDR and post TaskForce used MCSample
#lb-run Gauss v47r2 gaudirun.py Option.py

#For the TDR sample we were using Gauss v46r5 but apparently there is no way to use it
from Gauss.Configuration import *
#from Gaudi.Configuration import importOptions
#Latest Gauss production : with Gauss v47r2
# Event type, e.g. 30000000 == MinBias
# You can see the full list under: $DECFILESROOT/options
import sys
import inspect
import os

#from Gauss.Configuration import *
#from Gaudi.Configuration import *
from Configurables import Gauss, LHCbApp
import GaudiKernel.SystemOfUnits as units

local_dir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
sys.path.append(local_dir)

#Option = Decay+"_"+ str(eventType) +"_Upgrade_TDRtags_Spillover25_Py8_Upgrade_HorExtAngle_7000GeV_nu7.6"
def execute(eventType=13104013):
    if(eventType == 13104011):
        Decay='Bs_PhiPhi_DecProdCut'
    if(eventType == 13104012):
        Decay='Bs_PhiPhi_CDFAmp_DecProdCut'                                                       
    if(eventType == 13104013):                                                                    
        Decay='Bs_PhiPhi_CDFAmp_DecProdCut_hpt400'                                                
    if(eventType == 13104015):                                                                    
        Decay='Bs_PhiPhi_flatLT'                                                                  
    if(eventType == 27165100):                                                                    
        Decay='Dst_D0pi_KSpipi_DecProdCut'                                                        
    if(eventType == 27165103):                                                                    
        Decay='Dst_D0pi_KSpipi_TightCut'                                                          
    if(eventType == 27165175):                                                                    
        Decay='Dst_D0pi,KSpipi_UPT_DecProdCut'  
    if(eventType == 30000000):
        Decay='MinBias'
    # Information on colliding beams: momenta, crossing angles
    # Mag up , change the md into mu
    importOptions('$APPCONFIGOPTS/Gauss/Beam7000GeV-md100-nu7.6-HorExtAngle.py')
    #Option which enables spillover
    importOptions('$APPCONFIGOPTS/Gauss/EnableSpillover-25ns.py')
    # Specific event type
    importOptions('$DECFILESROOT/options/' + str(eventType) + '.py')
    # MC generator to use - all upgrade studies are done with PYTHIA 8
    importOptions('$LBPYTHIA8ROOT/options/Pythia8.py')
    # Options which enable hadronic physics in GEANT4
    importOptions('$APPCONFIGOPTS/Gauss/G4PL_FTFP_BERT_EmNoCuts.py')
    # Necessary for TDR file generation
    importOptions('$APPCONFIGOPTS/Conditions/Upgrade.py')

    # Options to use the upgrade geometry:
    # use the upgrade database and upgrade datatype, and specify the subdetectors
    
    # Used in older version of Gauss to generate the TDR sample and TaskForce
    #importOptions('$APPCONFIGOPTS/Gauss/Gauss-Upgrade-Baseline-20131029.py')
    importOptions('$APPCONFIGOPTS/Gauss/Gauss-Upgrade-Baseline-20150522.py')
    # Output compression Level
    importOptions("$APPCONFIGOPTS/Persistency/Compression-ZLIB-1.py")
    
#########################################################################
    
    # Important bit - database tags to load the geometry of various detectors
    from Configurables import LHCbApp
    
####################################
# TDR Tags

#    LHCbApp().DDDBtag    = "dddb-20131025"
# For magnet polarity 'down'
#    LHCbApp().CondDBtag  = "sim-20130830-vc-md100"

#####################################

# Latest tags (FT v2 is modified?)
    LHCbApp().DDDBtag    = 'dddb-20150424'
    LHCbApp().CondDBtag  = 'sim-20140204-vc-md100' 

    # This is usually not needed, but right now (june 2015) there is a bug
    # which tries to search caliboff.db and fails
    from Configurables import CondDB
    CondDB().LoadCALIBDB = 'HLT1'
    OutName = Decay+"_"+ str(eventType) +"_Upgrade_June2015_Spillover25_Py8_Upgrade_HorExtAngle_7000GeV_nu76_MagDown"
##Useful option if you do not want to run full detector simulation
##with GEANT4, but only the MC generator phase
##from Gauss.Configuration import *
##Gauss().Phases = [ "Generator", "GenToMCTree" ]

## Do not use pileup - single interaction per event
##from Configurables import Generation
##Generation().PileUpTool = "FixedNInteractions"

#########################################################################
# How many events to produce
    LHCbApp().Simulation = True
    LHCbApp().EvtMax = 2500
    HistogramPersistencySvc().OutputFile = OutName+'-GaussHistos.root'
# Output file name (not really necessary)
    from Gaudi.Configuration import OutputStream
    OutputStream("GaussTape").Output="DATAFILE='PFN:"+OutName+".sim' TYP='POOL_ROOTTREE' OPT='RECREATE'"
    


###############
# Run Locally with lb-run Gauss v47r2 gaudirun.py Option.py
# EvtType List:
#eventType = 30000000
#Decay='MinBias'
#eventType = 13104011
#Decay='Bs_PhiPhi=DecProdCut'
#eventType = 13104012
#Decay='Bs_PhiPhi=CDFAmp_DecProdCut'
#eventType = 13104013
#Decay='Bs_PhiPhi=CDFAmp_DecProdCut_hpt400'
#eventType = 13104015
#Decay='Bs_PhiPhi=flatLT'
#eventType = 27165100):
#Decay='Dst_D0pi_KSpipi=DecProdCut'
#eventType = 27165103):
#Decay='Dst_D0pi_KSpipi=TightCut'
#eventType = 27165175):
#Decay='Dst_D0pi,KSpipi=UPT,DecProdCut'
#execute(eventType)

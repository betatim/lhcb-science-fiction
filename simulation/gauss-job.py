# SetupProject gauss v46r7p2
#

import sys
import inspect
import os

from Gauss.Configuration import *
#from Gaudi.Configuration import *
from Configurables import Gauss, LHCbApp
import GaudiKernel.SystemOfUnits as units

local_dir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
sys.path.append(local_dir)

from common import set_tags


def execute(evt_type=13104021, stereo=5):
  importOptions("$APPCONFIGOPTS/Gauss/Beam7000GeV-md100-nu7.6-HorExtAngle.py")
  
  importOptions("$LBPYTHIA8ROOT/options/Pythia8.py")
  importOptions("$APPCONFIGOPTS/Gauss/G4PL_FTFP_BERT_EmNoCuts.py")
  importOptions("$APPCONFIGOPTS/Conditions/Upgrade.py")
  importOptions("$APPCONFIGOPTS/Persistency/Compression-ZLIB-1.py")
  importOptions("$APPCONFIGOPTS/Gauss/Gauss-Upgrade-Baseline-20131029.py")

  outpath = "%s_%s"%("Stereo", evt_type)
  Gauss().DataType = "Upgrade"

  set_tags(stereo)

  importOptions("$DECFILESROOT/options/%s.py"%(evt_type))
  
  GaussGen = GenInit("GaussGen")
  GaussGen.FirstEventNumber = 1
  GaussGen.RunNumber = 1082

  LHCbApp().EvtMax = 10

  HistogramPersistencySvc().OutputFile = outpath+'-GaussHistos.root'

  OutputStream("GaussTape").Output = "DATAFILE='PFN:%s.sim' TYP='POOL_ROOTTREE' OPT='RECREATE'"%outpath

#execute()

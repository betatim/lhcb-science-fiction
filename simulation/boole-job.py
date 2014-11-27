# SetupProject boole v28r2

import sys
import inspect
import os

from Boole.Configuration import *
from Configurables import Boole, LHCbApp

local_dir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
sys.path.append(local_dir)

from common import set_tags

      
def execute(evt_type=None, stereo=5):
  importOptions("$APPCONFIGOPTS/Boole/Default.py")
  importOptions("$APPCONFIGOPTS/Boole/Boole-Upgrade-Baseline-20131029.py")
  #importOptions("$APPCONFIGOPTS/Boole/patchUpgrade1.py")
  importOptions("$APPCONFIGOPTS/Boole/xdigi.py")
  importOptions("$APPCONFIGOPTS/Persistency/Compression-ZLIB-1.py")

  set_tags(stereo)

  outpath = "%s_%s"%("Stereo", evt_type)
  Boole().DataType = "Upgrade"
  
  Boole().DatasetName = outpath
  HistogramPersistencySvc().OutputFile = outpath+"-BooleHistos.root"
  FileCatalog().Catalogs = ["xmlcatalog_file:"+outpath+"-BooleCatalog.xml"]

#execute()

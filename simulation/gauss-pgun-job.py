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

  outpath = "%s_%s"%("Gun", evt_type)
  Gauss().DataType = "Upgrade"

  set_tags(stereo)

  importOptions('$LBPGUNSROOT/options/PGuns.py')
  from Configurables import ParticleGun
  #ParticleGun().EventType = 52210010

  # Set momentum
  from Configurables import MaterialEval
  ParticleGun().addTool(MaterialEval, name="MaterialEval")
  ParticleGun().ParticleGunTool = "MaterialEval"
  x_orig = 480
  y_orig = 500
  ParticleGun().MaterialEval.Xorig = x_orig
  ParticleGun().MaterialEval.Yorig = y_orig
  ParticleGun().MaterialEval.Zorig = 7620
  ParticleGun().MaterialEval.ModP = 150000 #150GeV
  
  ParticleGun().MaterialEval.ZPlane = 9439
  ParticleGun().MaterialEval.Xmin = x_orig - 20
  ParticleGun().MaterialEval.Xmax = x_orig + 20
  ParticleGun().MaterialEval.Ymin = y_orig - 5
  ParticleGun().MaterialEval.Ymax = y_orig + 5
  ParticleGun().MaterialEval.PdgCode = 211
  
  # Set min and max number of particles to produce in an event
  from Configurables import FlatNParticles
  ParticleGun().addTool(FlatNParticles, name="FlatNParticles")
  ParticleGun().NumberOfParticlesTool = "FlatNParticles"
  ParticleGun().FlatNParticles.MinNParticles = 2
  ParticleGun().FlatNParticles.MaxNParticles = 2
  
  GaussGen = GenInit("GaussGen")
  GaussGen.FirstEventNumber = 1
  GaussGen.RunNumber = 1082

  LHCbApp().EvtMax = 10

  HistogramPersistencySvc().OutputFile = outpath+'-GaussHistos.root'

  OutputStream("GaussTape").Output = "DATAFILE='PFN:%s.sim' TYP='POOL_ROOTTREE' OPT='RECREATE'"%outpath

#execute()

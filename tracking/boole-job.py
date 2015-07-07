#
from Configurables import Boole
from Gaudi.Configuration import *
from Configurables import LHCbApp, CondDB

from Configurables import Boole

# just instantiate the configurable
theApp = Boole()

from Configurables import Boole, CondDB

CondDB().Upgrade = True
Boole().DataType = "Upgrade"

Boole().DetectorDigi = ['VP', 'UT', 'FT', 'Rich1Pmt', 'Rich2Pmt', 'Ecal', 'Hcal', 'Muon']
Boole().DetectorLink = ['VP', 'UT', 'FT', 'Rich1Pmt', 'Rich2Pmt', 'Ecal', 'Hcal', 'Muon', 'Tr']
Boole().DetectorMoni = ['VP', 'UT', 'FT', 'Rich1Pmt', 'Rich2Pmt', 'Ecal', 'Hcal', 'Muon', 'Tr', 'MC']
# enable spillover 
from Configurables import Boole
Boole().UseSpillover = True
#   
Boole().SpilloverPaths = ["PrevPrev", "Prev", "Next", "NextNext"]
from Configurables import RichDigiSysConf
RichDigiSysConf().UseSpillover = False
# These options will set the flag necessary to have extended digi


Boole().DigiType = 'Extended'
# Change algorithm for ROOT compression of output files
# This setting is recommended for writing temporary intermediate files, for
# which speed of writing is more important than file size on disk

from Configurables import RootCnvSvc
#RootCnvSvc().GlobalCompression = "ZLIB:1"

LHCbApp().DDDBtag = "dddb-20150424"
LHCbApp().CondDBtag = "sim-20140204-vc-md100"
# Fix weird DB error that appeared once we started data taking in 2015
CondDB().LoadCALIBDB = 'HLT1'
# We are 'reprocessing' a file from the BK
#Boole().InputDataType = 'XDST'

Boole().EvtMax = 10
Boole().Outputs = ["DIGI"]

import glob
from GaudiConf import IOHelper
#input_files = glob.glob("/tmp/thead/00045401_00000030_1.xdst")
input_files = glob.glob("/tmp/thead/Gauss-13104013-10ev-20150707.sim")
IOHelper("ROOT").inputFiles(input_files)

from Configurables import OutputStream
OutputStream("DigiWriter").Output = "DATAFILE='PFN:/tmp/thead/june2015-withnoise-fromsim.xdigi' TYP='POOL_ROOTTREE' OPT='REC'"

# The defaults are with noise and 2bitADC
# uncomment the following if you want to turn it off
#from Configurables import MCFTDigitCreator, SiPMResponse
#MCFTDigitCreator().Force2bitADC = False
#MCFTDigitCreator().SimulateNoise = False
#SiPMResponse().useNewResponse = False

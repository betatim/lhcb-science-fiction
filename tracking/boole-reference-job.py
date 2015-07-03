# Use Boole v29r6 to reprocess files from the BK
# which were originally produced with v26r9
from Configurables import Boole
from Gaudi.Configuration import *
from Configurables import LHCbApp, CondDB


CondDB().Upgrade = True
CondDB().AllLocalTagsByDataType = ["VP_UVP+RICH_2019+UT_UUT", "FT_StereoAngle5", "Muon_NoM1", "Calo_NoSPDPRS"]

from Configurables import Boole
Boole().DataType     = "Upgrade" 

Boole().DetectorDigi = ['VP', 'UT', 'FT', 'Rich1Pmt', 'Rich2Pmt', 'Ecal', 'Hcal', 'Muon']
Boole().DetectorLink = ['VP', 'UT', 'FT', 'Rich1Pmt', 'Rich2Pmt', 'Ecal', 'Hcal', 'Muon', 'Tr']
Boole().DetectorMoni = ['VP', 'UT', 'FT', 'Rich1Pmt', 'Rich2Pmt', 'Ecal', 'Hcal', 'Muon', 'MC']

# enable spillover
Boole().UseSpillover = True
Boole().SpilloverPaths = ["PrevPrev", "Prev", "Next", "NextNext"]

# These options will set the flag necessary to have extended digi
Boole().DigiType = 'Extended'
Boole().Outputs = ["DIGI"]
Boole().EvtMax     = -1
# We are 'reprocessing' a file from the BK
Boole().InputDataType = 'XDST'

from Configurables import RootCnvSvc
RootCnvSvc().GlobalCompression = "ZLIB:1"

import glob
input_files = glob.glob("/tmp/thead/.xdst")
IOHelper("ROOT").inputFiles(input_files)

#
from Configurables import Boole
from Gaudi.Configuration import *
from Configurables import LHCbApp
from Configurables import Boole, CondDB


def execute(noise=True,
            two_bit=True,
            new_response=1):
    CondDB().Upgrade = True
    Boole().DataType = "Upgrade"
    
    Boole().DetectorDigi = ['VP', 'UT', 'FT', 'Rich1Pmt', 'Rich2Pmt', 'Ecal', 'Hcal', 'Muon']
    Boole().DetectorLink = ['VP', 'UT', 'FT', 'Rich1Pmt', 'Rich2Pmt', 'Ecal', 'Hcal', 'Muon', 'Tr']
    Boole().DetectorMoni = ['VP', 'UT', 'FT', 'Rich1Pmt', 'Rich2Pmt', 'Ecal', 'Hcal', 'Muon', 'Tr', 'MC']
    # enable spillover 

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
    RootCnvSvc().GlobalCompression = "ZLIB:1"

    LHCbApp().DDDBtag = "dddb-20150424"
    LHCbApp().CondDBtag = "sim-20140204-vc-md100"
    # Fix weird DB error that appeared once we started data taking in 2015
    CondDB().LoadCALIBDB = 'HLT1'

    Boole().Outputs = ["DIGI"]

    # The defaults are with noise and 2bitADC
    # uncomment the following if you want to turn it off
    from Configurables import MCFTDigitCreator, SiPMResponse
    MCFTDigitCreator().Force2bitADC = two_bit
    MCFTDigitCreator().SimulateNoise = noise
    SiPMResponse().useNewResponse = new_response

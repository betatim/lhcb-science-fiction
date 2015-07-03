from Configurables import Brunel, LHCbApp, CondDB
from Configurables import MessageSvc
from Configurables import RecMoniConf
from Configurables import GaudiSequencer, PrTrackAssociator, PrChecker

from GaudiConf import IOHelper
import Gaudi.Configuration as GC


# Fix weird DB error that appeared once we started data taking in 2015
CondDB().Upgrade = True
CondDB().LoadCALIBDB = 'HLT1'

Brunel().Detectors = ['VP', 'UT', 'FT', 'Rich1Pmt', 'Rich2Pmt', 'Ecal', 'Hcal', 'Muon', 'Magnet', 'Tr' ]
Brunel().DataType     = "Upgrade"

LHCbApp().DDDBtag = "dddb-20150424"
LHCbApp().CondDBtag = "sim-20140204-vc-md100"

#RecMoniConf().MoniSequence = []

from Configurables import TrackSys
TrackSys().TrackTypes = ["Velo","Forward","Seeding"]

Brunel().RecoSequence = ["Decoding", "Tr"]
Brunel().MCLinksSequence = ["Unpack", "Tr"]
Brunel().MCCheckSequence = ["Pat"]
Brunel().OutputType = "NONE"
Brunel().InputType = "XDST"
Brunel().WithMC = True
Brunel().Simulation = True
Brunel().PrintFreq = 100
Brunel().EvtMax = 1000
# ???????
Brunel().SplitRawEventInput  = 4.1


MessageSvc().Format = '% F%20W%S%7W%R%T %0W%M'

from Configurables import RecMoniConf
RecMoniConf().MoniSequence = []

from Configurables import L0Conf
#L0Conf().EnsureKnownTCK=False


# Change algorithm for ROOT compression of output files
# This setting is recommended for writing temporary intermediate files, for
# which speed of writing is more important than file size on disk

from Configurables import RootCnvSvc
RootCnvSvc().GlobalCompression = "ZLIB:1"

import glob
input_files = glob.glob("/tmp/thead/june2015-*.xdst")
IOHelper("ROOT").inputFiles(input_files)

def setup_mc_truth_matching():
    from Configurables import PrPixelTracking, PrForwardTracking, PrPixelHitManager
    GaudiSequencer("CaloBanksHandler").Members = []
    GaudiSequencer("DecodeTriggerSeq").Members = []
    GaudiSequencer("MCLinksTrSeq").Members = ["VPClusterLinker",
                                              "PrLHCbID2MCParticle",
                                              "PrTrackAssociator", "PrChecker"]

    from Configurables import PrLHCbID2MCParticle
    #PrTrackAssociator().RootOfContainers = "Rec/Track"

    PrChecker().TriggerNumbers = True
    PrChecker().Eta25Cut = True
    PrChecker().WriteVeloHistos = 2
    PrChecker().WriteForwardHistos = 2
    PrChecker().WriteMatchHistos = 2
    PrChecker().WriteDownHistos = 2
    PrChecker().WriteUpHistos = 2
    PrChecker().WriteTTrackHistos = 2
    PrChecker().WriteBestHistos = 2
    PrChecker().WriteBestLongHistos = 2
    PrChecker().WriteBestDownstreamHistos = 2

GC.appendPostConfigAction(setup_mc_truth_matching)

# SetupProject brunel v47r0
#betatim rocks
import glob

from Configurables import Brunel, LHCbApp, CondDB
from Configurables import MessageSvc
from Configurables import RecMoniConf
from Configurables import GaudiSequencer, PrTrackAssociator, PrChecker

from Configurables import STOfflinePosition
from DAQSys.Decoders import DecoderDB
from DAQSys.DecoderClass import decodersForBank
from Configurables import PrSeedingXLayers
from Configurables import PrPixelTracking, PrPixelStoreClusters
from Configurables import PrForwardTracking

from GaudiConf import IOHelper
import Gaudi.Configuration as GC


stereo = 5
x_only = False#True

LHCbApp().Simulation = True
CondDB().Upgrade = True
t = {
    "DDDB": "dddb-20131025",
    "CondDB": "sim-20130830-vc-md100",
    "Others": ["VP_UVP+RICH_2019+UT_UUT",
               "FT_StereoAngle%s"%stereo,
               "Muon_NoM1", "Calo_NoSPDPRS"],
    }
LHCbApp().DDDBtag = t['DDDB']
LHCbApp().CondDBtag = t['CondDB']
CondDB().AllLocalTagsByDataType = t['Others']
      
RecMoniConf().MoniSequence = []

Brunel().RecoSequence = ["L0", "HLT"]
Brunel().MCLinksSequence = ["Unpack", "Tr"]
Brunel().MCCheckSequence = ["Pat"]
Brunel().OutputType = "NONE"
Brunel().DataType = "Upgrade"
Brunel().InputType = "DIGI"
Brunel().WithMC = True
Brunel().PrintFreq = 100
Brunel().Simulation = True
Brunel().EvtMax = 200*5
Brunel().DatasetName = "seeding-%i%s"%(stereo, "-XOnly" if x_only else "")
Brunel().Detectors = ['VP', 'UT', 'FT', 'Rich1Pmt', 'Rich2Pmt',
                      'Spd', 'Prs', 'Ecal', 'Hcal', 'Muon', 'Magnet', 'Tr']

MessageSvc().Format = '% F%20W%S%7W%R%T %0W%M'

GaudiSequencer("RecoHLTSeq").Members = ["GaudiSequencer/SeedingSeq"]

seed_seq = GaudiSequencer("SeedingSeq")

decs = []
decs.extend(decodersForBank(DecoderDB,"VP"))
#decs.extend(decodersForBank(DecoderDB,"UT"))
decs.extend(decodersForBank(DecoderDB,"FTCluster"))
createUTLiteClusters = decodersForBank(DecoderDB, "UT")
seed_seq.Members += [d.setup() for d in createUTLiteClusters]

UT = STOfflinePosition('ToolSvc.UTClusterPosition')
UT.DetType = "UT"
        
seed_seq.Members += [d.setup() for d in decs]
seed_seq.Members += [PrPixelTracking(), PrPixelStoreClusters(),
                     PrForwardTracking(),
                     PrSeedingXLayers()
                     ]

PrSeedingXLayers().XOnly = x_only

input_files = glob.glob("/tmp/thead/stereo-%i/*.digi"%(stereo))
IOHelper("ROOT").inputFiles(input_files)

def setup_mc_truth_matching():
    GaudiSequencer("CaloBanksHandler").Members = []
    GaudiSequencer("DecodeTriggerSeq").Members = []
    GaudiSequencer("MCLinksTrSeq").Members = ["VPClusterLinker",
                                              "PrLHCbID2MCParticle",
                                              "PrTrackAssociator"]
    GaudiSequencer("CheckPatSeq" ).Members = ["PrChecker"]

    from Configurables import PrLHCbID2MCParticle
    #PrLHCbID2MCParticle().OutputLevel = 2
    PrTrackAssociator().RootOfContainers = "/Event/Rec/Track"

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

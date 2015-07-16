# File for setting hypotetical Beam conditions
# They are suitable for upgrade studies:
#   Beam 7 TeV, beta* = 3m , emittance(normalized) ~ 2 micron
#   No spill-over
#   External Horizontal Crossing Angle
#
# Requires Gauss v45r1 or higher.
#
# Syntax is: 
#  gaudirun.py $APPCONFIGOPTS/Gauss/Beam7000GeV-md100-nu7.6-HorExtAngle.py
#              $DECFILESROOT/options/30000000.opts (i.e. event type)
#              $LBGENROOT/options/GEN.py (i.e. production engine)
#              Sim08-2011-Tags.py (i.e. database tags to be used)
#              gaudi_extra_options_NN_II.py (ie. job specific: random seed,
#                               output file names, see Gauss-Job.py as example)
#
from Configurables import Gauss
from GaudiKernel import SystemOfUnits

#--Set the L/nbb, total cross section and revolution frequency and configure
#  the pileup tool, a CrossingRate of 11.245 kilohertz is used internally
#  This is the L per bunch, corresponding to
#                           L = 2 x 10^33 cm-2 s-1 with 2400 colliding bunches
#  It correspond to nu(total) = 7.6 and we assume mu(visible)=0.699*nu
Gauss().Luminosity        = 0.8338*(10**30)/(SystemOfUnits.cm2*SystemOfUnits.s)
Gauss().TotalCrossSection = 102.5*SystemOfUnits.millibarn

#--Set the average position of the IP: assume a perfectly centered beam in LHCb
Gauss().InteractionPosition = [ 0.0, 0.0, 0.0 ]

#--Set the bunch RMS, this will be used for calculating the sigmaZ of the
#  Interaction Region. SigmaX and SigmaY are calculated from the beta* and
#  emittance
Gauss().BunchRMS = 90.0*SystemOfUnits.mm

#--Set the energy of the beam,
Gauss().BeamMomentum      = 7.0*SystemOfUnits.TeV

#--the half effective crossing angle (in LHCb coordinate system), horizontal
#  and vertical. The horizontal one is given by the LHCb magnet and corrector
#  so its sign depend on the polarity (negative angle for magnet down)
Gauss().BeamHCrossingAngle = -0.385*SystemOfUnits.mrad
Gauss().BeamVCrossingAngle = 0.000*SystemOfUnits.mrad
Gauss().BeamLineAngles     = [ 0.0, 0.0 ]

#--beta* and emittance (beta* is nomimally 3m and e_norm 2.5um,
#                       adjusted to match sigmaX and sigmaY)
Gauss().BeamEmittance     = 0.0038*SystemOfUnits.mm
# Gives \sigma_{x,y} = 0.037697  ~= 0.0377
Gauss().BeamBetaStar      = 2.79*SystemOfUnits.m
#-- Enable spill-over 
#-- Set the bunch spacing to 25 ns, hence spill-over for the following slots
from Configurables import Gauss
Gauss().SpilloverPaths = [ 'PrevPrev',
                           'Prev',
                           'Next',
                           'NextNext' ]

from Configurables import GenInit
from GaudiKernel import SystemOfUnits
GenInit("GaussGen").BunchSpacing = 25 * SystemOfUnits.ns

# file /nightlies/jenkins/workspace/nightly-slot-checkout/tmp/checkout/DBASE/Gen/DecFiles/v27r48/options/13104013.py generated: Tue, 30 Jun 2015 10:33:12
#
# Event Type: 13104013
#
# ASCII decay Descriptor: [B_s0 -> (phi(1020) -> K+ K-) (phi(1020) -> K+ K-)]cc
#
from Gaudi.Configuration import *
importOptions( "$DECFILESROOT/options/B2PhiPhi.py" )
from Configurables import Generation
Generation().EventType = 13104013
Generation().SampleGenerationTool = "SignalRepeatedHadronization"
from Configurables import SignalRepeatedHadronization
Generation().addTool( SignalRepeatedHadronization )
Generation().SignalRepeatedHadronization.ProductionTool = "PythiaProduction"
from Configurables import ToolSvc
from Configurables import EvtGenDecay
ToolSvc().addTool( EvtGenDecay )
ToolSvc().EvtGenDecay.UserDecayFile = "$DECFILESROOT/dkfiles/Bs_phiphi=CDFAmp,DecProdCut,hpt400.dec"
Generation().SignalRepeatedHadronization.CutTool = "DaughtersInLHCbAndWithDaughAndBCuts"
Generation().SignalRepeatedHadronization.SignalPIDList = [ 531,-531 ]

# Ad-hoc particle gun code

from Configurables import ParticleGun
pgun = ParticleGun("ParticleGun")
pgun.SignalPdgCode = 531
pgun.DecayTool = "EvtGenDecay"
pgun.GenCutTool = "DaughtersInLHCbAndWithDaughAndBCuts"

pgun.addTool( Generation().SignalRepeatedHadronization.DaughtersInLHCbAndWithDaughAndBCuts.clone() )

from Configurables import FlatNParticles
pgun.NumberOfParticlesTool = "FlatNParticles"
pgun.addTool( FlatNParticles , name = "FlatNParticles" )

from Configurables import MomentumSpectrum
pgun.ParticleGunTool = "MomentumSpectrum"
pgun.addTool( MomentumSpectrum , name = "MomentumSpectrum" )
pgun.MomentumSpectrum.PdgCodes = [ 531,-531 ]
pgun.MomentumSpectrum.InputFile = "$PGUNSDATAROOT/data/Ebeam4000GeV/MomentumSpectrum_531.root"
pgun.MomentumSpectrum.BinningVariables = "pteta"
pgun.MomentumSpectrum.HistogramPath = "h_pteta"

from Configurables import BeamSpotSmearVertex
pgun.addTool(BeamSpotSmearVertex, name="BeamSpotSmearVertex")
pgun.VertexSmearingTool = "BeamSpotSmearVertex"
pgun.EventType = 13104013
from Configurables import Generation, MinimumBias, Pythia8Production
from Configurables import Inclusive, SignalPlain, SignalRepeatedHadronization
from Configurables import Special

Pythia8TurnOffFragmentation = [ "HadronLevel:all = off" ]

gen = Generation()
gen.addTool( MinimumBias , name = "MinimumBias" )
gen.MinimumBias.ProductionTool = "Pythia8Production"
gen.MinimumBias.addTool( Pythia8Production , name = "Pythia8Production" )
gen.MinimumBias.Pythia8Production.Tuning = "LHCbDefault.cmd"

gen.addTool( Inclusive , name = "Inclusive" )
gen.Inclusive.ProductionTool = "Pythia8Production"
gen.Inclusive.addTool( Pythia8Production , name = "Pythia8Production" )
gen.Inclusive.Pythia8Production.Tuning = "LHCbDefault.cmd"

gen.addTool( SignalPlain , name = "SignalPlain" )
gen.SignalPlain.ProductionTool = "Pythia8Production"
gen.SignalPlain.addTool( Pythia8Production , name = "Pythia8Production" )
gen.SignalPlain.Pythia8Production.Tuning = "LHCbDefault.cmd"

gen.addTool( SignalRepeatedHadronization , name = "SignalRepeatedHadronization" )
gen.SignalRepeatedHadronization.ProductionTool = "Pythia8Production"
gen.SignalRepeatedHadronization.addTool( Pythia8Production , name = "Pythia8Production" )
gen.SignalRepeatedHadronization.Pythia8Production.Tuning = "LHCbDefault.cmd"
gen.SignalRepeatedHadronization.Pythia8Production.Commands += Pythia8TurnOffFragmentation

gen.addTool( Special , name = "Special" )
gen.Special.ProductionTool = "Pythia8Production"
gen.Special.addTool( Pythia8Production , name = "Pythia8Production" )
gen.Special.Pythia8Production.Tuning = "LHCbDefault.cmd"
##
##  File containing options to activate the FTFP_BERT Hadronic
##  Physics List in Geant4 (the default for production is 
##  LHEP)
##

from Configurables import Gauss

Gauss().PhysicsList = {"Em":'NoCuts', "Hadron":'FTFP_BERT', "GeneralPhys":True, "LHCbPhys":True}
############################################################################
# File for running Gauss with all Baseline Upgrade detectors as of May 2015
############################################################################

from Configurables import Gauss, CondDB

CondDB().Upgrade = True

Gauss().DetectorGeo  = { "Detectors": ['VP', 'UT', 'FT', 'Rich1Pmt', 'Rich2Pmt', 'Ecal', 'Hcal', 'Muon', 'Magnet' ] }
Gauss().DetectorSim  = { "Detectors": ['VP', 'UT', 'FT', 'Rich1Pmt', 'Rich2Pmt', 'Ecal', 'Hcal', 'Muon', 'Magnet' ] }
Gauss().DetectorMoni = { "Detectors": ['VP', 'UT', 'FT', 'Rich1Pmt', 'Rich2Pmt', 'Ecal', 'Hcal', 'Muon', 'Magnet' ] }

Gauss().DataType = "Upgrade"
# Change algorithm for ROOT compression of output files
# This setting is recommended for writing temporary intermediate files, for
# which speed of writing is more important than file size on disk

from Configurables import RootCnvSvc
RootCnvSvc().GlobalCompression = "ZLIB:1"

from Configurables import LHCbApp, CondDB
LHCbApp().DDDBtag = "dddb-20150424"
LHCbApp().CondDBtag = "sim-20140204-vc-md100"
# Fix weird DB error that appeared once we started data taking in 2015
CondDB().LoadCALIBDB = 'HLT1'# We are 'reprocessing' a file from the BK

LHCbApp().EvtMax = 90

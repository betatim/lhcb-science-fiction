#source SetupProject.sh Gauss v47r2
#gaudirun.py opts.py

from Gaudi.Configuration import importOptions
#Latest Gauss production : with Gauss v47r2
# Event type, e.g. 30000000 == MinBias
# You can see the full list under: $DECFILESROOT/options
eventType = 30000000

# Information on colliding beams: momenta, crossing angles
importOptions('$APPCONFIGOPTS/Gauss/Beam7000GeV-mu100-nu7.6-HorExtAngle.py')

# Option which enables spillower
importOptions('$APPCONFIGOPTS/Gauss/EnableSpillover-25ns.py')

# Specific event type
importOptions('$DECFILESROOT/options/' + str(eventType) + '.py')

# MC generator to use - all upgrade studies are done with PYTHIA 8
importOptions('$LBPYTHIA8ROOT/options/Pythia8.py')

# Options which enable hadronic physics in GEANT4
importOptions('$APPCONFIGOPTS/Gauss/G4PL_FTFP_BERT_EmNoCuts.py')

# Options to use the upgrade geometry:
# use the upgrade database and upgrade datatype, and specify the
# subdetectors
importOptions('$APPCONFIGOPTS/Gauss/Gauss-Upgrade-Baseline-20150522.py')

#########################################################################

# Important bit - database tags
from Configurables import LHCbApp
LHCbApp().DDDBtag    = "dddb-20150424"
# For magnet polarity 'down'
LHCbApp().CondDBtag  = "sim-20140204-vc-md100"

# This is usually not needed, but right now there is a bug
# which tries to search caliboff.db and fails
from Configurables import CondDB
CondDB().LoadCALIBDB = 'HLT1'

## Useful option if you do not want to run full detecrot simulation
## with GEANT4, but only the MC generator phase
##from Gauss.Configuration import *
##Gauss().Phases = [ "Generator", "GenToMCTree" ]

## Do not use pileup - single interaction per event
##from Configurables import Generation
##Generation().PileUpTool = "FixedNInteractions"

#########################################################################

# How many events to produce
LHCbApp().EvtMax = 10

# Output file name (not really necessary)
from Gaudi.Configuration import OutputStream
OutputStream("GaussTape").Output="DATAFILE='PFN:OUTPUT.sim' TYP='POOL_ROOTTREE' OPT='RECREATE'"

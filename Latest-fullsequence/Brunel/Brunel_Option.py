#source SetupProject.sh Brunel v47r6p1
#gaudirun.py opts.py



from Gaudi.Configuration import importOptions

# Save MC Truth in the output DST
importOptions('$APPCONFIGOPTS/Brunel/MC-WithTruth.py')

# Options for the upgrade detector configuration
importOptions('$APPCONFIGOPTS/Brunel/Brunel-Upgrade-Baseline-20150522.py')

# Upgrade RICH configuration
importOptions('$APPCONFIGOPTS/Brunel/Upgrade-RichPmt.py')

# Some values which are not yet default in Brunel:
# empty monitoring sequence and ignore TCK
importOptions('$APPCONFIGOPTS/Brunel/patchUpgrade1.py')

# This is to produce an LDST
#importOptions('$APPCONFIGOPTS/Brunel/ldst.py')

#########################################################################

# Upgrade database tags
from Configurables import Brunel
Brunel().DDDBtag    = "dddb-20150424"
Brunel().CondDBtag  = "sim-20140204-vc-md100"

# CALIB fix, same as in the options for Gauss and Boole
from Configurables import CondDB
CondDB().LoadCALIBDB = 'HLT1'

# Input file from Boole = output of Boole
from Configurables import EventSelector
EventSelector().Input = [ "DATAFILE='PFN:../2-digi/OUTPUT.digi'" ]

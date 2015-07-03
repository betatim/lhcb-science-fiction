#source SetupProject.sh Boole v29r6
#gaudirun.py opts.py

from Gaudi.Configuration import importOptions

# Default application options
importOptions('$APPCONFIGOPTS/Boole/Default.py')

# Options for the upgrade detector configuration, upgrade data type...
importOptions('$APPCONFIGOPTS/Boole/Boole-Upgrade-Baseline-20150522.py')

# Spillower options
importOptions('$APPCONFIGOPTS/Boole/EnableSpillover.py')

# Switch off spillover for RICH (it is not supported yet as I understand)
importOptions('$APPCONFIGOPTS/Boole/Upgrade-RichMaPMT-NoSpilloverDigi.py')

# This is for 'extended Digi'
#importOptions('$APPCONFIGOPTS/Boole/xdigi.py')

#########################################################################

# Upgrade database tags
from Configurables import LHCbApp
LHCbApp().DDDBtag    = "dddb-20150424"
LHCbApp().CondDBtag  = "sim-20140204-vc-md100"

# CALIB fix, same as in the options for Gauss
from Configurables import CondDB
CondDB().LoadCALIBDB = 'HLT1'

# Input must be the output of the Sim (be carefull to have same DDDB tags between Gauss and Boole)
# Re-adapt it to accept a XDST file and create a new Series of scripts to do so.
# Gauss input
from Gaudi.Configuration import EventSelector
EventSelector().Input = ["DATAFILE='PFN:../1-sim/OUTPUT.sim'"]

# Output file name (not really necessary)
from Configurables import Boole
Boole().DatasetName = 'OUTPUT'

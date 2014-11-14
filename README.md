lhcb-science-fiction
====================

Scripts and tools for work on the SciFi detector simulation for the LHCb upgrade

To generate events for testing your work look in `simulation/`. There are option
files as well as ganga scripts for the Gauss and Boole stages.

The `seeding/` directory contains option file for running the actual
reconstruction (Brunel) as well as some basic checking of the output.

To compare cluster properties between the test beam and the simulation
look at `simulation/gauss-pgun-job.py` to create events and
`cluster-sizes/pgun-pions.py` to analyse them.


SciFi tracking comparisons
==========================


Reference sample
----------------

The reference sample reflects the state of play after the
end of the DILBERT task force.

Download a file from sim+std://MC/Upgrade/Beam7000GeV-Upgrade-MagDown-Nu7.6-25ns-Pythia8/Sim08c/Digi13/Reco14U4/13104013/XDST with:

```
lb-run LHCbDirac dirac-dms-get-file /lhcb/MC/Upgrade/XDST/00031726/0000/00031726_00000001_1.xdst
```

Run Boole v29r4 on this with `boole-reference-job.py`

Run Brunel v47r5 on this with `brunel-reference-job.py`


Brunel on June2015 samples
--------------------------

To run Brunel v47r6p1 on the samples from the book keeping you
need an updated version of Pr/PrPixel (at least r191270).

Download a file from sim+std://MC/Upgrade/Beam7000GeV-Upgrade-MagDown-Nu7.6-25ns-Pythia8/Sim08h-NoRichSpill/Reco14U5/13104013/XDST

You can run Brunel with the option file `brunel-job.py`. Make
sure to edit the input file location.


Full chain for June2015
-----------------------

To run the full simulation chain you can use the following
option files: gauss-job.py, boole-job.py, brunel-job.py

* Gauss v47r2
* Boole v29r6
* Brunel v47r6p1 (need Pr/PrPixel revision r191270)


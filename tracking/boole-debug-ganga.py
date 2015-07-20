from Ganga.GPI import *
import sys
import inspect
import os


local_dir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))

if len(sys.argv) != 2+3:
    sys.exit("Script requires the id of the gauss job to use as inputdata and the setting for noise, 2bit, response.")

old = int(sys.argv[1])

if jobs(old).application.__class__ is not Gauss:
    sys.exit("The given job is not a Gauss job.")

old_job = jobs(old)

j = Job(application=Boole(version="v29r6",
                          optsfile=local_dir + "/boole-debug-job.py",
                          extraopts="execute(%r, %r, %i)"%(bool(int(sys.argv[2])),
                                                           bool(int(sys.argv[3])),
                                                           int(sys.argv[4])),
                          #user_release_area="/afs/cern.ch/user/t/thead/git/lhcb-science-fiction/tracking/",
                          )
        )

j.outputfiles = [DiracFile("*.digi")]
j.backend = Dirac()

j.splitter = SplitByFiles(filesPerJob=2)
j.name = jobs(old).name
j.comment = "Input from job %i, debugging FTDet v2r6"%(old)

if len(jobs(old).subjobs) == 0:
    j.inputdata = jobs(old).outputfiles
else:
    j.inputdata = []
    for osj in jobs(old).subjobs.select(status='completed'):
        for f in osj.outputfiles:
            if isinstance(f, DiracFile):
                if f.lfn:
                    j.inputdata.extend([LogicalFile(f.lfn)])

j.prepare()
j.submit()

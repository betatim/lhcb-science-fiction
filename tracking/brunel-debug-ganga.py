from Ganga.GPI import *
import sys
import inspect
import os


local_dir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))

if len(sys.argv) != 2:
    sys.exit("Script requires the id of the Boole job to use as inputdata.")

old = int(sys.argv[1])

if jobs(old).application.__class__ is not Boole:
    sys.exit("The given job is not a Boole job.")

old_job = jobs(old)

j = Job(application=Brunel(version="v47r6p1",
                           optsfile=local_dir + "/brunel-debug-job.py",
                           #user_release_area='/afs/cern.ch/user/t/thead/git/lhcb-science-fiction/tracking'
                           )
        )

j.backend = Dirac()

j.name = jobs(old).name
j.comment = "Input from job %i debugging FTDet v2r6"%(old)

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

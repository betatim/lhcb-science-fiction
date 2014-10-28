from Ganga.GPI import *
import sys
import inspect
import os


# Stereo angle to use
stereo = 5 #int(sys.argv[1])

local_dir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))

print local_dir

j = Job(application=Gauss(
        version="v46r7p2",
        optsfile=local_dir + "/gauss-job.py",
        extraopts="execute(13104021, %s)"%stereo,
        #user_release_area=local_dir + "/../cmt",
        ))

j.name = "SciFi-stereo-%i"%stereo
j.outputfiles = [DiracFile("*.sim")]

j.backend=Dirac()
#j.backend.settings['BannedSites'] = ['LCG.RRCKI.ru']

events = 2000
eventsperjob = 50

j.splitter = GaussSplitter(numberOfJobs=int(round(events*1.1/eventsperjob)),
                           eventsPerJob=eventsperjob)

#j.do_auto_resubmit = True

j.prepare()
j.submit()

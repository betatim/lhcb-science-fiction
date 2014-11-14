# SetupProject boole v28r2p1

import GaudiPython as GP
from GaudiConf import IOHelper
from Configurables import LHCbApp, ApplicationMgr, DataOnDemandSvc
from Configurables import SimConf, DigiConf, DecodeRawEvent
from Configurables import CondDB

from LinkerInstances.eventassoc import *

import ROOT as R


MCParticle = GP.gbl.LHCb.MCParticle
Track = GP.gbl.LHCb.Track
MCHit = GP.gbl.LHCb.MCHit
Cluster = GP.gbl.LHCb.VPCluster
FTChannelID = GP.gbl.LHCb.FTChannelID

stereo = 5

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

# Configure all the unpacking, algorithms, tags and input files
appConf = ApplicationMgr()
appConf.ExtSvc+= ['ToolSvc', 'DataOnDemandSvc']
appConf.TopAlg += [#"PrPixelTracking", "PrPixelStoreClusters",
                   #"VPClusterLinker",
                   "MCFTDepositCreator",
                   "MCFTDigitCreator",
                   "FTClusterCreator",
                   ]

from Configurables import MCFTDigitCreator
MCFTDigitCreator().IntegrationOffset = [0,2,4]
MCFTDigitCreator().SimulateNoise = True

s = SimConf()
SimConf().Detectors = ['VP', 'UT', 'FT', 'Rich1Pmt', 'Rich2Pmt', 'Ecal', 'Hcal', 'Muon']
SimConf().EnableUnpack = True
SimConf().EnablePack = False

d = DigiConf()
DigiConf().Detectors = ['VP', 'UT', 'FT', 'Rich1Pmt', 'Rich2Pmt', 'Ecal', 'Hcal', 'Muon']
DigiConf().EnableUnpack = True
DigiConf().EnablePack = False

dre = DecodeRawEvent()
dre.DataOnDemand = True

lhcbApp = LHCbApp()
lhcbApp.Simulation = True

import sys
inputFiles = [sys.argv[-1]]
IOHelper('ROOT').inputFiles(inputFiles)


def cluster2mc_particles(cluster, event):
    links = event['/Event/Link/Raw/FT/Clusters']
    refs = links.linkReference()
    mc_particles = event['MC/Particles']
    next_idx = -1
    particles = []
    cluster_channel = cluster.channelID().channelID()
    for channel, key in links.keyIndex():
        if channel == cluster_channel:
            particles.append(mc_particles.object(refs[key].objectKey()))
            next_idx = refs[key].nextIndex()
            break

    while next_idx != -1:
        particles.append(mc_particles.object(refs[next_idx].objectKey()))
        next_idx = refs[next_idx].nextIndex()

    return particles

def rad2deg(rad):
    return 180 * rad / 3.1415

def keep_cluster(cluster):
    for p in cluster2mc_particles(cluster, evt):
        angle = rad2deg(p.momentum().theta())
        if angle < 4 and p.particleID().pid() != -99000000:
            return True
    return False
def pion_gun_cluster(cluster):
    for p in cluster2mc_particles(cluster, evt):
        origin = p.originVertex()
        if (p.particleID().abspid() == 211 and
            (origin.x(), origin.y(), origin.z()) == (500.0, 500.0, 7620.0)):
            return True
    return False

def print_cluster(cluster):
    print cluster.channelID().channelID(), cluster.size()
    for p in cluster2mc_particles(cluster, evt):
        print p.particleID().pid(), rad2deg(p.momentum().theta()),
        print p.originVertex().position().x(), p.originVertex().position().y(),
        print p.originVertex().position().z(), "->", [v.position().z() for v in p.endVertices()]

def cluster_neighbourhood(cluster, width=10):
    channel = cluster.channelID().channelID()
    indexer = FTChannelID(1234) # dummy
    all_digits = evt['/Event/MC/FT/Digits']
    near_digits = []
    for idx in xrange(channel-width, channel+width):
        indexer.setChannelID(idx)
        d = all_digits.object(indexer)
        if d:
            near_digits.append(d)
        
    return near_digits


# Configuration done, run time!
appMgr = GP.AppMgr()
evt = appMgr.evtsvc()

R.gROOT.ProcessLine(".x lhcbstyle2.C")

digit_adcs = R.TH1F("", ";channel ADC count;entries", 105,-5, 100)
cluster_size = R.TH1F("", ";cluster size;entries", 10,-0.5, 9.5)
cluster_adc_sum = R.TH1F("", ";cluster ADC sum;entries", 105,-5, 100)
neighbourhood_size = R.TH1F("", ";neighbourhood size;entries", 21,-0.5, 20.5)

# Make a few plots showing the digits
# in the neighbourhood of a cluster
detailed_clusters = []
n_detailed = 10

for n in xrange(300):
    appMgr.run(1)

    digits = evt['/Event/MC/FT/Digits'].containedObjects()
    for digit in digits:
        digit_adcs.Fill(digit.adcCount())
    
    clusters = evt['/Event/Raw/FT/Clusters'].containedObjects()
    for cluster in clusters:
        if keep_cluster(cluster):
        #if pion_gun_cluster(cluster):
            cluster_adc_sum.Fill(cluster.charge())
            cluster_size.Fill(cluster.size())
        
            #print_cluster(cluster)
            digits = cluster_neighbourhood(cluster)
            neighbourhood_size.Fill(len(digits))

            if len(detailed_clusters) < n_detailed:
                # shift all channel IDs by the channel ID of the cluster
                channel = cluster.channelID().channelID()
                h = R.TH1F("", ";neighbouring channels;ADC count", 21,-10.5, +10.5)
                detailed_clusters.append(h)

                for digit in digits:
                    digit_chan = digit.channelID()
                    h.Fill(digit_chan.channelID() - channel, digit.adcCount())
                    #print digit_chan.channelID(), digit_chan.sipmId(), digit_chan.sipmCell(), "="*digit.adcCount()

            #print "-"*60

c = R.TCanvas("wer", "wie was", 615,615)
c.SetLeftMargin(0.16)
c.SetTopMargin(0.03)

neighbourhood_size.Draw()
c.RedrawAxis()
c.SaveAs("neighbourhood_size.pdf")
c.SaveAs("neighbourhood_size.png")

digit_adcs.Draw()
c.RedrawAxis()
c.SaveAs("digit_adcs.pdf")
c.SaveAs("digit_adcs.png")

cluster_adc_sum.Draw()
c.RedrawAxis()
c.SaveAs("cluster_adc_sum.pdf")
c.SaveAs("cluster_adc_sum.png")

cluster_size.Draw()
c.RedrawAxis()
c.SaveAs("cluster_size.pdf")
c.SaveAs("cluster_size.png")

for n,h in enumerate(detailed_clusters):
    h.Draw()
    c.SaveAs("detailed_%i.png"%(n))

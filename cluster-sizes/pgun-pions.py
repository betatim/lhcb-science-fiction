# SetupProject boole v28r2p1
# SetupProject Boole v29r1p1
from collections import namedtuple

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
MyCluster = namedtuple("MyCluster", "size adcCount position")

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
#MCFTDigitCreator().SimulateNoise = True
MCFTDigitCreator().SiPMGain = sipm_gain = 10. * 10

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
    if isinstance(cluster, MyCluster):
        cluster_channel = cluster.position
        
    else:
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

def cluster2mc_hits(cluster, event):
    links = event['/Event/Link/Raw/FT/Clusters2MCHits']
    refs = links.linkReference()
    mc_hits = event['/Event/MC/FT/Hits']
    next_idx = -1
    hits = []
    if isinstance(cluster, MyCluster):
        cluster_channel = cluster.position
        
    else:
        cluster_channel = cluster.channelID().channelID()
    
    for channel, key in links.keyIndex():
        if channel == cluster_channel:
            hits.append(mc_hits[refs[key].objectKey()])
            next_idx = refs[key].nextIndex()
            break

    while next_idx != -1:
        hits.append(mc_hits[refs[next_idx].objectKey()])
        next_idx = refs[next_idx].nextIndex()

    return hits


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

def make_clusters(digits):
    """Form clusters from `digits`"""
    # thresholds in terms of photo electrons
    # digits give ADC which you divide by
    # sipm_gain to get PE
    seed = 1.5
    neighbour = 0.5

    clusters = []
    current = []
    for digit in digits:
        if current:
            # keep adding to current cluster
            if (digit.adcCount()/sipm_gain > neighbour and
                digit.channelID().channelID() == current[-1].channelID().channelID()+1):
                current.append(digit)

            # check if at least one digit exceeds seed threshold
            # and then finalise the cluster
            else:
                if any(d.adcCount() > seed for d in current):
                    adc_sum = 0
                    channel_sum = 0
                    for d in current:
                        adc_sum += d.adcCount()
                        channel_sum += d.channelID().channelID()
                        
                    clusters.append(MyCluster(len(current),
                                              adc_sum,
                                              channel_sum/len(current)))
                    current = []

        # start a new cluster
        else:
            if digit.adcCount()/sipm_gain > neighbour:
                current.append(digit)

    return clusters


# Configuration done, run time!
appMgr = GP.AppMgr()
evt = appMgr.evtsvc()
det = appMgr.detsvc()
ft_det = det['/dd/Structure/LHCb/AfterMagnetRegion/T/FT']

R.gROOT.ProcessLine(".x lhcbstyle2.C")

mchit_pos = R.TH2F("", ";x [mm];y [mm]", 100,0,2000, 100,0,2540)
digit_adcs = R.TH1F("", ";channel ADC count;entries", 105,-5, 100)
digit_pes = R.TH1F("PEs", ";Photo electrons;", 100, 0.5, 4)
cluster_size = R.TH1F("clusters", ";cluster size;entries", 10,-0.5, 9.5)
cluster_adc_sum = R.TH1F("", ";cluster ADC sum [pe];entries", 105,-5, 100)
neighbourhood_size = R.TH1F("", ";neighbourhood size;entries", 21,-0.5, 20.5)

my_cluster_size = R.TH1F("", ";cluster size;entries", 10,-0.5, 9.5)
my_cluster_adc_sum = R.TH1F("", ";cluster ADC sum [pe];entries", 105,-5, 100)

laurel = R.TH1F("", ";delta MCx - Clusterx;", 100, -2, 2)
hardy = R.TH1F("", ";delta MCx - Clusterx;", 100, -2, 2)

laurel1 = R.TH1F("", ";delta MCx - Clusterx;", 100, -2, 2)
hardy1 = R.TH1F("", ";delta MCx - Clusterx;", 100, -2, 2)

# Make a few plots showing the digits
# in the neighbourhood of a cluster
detailed_clusters = []
n_detailed = 10

my_detailed_clusters = []
my_n_detailed = 10


for n in xrange(100):
    appMgr.run(1)

    digits = evt['/Event/MC/FT/Digits'].containedObjects()
    for digit in digits:
        digit_adcs.Fill(digit.adcCount())
        digit_pes.Fill(digit.adcCount()/sipm_gain)

    my_clusters = make_clusters(digits)
    for cluster in my_clusters:
        if keep_cluster(cluster):
            my_cluster_adc_sum.Fill(cluster.adcCount/sipm_gain)
            my_cluster_size.Fill(cluster.size)
            
    clusters = evt['/Event/Raw/FT/Clusters'].containedObjects()
    for cluster in clusters:
        mchits = cluster2mc_hits(cluster, evt)
        if mchits and keep_cluster(cluster):
            mchit = mchits[0]
            mchit_x = mchit.entry().x()
            mchit_y = mchit.entry().y()
            mchit_pos.Fill(mchit_x, mchit_y)
            mat = ft_det.findFibreMat(cluster.channelID())
            det_segment = mat.createDetSegment(cluster.channelID(),
                                               cluster.fraction())

            cluster_x = det_segment.x(mchit_y)
            dX = mchit_x - cluster_x
            if mat.angle() == 0.:
                laurel.Fill(dX)
            else:
                hardy.Fill(dX)
            
        if keep_cluster(cluster):
            cluster_adc_sum.Fill(cluster.charge())
            cluster_size.Fill(cluster.size())
        
            #print_cluster(cluster)
            digits = cluster_neighbourhood(cluster)
            neighbourhood_size.Fill(len(digits))

            if len(detailed_clusters) < n_detailed:
                # shift all channel IDs by the channel ID of the cluster
                channel = cluster.channelID().channelID()
                h = R.TH1F("", ";neighbouring channels;ADC count [pe]",
                           21,-10.5, +10.5)
                detailed_clusters.append(h)

                for digit in digits:
                    digit_chan = digit.channelID()
                    h.Fill(digit_chan.channelID() - channel,
                           digit.adcCount()/sipm_gain)
                    #print digit_chan.channelID(), digit_chan.sipmId(), digit_chan.sipmCell(), "="*digit.adcCount()

            #print "-"*60

c = R.TCanvas("wer", "wie was", 615,615)
c.SetLeftMargin(0.16)
c.SetTopMargin(0.03)

laurel.Draw()
print "laurel (0deg, x layer) mean:", laurel.GetMean()
c.RedrawAxis()
c.SaveAs("laurel.pdf")
c.SaveAs("laurel.png")

hardy.Draw()
print "hardy (u,v layer) mean:", hardy.GetMean()
c.RedrawAxis()
c.SaveAs("hardy.pdf")
c.SaveAs("hardy.png")

laurel1.Draw()
print "laurel1 (0deg, x layer) mean:", laurel1.GetMean()
c.RedrawAxis()
c.SaveAs("laurel1.pdf")
c.SaveAs("laurel1.png")

hardy1.Draw()
print "hardy1 (u,v layer) mean:", hardy1.GetMean()
c.RedrawAxis()
c.SaveAs("hardy1.pdf")
c.SaveAs("hardy1.png")

mchit_pos.Draw("colz")
c.RedrawAxis()
c.SaveAs("mchit_pos.pdf")
c.SaveAs("mchit_pos.png")

neighbourhood_size.Draw()
c.RedrawAxis()
c.SaveAs("neighbourhood_size.pdf")
c.SaveAs("neighbourhood_size.png")

digit_adcs.Draw()
c.RedrawAxis()
c.SaveAs("digit_adcs.pdf")
c.SaveAs("digit_adcs.png")

digit_pes.Draw()
c.RedrawAxis()
c.SaveAs("digit_pes.pdf")
c.SaveAs("digit_pes.png")

cluster_adc_sum.Draw()
c.RedrawAxis()
c.SaveAs("cluster_adc_sum.pdf")
c.SaveAs("cluster_adc_sum.png")

cluster_size.Draw()
c.RedrawAxis()
c.SaveAs("cluster_size.pdf")
c.SaveAs("cluster_size.png")
c.SaveAs("cluster_size.C")

cluster_size.Draw()
my_cluster_size.SetLineColor(R.kRed)
my_cluster_size.Draw("same")
c.RedrawAxis()
c.SaveAs("my_cluster_size.pdf")
c.SaveAs("my_cluster_size.png")

my_cluster_adc_sum.Draw()
c.RedrawAxis()
c.SaveAs("my_cluster_adc_sum.pdf")
c.SaveAs("my_cluster_adc_sum.png")

for n,h in enumerate(detailed_clusters):
    h.Draw("hist")
    c.SaveAs("detailed_%i.png"%(n))

for n,h in enumerate(my_detailed_clusters):
    h.Draw("hist")
    c.SaveAs("my_detailed_%i.png"%(n))


f = R.TFile("/afs/cern.ch/user/b/bleverin/public/00degrees_0cm_withmirror.root")
t = f.adjustedtree
ph = R.TH1F("ph", "", 100,0.5,4)
for e in t:
    for adc in e.adc_of_channel:
        ph.Fill(adc)

for h in (digit_pes, ph):
    h.Scale(1./h.Integral())
    
digit_pes.SetLineColor(R.kRed)
digit_pes.GetYaxis().SetRangeUser(10**-3, 3*(10**-1))
digit_pes.Draw()
ph.Draw("same")
c.SetLogy()
c.RedrawAxis()
c.SaveAs("PEs.pdf")
c.SaveAs("PEs.png")
c.SaveAs("PEs.C")

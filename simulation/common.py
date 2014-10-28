from Configurables import LHCbApp, CondDB

def set_tags(stereo=5):
    LHCbApp().Simulation = True
    CondDB().Upgrade = True
    t = {#"DDDB": "dddb-20140606",
         "DDDB": "dddb-20140827", #latest and greatest
         "CondDB": "sim-20140204-vc-md100",
         #"Others": ["VP_UVP_Rotation"],
         #"Others": ["VP_UVP+RICH_2019+UT_UUT",
         #           "FT_StereoAngle5", "Muon_NoM1", "Calo_NoSPDPRS"],
         }
    t = {
        "DDDB": "dddb-20131025",
        "CondDB": "sim-20130830-vc-md100",
        "Others": ["VP_UVP+RICH_2019+UT_UUT",
                   "FT_StereoAngle%s"%stereo,
                   "Muon_NoM1", "Calo_NoSPDPRS"],
        }
    LHCbApp().DDDBtag = t['DDDB']
    LHCbApp().CondDBtag = t['CondDB']
    if 'Others' in t:
      CondDB().AllLocalTagsByDataType = t['Others']

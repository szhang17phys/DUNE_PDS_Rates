import matplotlib.pyplot as plt
import numpy as np
#import psycopg2
import csv
#import datetime
import time
import argparse
import os
import code
from ROOT import * #TH1F,TH2F,gROOT,TCanvas,TFile,gPad
import sys
from array import array
import math
gs=[]
# When ROOT objects get garbage-collected they disappear from the screen
# again. Need to leak them like in C++
def New(cons, *args):
    ret = cons(*args)
    gs.append(ret)
    return ret

#%%%%%%%%%%%%%%%%%%%% loop through runs here %%%%%%%%%%%%%%%%%%%%%%%%%%
#RunNum=5888
arg_len=len(sys.argv)
if arg_len <4:
   print "Please enter \"python -b\" and at least one run number. For multiple runs, use a space as the delimitter."
   print "For Example: \"python Ntuple_PDS_LeonOutput.py -b Random 7528 7529\""
   sys.exit()
dir_= sys.argv[2]
#sub_direct= sys.argv[3]
#sub_direct=sub_direct.replace("GeV","").replace("GEV","").replace("gev","").replace("geV","").replace("Gev","")
arg_list=[int(sys.argv[i]) for i in range(3,arg_len)]
print arg_list
#arg_list.sort()
print arg_list
runs=[str(i) for i in arg_list]
print runs
mean_ch_frac_run=[]
all_ch_frac_run=[]

#--------------------- Calibration Constants & DAQ Channel Info ----------------------------------------

Bad_channels =[25, 36, 58, 62, 65, 73, 75, 82, 101, 110, 119, 125, 156, 160]
ch_arapuca =[132,	133,	134,	135,	136,	137,	138,	139,	140,	141,	142,	143,	264,	265,	266,	267,	268,	269,	270,	271,	272,	273,	274,	275]
adc_photon_arapuca = [1153,	1068,	1105,	1184,	1152,	857,	972,	783,	822,	793,	1045,	1096,	894,	956,	925,	779,	965,	722,	774,	885,	779,	965,	995,	1035]
adc_avalanche_arapuca =[780,	734,	763,	777,	813,	665,	739,	614,	638,	639,	781,	803,	743,	744,	743,	622,	815,	647,	684,	747,	639,	780,	753,	827]

calib_ADC_Avalanche_ch = [1585.75, 1595.02, 1588.62, 1627.83, 1594.07, 1591.99, 1593.12, 1590.6, 1555.83, 1588.16, 1574.33, 1576.55, 1561.16, 1535.62, 1551.06, 1554.26, 1567.53, 1570.21, 1587.21, 1712.37, 1528.0, 1564.09, 1542.86, 1555.29, 1582.26, 99999999.0, 1580.84, 1549.25, 1590.8, 1576.32, 1562.32, 1605.0, 1594.64, 1697.21, 1554.42, 1555.76, 99999999.0, 1529.56, 1538.75, 1558.99, 1589.4, 1817.46, 1572.45, 1841.61, 1530.65, 1576.78, 1571.13, 1594.26, 1548.57, 1559.18, 99999999.0, 1543.5, 1577.9, 1577.07, 99999999.0, 1597.91, 1587.24, 99999999.0, 1563.0, 1594.78, 1592.74, 1563.09, 1533.01, 1580.67, 1569.16, 99999999.0, 1579.86, 99999999.0, 1594.44, 1714.15, 1592.27, 1584.65, 1584.55, 1559.67, 99999999.0, 1553.73, 1587.9, 1570.09, 1567.89, 1573.0, 1549.35, 1590.3, 1574.06, 1570.38, 1580.5, 99999999.0, 1594.68, 1586.22, 1720.03, 1577.49, 1711.62, 1712.25, 1562.98, 1586.57, 99999999.0, 1546.62, 1579.77, 1573.27, 1567.41, 1576.85, 1590.74, 1587.57, 1587.14, 99999999.0, 1709.4, 1553.58, 1588.15, 1576.56, 1685.94, 1859.2, 1734.66, 1705.93, 1573.91, 1563.66, 1568.62, 1592.2, 1600.09, 1578.4, 1615.34, 1578.02, 1574.26, 1596.53, 1608.19, 1568.61, 1568.17, 1573.99, 1568.68, 1551.96, 99999999.0, 1594.35, 1601.11, 1577.0, 99999999.0, 1550.02, 1578.9, 1563.75, 1568.08, 1570.87, 1581.89, 1584.56, 1565.42, 1589.2, 1582.63, 1571.7, 1747.53, 1618.93, 1586.41, 1751.84, 1835.31, 1579.94, 1555.0, 1596.82, 1697.18, 1591.97, 1568.05, 1578.05, 1580.45, 1589.44, 1572.44, 1563.93, 1612.54, 1599.95, 1544.78, 1579.91, 1596.85, 1718.35, 1617.39, 1573.39, 1608.3, 1628.96, 1617.57, 1600.4]
# BADcalib_PE_Photon_ch = [1.31864769413142, 1.3222062871376967, 1.3145245909075225, 1.2983297840467523, 0.6026930806242735, 0.3625731120423674, 0.3156150144680083, 0.5596963201089908, 1.156058212986452, 0.9780505937156371, 1.027099272305324, 1.1738429619808322, 0.0010945105963543337, 0.0007111062933356863, 0.0008649422120712251, 0.0032157873896678205, 1.3335801574021064, 1.309284900908437, 1.268864675685497, 1.2462202285037758, 0.3869321472593093, 0.04037896007473809, 0.04174124082421995, 0.13957602354560808, 1.2613130586653674, 0.0, 1.2390648729825278, 1.303085336510339, 0.16128998115011048, 0.10371528398898436, 0.1160367520674321, 0.2892516062090161, 1.2910499134256124, 1.2739226252824152, 1.3104391768667616, 1.3227989127204312, 0.0, 1.2189977847187645, 1.24367724237895, 1.2432506438319186, 1.2965976108347017, 1.3362648203133614, 1.2800840071402075, 1.3203238583634485, 1.352188109956931, 1.358425721288801, 1.3608928439134316, 1.2757995781961462, 1.331647578833712, 1.3299297217283788, 0.0, 1.3302548856494112, 0.9869994014044838, 0.9551280622036993, -0.0, 1.3172002376273535, 1.3815448874495826, -0.0, 1.3969870441292451, 1.4067524316981415, 0.2594469948184602, 0.24503213997084725, 0.32184095641028626, 1.0763994173233344, 1.3757575956376202, -0.0, 1.3833211583414962, -1.207997046444396e-05, 1.2001746883597024, 1.2029993297685717, 1.2160559503759067, 1.2511141852029548, 1.2923836396485913, 1.294127766361399, 0.0, 1.2786583768660804, 1.2558197878928805, 1.2883433986788984, 1.2796115943071678, 1.2756501397156985, 1.2997173303642926, 1.3039658022283784, 1.298929006952764, 1.298177054830344, 1.2318544704587655, 0.0002588910550500434, 1.227408008916664, 1.2315782649486335, 1.3284898758389305, 1.292115120189456, 1.3195433703903796, 1.31691660130858, 1.3353751475444136, 1.3697229234721895, -0.0, 1.3640599441828094, 1.1942574002889335, 1.1410116428592456, 1.1651721444909362, 1.2364764933529313, 1.3679024433398168, 1.3697117454203156, 1.3517444335893922, 0.0, 1.1697225519931371, 1.035141056603562, 1.0388476188377298, 1.1860329598638968, 1.2908551363328093, 1.3010356043935163, 1.3152835511820347, 1.299689783890721, 1.2777820562599, 1.281003079783665, 1.2838722106448777, 1.2725820272786341, 1.205901022131409, 1.2143440902919447, 1.2189701109577902, 1.2186291735320187, 1.299417930457352, 1.3126699973279117, 1.3199184388735272, 1.3056317121727372, 1.4003741604502533, 1.4651860711617992, 1.4435590447687991, 1.3835344533256497, 0.0, 1.385264838182425, 1.3948059018536363, 1.3795356897825883, 6.361591847599354e-05, 0.9728135369459245, 0.987172213949882, 1.2383032755079026, 1.4848223519179393, 1.5018374160317185, 1.4361109913154089, 1.4557686766315303, 0.005048739833121254, 0.00142324109172891, 0.0017325673745176315, 0.01855629462119881, 1.138963547032604, 0.7423422228678944, 0.8365362650921733, 1.1969112961181207, 1.2594898321130772, 1.222791546866036, 1.2674476337693708, 1.306435925089415, 1.0735544647587552, 1.4072537426819909, 0.9300366646602494, 1.1104264836999096, 1.439125304385866, 1.350032321881117, 1.3632402491991942, 1.4213188157451597, 0.737033594778227, 0.23654711395077987, 0.32885197939882505, 0.7104864347969025, 1.2991868749767266, 1.2815796281493128, 1.1486850663363373, 1.4327114203298923, 1.3359993647736832, 1.345681710227898, 1.3481721294260145, 1.3221401679288276]
calib_PE_Photon_ch = [1.4126430695182026, 1.4006449431694799, 1.3878747224010952, 1.4280384757532598, 1.185022547422883, 1.186352369348883, 1.1758355264180493, 1.181625241230633, 1.3664132291969349, 1.3523466245350817, 1.3863813662653377, 1.3820280363103419, 1.2100936937622748, 1.1926488325228475, 1.166773622149775, 1.1964983285387456, 1.3795231612656054, 1.3362544111395196, 1.3512221729146756, 1.420220362811809, 1.220829353791607, 1.220655018152973, 1.222912626282276, 1.2086984627725916, 1.3279071231028676, 10000000000.0, 1.3192914529810806, 1.32335710492287, 1.2178592659326009, 1.2203530216428102, 1.2188316009735298, 1.2313848964565905, 1.3181406072998099, 1.3760141447157346, 1.3111758326415797, 1.3122231701084452, 10000000000.0, 1.209155402169935, 1.198612998224154, 1.20515523309421, 1.3439645853941715, 1.4850901741907676, 1.3065163969045523, 1.465787725582078, 1.2256408388796185, 1.235425395781877, 1.2257570841575671, 1.2173598297961232, 1.3188955310034693, 1.3241719725819916, 10000000000.0, 1.237552878249943, 1.1695109665642507, 1.1744845457253708, 10000000000.0, 1.1929995992800138, 1.360413865089201, 10000000000.0, 1.3376860393924377, 1.340222639038174, 1.2588606395339457, 1.2763486214301434, 1.2899488305793958, 1.2747758611633246, 10000000000.0, 1.3016142483520656, 1.2810716350302742, 10000000000.0, 1.2980323409381538, 1.2820907816391311, 1.3069571690831912, 1.2859131188303687, 1.3141236347338188, 1.3111583352594673, 10000000000.0, 1.3012498051965924, 1.2281420148878768, 1.239712206299814, 1.2483571183388467, 1.231825616983547, 1.2785518539521004, 1.292858862836752, 1.2931883601261052, 1.2856247977051716, 1.2286502587258998, 10000000000.0, 1.220619754426727, 1.2251631525544684, 1.3551816929628346, 1.3135420013268602, 1.3413934199179152, 1.3448574964610382, 1.309162800360985, 1.2902811685087803, 10000000000.0, 1.3144181250562461, 1.2039746406100258, 1.2179707716893684, 1.2232233009506421, 1.239241811163499, 1.3306810805087887, 1.3044448650710523, 1.3082530433843111, 10000000000.0, 1.2553165386489094, 1.221040133280749, 1.1793367353071282, 1.21525774937779, 1.423437892315113, 1.4593070350087634, 1.390138650653633, 1.3965840197328665, 1.2377228589020963, 1.2227206029740612, 1.2439043942708432, 1.235466013982504, 1.1596472079381557, 1.1826476438324562, 1.1834440598913651, 1.1749501976972254, 1.3470283494858035, 1.3273469701443183, 1.3375870827262613, 1.3255450853997357, 1.2265382059183128, 1.242088445847263, 1.2264332669361386, 1.2153406989901145, 10000000000.0, 1.2927901896579428, 1.3076366288325245, 1.3004719180012512, 10000000000.0, 1.408412209338035, 1.355740746213033, 1.248978478328936, 1.2986300614938673, 1.2761278119832034, 1.299053007227065, 1.3031640760446095, 1.27333745751015, 1.2899024999034638, 1.3106641122990939, 1.2583383482210118, 1.3399717345000552, 1.300479178457047, 1.2892622461764613, 1.3321080323552814, 1.3456345778450383, 1.2836887653119438, 1.2786683780724184, 1.2832352334424384, 1.2510879728857287, 1.2704979820133029, 1.2587566749613968, 1.2674865376828923, 1.3946563165605779, 1.3937508391824676, 1.413499941389469, 1.293988806834509, 1.2547118342431276, 1.2747367332366852, 1.2890150223867227, 1.26727520938633, 1.3178309915663564, 1.336378985917566, 1.3217581882276872, 1.3136199620167408, 1.2985625926483906, 1.305201438798312, 1.306984781610701, 1.3104070494351854]
calib_ADC_Photon_ch = [calib_ADC_Avalanche_ch[pl]*calib_PE_Photon_ch[pl] for pl in range(len(calib_ADC_Avalanche_ch))]
AllChannels=range(0,208)
Channels=range(0,208)
for uu in range(40,48):
    Channels.remove(uu)
for uu in range(88,96):
    Channels.remove(uu)
for uu in range(132,144):
    Channels.remove(uu)
for uu in range(184,192):
    Channels.remove(uu)

# list with "empty channels"
empty_ch= range(40,48) +range(88,96) +range(132,144) +range(184,192)
#print empty_ch
#-----------------------------------------------------------
#-----------------------------------------------------------
apa_labels=range(1,5)
mod_labels = ["mod 0","mod 1","mod 2","mod 3","mod 4","mod 5","mod 6","mod 7","mod 8","mod 9"]
photons_mod_label=[]
mod_list=[]
for a in apa_labels:
   for m in mod_labels:
      exec("apa"+str(a)+"_"+m.replace(" ","_")+"=[]")
      exec("photons_mod_label.append(\"apa"+str(a)+"_"+m.replace(" ","_")+"\")")
      exec("mod_list.append("+str(a)+str("0")+str(m[-1])+")")
mod_list.remove(303)
time_started = os.popen("date").read()
#print photons_mod_label
#print len(photons_mod_label);sys.exit()
apa_num=1
apa_mod=0
for ch_i in range(0,208,4):
   if ch_i==48 or ch_i==96 or ch_i==144 or ch_i==192 or ch_i==240:apa_num+=1;
   if ch_i in empty_ch:continue
   if apa_mod==10:apa_mod=0
   if ch_i== 108 or ch_i==196 or ch_i==204:apa_mod+=1;
   if ch_i==192: apa_mod+=4
   print apa_num,range(ch_i,ch_i+4), apa_mod
   if apa_num==5:break
   for er in range(ch_i,ch_i+4):
      if er in Bad_channels:continue;
      else: eval("apa"+str(apa_num)+"_mod_"+str(apa_mod)+".append("+str(er)+")")
   apa_mod+=1

## Start reading in Dante's output root files based on Run Number
for r_i in range(len(runs)): 
   RunNum=runs[r_i]
   print "%%%%%%%%%%%%%% Working on Run ",RunNum,"   :  "+ str(r_i)+"/"+str(len(runs))+"     %%%%%%%%%%%%%%%%%%%%"
### Reading file from local directory
  # if dir_=="Dante" or dir_=="dante":
  #    myfile = TFile.Open('/dune/app/users/dtotani/6APA/'+str(sub_direct)+'GeV/output_beam_run'+str(RunNum)+'_done.root')
  # else:
  #    myfile = TFile.Open('./'+str(sub_direct)+'GeV/output_beam_run'+str(RunNum)+'_Chris.root')
   myfile = TFile.Open('/pnfs/dune/persistent/users/pds/protodune/runsummaries/root/Run'+str(RunNum)+'RawDecoderTFile.root')
   ttree_dir = myfile.Get("sspmonitor")
   ttree = ttree_dir.Get('PDwfm')
   ttree.Print();
   #ttree.Scan()
   ttree_labels = ["Run",'Event','TS','PH','Amp','Ped','TMax','BeamInt','PulserInt','AllInt','AllWindow','BeamWindow','PulserWindow','Chan']
#"run","eventNumber","time","TOF","CKov0pressure","CKov1pressure","CKov0status","CKov1status","Track_index","RDTSTrigger","Shower_index","Integral","BG"]
   ## Making ntuple labels for new ntuple output
   ntuple_labels = ["Type","Run",'Event','TS','PH','Amp','Ped','TMax','BeamInt','PulserInt','AllInt','AllWindow','BeamWindow','PulserWindow','module']
#"run","eventNumber","time","TOF","CKov0pressure","CKov1pressure","CKov0status","CKov1status","Track_index","RDTSTrigger","Shower_index","Photon","BG","module"]
   entries = ttree.GetEntries()
   for p in ntuple_labels[:-1]: # -1 because last element is Channel
      exec(str(p)+"_ch=[]")
   ## Going through Dante's root file, saving each parameter value per Channel
   photon_val=[]
   BG_photon_val=[]
   for module in range(len(photons_mod_label)):
      if  int(module)==23:continue
      chan_len=len(eval(photons_mod_label[module]))
      ph=0.
      bg=0.
      ch_count=0
      for p in ttree_labels[:-2]:# -2 because I am looping through the Integral & BG
         exec(str(p)+"_i=[]")
      photon_val=[]
      BG_photon_val=[]

      for Chan in range(4):
      #for Chan in AllChannels:
      #for Chan in range(4):
         ## Creating temp list to gather all information per channel 1D-list
   #      event_num=[]
   #      event_time=[]
         if Chan >207:
            conv_to_photons=float(999999999)
         elif Chan in empty_ch:
            conv_to_photons=float(999999999)
         elif Chan in range(132,144):
            conv_to_photons=float(adc_photon_arapuca[ch_arapuca.index(Chan)])
         else:
         #   print Chan
            conv_to_photons=float(calib_ADC_Photon_ch[Channels.index(Chan)])
         #conv_to_photons=float(1)# just added here to look at ADC values in Leons post macro
         event_counter=[]
         event_bleh =[]
         for event in ttree:#myfile.t1 :
         #for event in myfile.t1 :
   
            if Chan in eval(photons_mod_label[module]) and int(Chan) ==int(event.Chan):
#               print Chan, event.Chan, event.Event
               event_counter.append(int(event.Event))
#               if int(event.Event) == 535 and Chan <4: 
#                  event_bleh.append(float(event.BeamInt))
               new_ped = ( event.AllInt - event.BeamInt + (event.AllWindow - event.BeamWindow)*event.Ped ) / (event.AllWindow - event.BeamWindow)
               corr_BeamInt = event.BeamInt + event.BeamWindow *(event.Ped - new_ped)
               Int_photons = float(corr_BeamInt) / conv_to_photons
               ph+=Int_photons ; ch_count+=1
#               print Chan,Int_photons;
#               print Chan, event.Event, corr_BeamInt,conv_to_photons, ph;sys.exit()
               ##exec("ph+=(event.Integral_DAQch_"+str(Chan)+"/conv_to_photons);ch_count+=1")
               #exec("ph+=(event.Integral_DAQch_"+str(Chan)+"/conv_to_photons);ch_count+=1")
               #exec("bg+=(event.BG_Int_DAQch_"+str(Chan)+"/conv_to_photons);")

#############added to check first module total count
#            if Chan==4:
#               print Chan,conv_to_photons, ph;sys.exit()
#               print sys.exit()
            if ch_count==chan_len:
               for p in ttree_labels[:-2]: 
                  eval(str(p)+"_i.append(event."+str(p)+")")
               photon_val.append(ph*(4./float(chan_len)))
#               BG_photon_val.append(bg*(4./float(chan_len)))
               ph=0.;ch_count=0.;            
#         print len(event_counter), entries
#         print sys.exit()
      ## Appending to 2D-list   
#   ntuple_labels = ["Type","Run",'Event','TS','PH','Amp','Ped','TMax','BeamInt','PulserInt','AllInt','AllWindow','BeamWindow','PulserWindow','module']
      for p in ntuple_labels[:-3]:# -3 because I have Photon & BG_Photon appended below and last element is Channel
         eval(str(p)+"_ch.append("+str(p)+"_i)")
      Photon_ch.append(photon_val)
      BG_ch.append(BG_photon_val)
   for p in ntuple_labels[:-1]: # -1 because last element is Channel
      print str(p)+"_ch",len(eval(str(p)+"_ch"))
   print "Photon_ch",len(Photon_ch)
   print "BG_ch",len(BG_ch)
   print "mod_list",len(mod_list)
   myfile.Close() # Closing Dante's file
   long_string= '_ch[MOD][i],'.join(ntuple_labels[:-1])+'_ch[MOD][i]' 
  ## Making Output root file w/ ntuple##
   Output_file= TFile("/dune/app/users/cmacias/LArSoft_v08_15_01/Beamcode_Dante/ntuple_outputRuns/"+str(dir_)+"/BeamNtuple_output_Run"+str(RunNum)+"_"+str(dir_)+".root","RECREATE")
   Output_TNtuple= TNtuple('ntuple',"Data from "+str(RunNum),':'.join(ntuple_labels))
   for MOD in range(len(mod_list)):
#   for Chan in AllChannels:
   #for Chan in range(4):
      for i in range(len(photon_val)):
         exec("Output_TNtuple.Fill(*["+str(long_string)+",mod_list[MOD]"+"])")
   Output_TNtuple.Write()
   Output_file.Close()
sys.exit()

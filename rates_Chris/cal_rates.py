import matplotlib.pyplot as plt
import numpy as np
#import psycopg2
import csv
#import datetime
import time
import argparse
import os
import code
from ROOT import TH1F,TH2F,gROOT,TCanvas,TFile,gPad
import sys
gs=[]
# When ROOT objects get garbage-collected they disappear from the screen
# again. Need to leak them like in C++
def New(cons, *args):
    ret = cons(*args)
    gs.append(ret)
    return ret
Bad_channels =[25, 36, 58, 62, 65, 73, 75, 82, 101, 110, 119, 125, 156, 160]
#%%%%%%%%%%%%%%%%%%%% loop through runs here %%%%%%%%%%%%%%%%%%%%%%%%%%
#RunNum=5888
arg_len=len(sys.argv)
if arg_len <3:
   print "Please enter \"python -b\" and at least one run number. For multiple runs, use a space as the delimitter., final argument is Beam/Pulser"
   print "For Example: \"python python cal_rates.py -b 6624 7528 7529 \""
   sys.exit() 
arg_list=[int(sys.argv[i]) for i in range(2,arg_len)]
print arg_list
arg_list.sort()
print arg_list
runs=[str(i) for i in arg_list]
for r_i in range(len(runs)):
   RunNum=runs[r_i]
#for RunNum in [4600]: #5888
#for RunNum in [4581,4583,4586,4589,4593,4594,4595,4600,4604,4609,4631]:
   print "%%%%%%%%%%%%%% Working on Run ",RunNum, "%%%%%%%%%%%%%%%%%%%%"

### Old directory I used to get data from
###   myfile = TFile.Open('/dune/data/users/mualem/protoDUNE/intOffby1/Run'+str(RunNum)+'RawDecoderTFile.root')
   myfile = TFile.Open('/pnfs/dune/persistent/users/pds/protodune/runsummaries/root/Run'+str(RunNum)+'RawDecoderTFile.root')
   #TH2F *maxpedvals = myfile.FindObjectAny("MaxPedVals vs. Channel")
   t1 = myfile.Get("sspmonitor")
   ntuple=t1.Get("PDwfm")
   #starting my txt file output
   text_file_indiv = open("cdf_Calibrated_Intval_"+str(RunNum)+".txt", "w") 
   bin_size=100 # this is for CDF, also, helping with the adc/pe error, when trying to find CDF values for int PEs
   #ntuple.Print()
   #ChanNum=96
   # Making a list of all channel numbers for APA 1-3
   Channels=range(0,208)
   for uu in range(40,48):
       Channels.remove(uu)
   for uu in range(88,96):
       Channels.remove(uu)
#   for uu in range(132,144):
#       Channels.remove(uu)
   for uu in range(184,192):
       Channels.remove(uu)

#### calibrations for SensLs- first three APAs at the moment, by channel order above- currently not used
   calib_ADC_Avalanche_ch=[1585.75, 1595.02, 1588.62, 1627.83, 1594.07, 1591.99, 1593.12, 1590.6, 1555.83, 1588.16, 1574.33, 1576.55, 1561.16, 1535.62, 1551.06, 1554.26, 1567.53, 1570.21, 1587.21, 1712.37, 1528.0, 1564.09, 1542.86, 1555.29, 1582.26, 99999999.0, 1580.84, 1549.25, 1590.8, 1576.32, 1562.32, 1605.0, 1594.64, 1697.21, 1554.42, 1555.76, 99999999.0, 1529.56, 1538.75, 1558.99, 1589.4, 1817.46, 1572.45, 1841.61, 1530.65, 1576.78, 1571.13, 1594.26, 1548.57, 1559.18, 99999999.0, 1543.5, 1577.9, 1577.07, 99999999.0, 1597.91, 1587.24, 99999999.0, 1563.0, 1594.78, 1592.74, 1563.09, 1533.01, 1580.67, 1569.16, 99999999.0, 1579.86, 99999999.0, 1594.44, 1714.15, 1592.27, 1584.65, 1584.55, 1559.67, 99999999.0, 1553.73, 1587.9, 1570.09, 1567.89, 1573.0, 1549.35, 1590.3, 1574.06, 1570.38, 1580.5, 99999999.0, 1594.68, 1586.22, 1720.03, 1577.49, 1711.62, 1712.25, 1562.98, 1586.57, 99999999.0, 1546.62, 1579.77, 1573.27, 1567.41, 1576.85, 1590.74, 1587.57, 1587.14, 99999999.0, 1709.4, 1553.58, 1588.15, 1576.56, 1685.94, 1859.2, 1734.66, 1705.93, 1573.91, 1563.66, 1568.62, 1592.2, 1600.09, 1578.4, 1615.34, 1578.02, 1574.26, 1596.53, 1608.19, 1568.61, 1568.17, 1573.99, 1568.68, 1551.96, 99999999.0, 1594.35, 1601.11, 1577.0, 99999999.0, 1550.02, 1578.9, 1563.75, 1568.08, 1570.87, 1581.89, 1584.56, 1565.42, 1589.2, 1582.63, 1571.7, 1747.53, 1618.93, 1586.41, 1751.84, 1835.31, 1579.94, 1555.0, 1596.82, 1697.18, 1591.97, 1568.05, 1578.05, 1580.45, 1589.44, 1572.44, 1563.93, 1612.54, 1599.95, 1544.78, 1579.91, 1596.85, 1718.35, 1617.39, 1573.39, 1608.3, 1628.96, 1617.57, 1600.4]
   #
   ch_arapuca =[132,	133,	134,	135,	136,	137,	138,	139,	140,	141,	142,	143,	264,	265,	266,	267,	268,	269,	270,	271,	272,	273,	274,	275]
   adc_photon_arapuca = [1153,	1068,	1105,	1184,	1152,	857,	972,	783,	822,	793,	1045,	1096,	894,	956,	925,	779,	965,	722,	774,	885,	779,	965,	995,	1035]
   Channels_sensl=range(0,208)
   for uu in range(40,48):
       Channels_sensl.remove(uu)
   for uu in range(88,96):
       Channels_sensl.remove(uu)
   for uu in range(132,144):
       Channels_sensl.remove(uu)
   for uu in range(184,192):
       Channels_sensl.remove(uu)
   print len(calib_ADC_Avalanche_ch)
   calib_PE_Photon_ch = [1.31864769413142, 1.3222062871376967, 1.3145245909075225, 1.2983297840467523, 0.6026930806242735, 0.3625731120423674, 0.3156150144680083, 0.5596963201089908, 1.156058212986452, 0.9780505937156371, 1.027099272305324, 1.1738429619808322, 0.0010945105963543337, 0.0007111062933356863, 0.0008649422120712251, 0.0032157873896678205, 1.3335801574021064, 1.309284900908437, 1.268864675685497, 1.2462202285037758, 0.3869321472593093, 0.04037896007473809, 0.04174124082421995, 0.13957602354560808, 1.2613130586653674, 0.0, 1.2390648729825278, 1.303085336510339, 0.16128998115011048, 0.10371528398898436, 0.1160367520674321, 0.2892516062090161, 1.2910499134256124, 1.2739226252824152, 1.3104391768667616, 1.3227989127204312, 0.0, 1.2189977847187645, 1.24367724237895, 1.2432506438319186, 1.2965976108347017, 1.3362648203133614, 1.2800840071402075, 1.3203238583634485, 1.352188109956931, 1.358425721288801, 1.3608928439134316, 1.2757995781961462, 1.331647578833712, 1.3299297217283788, 0.0, 1.3302548856494112, 0.9869994014044838, 0.9551280622036993, -0.0, 1.3172002376273535, 1.3815448874495826, -0.0, 1.3969870441292451, 1.4067524316981415, 0.2594469948184602, 0.24503213997084725, 0.32184095641028626, 1.0763994173233344, 1.3757575956376202, -0.0, 1.3833211583414962, -1.207997046444396e-05, 1.2001746883597024, 1.2029993297685717, 1.2160559503759067, 1.2511141852029548, 1.2923836396485913, 1.294127766361399, 0.0, 1.2786583768660804, 1.2558197878928805, 1.2883433986788984, 1.2796115943071678, 1.2756501397156985, 1.2997173303642926, 1.3039658022283784, 1.298929006952764, 1.298177054830344, 1.2318544704587655, 0.0002588910550500434, 1.227408008916664, 1.2315782649486335, 1.3284898758389305, 1.292115120189456, 1.3195433703903796, 1.31691660130858, 1.3353751475444136, 1.3697229234721895, -0.0, 1.3640599441828094, 1.1942574002889335, 1.1410116428592456, 1.1651721444909362, 1.2364764933529313, 1.3679024433398168, 1.3697117454203156, 1.3517444335893922, 0.0, 1.1697225519931371, 1.035141056603562, 1.0388476188377298, 1.1860329598638968, 1.2908551363328093, 1.3010356043935163, 1.3152835511820347, 1.299689783890721, 1.2777820562599, 1.281003079783665, 1.2838722106448777, 1.2725820272786341, 1.205901022131409, 1.2143440902919447, 1.2189701109577902, 1.2186291735320187, 1.299417930457352, 1.3126699973279117, 1.3199184388735272, 1.3056317121727372, 1.4003741604502533, 1.4651860711617992, 1.4435590447687991, 1.3835344533256497, 0.0, 1.385264838182425, 1.3948059018536363, 1.3795356897825883, 6.361591847599354e-05, 0.9728135369459245, 0.987172213949882, 1.2383032755079026, 1.4848223519179393, 1.5018374160317185, 1.4361109913154089, 1.4557686766315303, 0.005048739833121254, 0.00142324109172891, 0.0017325673745176315, 0.01855629462119881, 1.138963547032604, 0.7423422228678944, 0.8365362650921733, 1.1969112961181207, 1.2594898321130772, 1.222791546866036, 1.2674476337693708, 1.306435925089415, 1.0735544647587552, 1.4072537426819909, 0.9300366646602494, 1.1104264836999096, 1.439125304385866, 1.350032321881117, 1.3632402491991942, 1.4213188157451597, 0.737033594778227, 0.23654711395077987, 0.32885197939882505, 0.7104864347969025, 1.2991868749767266, 1.2815796281493128, 1.1486850663363373, 1.4327114203298923, 1.3359993647736832, 1.345681710227898, 1.3481721294260145, 1.3221401679288276]
   calib_ADC_Photon_ch = [calib_ADC_Avalanche_ch[pl]*calib_PE_Photon_ch[pl] for pl in range(len(calib_ADC_Avalanche_ch))]

   print len(calib_PE_Photon_ch);
   print len(calib_ADC_Photon_ch)#;sys.exit()
#   print calib_ch[26], Channels[26]
#   sys.exit()

#   for i_ in [0]:#range(len(Channels)):
   for i_ in range(len(Channels)):
      ## only starting the open txt file for indiv. channels
   #   text_file_indiv = open("cdf_Intval_"+str(RunNum)+"_ch"+str(ChanNum)+".txt", "w") 
   
      ChanNum=Channels[i_]
      chan_index = Channels.index(ChanNum)
#      adc_pe=calib_ch[chan_index]
      if ChanNum in Bad_channels: adc_pe=99999999999.
      elif ChanNum in ch_arapuca:adc_pe =adc_photon_arapuca[ch_arapuca.index(int(ChanNum))]

      else: adc_pe=calib_ADC_Photon_ch[Channels_sensl.index(int(ChanNum))]
      print ChanNum, adc_pe
   
      ## for loop for all channels should start here ##############
      c1 = New(TCanvas,"c1","c1",67,52,700,500)
      HistoTitle = "Int "+str(ChanNum)
      Event_hist= New(TH1F,HistoTitle,HistoTitle,600,-10000,50000)
   #   Event_hist= New(TH1F,HistoTitle,HistoTitle,530,-3000.0,50000)
      ntuple.Draw("BeamInt + BeamWindow*( Ped - (( AllInt - BeamInt + (AllWindow-BeamWindow)*Ped )/ (AllWindow-BeamWindow)) ) >>"+str(HistoTitle),"Chan =="+str(ChanNum))
###   Older way of calculating integration regime
###     ### Pulling in Integral histograms
###      ntuple.Draw("(BeamInt-Ped)+1276.*(Ped-+(AllInt-(BeamInt-Ped)+Ped*(726.0))/726.0)>>"+str(HistoTitle),"Chan =="+str(ChanNum))#,"goff")#+str(ChanNum))
###      #%%%%%%%%%%%%This one below seemed to work. %%%
###      #ntuple.Draw("(PulserInt-Ped -(501./726.)*(AllInt-BeamInt-Ped))>>"+str(HistoTitle),"Chan =="+str(ChanNum))#,"goff")#+str(ChanNum))
###      
###      #ntuple.Draw("(PulserInt-Ped -(501./726.)*(AllInt-BeamInt))>>"+str(HistoTitle),"TMax>1050 && TMax < 1550 && Chan =="+str(ChanNum))#,"goff")#+str(ChanNum))
###      #ntuple.Draw("PulserInt>>"+str(HistoTitle)," Chan =="+str(ChanNum))#,"goff")#+str(ChanNum))
###      
      #gPad.SetLogy(1);
      gPad.Update()
      print Event_hist.Integral()
      #ntuple.Draw("Event>>"+str(HistoTitle),"PulserInt>"+str(int(int(ph)))+" && Chan =="+str(ChanNum))#,"goff")#+str(ChanNum))
      
      #time.sleep(30)
      Event_hist.Draw()
   #   gPad.SetLogx(1);
      gPad.SetLogy(1);
      gPad.Update()
      outfile = "EventHist_Run_"+str(RunNum)+"_ch"+str(ChanNum)+".png";
      c1.Print(outfile);
      c1.Clear()
      c1.Clear()
      gPad.Update()
      
      HistoTitle_CDF = HistoTitle+ "_CDF"
      HistoTitle_PDF = HistoTitle+ "_PDF"
         
#      CDF_ch = New(TH1F,HistoTitle_CDF,HistoTitle_CDF,600,-1000,5000); #1000,0.0,10000.0);
      CDF_ch = New(TH1F,HistoTitle_CDF,HistoTitle_CDF,10000,0.0,1000.0);
      PDF_ch = New(TH1F,HistoTitle_PDF,HistoTitle_PDF,18011,0.0,16011.0);
      CDF_ch_py=[]
      adc_val_ch_corr=[]
      #// Adding this section to calculate the CDF //
      n_samp= Event_hist.Integral() #*1.67245873154
      print "This is  n_samp--->",n_samp

      ## Start counting (1-CDF) as sum_of_elems
      sum_of_elems=0.;
      
      
      check_one=0.;
#      bin_PhC=Event_hist.GetNbinsX()-1
      bin_PhC=599 #Event_hist.GetNbinsX()-1
      print bin_PhC
      text_file_indiv.write(str(ChanNum) + ",")
      how_many_samples = 10000 # this is how many samples I went negative in CDF hist
      while(bin_PhC >=0):
      #       //   Finding the probability of each ADC value, per bin
         q_i= Event_hist.GetBinContent(bin_PhC)/n_samp;
      #  #   print q_i
#         adc_val = 100.*(Event_hist.GetBinCenter(bin_PhC) -50)/adc_pe # 100* to make 100*PE for fractional-integer purposes. The " -50" needs to be checked
         adc_val = Event_hist.GetBinCenter(bin_PhC) -50#/adc_pe #;//+10.;
      #  ##  // Summing up probability to calculate the CDF, as a function of ADC value
         sum_of_elems+=(q_i);
      #     PDF_ch.SetBinContent(int(adc_val),q_i);
#         CDF_ch.SetBinContent(adc_val,sum_of_elems);
         CDF_ch.SetBinContent(int(adc_val),sum_of_elems);

         # only saving values above Zero
         if int(adc_val)<how_many_samples and int(adc_val)>=0:
            #print "adc val: ",int(adc_val),"CDF_vals: ",sum_of_elems    
            CDF_ch_py.append(sum_of_elems)
            adc_val_ch_corr.append(int(adc_val))
         check_one+=q_i;
         bin_PhC-=1
      print "This should be 1.0 ------->",check_one

      ##### reversing lists to make into  ascending order
      CDF_ch_py.reverse()
      adc_val_ch_corr.reverse()
#      print adc_val_ch_corr;sys.exit()
      
      num_cdf_val= len(CDF_ch_py)
      print "length of cdf_pe_vals: ", len(CDF_ch_py)
      #saving values to txt file
      ### This is here for bad channels. If channel is dead/bad, the length of CDF is all screwed up. This just gives a adc_val range and cdf vals of Zero.
      #if num_cdf_val!=(599-100):
      #   num_cdf_val=int(599-100)
      #   adc_val_ch_corr=[0+6*j for j in range(num_cdf_val)]
      #   CDF_ch_py=[0. for j in range(num_cdf_val)]
      #   print "Channel ",ChanNum,"Not enough bin output"
      #   print "now num_cdf =", num_cdf_val,"now cdf is", len(CDF_ch_py)
      #else:
      #   print ''
      text_file_indiv.write(str(num_cdf_val) + ",")  
      for u in range(len(CDF_ch_py)):
      #   print "adc val: ",adc_val_ch_corr[u],"CDF_vals: ",CDF_ch_py[u]   
         text_file_indiv.write(str(adc_val_ch_corr[u]) + ", ")
      for u in range(len(CDF_ch_py)-1):
         text_file_indiv.write(str(CDF_ch_py[u]) + ", ")
      text_file_indiv.write(str(CDF_ch_py[len(CDF_ch_py)-1]) + "\n")
   
   
   
      CDF_ch.GetXaxis().SetTitle("[ADC]");
      CDF_ch.Draw()
      gPad.SetLogx(1);
      gPad.SetLogy(1);
      gPad.Update()
      outfile = "Calibrated_CDF_Run_"+str(RunNum)+"_ch"+str(ChanNum)+".png";
      c1.Print(outfile);
      c1.Clear()
      c1.Close()
   text_file_indiv.close() 


sys.exit()
#print 'Ctrl-D to quit'
code.interact(local = locals(), banner='')
time.sleep(130)

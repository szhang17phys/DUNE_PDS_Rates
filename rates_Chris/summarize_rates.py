#_author__ = 'ctmacias'
#import numpy as np
#import matplotlib.pyplot as plt
#from scipy.stats import *
import sys
import os
#from os import walk
#formatting_function = np.vectorize(lambda f: format(f, '.5E'))
#import shutil
from matplotlib.ticker import MultipleLocator, AutoMinorLocator
## import pylab as pl
#from scipy.optimize import curve_fit
minorLocator = AutoMinorLocator()
majorLocator = AutoMinorLocator()
#from scipy.odr import *
import matplotlib.pyplot as plt
import matplotlib.colors as colors
import numpy as np


Bad_channels =[25, 36, 58, 62, 65, 73, 75, 82, 101, 110, 119, 125, 156, 160]
ch_arapuca =[132,	133,	134,	135,	136,	137,	138,	139,	140,	141,	142,	143,	264,	265,	266,	267,	268,	269,	270,	271,	272,	273,	274,	275]
adc_photon_arapuca = [1153,	1068,	1105,	1184,	1152,	857,	972,	783,	822,	793,	1045,	1096,	894,	956,	925,	779,	965,	722,	774,	885,	779,	965,	995,	1035]
adc_avalanche_arapuca =[780,	734,	763,	777,	813,	665,	739,	614,	638,	639,	781,	803,	743,	744,	743,	622,	815,	647,	684,	747,	639,	780,	753,	827]

runs =[4600]
# runs =[4583, 4600, 5723, 5727, 6212, 6221, 6508, 7198]
# runs = [4581, 4583, 4586, 4589, 4593, 4595, 4600, 4604, 4609, 4631]#, 5700, 5702]
# runs = [4600]#[4600]#, 4583, 4586, 4589, 4593, 4594, 4595, 4600, 4604, 4609, 4631, 5700, 5702]
# runs = [4600, 4583]#, 4586, 4589, 4593, 4594, 4595, 4600, 4604, 4609, 4631, 5700, 5702]
# runs = [4593, 4594, 4595, 4600, 4604, 4609, 4631]
# runs = [4581, 4583, 4586, 4589, 4593, 4594, 4595, 4600, 4604, 4609, 4631]#, 5700, 5702]
calib_ADC_Avalanche_ch = [1585.75, 1595.02, 1588.62, 1627.83, 1594.07, 1591.99, 1593.12, 1590.6, 1555.83, 1588.16, 1574.33, 1576.55, 1561.16, 1535.62, 1551.06, 1554.26, 1567.53, 1570.21, 1587.21, 1712.37, 1528.0, 1564.09, 1542.86, 1555.29, 1582.26, 99999999.0, 1580.84, 1549.25, 1590.8, 1576.32, 1562.32, 1605.0, 1594.64, 1697.21, 1554.42, 1555.76, 99999999.0, 1529.56, 1538.75, 1558.99, 1589.4, 1817.46, 1572.45, 1841.61, 1530.65, 1576.78, 1571.13, 1594.26, 1548.57, 1559.18, 99999999.0, 1543.5, 1577.9, 1577.07, 99999999.0, 1597.91, 1587.24, 99999999.0, 1563.0, 1594.78, 1592.74, 1563.09, 1533.01, 1580.67, 1569.16, 99999999.0, 1579.86, 99999999.0, 1594.44, 1714.15, 1592.27, 1584.65, 1584.55, 1559.67, 99999999.0, 1553.73, 1587.9, 1570.09, 1567.89, 1573.0, 1549.35, 1590.3, 1574.06, 1570.38, 1580.5, 99999999.0, 1594.68, 1586.22, 1720.03, 1577.49, 1711.62, 1712.25, 1562.98, 1586.57, 99999999.0, 1546.62, 1579.77, 1573.27, 1567.41, 1576.85, 1590.74, 1587.57, 1587.14, 99999999.0, 1709.4, 1553.58, 1588.15, 1576.56, 1685.94, 1859.2, 1734.66, 1705.93, 1573.91, 1563.66, 1568.62, 1592.2, 1600.09, 1578.4, 1615.34, 1578.02, 1574.26, 1596.53, 1608.19, 1568.61, 1568.17, 1573.99, 1568.68, 1551.96, 99999999.0, 1594.35, 1601.11, 1577.0, 99999999.0, 1550.02, 1578.9, 1563.75, 1568.08, 1570.87, 1581.89, 1584.56, 1565.42, 1589.2, 1582.63, 1571.7, 1747.53, 1618.93, 1586.41, 1751.84, 1835.31, 1579.94, 1555.0, 1596.82, 1697.18, 1591.97, 1568.05, 1578.05, 1580.45, 1589.44, 1572.44, 1563.93, 1612.54, 1599.95, 1544.78, 1579.91, 1596.85, 1718.35, 1617.39, 1573.39, 1608.3, 1628.96, 1617.57, 1600.4]
# BADcalib_PE_Photon_ch = [1.31864769413142, 1.3222062871376967, 1.3145245909075225, 1.2983297840467523, 0.6026930806242735, 0.3625731120423674, 0.3156150144680083, 0.5596963201089908, 1.156058212986452, 0.9780505937156371, 1.027099272305324, 1.1738429619808322, 0.0010945105963543337, 0.0007111062933356863, 0.0008649422120712251, 0.0032157873896678205, 1.3335801574021064, 1.309284900908437, 1.268864675685497, 1.2462202285037758, 0.3869321472593093, 0.04037896007473809, 0.04174124082421995, 0.13957602354560808, 1.2613130586653674, 0.0, 1.2390648729825278, 1.303085336510339, 0.16128998115011048, 0.10371528398898436, 0.1160367520674321, 0.2892516062090161, 1.2910499134256124, 1.2739226252824152, 1.3104391768667616, 1.3227989127204312, 0.0, 1.2189977847187645, 1.24367724237895, 1.2432506438319186, 1.2965976108347017, 1.3362648203133614, 1.2800840071402075, 1.3203238583634485, 1.352188109956931, 1.358425721288801, 1.3608928439134316, 1.2757995781961462, 1.331647578833712, 1.3299297217283788, 0.0, 1.3302548856494112, 0.9869994014044838, 0.9551280622036993, -0.0, 1.3172002376273535, 1.3815448874495826, -0.0, 1.3969870441292451, 1.4067524316981415, 0.2594469948184602, 0.24503213997084725, 0.32184095641028626, 1.0763994173233344, 1.3757575956376202, -0.0, 1.3833211583414962, -1.207997046444396e-05, 1.2001746883597024, 1.2029993297685717, 1.2160559503759067, 1.2511141852029548, 1.2923836396485913, 1.294127766361399, 0.0, 1.2786583768660804, 1.2558197878928805, 1.2883433986788984, 1.2796115943071678, 1.2756501397156985, 1.2997173303642926, 1.3039658022283784, 1.298929006952764, 1.298177054830344, 1.2318544704587655, 0.0002588910550500434, 1.227408008916664, 1.2315782649486335, 1.3284898758389305, 1.292115120189456, 1.3195433703903796, 1.31691660130858, 1.3353751475444136, 1.3697229234721895, -0.0, 1.3640599441828094, 1.1942574002889335, 1.1410116428592456, 1.1651721444909362, 1.2364764933529313, 1.3679024433398168, 1.3697117454203156, 1.3517444335893922, 0.0, 1.1697225519931371, 1.035141056603562, 1.0388476188377298, 1.1860329598638968, 1.2908551363328093, 1.3010356043935163, 1.3152835511820347, 1.299689783890721, 1.2777820562599, 1.281003079783665, 1.2838722106448777, 1.2725820272786341, 1.205901022131409, 1.2143440902919447, 1.2189701109577902, 1.2186291735320187, 1.299417930457352, 1.3126699973279117, 1.3199184388735272, 1.3056317121727372, 1.4003741604502533, 1.4651860711617992, 1.4435590447687991, 1.3835344533256497, 0.0, 1.385264838182425, 1.3948059018536363, 1.3795356897825883, 6.361591847599354e-05, 0.9728135369459245, 0.987172213949882, 1.2383032755079026, 1.4848223519179393, 1.5018374160317185, 1.4361109913154089, 1.4557686766315303, 0.005048739833121254, 0.00142324109172891, 0.0017325673745176315, 0.01855629462119881, 1.138963547032604, 0.7423422228678944, 0.8365362650921733, 1.1969112961181207, 1.2594898321130772, 1.222791546866036, 1.2674476337693708, 1.306435925089415, 1.0735544647587552, 1.4072537426819909, 0.9300366646602494, 1.1104264836999096, 1.439125304385866, 1.350032321881117, 1.3632402491991942, 1.4213188157451597, 0.737033594778227, 0.23654711395077987, 0.32885197939882505, 0.7104864347969025, 1.2991868749767266, 1.2815796281493128, 1.1486850663363373, 1.4327114203298923, 1.3359993647736832, 1.345681710227898, 1.3481721294260145, 1.3221401679288276]
calib_PE_Photon_ch = [1.4126430695182026, 1.4006449431694799, 1.3878747224010952, 1.4280384757532598, 1.185022547422883, 1.186352369348883, 1.1758355264180493, 1.181625241230633, 1.3664132291969349, 1.3523466245350817, 1.3863813662653377, 1.3820280363103419, 1.2100936937622748, 1.1926488325228475, 1.166773622149775, 1.1964983285387456, 1.3795231612656054, 1.3362544111395196, 1.3512221729146756, 1.420220362811809, 1.220829353791607, 1.220655018152973, 1.222912626282276, 1.2086984627725916, 1.3279071231028676, 10000000000.0, 1.3192914529810806, 1.32335710492287, 1.2178592659326009, 1.2203530216428102, 1.2188316009735298, 1.2313848964565905, 1.3181406072998099, 1.3760141447157346, 1.3111758326415797, 1.3122231701084452, 10000000000.0, 1.209155402169935, 1.198612998224154, 1.20515523309421, 1.3439645853941715, 1.4850901741907676, 1.3065163969045523, 1.465787725582078, 1.2256408388796185, 1.235425395781877, 1.2257570841575671, 1.2173598297961232, 1.3188955310034693, 1.3241719725819916, 10000000000.0, 1.237552878249943, 1.1695109665642507, 1.1744845457253708, 10000000000.0, 1.1929995992800138, 1.360413865089201, 10000000000.0, 1.3376860393924377, 1.340222639038174, 1.2588606395339457, 1.2763486214301434, 1.2899488305793958, 1.2747758611633246, 10000000000.0, 1.3016142483520656, 1.2810716350302742, 10000000000.0, 1.2980323409381538, 1.2820907816391311, 1.3069571690831912, 1.2859131188303687, 1.3141236347338188, 1.3111583352594673, 10000000000.0, 1.3012498051965924, 1.2281420148878768, 1.239712206299814, 1.2483571183388467, 1.231825616983547, 1.2785518539521004, 1.292858862836752, 1.2931883601261052, 1.2856247977051716, 1.2286502587258998, 10000000000.0, 1.220619754426727, 1.2251631525544684, 1.3551816929628346, 1.3135420013268602, 1.3413934199179152, 1.3448574964610382, 1.309162800360985, 1.2902811685087803, 10000000000.0, 1.3144181250562461, 1.2039746406100258, 1.2179707716893684, 1.2232233009506421, 1.239241811163499, 1.3306810805087887, 1.3044448650710523, 1.3082530433843111, 10000000000.0, 1.2553165386489094, 1.221040133280749, 1.1793367353071282, 1.21525774937779, 1.423437892315113, 1.4593070350087634, 1.390138650653633, 1.3965840197328665, 1.2377228589020963, 1.2227206029740612, 1.2439043942708432, 1.235466013982504, 1.1596472079381557, 1.1826476438324562, 1.1834440598913651, 1.1749501976972254, 1.3470283494858035, 1.3273469701443183, 1.3375870827262613, 1.3255450853997357, 1.2265382059183128, 1.242088445847263, 1.2264332669361386, 1.2153406989901145, 10000000000.0, 1.2927901896579428, 1.3076366288325245, 1.3004719180012512, 10000000000.0, 1.408412209338035, 1.355740746213033, 1.248978478328936, 1.2986300614938673, 1.2761278119832034, 1.299053007227065, 1.3031640760446095, 1.27333745751015, 1.2899024999034638, 1.3106641122990939, 1.2583383482210118, 1.3399717345000552, 1.300479178457047, 1.2892622461764613, 1.3321080323552814, 1.3456345778450383, 1.2836887653119438, 1.2786683780724184, 1.2832352334424384, 1.2510879728857287, 1.2704979820133029, 1.2587566749613968, 1.2674865376828923, 1.3946563165605779, 1.3937508391824676, 1.413499941389469, 1.293988806834509, 1.2547118342431276, 1.2747367332366852, 1.2890150223867227, 1.26727520938633, 1.3178309915663564, 1.336378985917566, 1.3217581882276872, 1.3136199620167408, 1.2985625926483906, 1.305201438798312, 1.306984781610701, 1.3104070494351854]
calib_ADC_Photon_ch = [calib_ADC_Avalanche_ch[pl]*calib_PE_Photon_ch[pl] for pl in range(len(calib_ADC_Avalanche_ch))]
Channels=range(0,208)
for uu in range(40,48):
    Channels.remove(uu)
for uu in range(88,96):
    Channels.remove(uu)
for uu in range(132,144):
    Channels.remove(uu)
for uu in range(184,192):
    Channels.remove(uu)
# for uu in range(208,216):
#     Channels.remove(uu)
# print len(Channels)
# print len(Bad_channels)
# # sys.exit()
# print len(calib_ADC_Avalanche_ch)
# print len(calib_PE_Photon_ch);
# print len(calib_ADC_Photon_ch);sys.exit()

apa1_funct_run = []
apa2_funct_run = []
apa3_funct_run = []
apa1_per_run = []
apa2_per_run = []
apa3_per_run = []
# adc_sample_bin=11
# samp_range = range(0, 20)
text_file_indiv = open("Freq_Calibrated_output.txt", "w")
# text_file_indiv = open("Freq_output.txt", "w")
## Will use these to append to later for summarize plots
apa1_mod=[]
apa2_mod=[]
apa3_mod=[]


###############################
# Need to add this to correct for BAD Channels
mod_corr = [0] * 36 # will add +1 for every bad channel in module number
print mod_corr
for ch_check in Channels:
    if ch_check in Bad_channels:
        for apamod_num in range(10):
            if ch_check>= 0 and ch_check< 40 and (ch_check/ 4. - apamod_num) < 1 and (ch_check/ 4. - apamod_num) >= 0:
                print apamod_num, ch_check, (ch_check/ 4. - apamod_num);
                mod_corr[(apamod_num)] += 1
            elif ch_check> 47 and ch_check< 88 and (ch_check/ 4. - 12 - apamod_num) < 1 and (ch_check/ 4. - 12 - apamod_num) >= 0:
                print (12 + apamod_num), ch_check, (ch_check/ 4. - 12 - apamod_num);
                mod_corr[(12 + apamod_num)] += 1
            elif ch_check> 95 and ch_check< 132 and (ch_check/ 4. - 24 - apamod_num) < 1 and (ch_check/ 4. - 24 - apamod_num) >= 0:
                print (24+apamod_num),ch_check, (ch_check/ 4. - 24 - apamod_num);
                mod_corr[(24 + apamod_num)] += 1
###############################################################
print mod_corr;
#kicking out "imaginary modules"
mod_corr.pop(23)
mod_corr.pop(22)
mod_corr.pop(11)
mod_corr.pop(10)
print mod_corr;
# creating scale factor to correct for bad channels in modules. Will use later in code.
# Ex: 1 bad channel in apa1-mod6, will have mod_corr value of "1.33"
for fg in range(len(mod_corr)):
    if mod_corr[fg]>0:
        if fg>19:
            print 'apa3',fg-20, mod_corr[fg],
            mod_corr[fg] = 1./(1-mod_corr[fg]/4.);print mod_corr[fg]
        elif fg>9:
            print 'apa2',fg-10, mod_corr[fg],
            mod_corr[fg] = 1./(1-mod_corr[fg]/4.);print mod_corr[fg]
        else:
            print 'apa1', fg, mod_corr[fg],
            mod_corr[fg] = 1./(1-mod_corr[fg]/4.);print mod_corr[fg]
            # print sum_cols[fg]
            # sum_cols[fg]=[]
            # print sum_cols[fg]
    else: mod_corr[fg] = 1./(1-mod_corr[fg]/4.);
print mod_corr;
print len(mod_corr);

# for run in [runs[1]]:
for run in runs:
    print "%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%% Run ", str(run),"%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%"
    avg_per_apa=[]

    with open('/dune/app/users/cmacias/pDUNE_PD_larsoft_env/Rates/cdf_Calibrated_Intval_'+str(run)+'.txt', "r") as myfile:
        # run=4600
        # with open('/home/ctmacias/Desktop/pDUNE/cdf_val_at_samp_11_Run_4600.txt', "r") as myfile:
        # with open('/home/ctmacias/Downloads/cdf_check.csv', "r") as myfile:
        importedfile1 = myfile.readlines()
        # print len(importedfile1)

    row = importedfile1[0].split(",")
    row =[f.replace(" ","") for f in row]
    ### Since, we import all info as one line per channel, we need to make cuts
    ###### Txt file: <ch#>, <len(cdf values)>, <pe values>......, <cdf values>.....

    sample_len=int(row[1])
    # print sample_len
    samp_range=row[2:(2+sample_len)]
    # the adc or PE values are "*100" for fractional-integer purposes. Dividing here to correct for it
    samp_range =[(float(adc_val_i)/100.) for adc_val_i in samp_range]


    ch = []
    fre_val = []

    # ---------------------------
    # Averaging values per fraction Photon- this is to match all channels per module to same Photon-frequency values.
    # they differ since they have different ADC/PE values...
    photon_count_interval = .1
    max_photon_count = 5.  # max(Photon_range)
    #defining photon-count bins
    fixed_photon_range = list(np.arange(photon_count_interval / 2. - .05, max_photon_count + photon_count_interval, photon_count_interval))
    #redefining sample range to fixed bin range for average cdfs
    samp_range =fixed_photon_range

    ########## Organizing things
    for r in range(len(importedfile1)):
        row = importedfile1[r].split(",")
        row = [f.replace(" ", "") for f in row]
        sample_len = int(row[1])
        # print row
        # print float(row[0]);
        adc_val= row[2:(2 + sample_len)]
        cdf_range = row[(2 + sample_len):]
        freq_mod = [float(v) for v in cdf_range]#[((-np.log(1. - float(cdf_val_i))) / (1275./150000000.)) for cdf_val_i in cdf_range]
        # # print adc_val;sys.exit()
        # Using calibrations constants to convert ADC -> PE
        if int(row[0]) in Bad_channels:cal_val =999999999.; freq_mod = [float(v)*0. for v in cdf_range]
        elif int(row[0]) in ch_arapuca:cal_val = adc_photon_arapuca[ch_arapuca.index(int(row[0]))] #adc_avalanche_arapuca[ch_arapuca.index(int(row[0]))]
        else: cal_val =calib_ADC_Photon_ch[Channels.index(int(row[0]))] #cal_val =calib_ADC_Avalanche_ch[Channels.index(int(row[0]))]
        # Converting ADC counts to Signal (photon/avalanche) counts
        Signal_range =[float(yhu) / float(cal_val) for yhu in adc_val]

        channel =[int(row[0])]
        ch.append(int(row[0]))

        # Averaging values per fraction Photon- this is to match all channels to same frequency per photon count values.
        # they differ since they have different ADC/Photon values...
        avg_PE_range=[]
        avg_cdf =[]
        count_PE = 0
        while count_PE<= max_photon_count:

            avg_Photon_range_i = []
            avg_cdf_i = []
            for val_i in range(len(Signal_range)):
                # print Photon_range[val_i];continue
                if Signal_range[val_i]> count_PE and Signal_range[val_i]< (count_PE + photon_count_interval):
                    avg_Photon_range_i.append(Signal_range[val_i])
                    avg_cdf_i.append(freq_mod[val_i])
            #Checking for no signals- will most likely be for Zero signal and very high signals
            if len(avg_cdf_i)==0:
                avg_cdf.append(0)
                # print photon_count_interval*(count_PE+.5), 0
            # averaging rate per bin-interval
            else:
                avg_cdf.append(np.nanmean(avg_cdf_i))
                # print photon_count_interval*(count_PE+.5), avg_cdf_i,np.nanmean(avg_cdf_i)

            avg_PE_range.append((count_PE + photon_count_interval))
            count_PE += photon_count_interval
        if int(row[0]) == 137: print row[0];print avg_cdf;print freq_mod


        #---- Redefining cdf values to the average cdf value
        freq_mod=avg_cdf[:]
        ##### combining channel with cdf values -> [ch, cdf_val1,cdf_val2, cdf_val3,...etc.]
        c =np.hstack((np.array(channel),np.array(freq_mod)))
        fre_val.append(list(c))

    ########### Summing channel for each module
    modules=[]
    for mod in range(0,len(fre_val),4):
        print mod,'---------------'
        if fre_val[mod][0] <132:# all channels below channel 132 are bars, so 4 channels per module
            # grabbing the four channels and putting into 4-length list
            values = fre_val[mod:(mod+4)]
            # Summing all channels per module
            sum_cols = [np.nansum(x) for x in zip(*values)]
            # Correcting for over counting "true events"
            modules_i=[]
            #collecting module-sum number:: i.e. first module on apa1, ch 0-3 == 0+1+2+3 =6.
            modules_i.append(sum_cols[0])
            # looping through adc/PE values
            for sum_cols_i in range(1,len(sum_cols)):# start a second element to skip module-sum number
                if sum_cols[sum_cols_i]>1.:# This is to avoid inf values when taking the log later
                    modules_i.append(0)
                else:
                    modules_i.append((-np.log(1. - float(sum_cols[sum_cols_i]))) / (1275. / 150000000.))#applying correction
            modules.append(modules_i)
        elif fre_val[mod][0]==132:# applying this one time to the arapuca 12-channel sum
            print "-------------ARAPUCA"
            values = fre_val[mod:(mod+12)]
            sum_cols = [np.nansum(x) for x in zip(*values)]
            modules_i=[]
            modules_i.append(sum_cols[0])
            for sum_cols_i in range(1,len(sum_cols)):
                if sum_cols[sum_cols_i]>1.:
                    modules_i.append(0)
                else:
                    modules_i.append((-np.log(1. - float(sum_cols[sum_cols_i]))) / (1275. / 150000000.))
            modules.append(modules_i)
        elif fre_val[mod][0] >132 and fre_val[mod][0]<144:
            # print "----------------repeat of ARAPUCA"
            continue

        ## Can add other APA channels here
        else: print ""
    # print len(modules)
    #--- Separating modules into apa's..... maybe going forward we should switch this to opdet number tag?
    apa1=modules[:10]
    print len(apa1[0][1:])
    print len(samp_range)
    apa2=modules[10:20]
    apa3=modules[20:30]
    ### rearranging for Arapucas to be in fourth position APA3
    apa3_corr=[]
    for r in range(3):
        apa3_corr.append(apa3[r])
    apa3_corr.append(apa3[9])
    for r in range(3,9,1):
        apa3_corr.append(apa3[r])
    apa3 =apa3_corr
    # Correcting for the bad channels-multiplying by scale factor "mod_corr" defined above
    for g in range(len(apa1)):
        # print apa1[g];
        temp_1=apa1[g][0]
        temp_2=apa2[g][0]
        temp_3=apa3[g][0]
        apa1[g]= [mod_i*mod_corr[g] for mod_i in apa1[g]]
        apa2[g]= [mod_i*mod_corr[g+10] for mod_i in apa2[g]]
        apa3[g]= [mod_i*mod_corr[g+20] for mod_i in apa3[g]]
        apa1[g][0]=temp_1
        apa2[g][0]=temp_2
        apa3[g][0]=temp_3
    # Done correcting for the bad channels-multiplying by scale factor "mod_corr" defined above

    ######## Time to Plot
    labels = ["mod 1","mod 2","mod 3","mod 4","mod 5","mod 6","mod 7","mod 8","mod 9","mod 10"]
    apa_label_check=[]
    from matplotlib.pyplot import cm

    NUM_COLORS = len(apa1)
    color = iter(cm.rainbow(np.linspace(0, 1, NUM_COLORS)))
    # print apa3[len(apa3)-1][1:]
    fig, ax = plt.subplots(1,3, figsize=(20, 10))
    text_file_indiv.write(str(run))
    for y in range(len(samp_range)):
        text_file_indiv.write( ", "+str(samp_range[y]))
    for y in range(len(samp_range)):
        text_file_indiv.write( ", "+str(samp_range[y]))
    for y in range(len(samp_range)):
        text_file_indiv.write( ", "+str(samp_range[y]))
    text_file_indiv.write("\n")
    for r in range(len(apa1)):
        # print samp_range
        # print apa1[r][0], '----------',str((apa1[r][0] - 6) / 16 + 1)
        # print apa2[r][0], '----------',str((((apa2[r][0]-6)/16)+1-12))
        if float(str((((apa3[r][0]-6)/16)-24))) <3.:
            print apa3[r][0], '----------',str((((apa3[r][0]-6)/16)-24))
            apa_label_check.append(str((((apa3[r][0]-6)/16)-24)))
        elif float(apa3[r][0])==1650.0:# equals sum of all arapuca channels(132-143)
            print 'arapuca'
            print apa3[r][0], '----------',str(3)
            apa_label_check.append(str(3))

        else:
            print apa3[r][0], '----------', str((((apa3[r][0] - 6) / 16) - 24+1))
            apa_label_check.append(str((((apa3[r][0] - 6) / 16) - 24+1)))
        print '----================================================'
        # -48)/4+1))
        c = next(color)
        lk=0

        run_color = ['black', 'red','orange','darkgreen','cyan','blue', 'purple','magenta','maroon','yellow']#''darkorchid', 'indigo', 'darkcyan', 'firebrick', 'darkorange']
        # print len(run_color);sys.exit()
        # ax[2].plot([float(u) for u in samp_range[10:]], [k/1000. for k in apa1[r][1:]], 'o-',c=c,label=("mod "+str(int(float((apa1[r][0]-6)/16+1)))))
        ax[2].plot(samp_range, [k/1000. for k in apa1[r][1:]], 'o', alpha=.6,c=run_color[r],label=("mod "+str(int(float((apa1[r][0]-6)/16)))))
        ax[1].plot(samp_range, [k/1000. for k in apa2[r][1:]], 'o',alpha=.6,c=run_color[r],label=("mod "+str(int(float((((apa2[r][0]-6)/16)-12))))))
        if r!=3:ax[0].plot(samp_range, [k/1000. for k in apa3[r][1:]], 'o',alpha=.6,c=run_color[r],label=("mod "+str (int(float(apa_label_check[r])))))

        apa1_mod.append([k/1000. for k in apa1[r][1:]])
        apa2_mod.append([k/1000. for k in apa2[r][1:]])
        apa3_mod.append([k/1000. for k in apa3[r][1:]])
        # print apa2[r][0]
        # sys.exit()
        text_file_indiv.write("mod_"+str(int(float((apa1[r][0]-6)/16))))
        for y in range(len(apa3[r][1:])):
            text_file_indiv.write(", "+str(apa3[r][(y+1)]/1000.))
        # text_file_indiv.write("\n")
        # text_file_indiv.write("apa2")
        for y in range(len(apa2[r][1:])):
            text_file_indiv.write(", "+str(apa2[r][(y+1)]/1000.))
        # text_file_indiv.write("\n")
        # text_file_indiv.write("apa1")
        for y in range(len(apa1[r][1:])):
            text_file_indiv.write(", "+str(apa1[r][(y+1)]/1000.))
        # text_file_indiv.write("\n")

        text_file_indiv.write("\n")
    text_file_indiv.write("\n")
    # avg_per_apa.append(apa1[1:])
    # avg_per_apa.append(apa2[1:])
    # avg_per_apa.append(apa3[1:])
    # # print avg_per_apa[6][:]
    # # avg_per_apa=list(map(list, zip(*avg_per_apa)))
    # # np.array(avg_per_apa).T.tolist()
    # # print avg_per_apa
    # # print(len(avg_per_apa))
    # fig, ax = plt.subplots(1, figsize=(20, 10))
    #
    # for y_arr, label in zip(avg_per_apa, labels):
    #     # ax.plot(samp_range, y_arr, label=label)
    #     ax.plot(samp_range, y_arr, "o-",label=label)
    # # plt.plot(range(5,15), avg_per_apa)
    # ax.axvline(x=12., color='k', linestyle='-', alpha=0.55)
    # ax.set_xlabel('[ADC]', size =20)
    # ax.set_ylabel('Avg APA (1-CDF) Value', size =20)
    # ax.set_title('Avg APA (1-CDF) Value as a Function of ADC- Run %s' % run, size =20)
    fig.subplots_adjust(wspace=0.1)
    ax[0].set_xlabel('[Photons]', size=20)
    ax[1].set_xlabel('[Photons]', size=20)
    ax[2].set_xlabel('[Photons]', size=20)
    ax[0].set_yscale('log')
    ax[1].set_yscale('log')
    ax[2].set_yscale('log')
    ax[0].set_ylabel('Frequency [kHz]', size=20)
    # ax[0].legend()
    # ax[1].legend()
    ax[2].legend(loc=1)
    ax[0].set_ylim(1, 1000)
    ax[1].set_ylim(1, 1000)
    ax[2].set_ylim(1, 1000)
    ax[0].set_xlim(0, 7)
    ax[1].set_xlim(0, 7)
    ax[2].set_xlim(0, 7)
    ## Drawing Bkgrnd Lines
    for u in np.arange(1, 11):
        ax[0].axhline(y=u / 10., color='k', linestyle='-', alpha=0.15);ax[1].axhline(y=u / 10., color='k', linestyle='-', alpha=0.15);ax[2].axhline(y=u / 10., color='k', linestyle='-', alpha=0.15)
        ax[0].axhline(y=u * 10., color='k', linestyle='-', alpha=0.15);ax[1].axhline(y=u * 10., color='k', linestyle='-', alpha=0.15);ax[2].axhline(y=u * 10., color='k', linestyle='-', alpha=0.15)
        ax[0].axhline(y=u *100., color='k', linestyle='-', alpha=0.15);ax[1].axhline(y=u * 100., color='k', linestyle='-', alpha=0.15);ax[2].axhline(y=u * 100., color='k', linestyle='-', alpha=0.15)
        ax[0].axhline(y=u, color='k', linestyle='-', alpha=0.15);      ax[1].axhline(y=u, color='k', linestyle='-', alpha=0.15);      ax[2].axhline(y=u, color='k', linestyle='-', alpha=0.15)
        ax[0].axvline(x=1. * u, color='k', linestyle='-', alpha=0.15); ax[1].axvline(x=1. * u, color='k', linestyle='-', alpha=0.15); ax[2].axvline(x=1. * u, color='k', linestyle='-', alpha=0.15)
    # ax[2].legend(numpoints=1, bbox_to_anchor=(1.305, 1.012))#fontsize=25

    fig.text(0.5, 0.965, "Module Sum " + r"${\bf{Total\ Signal\ Rate}}$" + " per APA, as a Function of Detected Photon",
             ha='center', va='center', size=20)  # ,fontweight="bold")
    fig.text(0.396, 0.957, r"${\bf{\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_}}$", ha='center', va='center',
             size=20)  # ,fontweight="bold")
    # fig.text(0.865, 0.91, 'Run#' , ha='center', va='center', size =15)
    fig.text(0.852, 0.91, ('Run '+str(run)), ha='center', va='center', size=15)
    # fig.text(0.23, 0.91, 'APA-3', ha='center', va='center', size=20)
    # fig.text(0.49, 0.91, 'APA-2', ha='center', va='center', size=20)
    # fig.text(0.74, 0.91, 'APA-1', ha='center', va='center', size=20)
    ax[0].set_title('APA-3', size=15)
    ax[1].set_title('APA-2', size=15)
    ax[2].set_title('APA-1', size=15)
    # fig.text(0.23, 0.85, 'APA-3', ha='center', va='center', size=20)
    # fig.text(0.49, 0.85, 'APA-2', ha='center', va='center', size=20)
    # fig.text(0.74, 0.85, 'APA-1', ha='center', va='center', size=20)
    fig.savefig("Freq_PerModule" + str(run) + ".png")
    plt.close(fig)

text_file_indiv.close()
# print apa1_mod
# print len(apa1_mod)
# print apa1_mod[int(r*(len(apa1_mod) / len(runs)))]

################### Time to plot individual modules per APA for ALL runs
NUM_COLORS = 10 # len(10)
color = iter(cm.rainbow(np.linspace(0, 1, NUM_COLORS)))

fig, ax = plt.subplots(10, 3,sharex=True,sharey=True, figsize=(20, 15))
for r in range(len(runs)):
    c = next(color)
    ax[0][0].plot(samp_range,apa3_mod[r*10],"o",c=c, label=str(runs[r]))
    ax[1][0].plot(samp_range,apa3_mod[r*10+1],"o",c=c, label=str(runs[r]))
    ax[2][0].plot(samp_range,apa3_mod[r*10+2],"o",c=c, label=str(runs[r]))
    ax[3][0].plot(samp_range,apa3_mod[r*10+3],"o",c=c, label=str(runs[r]))
    ax[4][0].plot(samp_range,apa3_mod[r*10+4],"o",c=c, label=str(runs[r]))
    ax[5][0].plot(samp_range,apa3_mod[r*10+5],"o",c=c, label=str(runs[r]))
    ax[6][0].plot(samp_range,apa3_mod[r*10+6],"o",c=c, label=str(runs[r]))
    ax[7][0].plot(samp_range,apa3_mod[r*10+7],"o",c=c, label=str(runs[r]))
    ax[8][0].plot(samp_range,apa3_mod[r*10+8],"o",c=c, label=str(runs[r]))
    ax[9][0].plot(samp_range,apa3_mod[r*10+9],"o",c=c, label=str(runs[r]))

    ax[0][1].plot(samp_range,apa2_mod[r*10],"o",c=c, label=str(runs[r]))
    ax[1][1].plot(samp_range,apa2_mod[r*10+1],"o",c=c, label=str(runs[r]))
    ax[2][1].plot(samp_range,apa2_mod[r*10+2],"o",c=c, label=str(runs[r]))
    ax[3][1].plot(samp_range,apa2_mod[r*10+3],"o",c=c, label=str(runs[r]))
    ax[4][1].plot(samp_range,apa2_mod[r*10+4],"o",c=c, label=str(runs[r]))
    ax[5][1].plot(samp_range,apa2_mod[r*10+5],"o",c=c, label=str(runs[r]))
    ax[6][1].plot(samp_range,apa2_mod[r*10+6],"o",c=c, label=str(runs[r]))
    ax[7][1].plot(samp_range,apa2_mod[r*10+7],"o",c=c, label=str(runs[r]))
    ax[8][1].plot(samp_range,apa2_mod[r*10+8],"o",c=c, label=str(runs[r]))
    ax[9][1].plot(samp_range,apa2_mod[r*10+9],"o",c=c, label=str(runs[r]))

    ax[0][2].plot(samp_range,apa1_mod[r*10],"o",c=c, label=str(runs[r]))
    ax[1][2].plot(samp_range,apa1_mod[r*10+1],"o",c=c, label=str(runs[r]))
    ax[2][2].plot(samp_range,apa1_mod[r*10+2],"o",c=c, label=str(runs[r]))
    ax[3][2].plot(samp_range,apa1_mod[r*10+3],"o",c=c, label=str(runs[r]))
    ax[4][2].plot(samp_range,apa1_mod[r*10+4],"o",c=c, label=str(runs[r]))
    ax[5][2].plot(samp_range,apa1_mod[r*10+5],"o",c=c, label=str(runs[r]))
    ax[6][2].plot(samp_range,apa1_mod[r*10+6],"o",c=c, label=str(runs[r]))
    ax[7][2].plot(samp_range,apa1_mod[r*10+7],"o",c=c, label=str(runs[r]))
    ax[8][2].plot(samp_range,apa1_mod[r*10+8],"o",c=c, label=str(runs[r]))
    ax[9][2].plot(samp_range,apa1_mod[r*10+9],"o",c=c, label=str(runs[r]))
    # plt.show()
    # print int(r * (len(apa1_mod) / len(runs)))
    # sys.exit()
ax[9][0].set_xlabel('[Photons]', size=20)
ax[9][1].set_xlabel('[Photons]', size=20)
ax[9][2].set_xlabel('[Photons]', size=20)
ax[9][0].set_xlim(0, 7)
ax[9][1].set_xlim(0, 7)
ax[9][2].set_xlim(0, 7)
# plt.xlabel('[ADC]', size=20)
plt.yscale('log')
plt.ylim(2, 999)
for r in range(10):
    for u in np.arange(1,4):
        ax[r][2].axhline(y=10**u, color='k', linestyle='-', alpha=0.15)
        ax[r][1].axhline(y=10**u, color='k', linestyle='-', alpha=0.15)
        ax[r][0].axhline(y=10**u, color='k', linestyle='-', alpha=0.15)
# for r in range(10):
#     ax[r][0].set_xlabel('[ADC]', size=20)
#     ax[r][0].set_yscale('log')
    # ax[r][1].set_xlabel('[ADC]', size=20)
    # ax[r][1].set_yscale('log')
    # ax[r][2].set_xlabel('[ADC]', size=20)
    # ax[r][2].set_yscale('log')
    # ax[r][0].set_ylim(5, 999)
    # ax[r][1].set_ylim(5, 999)
    # ax[r][2].set_ylim(5, 999)
    # ax[r][0].set_ylabel('Frequency [kHz]', size=20)
ax[0][2].legend(bbox_to_anchor=(1.27, 1.08))

fig.subplots_adjust(wspace=0.01)
fig.subplots_adjust(hspace=0.1)

fig.text(0.53, 0.95, "Module Sum " + r"${\bf{Total\ Signal\ Rate}}$" + " per APA, as a Function of Detected Photons",
         ha='center', va='center', size=20)  # ,fontweight="bold")
fig.text(0.421, 0.942, r"${\bf{\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_}}$", ha='center', va='center',
         size=20)  # ,fontweight="bold")
# fig.text(0.852, 0.91, ('Run ' + str(run)), ha='center', va='center', size=15)
fig.text(0.26, 0.91, 'APA-3', ha='center', va='center', size=20)
fig.text(0.52, 0.91, 'APA-2', ha='center', va='center', size=20)
fig.text(0.77, 0.91, 'APA-1', ha='center', va='center', size=20)
fig.text(.935, 0.91, 'Run#' , ha='right', va='center', size =15)
fig.text(.075, 0.51, 'Frequency [kHz]', size=20 , ha='center', va='center', rotation=90)
fig.savefig("Freq_PerModule_PerAPA.png")
plt.close(fig)




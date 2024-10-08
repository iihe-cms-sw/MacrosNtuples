from ROOT import TFile, TH1, TH1F, TH2, TH2F, TLegend, TCanvas, gDirectory, gStyle, gROOT, gPad
from ROOT import TAttMarker, TColor, TLine
from ROOT import kBlack, kBlue, kRed
from array import array
import os
import sys

gROOT.SetBatch(True)
gStyle.SetOptStat(0)

sys.path.insert(1, '../..') # for importing the binning from another directory
from binning import *

# Data input
infile_dt = TFile('/pnfs/iihe/cms/store/user/gparaske/JEC/2022/EGamma/WithResiduals/Unprescaled/RunEFG.root')
# MC input
infile_MC = TFile('/pnfs/iihe/cms/store/user/gparaske/JEC/2022/G-4Jets/WithResiduals/Unprescaled/G-4Jets_EFG.root')

# Get the 2D histograms with the pt balance and create the Y projections
keys_dt = infile_dt.GetListOfKeys() # Data 
keys_MC = infile_MC.GetListOfKeys() # MC

# Below we create a dictionary which contains lists
# Each list will correspond to all the different alpha values for each eta and pt bin 
str_binetas_pts = []
for e in str_binetas:
    for p in str_binpts:
        str_binetas_pts.append(e + p) # These will be the keys of the dictionary 
#print('Keys of the dictionary: ', str_binetas_pts)

# Data
all_plots_per_eta_per_pt_dt = dict([(k, []) for k in str_binetas_pts])
# Read all the histograms and put them in the lists (no projections and profiles yet)
for key in keys_dt:
    histo2D = key.ReadObj()
    if isinstance(histo2D, TH2):
       name = key.GetName() 
       for e in str_binetas:
           if e in name:
              for p in str_binpts:
                  if p in name:
                     all_plots_per_eta_per_pt_dt[e+p].append(histo2D)

# MC
all_plots_per_eta_per_pt_MC = dict([(k, []) for k in str_binetas_pts])
# Read all the histograms and put them in the lists (no projections and profiles yet)
for key in keys_MC:
    histo2D = key.ReadObj()
    if isinstance(histo2D, TH2):
       name = key.GetName() 
       for e in str_binetas:
           if e in name:
              for p in str_binpts:
                  if p in name:
                     all_plots_per_eta_per_pt_MC[e+p].append(histo2D)

#print('Dictionary with lists: ')
#for etapt, histo in all_plots_per_eta_per_pt_dt.items():
#    print(f'Key: {etapt}')
#    for histoname in histo:
#        print(f'Histogram: {histoname}')

# Prepare the lists for inclusive alpha 2D plots for Projections and Profiles
# Data
h_ptBalance_alpha_incl_0p3_dt = []          # Full list of histos for each eta, pt bin and alpha < 0.3
h_ptBalance_alpha_incl_1p0_dt = []          # Full list of histos for each eta, pt bin and alpha < 1.0
h_ptBalance_vs_refpt_alpha_incl_0p3_dt = [] # Full list of histos for each eta, pt bin and alpha < 0.3 (To be used later for plotting)
h_ptBalance_vs_refpt_alpha_incl_1p0_dt = [] # Full list of histos for each eta, pt bin and alpha < 1.0 (To be used later for plotting)
# MC
h_ptBalance_alpha_incl_0p3_MC = []          # Full list of histos for each eta, pt bin and alpha < 0.3
h_ptBalance_alpha_incl_1p0_MC = []          # Full list of histos for each eta, pt bin and alpha < 1.0
h_ptBalance_vs_refpt_alpha_incl_0p3_MC = [] # Full list of histos for each eta, pt bin and alpha < 0.3 (To be used later for plotting)
h_ptBalance_vs_refpt_alpha_incl_1p0_MC = [] # Full list of histos for each eta, pt bin and alpha < 1.0 (To be used later for plotting)

# Add histograms with the same key for alpha inclusive plots 
# Data
for etapt, histo_list in all_plots_per_eta_per_pt_dt.items():
    h_0p3 = TH2F(etapt + '_0p3_dtpt', etapt + '0p3_dtpt', NptBins, jetptBins, NptbalanceBins, ptbalanceBins)    
    h_1p0 = TH2F(etapt + '_1p0_dtpt', etapt + '1p0_dtpt', NptBins, jetptBins, NptbalanceBins, ptbalanceBins)    
    #print(h_1p0.GetName())
    for idx, histogram in enumerate(histo_list):
        #print(' adding: ', histogram.GetName())
        h_1p0.Add(histogram) # for alpha < 1.0
        if(idx < 6):         # only 6 first bins of alpha for alpha < 0.3 (if you change alpha binning adapt this)
           h_0p3.Add(histogram)
           #print(' adding: ', histogram.GetName())
    # Projections    
    h_ptBalance_alpha_incl_0p3_dt.append(h_0p3.ProjectionY())
    h_ptBalance_alpha_incl_1p0_dt.append(h_1p0.ProjectionY())
    # Profiles   
    h_ptBalance_vs_refpt_alpha_incl_0p3_dt.append(h_0p3.ProfileX())
    h_ptBalance_vs_refpt_alpha_incl_1p0_dt.append(h_1p0.ProfileX())

# MC
for etapt, histo_list in all_plots_per_eta_per_pt_MC.items():
    h_0p3 = TH2F(etapt + '_0p3_MCpt', etapt + '0p3_MCpt', NptBins, jetptBins, NptbalanceBins, ptbalanceBins)    
    h_1p0 = TH2F(etapt + '_1p0_MCpt', etapt + '1p0_MCpt', NptBins, jetptBins, NptbalanceBins, ptbalanceBins)    
    #print(h_1p0.GetName())
    for idx, histogram in enumerate(histo_list):
        #print(' adding: ', histogram.GetName())
        h_1p0.Add(histogram) # for alpha < 1.0
        if(idx < 6):         # only 6 first bins of alpha for alpha < 0.3 (if you change alpha binning adapt this)
           h_0p3.Add(histogram)
           #print(' adding: ', histogram.GetName())
    # Projections    
    h_ptBalance_alpha_incl_0p3_MC.append(h_0p3.ProjectionY())
    h_ptBalance_alpha_incl_1p0_MC.append(h_1p0.ProjectionY())
    # Profiles   
    h_ptBalance_vs_refpt_alpha_incl_0p3_MC.append(h_0p3.ProfileX())
    h_ptBalance_vs_refpt_alpha_incl_1p0_MC.append(h_1p0.ProfileX())

# Print the lists for checks
#print('Full list of histos: ')
#for h in range(len(h_ptBalance_alpha_incl_0p3)):
#    print(h_ptBalance_alpha_incl_0p3[h])
#print('Full list of histos: ')
#for h in range(len(h_ptBalance_alpha_incl_1p0)):
#    print(h_ptBalance_alpha_incl_1p0[h])
 
# First create canvases with all the pt balance plots for all eta and alpha inclusive bins
dir0 = 'jet_response_alpha_0p3'
os.makedirs(dir0, exist_ok = True)

index = 0
for e in range(NetaBins):
    str1 = '[' + str("{:.1f}".format(jetetaBins[e])) + ',' + str("{:.1f}".format(jetetaBins[e+1])) + ')' 
    for p in range(NptBins):
        str2 = '[' + str(jetptBins[p]) + ',' + str(jetptBins[p+1]) + ')'

        c = TCanvas(str1 + ',' + str2, str1 + ',' + str2, 1000, 1000)
        h_ptBalance_alpha_incl_0p3_dt[index].SetTitle('p_{T} balance: #eta=' + str1 + ', p_{T}^{#gamma}=' + str2 + ', #alpha < 0.3')
        h_ptBalance_alpha_incl_0p3_dt[index].GetXaxis().SetTitle('p_{T}^{jet}/p_{T}^{#gamma}')
        h_ptBalance_alpha_incl_0p3_dt[index].GetXaxis().SetTitleOffset(1.2)
        h_ptBalance_alpha_incl_0p3_dt[index].GetYaxis().SetTitle('Events')
        h_ptBalance_alpha_incl_0p3_dt[index].GetYaxis().SetLabelSize(0.03)
        h_ptBalance_alpha_incl_0p3_dt[index].GetYaxis().SetTitleOffset(1.5)
        h_ptBalance_alpha_incl_0p3_dt[index].SetLineColor(kBlue+1)
        h_ptBalance_alpha_incl_0p3_MC[index].SetTitle('p_{T} balance: #eta=' + str1 + ', p_{T}^{#gamma}=' + str2 + ', #alpha < 0.3')
        h_ptBalance_alpha_incl_0p3_MC[index].GetXaxis().SetTitle('p_{T}^{jet}/p_{T}^{#gamma}')
        h_ptBalance_alpha_incl_0p3_MC[index].GetXaxis().SetTitleOffset(1.2)
        h_ptBalance_alpha_incl_0p3_MC[index].GetYaxis().SetTitle('Events')
        h_ptBalance_alpha_incl_0p3_MC[index].GetYaxis().SetLabelSize(0.03)
        h_ptBalance_alpha_incl_0p3_MC[index].GetYaxis().SetTitleOffset(1.5)
        h_ptBalance_alpha_incl_0p3_MC[index].SetLineColor(kRed+1)

        m_MC = h_ptBalance_alpha_incl_0p3_MC[index].GetMaximum()
        m_dt = h_ptBalance_alpha_incl_0p3_dt[index].GetMaximum()
     
        m = 0.
        if ( m_MC > m_dt):
           m = m_MC
           h_ptBalance_alpha_incl_0p3_MC[index].Draw('HIST')
           h_ptBalance_alpha_incl_0p3_dt[index].Draw('same HIST')
        else:
           m = m_dt
           h_ptBalance_alpha_incl_0p3_dt[index].Draw('HIST')
           h_ptBalance_alpha_incl_0p3_MC[index].Draw('same HIST')
         
        leg = TLegend(0.62,0.50,0.92,0.75)
        leg.AddEntry(h_ptBalance_alpha_incl_0p3_MC[index], "MC (G-4Jets)", "l")
        leg.AddEntry(h_ptBalance_alpha_incl_0p3_dt[index], "Data (EGamma)", "l")
        leg.SetBorderSize(0)
        leg.SetFillStyle(0)
        leg.Draw()

        l = TLine(1.0,0.0,1.0,m)
        l.SetLineStyle(2)
        l.Draw()

        gPad.RedrawAxis()
        c.SaveAs(dir0 + '/ptBalance_' + str_binetas[e] + str_binpts[p] + '.png')
        #c.SaveAs(dir0 + '/ptBalance_' + str_binetas[e] + str_binpts[p] + '.pdf')
        index += 1

dir1 = 'jet_response_alpha_1p0'
os.makedirs(dir1, exist_ok = True)

index = 0
for e in range(NetaBins):
    str1 = '[' + str("{:.1f}".format(jetetaBins[e])) + ',' + str("{:.1f}".format(jetetaBins[e+1])) + ')' 
    for p in range(NptBins):
        str2 = '[' + str(jetptBins[p]) + ',' + str(jetptBins[p+1]) + ')'

        c = TCanvas(str1 + ',' + str2, str1 + ',' + str2, 1000, 1000)
        h_ptBalance_alpha_incl_1p0_dt[index].SetTitle('p_{T} balance: #eta=' + str1 + ', p_{T}^{#gamma}=' + str2 + ', #alpha < 1.0')
        h_ptBalance_alpha_incl_1p0_dt[index].GetXaxis().SetTitle('p_{T}^{jet}/p_{T}^{#gamma}')
        h_ptBalance_alpha_incl_1p0_dt[index].GetXaxis().SetTitleOffset(1.2)
        h_ptBalance_alpha_incl_1p0_dt[index].GetYaxis().SetTitle('Events')
        h_ptBalance_alpha_incl_1p0_dt[index].GetYaxis().SetLabelSize(0.03)
        h_ptBalance_alpha_incl_1p0_dt[index].GetYaxis().SetTitleOffset(1.5)
        h_ptBalance_alpha_incl_1p0_dt[index].SetLineColor(kBlue+1)
        h_ptBalance_alpha_incl_1p0_MC[index].SetTitle('p_{T} balance: #eta=' + str1 + ', p_{T}^{#gamma}=' + str2 + ', #alpha < 1.0')
        h_ptBalance_alpha_incl_1p0_MC[index].GetXaxis().SetTitle('p_{T}^{jet}/p_{T}^{#gamma}')
        h_ptBalance_alpha_incl_1p0_MC[index].GetXaxis().SetTitleOffset(1.2)
        h_ptBalance_alpha_incl_1p0_MC[index].GetYaxis().SetTitle('Events')
        h_ptBalance_alpha_incl_1p0_MC[index].GetYaxis().SetLabelSize(0.03)
        h_ptBalance_alpha_incl_1p0_MC[index].GetYaxis().SetTitleOffset(1.5)
        h_ptBalance_alpha_incl_1p0_MC[index].SetLineColor(kRed+1)

        m_MC = h_ptBalance_alpha_incl_1p0_MC[index].GetMaximum()
        m_dt = h_ptBalance_alpha_incl_1p0_dt[index].GetMaximum()
     
        m = 0.
        if ( m_MC > m_dt):
           m = m_MC
           h_ptBalance_alpha_incl_1p0_MC[index].Draw('HIST')
           h_ptBalance_alpha_incl_1p0_dt[index].Draw('same HIST')
        else:
           m = m_dt
           h_ptBalance_alpha_incl_1p0_dt[index].Draw('HIST')
           h_ptBalance_alpha_incl_1p0_MC[index].Draw('same HIST')
         
        leg = TLegend(0.62,0.50,0.92,0.75)
        leg.AddEntry(h_ptBalance_alpha_incl_1p0_MC[index], "MC (G-4Jets)", "l")
        leg.AddEntry(h_ptBalance_alpha_incl_1p0_dt[index], "Data (EGamma)", "l")
        leg.SetBorderSize(0)
        leg.SetFillStyle(0)
        leg.Draw()

        l = TLine(1.0,0.0,1.0,m)
        l.SetLineStyle(2)
        l.Draw()
        gPad.RedrawAxis()

        c.SaveAs(dir1 + '/ptBalance_' + str_binetas[e] + str_binpts[p] + '.png')
        #c.SaveAs(dir1 + '/ptBalance_' + str_binetas[e] + str_binpts[p] + '.pdf')
        index += 1

# Then create canvases with all the pt balance plots vs pt_ref for all eta and alpha bins
dir2 = 'jet_response_vs_refpt_alpha_0p3'
os.makedirs(dir2, exist_ok = True)

index = 0
for e in range(NetaBins):
    str1 = '[' + str("{:.1f}".format(jetetaBins[e])) + ',' + str("{:.1f}".format(jetetaBins[e+1])) + ')' 

    #print('Adding histograms to: ', h_ptBalance_vs_refpt_alpha_incl_0p3[index].GetName())
    # Here we add all the different pt histograms such that we have one histogram per eta and alpha bin
    for p in range(NptBins-1):
        h_ptBalance_vs_refpt_alpha_incl_0p3_MC[index].Add(h_ptBalance_vs_refpt_alpha_incl_0p3_MC[index+p+1])
        h_ptBalance_vs_refpt_alpha_incl_0p3_dt[index].Add(h_ptBalance_vs_refpt_alpha_incl_0p3_dt[index+p+1])
        #print(' adding: ', h_ptBalance_vs_refpt_alpha_incl_0p3[index+p+1].GetName())

    c = TCanvas(str1, str1, 1000, 1000)
    gPad.SetLogx()
    h_ptBalance_vs_refpt_alpha_incl_0p3_dt[index].GetXaxis().SetMoreLogLabels()
    h_ptBalance_vs_refpt_alpha_incl_0p3_dt[index].GetXaxis().SetNoExponent()
    h_ptBalance_vs_refpt_alpha_incl_0p3_dt[index].SetMaximum(1.25)
    h_ptBalance_vs_refpt_alpha_incl_0p3_dt[index].SetMinimum(0.5)
    h_ptBalance_vs_refpt_alpha_incl_0p3_dt[index].SetMarkerStyle(8)
    h_ptBalance_vs_refpt_alpha_incl_0p3_dt[index].SetMarkerSize(1.4)
    h_ptBalance_vs_refpt_alpha_incl_0p3_dt[index].SetMarkerColor(kBlue+1)
    h_ptBalance_vs_refpt_alpha_incl_0p3_dt[index].SetLineColor(kBlue+1)
    h_ptBalance_vs_refpt_alpha_incl_0p3_dt[index].SetTitle('p_{T} balance: #eta=' + str1 + ', #alpha < 0.3')
    h_ptBalance_vs_refpt_alpha_incl_0p3_dt[index].GetXaxis().SetTitle('p_{T}^{#gamma} (GeV)')
    h_ptBalance_vs_refpt_alpha_incl_0p3_dt[index].GetXaxis().SetTitleOffset(1.3)
    h_ptBalance_vs_refpt_alpha_incl_0p3_dt[index].GetYaxis().SetTitle('p_{T} balance')
    h_ptBalance_vs_refpt_alpha_incl_0p3_dt[index].GetYaxis().SetLabelSize(0.03)
    h_ptBalance_vs_refpt_alpha_incl_0p3_dt[index].GetYaxis().SetTitleOffset(1.4)
    #h_ptBalance_vs_refpt_alpha_incl_0p3_dt[index].GetXaxis().SetRangeUser(115., 1000.) # For VBF
    h_ptBalance_vs_refpt_alpha_incl_0p3_MC[index].GetXaxis().SetMoreLogLabels()
    h_ptBalance_vs_refpt_alpha_incl_0p3_MC[index].GetXaxis().SetNoExponent()
    h_ptBalance_vs_refpt_alpha_incl_0p3_MC[index].SetMaximum(1.25)
    h_ptBalance_vs_refpt_alpha_incl_0p3_MC[index].SetMinimum(0.5)
    h_ptBalance_vs_refpt_alpha_incl_0p3_MC[index].SetMarkerStyle(8)
    h_ptBalance_vs_refpt_alpha_incl_0p3_MC[index].SetMarkerSize(1.4)
    h_ptBalance_vs_refpt_alpha_incl_0p3_MC[index].SetMarkerColor(kRed+1)
    h_ptBalance_vs_refpt_alpha_incl_0p3_MC[index].SetLineColor(kRed+1)
    h_ptBalance_vs_refpt_alpha_incl_0p3_MC[index].SetTitle('p_{T} balance: #eta=' + str1 + ', #alpha < 0.3')
    h_ptBalance_vs_refpt_alpha_incl_0p3_MC[index].GetXaxis().SetTitle('p_{T}^{#gamma} (GeV)')
    h_ptBalance_vs_refpt_alpha_incl_0p3_MC[index].GetXaxis().SetTitleOffset(1.3)
    h_ptBalance_vs_refpt_alpha_incl_0p3_MC[index].GetYaxis().SetTitle('p_{T} balance')
    h_ptBalance_vs_refpt_alpha_incl_0p3_MC[index].GetYaxis().SetLabelSize(0.03)
    h_ptBalance_vs_refpt_alpha_incl_0p3_MC[index].GetYaxis().SetTitleOffset(1.4)
    #h_ptBalance_vs_refpt_alpha_incl_0p3_MC[index].GetXaxis().SetRangeUser(115., 1000.) # For VBF
    h_ptBalance_vs_refpt_alpha_incl_0p3_dt[index].Draw()
    h_ptBalance_vs_refpt_alpha_incl_0p3_MC[index].Draw('same')

    leg = TLegend(0.62,0.75,0.92,0.90)
    leg.AddEntry(h_ptBalance_vs_refpt_alpha_incl_0p3_MC[index], "MC (G-4Jets)", "l")
    leg.AddEntry(h_ptBalance_vs_refpt_alpha_incl_0p3_dt[index], "Data (EGamma)", "l")
    leg.SetBorderSize(0)
    leg.SetFillStyle(0)
    leg.Draw()

    l = TLine(0.0,1.0,1000,1.0)
    l.SetLineStyle(2)
    l.Draw()
    gPad.RedrawAxis()

    c.SaveAs(dir2 + '/ptBalance_' + str_binetas[e] + '.png')
    #c.SaveAs(dir2 + '/ptBalance_' + str_binetas[e] + '.pdf')
    index += NptBins

dir3 = 'jet_response_vs_refpt_alpha_1p0'
os.makedirs(dir3, exist_ok = True)

index = 0
for e in range(NetaBins):
    str1 = '[' + str("{:.1f}".format(jetetaBins[e])) + ',' + str("{:.1f}".format(jetetaBins[e+1])) + ')' 

    #print('Adding histograms to: ', h_ptBalance_vs_ref_alpha_ptincl_1p0[index].GetName())
    # Here we add all the different pt histograms such that we have one histogram per eta and alpha bin
    for p in range(NptBins-1):
        h_ptBalance_vs_refpt_alpha_incl_1p0_MC[index].Add(h_ptBalance_vs_refpt_alpha_incl_1p0_MC[index+p+1])
        h_ptBalance_vs_refpt_alpha_incl_1p0_dt[index].Add(h_ptBalance_vs_refpt_alpha_incl_1p0_dt[index+p+1])
        #print(' adding: ', h_ptBalance_vs_refptalpha_incl_1p0[index+p+1].GetName())

    c = TCanvas(str1, str1, 1000, 1000)
    gPad.SetLogx()
    h_ptBalance_vs_refpt_alpha_incl_1p0_dt[index].GetXaxis().SetMoreLogLabels()
    h_ptBalance_vs_refpt_alpha_incl_1p0_dt[index].GetXaxis().SetNoExponent()
    h_ptBalance_vs_refpt_alpha_incl_1p0_dt[index].SetMaximum(1.25)
    h_ptBalance_vs_refpt_alpha_incl_1p0_dt[index].SetMinimum(0.5)
    h_ptBalance_vs_refpt_alpha_incl_1p0_dt[index].SetMarkerStyle(8)
    h_ptBalance_vs_refpt_alpha_incl_1p0_dt[index].SetMarkerSize(1.4)
    h_ptBalance_vs_refpt_alpha_incl_1p0_dt[index].SetMarkerColor(kBlue+1)
    h_ptBalance_vs_refpt_alpha_incl_1p0_dt[index].SetLineColor(kBlue+1)
    h_ptBalance_vs_refpt_alpha_incl_1p0_dt[index].SetTitle('p_{T} balance: #eta=' + str1 + ', #alpha < 1.0')
    h_ptBalance_vs_refpt_alpha_incl_1p0_dt[index].GetXaxis().SetTitle('p_{T}^{#gamma} (GeV)')
    h_ptBalance_vs_refpt_alpha_incl_1p0_dt[index].GetXaxis().SetTitleOffset(1.3)
    h_ptBalance_vs_refpt_alpha_incl_1p0_dt[index].GetYaxis().SetTitle('p_{T} balance')
    h_ptBalance_vs_refpt_alpha_incl_1p0_dt[index].GetYaxis().SetLabelSize(0.03)
    h_ptBalance_vs_refpt_alpha_incl_1p0_dt[index].GetYaxis().SetTitleOffset(1.4)
    #h_ptBalance_vs_refpt_alpha_incl_1p0_dt[index].GetXaxis().SetRangeUser(115., 1000.) # For VBF
    h_ptBalance_vs_refpt_alpha_incl_1p0_MC[index].GetXaxis().SetMoreLogLabels()
    h_ptBalance_vs_refpt_alpha_incl_1p0_MC[index].GetXaxis().SetNoExponent()
    h_ptBalance_vs_refpt_alpha_incl_1p0_MC[index].SetMaximum(1.25)
    h_ptBalance_vs_refpt_alpha_incl_1p0_MC[index].SetMinimum(0.5)
    h_ptBalance_vs_refpt_alpha_incl_1p0_MC[index].SetMarkerStyle(8)
    h_ptBalance_vs_refpt_alpha_incl_1p0_MC[index].SetMarkerSize(1.4)
    h_ptBalance_vs_refpt_alpha_incl_1p0_MC[index].SetMarkerColor(kRed+1)
    h_ptBalance_vs_refpt_alpha_incl_1p0_MC[index].SetLineColor(kRed+1)
    h_ptBalance_vs_refpt_alpha_incl_1p0_MC[index].SetTitle('p_{T} balance: #eta=' + str1 + ', #alpha < 0.3')
    h_ptBalance_vs_refpt_alpha_incl_1p0_MC[index].GetXaxis().SetTitle('p_{T}^{#gamma} (GeV)')
    h_ptBalance_vs_refpt_alpha_incl_1p0_MC[index].GetXaxis().SetTitleOffset(1.3)
    h_ptBalance_vs_refpt_alpha_incl_1p0_MC[index].GetYaxis().SetTitle('p_{T} balance')
    h_ptBalance_vs_refpt_alpha_incl_1p0_MC[index].GetYaxis().SetLabelSize(0.03)
    h_ptBalance_vs_refpt_alpha_incl_1p0_MC[index].GetYaxis().SetTitleOffset(1.4)
    #h_ptBalance_vs_refpt_alpha_incl_1p0_MC[index].GetXaxis().SetRangeUser(115., 1000.) # For VBF
    h_ptBalance_vs_refpt_alpha_incl_1p0_dt[index].Draw()
    h_ptBalance_vs_refpt_alpha_incl_1p0_MC[index].Draw('same')

    leg = TLegend(0.62,0.75,0.92,0.90)
    leg.AddEntry(h_ptBalance_vs_refpt_alpha_incl_1p0_MC[index], "MC (G-4Jets)", "l")
    leg.AddEntry(h_ptBalance_vs_refpt_alpha_incl_1p0_dt[index], "Data (EGamma)", "l")
    leg.SetBorderSize(0)
    leg.SetFillStyle(0)
    leg.Draw()
    gPad.RedrawAxis()

    c.SaveAs(dir3 + '/ptBalance_' + str_binetas[e] + '.png')
    #c.SaveAs(dir3 + '/ptBalance_' + str_binetas[e] + '.pdf')
    index += NptBins

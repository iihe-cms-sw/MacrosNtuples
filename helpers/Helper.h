#include "ROOT/RDataFrame.hxx"
#include "ROOT/RVec.hxx"
#include "TCanvas.h"
#include "TH1D.h"
#include "TLatex.h"
#include "Math/Vector4D.h"
#include "TStyle.h"
 
using namespace ROOT;
using namespace ROOT::VecOps;
using RNode = ROOT::RDF::RNode;
int EventsToPrint = 0;

vector<int> FindL1ObjIdx(ROOT::VecOps::RVec<float>L1Obj_eta, ROOT::VecOps::RVec<float>L1Obj_phi, ROOT::VecOps::RVec<float>recoObj_Eta, ROOT::VecOps::RVec<float>recoObj_Phi, ROOT::VecOps::RVec<int>L1Obj_CutVar={}, int CutVar=-1){
  vector <int> result={};
  for(unsigned int i = 0; i<recoObj_Eta.size(); i++){
    double drmin = 0.4; 
    int idx = -1;
    for(unsigned int j = 0; j<L1Obj_eta.size(); j++){

      if(L1Obj_CutVar.size()==L1Obj_eta.size()){
	if(L1Obj_CutVar[j]<CutVar)continue;
      }
      double deta = abs(recoObj_Eta[i]-L1Obj_eta[j]);
      double dphi = abs(acos(cos(recoObj_Phi[i]-L1Obj_phi[j]))); 
      double dr = sqrt(deta*deta+dphi*dphi);
      if(dr<=drmin){ 
	drmin = dr; 
	idx = j;
      }
    }
    result.push_back(idx);
  }
  return result;
}



ROOT::VecOps::RVec<float> GetVal(ROOT::VecOps::RVec<int>idxL1Obj, ROOT::VecOps::RVec<float>L1Obj_val){
  ROOT::VecOps::RVec<float> result ={}; 
  for(unsigned int i = 0; i<idxL1Obj.size(); i++){
    if(idxL1Obj[i]<0) result.push_back(-1);
    else result.push_back(L1Obj_val[idxL1Obj[i]]);
  }
  return result;
}



vector<float> HighestMjj_L1(ROOT::VecOps::RVec<float>pt, ROOT::VecOps::RVec<float>eta, ROOT::VecOps::RVec<float>phi,  ROOT::VecOps::RVec<int>bx){

  vector<float> result;
  result.push_back(0);
  result.push_back(0);
  result.push_back(0);
  result.push_back(0);
  result.push_back(0);
  for(unsigned int i = 0; i<pt.size(); i++){
    if(pt[i]<30.)continue;
    if(bx[i]!=0)continue;
    for(unsigned int j = 0; j<pt.size(); j++){
      if(eta[i]*eta[j]>0) continue;
      if(pt[j]<30.)continue;
      if(bx[j]!=0)continue;
      TLorentzVector jet1, jet2;
      jet1.SetPtEtaPhiM(pt[i], eta[i], phi[i], 0.);
      jet2.SetPtEtaPhiM(pt[j], eta[j], phi[j], 0.);
      float mass = (jet1+jet2).Mag();
      if(mass>result[0]){
	result[0] = mass;
	result[3] = abs(eta[i]-eta[j]);
	result[4] = abs(acos(cos(phi[i]-phi[j])));
	if(pt[j]> pt[i]){ result[1] = pt[j] ; result[2] = pt[i] ;}
	else {  result[1] = pt[i] ; result[2] = pt[j] ; }
      }
    }
  }
  return result;
}





bool L1SeedDoubleJetEtaMin(ROOT::VecOps::RVec<float>pt, ROOT::VecOps::RVec<float>eta, ROOT::VecOps::RVec<float>phi,  ROOT::VecOps::RVec<int>bx, double ptlead, double pttrail, double detacut, double dphicut){
  for(unsigned int i = 0; i<pt.size(); i++){
    if(pt[i]<ptlead)continue;
    if(bx[i]!=0)continue;
    for(unsigned int j = 0; j<pt.size(); j++){
      if(eta[i]*eta[j]>0) continue;
      if(pt[j]<pttrail)continue;
      if(bx[j]!=0)continue;
      float dphi = abs(acos(cos(phi[i]-phi[j])));
      if(abs(eta[i]-eta[j]) >= detacut&& dphi< dphicut )return true;
    }      
  }
  return false;
}


bool L1SeedDoubleJetMassMin(ROOT::VecOps::RVec<float>pt, ROOT::VecOps::RVec<float>eta, ROOT::VecOps::RVec<float>phi,  ROOT::VecOps::RVec<int>bx, double ptlead, double pttrail, double masscut, double dphicut){
  for(unsigned int i = 0; i<pt.size(); i++){
    if(pt[i]<ptlead)continue;
    if(bx[i]!=0)continue;
    for(unsigned int j = 0; j<pt.size(); j++){
      if(eta[i]*eta[j]>0) continue;
      if(pt[j]<pttrail)continue;
      if(bx[j]!=0)continue;

      TLorentzVector jet1, jet2;
      jet1.SetPtEtaPhiM(pt[i], eta[i], phi[i], 0.);
      jet2.SetPtEtaPhiM(pt[j], eta[j], phi[j], 0.);
      float mass = (jet1+jet2).Mag();
      float dphi = abs(acos(cos(phi[i]-phi[j])));
      if(mass >= masscut && dphi< dphicut )return true;
    }      
  }
  return false;
}


#!/Usr-/bin/env python
import os,sys
from PhysicsTools.NanoAODTools.postprocessing.framework.postprocessor import * 
from WTopScalefactorProducer.Skimmer.skimmer import Skimmer
if len(sys.argv)>1:
   infile = sys.argv[1].split(',')
else:
  infile = [
#      "root://cms-xrd-global.cern.ch//store/data/Run2018D/SingleMuon/NANOAOD/Nano14Dec2018_ver2-v1/80000/CA6BFADB-55E3-3246-B1A0-4901C4A8629D.root"
#    "root://cms-xrd-global.cern.ch//store/data/Run2018B/SingleMuon/NANOAOD/Nano14Dec2018-v1/90000/DCE0C611-C17C-B845-9430-70073E7B1D5B.root"
      "root://cms-xrd-global.cern.ch//store/mc/RunIIFall17NanoAODv4/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8/NANOAODSIM/PU2017_12Apr2018_Nano14Dec2018_new_pmx_102X_mc2017_realistic_v6-v1/10000/73EF6D03-FCD7-0C40-AA72-6CE9F1EE1ECD.root"
#    "root://cms-xrd-global.cern.ch//store/mc/RunIIFall17NanoAODv4/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8/NANOAODSIM/PU2017_12Apr2018_Nano14Dec2018_new_pmx_102X_mc2017_realistic_v6-v1/10000/0ABFB9E6-C892-144D-AFB8-ED9E0D8AFB1A.root"
  ]

if len(sys.argv)>2: outputDir = sys.argv[2]
else: outputDir = "TEST"	

if len(sys.argv)>3: name = sys.argv[3]
else: name = "test.root"

if len(sys.argv)>4: chunck = sys.argv[4]
else: chunck = ""  

#"keep_and_drop.txt"
#FatJet_msoftdrop>30&&MET_sumEt>40&&    ((nElectron>0&&HLT_Ele115_CaloIdVT_GsfTrkIdT)||
if infile[0].find("SingleMuon")!=-1:
  channel = "mu"
  print "Processing a Single Muon dataset file..."
  p=PostProcessor(outputDir, infile,"" ,"",
                    modules=[Skimmer(channel)],provenance=False,fwkJobReport=False,
                    jsonInput='/work/zucchett/CMSSW_10_2_6/src/WTopScalefactorProducer/Skimmer/python/JSON/Cert_314472-325175_13TeV_PromptReco_Collisions18_JSON.txt')
                   
elif infile[0].find("SingleElectron")!=-1:
  channel = "el"
  print "Processing a Single Electron dataset file..."
  p=PostProcessor(outputDir, infile,"" ,"",
                    modules=[Skimmer(channel)],provenance=False,fwkJobReport=False,
                    jsonInput='/afs/cern.ch/cms/CAF/CMSCOMM/COMM_DQM/certification/Collisions18/13TeV/PromptReco/Cert_314472-325175_13TeV_PromptReco_Collisions18_JSON.txt')
                    
else:
  print "Processing MC..."
  channel = "mu"
  p=PostProcessor(outputDir, infile, "" ,"",
                    modules=[Skimmer(channel)],provenance=False,fwkJobReport=False)
p.run()
print "DONE"

### Producing JMAR skims of expanded NanoAOD datasets

#To make JMAR Skims (Loose skim with >=1 AK8 Jet with Pt > 200 GeV and >=1 Lepton ):
#```
#cd crab/JMARskim
#ln -s $CMSSW_BASE/src/PhysicsTools/NanoAODTools/scripts/haddnano.py .
#python  submit_all_uif.py  -c  PSet.py -d June5_nanoskim-JetsAndLepton  -f test94X_DY_madgraph.txt
# 
#```

Step1 :

Use JMAR twiki to find sample

https://twiki.cern.ch/twiki/bin/view/CMS/JetMET/JMARNanoAODv1

Step 2 :

Use DAS to find file location

https://cmsweb.cern.ch/das/request?instance=prod/phys03&input=file+dataset%3D%2FTTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8%2Falgomez-TTToSemiLeptonicTuneCP513TeV-powheg-pythia8RunIIFall17MiniAODv2-PU201712Apr2018newpmx-2632477341b0033d0ee33ee9e5481e57%2FUSER



Step 3 :

make a txt file of the files you need

xrdfsls -u /store/group/lpctlbsm/NanoAODJMAR_2019_V1/Production/CRAB/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8/TTToSemiLeptonicTuneCP513TeV-powheg-pythia8RunIIFall17MiniAODv2-PU201712Apr2018newpmx/190326_110839/0000/ | grep 'NANO' >& nanoskim-TTToSemiLeptonicTuneCP513TeV-powheg-pythia8RunIIFall17MiniAODv2-PU201712Apr2018newpmx-filenames4CRAB.txt &

Step 4 :

change redirector to global one :  cms-xrd-global.cern.ch cms-xrd-global.cern.ch

Step 5 :

write CRAB command

cmsenv
scrab
 voms-proxy-initvoms cms
python submitCRABfilelist.py --f nanoskim-TTToSemiLeptonicTuneCP513TeV-powheg-pythia8RunIIFall17MiniAODv2-PU201712Apr2018newpmx-filenames4CRAB.txt  --e 2017MC --t Aug5
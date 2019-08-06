import argparse
import subprocess

# set up an argument parser
parser = argparse.ArgumentParser()
parser.add_argument('--f', dest='INFILENAME')
parser.add_argument('--e', dest='ERA') #2017MC or 2017DATA are only options for now
parser.add_argument('--t', dest='TAG')
ARGS = parser.parse_args()

### This scrip makes all of the files needed to submit the CRAB job:
### The CRAB config - crabConfig.py
### The scriptexe - runPostProcessor.sh
### The crab script (that runs the nanaod-tools postprocessor on the nano ntuples) - runPostProcessor.py



# make a CRAB config file with template arguments
CRAB_CFG = '''

from CRABClient.UserUtilities import config, getUsernameFromSiteDB
config = config()

datasetsFile = open( '{INFILENAME}' )
jobsLines = datasetsFile.readlines()
name = ''
splits = jobsLines[0].split('/')
#name = jobsLines[0].split('/')[5][21:]                                                                                  
for s in splits :
    if 'MiniAOD' in s :
        name = s

#if 'extendedNANOSkim' in name :
#    name = name.split('extendedNANOSkim_')[1]
#elif '94X_' in name :                                                                                                        #    name =    name.split('94X_')[1]
#elif 'JetsAndLepton-94XMC-' in name :
#    name.split('94XMC-')[1]
#elif 'JetsAndLepton-Data-' in name :                                                                                         #    name.split('Lepton-')[1]  

rn = 'TTSemiLeptSkim_%s_%s'%('{TAG}', name)

#if 'TTJets' in '{INFILENAME}':
#    infin = '{INFILENAME}'
#    #numt = infin.split('RunIIFall17')[1]
#    if '17' in ARGS.ERA:
#        numt = infin.split('RunIIFall17')[1]
#    elif '16' in ARGS.ERA : 
#        numt = infin.split('16')[1]
#    namt = numt.split('_filenames4CRAB')[0]
#    rn = rn + str(namt)
#nanoskim-JetsAndLepton-94XMC-TTJets_TuneCP5_13TeV-amcatnloFXFX-pythia8_RunIIFall17_1of3_filenames4CRAB.txt


if len(rn) > 99 : 
    rn = rn.split('-')[0]

#'ZplusJetSkim_Nov16_-Sept24-94XMC-extendedNANOSkim_DYJetsToLL_M-50_HT-100to200_TuneCP5_13TeV-madgraphM'

#rn= ''.join((rn[:100-len(rn)]).split('_')[:-1])

config.General.requestName   = rn
print rn
config.General.workArea      = 'crabBattle_%s'%('{TAG}')

config.JobType.pluginName    = 'Analysis'
config.JobType.psetName      = 'PSet.py'
config.JobType.outputFiles = [ 'TTSemilept_SkimNANO-trees.root','TTSemilept_SkimNANO-histos.root' ]
config.JobType.scriptExe = 'runPostProcessor.sh'
config.JobType.inputFiles =  [ 'PSet.py' ,'runPostProcessor.sh', 'runPostProcessor.py' ,'./haddnano.py', 'keep_and_drop.txt']

#[ 'PSet.py' ,'runPostProcessor.sh', 'runPostProcessor.py' ,'./haddnano.py', 'keep_and_drop.txt', '/uscms_data/d3/aparker/2018/ZJet_Nov18/CMSSW_9_4_10/src/data/egammaEffi_EGM2D.root' , '/uscms_data/d3/aparker/2018/ZJet_Nov18/CMSSW_9_4_10/src/data/2017_ElectronMedium.root' , '/uscms_data/d3/aparker/2018/ZJet_Nov18/CMSSW_9_4_10/src/data/RunBCDEF_SF_ISO_syst.root' , '/uscms_data/d3/aparker/2018/ZJet_Nov18/CMSSW_9_4_10/src/data/RunBCDEF_SF_ID_syst.root' , '/uscms_data/d3/aparker/2018/ZJet_Nov18/CMSSW_9_4_10/src/data/EfficienciesAndSF_RunBtoF_Nov17Nov2017.root' ]

# https://twiki.cern.ch/twiki/bin/view/CMS/MuonReferenceEffs2016LegacyRereco
# https://twiki.cern.ch/twiki/bin/view/CMS/EgammaIDRecipesRun2
config.JobType.sendPythonFolder  = True


config.Data.outputDatasetTag = rn
config.Data.splitting = 'FileBased'
config.Data.publication = False
config.Data.unitsPerJob      = int(1)
config.Data.outLFNDirBase    = '/store/group/lpctlbsm/ZplusJetSkims_%s/CRAB/' % ( '{TAG}' ) # getUsernameFromSiteDB()
config.Site.storageSite = 'T3_US_FNALLPC'
config.Data.inputDataset     = None

filelist = []
for l in jobsLines:
    filelist.append(str(l[:-1]))
print filelist
config.Data.userInputFiles = filelist


print 'Configuration :'
print config

'''

# open crabConfig.py, substitute into CRAB_CFG the arguments from ARGS, write it, run it, and remove it

open('crabConfig.py', 'w').write(CRAB_CFG.format(**ARGS.__dict__))


### make the runPostProcessor.py script

CRAB_SCRIPT = '''

#!/Usr-/bin/env python                                                                                                                                                                                                                                     
import os,sys
#import ROOT
from importlib import import_module

### Import the nanoAODtools
from PhysicsTools.NanoAODTools.postprocessing.framework.postprocessor import PostProcessor
from PhysicsTools.NanoAODTools.postprocessing.framework.datamodel import Collection
from PhysicsTools.NanoAODTools.postprocessing.framework.eventloop import Module
#from PhysicsTools.NanoAODTools.postprocessing.modules.jme.jetmetUncertainties import *
#from PhysicsTools.NanoAODTools.postprocessing.modules.jme.jetRecalib import *
from PhysicsTools.NanoAODTools.postprocessing.modules.common.puWeightProducer import *
#from PhysicsTools.NanoAODTools.postprocessing.modules.common.pdfWeightProducer import * 

#this takes care of converting the input files from CRAB                                                                                                                                                                                                                                                                     
from PhysicsTools.NanoAODTools.postprocessing.framework.crabhelper import inputFiles,runsAndLumis

### this is the selection module to pick Z + Jets events
#from Analysis.QJetMass.skimmers.ZPlusJet_SkimNANO import *
#from ZPlusJet_SkimNANO4 import *
from TTSkimmer_Aug5 import *


era =  '{ERA}'
preselection = ''
modulesToRun = []

if '17MC' in era :
    #modulesToRun.append( pdfWeightProducer() ) 
    #modulesToRun.append( jetmetUncertainties2017AK8PFPuppiAll() )
    modulesToRun.append( puAutoWeight() )
if '16MC' in era :                                                                                                                          
    #modulesToRun.append( pdfWeightProducer() )                                                                                              
    #modulesToRun.append( jetmetUncertainties2016AK8PFPuppiAll() )                                                                           
    modulesToRun.append( puWeight() )  

if '17' in era :
    preselection = "nFatJet>0 && FatJet_pt>200 &&  abs(FatJet_eta)<2.5  &&   Jet_pt>30 && abs(Jet_eta)<2.5  && ( nMuon>0 || nElectron > 0   )"
if '16' in era : 
    preselection = ""# NONE FIX THIS

modulesToRun.append( TTbar_SemiLep() )


print "era"
print era
print "preselection"
print preselection

nameis = 'TTSemilept_SkimNANO'                                                                                                                                                                                                                                                                                                 
p1=PostProcessor(".", inputFiles()  , preselection, "keep_and_drop.txt", modulesToRun, provenance=True,fwkJobReport=True,histFileName= nameis +'-histos.root', histDirName='ttsemilept', haddFileName =  nameis +'-trees.root',jsonInput=runsAndLumis() )

#if '16MC' in era :
#    print "ERROR not running: Not yet set up to process 2016 data or MC, fix preselection triggers for this!"
#else :
p1.run()

print "DONE"
#os.system("ls -lR")

'''

open('runPostProcessor.py', 'w').write(CRAB_SCRIPT.format(**ARGS.__dict__))


BASH_SCRIPT = '''

#this is not mean to be run locally                                                                                                                                                                                                                                                                                          
#                                                                                                                                                                                                                                                          
echo Check if TTY
if [ "`tty`" != "not a tty" ]; then
  echo "YOU SHOULD NOT RUN THIS IN INTERACTIVE, IT DELETES YOUR LOCAL FILES"
else

ls -lR .
echo "ENV..................................."
env
echo "VOMS"
voms-proxy-info -all
echo "CMSSW BASE, python path, pwd"
echo $CMSSW_BASE
echo $PYTHON_PATH
echo $PWD
rm -rf $CMSSW_BASE/lib/
rm -rf $CMSSW_BASE/src/
rm -rf $CMSSW_BASE/module/
rm -rf $CMSSW_BASE/python/
mv lib $CMSSW_BASE/lib
mv src $CMSSW_BASE/src
mv python $CMSSW_BASE/python

echo Found Proxy in: $X509_USER_PROXY

echo "python runPostProcessor.py  .......---------------" 
python runPostProcessor.py $1                                                                                                
fi
'''
open('runPostProcessor.sh', 'w').write(BASH_SCRIPT.format(**ARGS.__dict__))

#use crabConfig.py- run it, and remove it
subprocess.call('crab submit -c crabConfig.py', shell=True)
subprocess.call('echo "crab submit -c crabConfig.py"', shell=True)
subprocess.call('rm crabConfig.py', shell=True)


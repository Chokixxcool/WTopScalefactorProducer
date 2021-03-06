### W-tagging scalefactor producer ###
#########################################

Repository for fitting W-tagging scalefactors in a semi-leptonic ttbar enriched region. Contains code to skim nanoAOD samples using a semi-leptonic ttbar selection (WTopScalefactorProducer/Skimmer). This output is then used to fit data and MC and extract W-tagging scalefactors (WTopScalefactorProducer/Fitter) both from fitting the AK8 W-jet mass at low-pT (around 200 GeV) and fitting the top AK8 W-subjet mass (around 400 GeV). The calculated scalefactors are then statistically combined and fitted, yielding a parametrisation for the W-tagging pT-dependence.

WTopScalefactorProducer/Skimmer : Start here. Produce samples.
WTopScalefactorProducer/Fitter  : Based on output from above, run script mainBLABLA.sh to compute fully- and partially-merged W-tagging scalfactors as well as statistically combining the two

## installation instructions for CMSSW_10_2_X
Setup CMSSW and get nanoAOD packages
```
cmsrel CMSSW_10_2_6
cd CMSSW_10_2_6/src
cmsenv

git clone https://github.com/cms-nanoAOD/nanoAOD-tools.git PhysicsTools/NanoAODTools
scram b -j8

cd $CMSSW_base/src
git clone git@github.com:Chokixxcool/WTopScalefactorProducer.git
cd WTopScalefactorProducer
```

## Step 1: Producing samples

First you need to produce your input files by skimming nanoAOD samples. For this, see README in subdirectory Skimmer/.


## Step 2: Running scalefactor code

When you have skimmed your samples you can move to fitting the W-tagging scalefactor. The fitting code is located in Fitter/, see README in that directory. For scalefactors from merged W AK8 jet, use Fitter/partiallyMerged. For scalefactors from merged top AK8 jet, use Fitter/fullyMerged


import os
import sys
import optparse
import re
import commands
import das_client
import json

def listFichier(theRelease, theSample, dataTier, tag):
	theQuery = "file dataset=/"+theSample+"*/"+theRelease+"-"+tag+"*/"+dataTier
	jsondict = das_client.get_data('https://cmsweb.cern.ch', theQuery, 0, 0, False)
	status = jsondict['status']
	if status != 'ok':
		print "DAS query status: %s"%(status)
	data = jsondict['data']
	theFileList = []
	for aRaw in data:
		recordStuff = aRaw['file']
   		for aRecord in recordStuff:
        		print "theFile===",aRecord['name']
        		theFileList.append(aRecord['name'])
   	return theFileList



print "inPYthon"

#listFichier('CMSSW_7_1_0_pre5','RelValZMM')

file = open("listSample","r")
jobs = file.readlines()
file.close()

file = open("hltHiggsValidator_cfg.py","r")
scriptLine = file.readlines()
file.close()

sizeList = len(jobs)
listIterator = 2



if (sizeList<3):
    print "size list too small"

sampleRelease = jobs[0][:-1]
sampleTag = jobs[1][:-1]
while (listIterator<sizeList):
    theJob = jobs[listIterator][:-1]
    print "will do ",theJob
    listIterator = listIterator+1
    outFile = open("hltHiggsValidator_"+theJob+".py","w")
    for line in scriptLine:
        if len(re.split("theRECOfiles",line))> 1:
            theFileList = listFichier(sampleRelease, theJob, "GEN-SIM-RECO",sampleTag)
            for theSingleFile in theFileList:
                outFile.write("'"+theSingleFile+"',\n")
            continue
        if len(re.split("theRAWfiles",line))> 1:
            theFileList = listFichier(sampleRelease, theJob, "GEN-SIM-DIGI-RAW-HLTDEBUG",sampleTag)
            for theSingleFile in theFileList:
                outFile.write("'"+theSingleFile+"',\n")
            continue
        if len(re.split("fileName",line))> 1:
            outFile.write("fileName = cms.untracked.string('hltHiggsValidator_"+theJob+".root')")
            continue
        outFile.write(line)










from __future__ import division
import sklearn.ensemble
from lxml import etree
from lxml import html
from bs4 import BeautifulSoup
import scipy as sp
from scipy import stats
import numpy as np
import cPickle as pickle
import sys
import math
import time
import urllib
from functools import reduce
from timeit import timeit
from collections import Counter
import random

np.set_printoptions(precision=3)

def errormat(out,actual):
    error = np.zeros([7,7])
    for i in range(0,len(out)):
        for j in range(1,8):
            if actual[i] == j:
                if out[i] == 1:
                    error[j-1,0] += 1
                elif out[i] == 2:
                    error[j-1,1] += 1
                elif out[i] == 3:
                    error[j-1,2] += 1
                elif out[i] == 4:
                    error[j-1,3] += 1
                elif out[i] == 5:
                    error[j-1,4] += 1
                elif out[i] == 6:
                    error[j-1,5] += 1
                elif out[i] == 7:
                    error[j-1,6] += 1
    return error


def pitchscore(pitchall):
    #print len(pitchall)
    if type(pitchall) == str:
        pitch = pitchall
        #pt = np.zeros([1,1])
        if 'FA' in pitch or 'FF' in pitch or 'FT' in pitch or 'FS' in pitch or 'SF' in pitch:
                pt=1
        elif 'FC' in pitch:
            pt = 2
        elif 'SI' in pitch:
            pt=3
        elif 'SL' in pitch:
            pt=4
        elif 'CH' in pitch:
            pt=6
        elif 'CB' in pitch or 'CU' in pitch or 'KC' in pitch or 'SC' in pitch:
            pt=5
        elif 'KN' in pitch or 'EP' in pitch:
            pt = 7
        elif '0' in pitch:
            pt = 0
        else:
            pt=-1
    else:
        pt = np.zeros([len(pitchall),1])
        pt = pt - np.ones([len(pitchall),1])
        pitches = pitchall
        FBinds = np.concatenate((np.asarray(np.where(pitches == 'FA')[0]),np.asarray(np.where(pitches == 'FF')[0]),np.asarray(np.where(pitches == 'FT')[0]),np.asarray(np.where(pitches == 'FS')[0]),np.asarray(np.where(pitches == 'SF')[0])))
        FCinds = np.asarray(np.where(pitches == 'FC'))
        SIinds = np.asarray(np.where(pitches == 'SI'))
        SLinds = np.asarray(np.where(pitches == 'SL'))
        CBinds = np.concatenate((np.asarray(np.where(pitches == 'CU')[0]),np.asarray(np.where(pitches == 'KC')[0]),np.asarray(np.where(pitches == 'SC')[0])))
        CHinds = np.asarray(np.where(pitches == 'CH'))
        KNinds = np.concatenate((np.asarray(np.where(pitches == 'KN')[0]),np.asarray(np.where(pitches == 'EP')[0])))
        Zinds = np.asarray(np.where(pitches == '0'))
        pt[FBinds] = 1
        pt[FCinds] = 2
        pt[SIinds] = 3
        pt[SLinds] = 4
        pt[CBinds] = 5
        pt[CHinds] = 6
        pt[KNinds] = 7
        pt[Zinds] = 0
    return pt

def getcount(pitches):

    count = np.empty([7,1])
    #for i in range(0,6):
    count[0] = len(np.where(pitches == 1)[0])
    count[1] = len(np.where(pitches == 2)[0])
    count[2] = len(np.where(pitches == 3)[0])
    count[3] = len(np.where(pitches == 4)[0])
    count[4] = len(np.where(pitches == 5)[0])
    count[5] = len(np.where(pitches == 6)[0])
    count[6] = len(np.where(pitches == 7)[0])

    if np.sum(count) > 0:
        return np.ceil(10000*count.T/np.sum(count))/10000
    else:
        return count.T

def getbatterstats(bID,allbats,bpt,typebs):
    outmat = np.zeros([1,22])
    bInds = np.where(allbats == bID)[0]

    
    s1 = np.where(typebs[bInds] == 'S')
    b1 = np.where(typebs[bInds] == 'B')
    ip1 = np.where(typebs[bInds] == 'X')

    try:
        temp1 = getcount(bpt[ip1])
    except TypeError:
        temp1 = np.zeros([1,7])
    try:
        temp2 = getcount(bpt[s1])
    except TypeError:
        temp2 = np.zeros([1,7])
    try:
        temp3 = getcount(bpt[b1])
    except TypeError:
        temp3 = np.zeros([1,7])
    outmat[:,0:7] = temp1
    outmat[:,7:14] = temp2
    outmat[:,14:21] = temp3
    outmat[:,21] = bID

    return outmat

def makeliveprediction(day):

    print 'Loading...'

    start = time.clock()
    with open('MLBData2012through2016.pkl','rb') as input:
        Data = pickle.load(input)
    print time.clock() - start

    print 'Loaded'

    #print np.unique(Data.res_des,return_counts=True)

    ovrinds = np.asarray(range(0,len(Data.Inning)))

    predayinds = np.intersect1d(ovrinds[np.where(Data.gameID > 201500000000)[0]],ovrinds[np.where(Data.gameID < day)[0]])

    #print len(predayinds)

    curdayinds = np.intersect1d(ovrinds[np.where(Data.gameID > day)[0]],ovrinds[np.where(Data.gameID < day + 10000)[0]])

    #print curdayinds

    pitcherstoday = np.unique(Data.pitcher[curdayinds])

    print len(pitcherstoday)

    batterstoday = np.unique(Data.batter[curdayinds])

    batmat = np.zeros([len(batterstoday),22])

    print np.shape(batmat)

    for i in range(0,len(batterstoday)):
        batmat[i,:] = getbatterstats(batterstoday[i],Data.batter[predayinds],pitchscore(Data.outpitch[predayinds]),Data.res_typebs[predayinds])
   
    print 'Batters Done'

    print batmat

    dayout = np.zeros([1,6]);

    ind = 0

    for pitcher in pitcherstoday:
    
        print pitcher
        
        try:

            data = np.loadtxt('PitDataUpdate/' + str(pitcher) + 'Data2014pwCut.txt')
            outputs = np.loadtxt('PitDataUpdate/' + str(pitcher) + 'Outputs2014pwCut.txt')
            
            pretoday = np.where(data[:,0] < day)[0]
            today = np.intersect1d(np.where(data[:,0] > day)[0],np.where(data[:,0] < day + 10000))
            traindata = data[pretoday,1:110]
            trainoutputs = outputs[pretoday,:]
            
            spdata = np.column_stack((traindata[:,0:24],trainoutputs[:,1].astype(int)))
            zdata = np.column_stack((spdata,trainoutputs[:,2].astype(int)))
            pmodels = []; spmodels = []; zmodels = [];
            for i in range(0,10):
                clf = sklearn.ensemble.RandomForestClassifier(n_estimators=100)
                clf = clf.fit(traindata[:,0:108],trainoutputs[:,0].astype(int))
                clf2 = sklearn.ensemble.RandomForestRegressor(n_estimators=100)
                clf2 = clf2.fit(spdata,trainoutputs[:,1])
                clf3 = sklearn.ensemble.RandomForestClassifier(n_estimators=100)
                clf3 = clf3.fit(zdata,trainoutputs[:,2].astype(int))
                pmodels.append(clf)
                spmodels.append(clf2)
                zmodels.append(clf3)
            
            print 'Models made'

            todaydata = np.zeros([len(today),108])

            todaydata[:,:20] = data[today,1:21]
            todaydata[:,24:73] = data[today,25:74]

            for i in range(0,len(today)):

                strikes = todaydata[i,9]
                balls = todaydata[i,8]
                countinds = np.intersect1d(np.where(traindata[:,9] == strikes)[0],np.where(traindata[:,8] == balls)[0])
                spot = countinds[len(countinds)-1]
                todaydata[i,73:80] = traindata[spot,73:80]
                binds = np.where(traindata[:,108] == data[today[i],108])[0]
                if len(binds) > 0:
                    spot2 = binds[len(binds)-1]
                    todaydata[i,80:87] = traindata[spot2,80:87]
                else:
                    todaydata[i,80:87] = np.zeros([1,7])
                bspot = np.where(batmat[:,21] == int(data[today[i],109]))
                todaydata[i,87:108] = batmat[bspot,0:21]
                prvptype = todaydata[i,17]
                pinds = np.where(traindata[:,17] == prvptype)[0]
                todaydata[i,20:24] = np.mean(traindata[pinds,20:24],axis=0)

            pred1 = np.zeros([len(today),10]); pred2 = np.zeros([len(today),10]); pred3 = np.zeros([len(today),10])
            for i in range(0,10):
                pred1[:,i] = pmodels[i].predict(todaydata)
                newinput = np.hstack((todaydata[:,0:24],np.atleast_2d(pred1[:,i]).T))
                pred2[:,i] = spmodels[i].predict(newinput)
                newinput2 = np.hstack((newinput,np.atleast_2d(pred2[:,i]).T))
                pred3[:,i] = zmodels[i].predict(newinput2)

            outpitch = stats.mode(pred1,axis=1)[0]
            outspeed = np.mean(pred2,axis=1)
            outzone = stats.mode(pred3,axis=1)[0]

            outs = np.hstack((outpitch,np.atleast_2d(outputs[today,0]).T,np.atleast_2d(outspeed).T,np.atleast_2d(outputs[today,1]).T,outzone,np.atleast_2d(outputs[today,2]).T))

            name = np.atleast_2d(np.asarray([pitcher]*6))

            print errormat(outpitch,outputs[today,0])
            
            print np.abs(np.mean(np.atleast_2d(outspeed).T - np.atleast_2d(outputs[today,1]).T))
            
            outtemp = np.vstack((name,outs))

            dayout = np.vstack((dayout,outtemp))

            str1 = '%i %i %2.2f %2.2f %i %i'

            np.savetxt('100TreesLive/' + str(day)[0:8] + 'dailyprediction.txt',dayout,str1)
            
            ind += 1
            print ind

        except Exception as e:
            print e
            continue

lst = range(1,3)

#lst.insert(0,1)
print lst

for i in lst:

    jump = i*10000
    day = 201610000000 + jump
    makeliveprediction(day)




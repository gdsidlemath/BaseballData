from __future__ import division
from scipy import stats
import numpy as np
import cPickle as pickle
from definedataclass import GamePitchData
import sys
import math
import time
from functools import reduce
from timeit import timeit

np.set_printoptions(precision=3)

def fixstand(stand):
    ost = np.zeros([len(stand),1])

    ost[np.where(stand == 'R')] = 1

    return ost

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

def eventscore(eventall):
    if type(eventall) == str:
        event = eventall
        if 'Strikeout' in event or 'Strikeout - DP' in event:
            esc = 1
        elif 'Pop Out' in event or 'Groundout' in event or 'Grounded Into D' in event or 'Flyout' in event or 'Fielders Choice' in event or 'Bunt Pop Out' in event or 'Bunt Groundout' in event or 'Double Play' in event or 'Forceout' in event:
            esc = 2
        elif 'Sac Bunt' in event or 'Sac Fly' in event or 'Sacrifice Bunt ' in event or 'Lineout' in event or 'Sac Fly DP' in event or 'Field Error' in event:
            esc = 3
        elif 'Intent Walk' in event or 'Single' in event:
            esc = 4
        elif 'Hit By Pitch' in event or 'Double' in event or 'Triple' in event or 'Walk' in event:
            esc = 5
        elif 'Home Run' in event:
            esc = 6
        elif '0' in event:
            esc = 0
        else:
            esc = 0
    else:
        esc = np.zeros([len(eventall),1])
        #esc = esc + 3
        ind1 = np.concatenate((np.asarray(np.where(eventall =='Strikeout')[0]),np.asarray(np.where(eventall=='Strikeout - DP')[0])))
        esc[ind1] = 1
        ind2 = np.concatenate((np.asarray(np.where(eventall =='Pop Out')[0]),np.asarray(np.where(eventall=='Groundout')[0]),np.asarray(np.where(eventall=='Grounded Into D')[0]),np.asarray(np.where(eventall=='Flyout')[0]),np.asarray(np.where(eventall=='Fielders Choice')[0]),np.asarray(np.where(eventall=='Bunt Pop Out')[0]),np.asarray(np.where(eventall=='Bunt Groundout')[0]),np.asarray(np.where(eventall=='Double Play')[0]),np.asarray(np.where(eventall=='Forceout')[0])))
        esc[ind2] = 2
        ind3 = np.concatenate((np.asarray(np.where(eventall =='Sac Bunt')[0]),np.asarray(np.where(eventall=='Sac Fly')[0]),np.asarray(np.where(eventall=='Sacrifice Bunt ')[0]),np.asarray(np.where(eventall=='Lineout')[0]),np.asarray(np.where(eventall=='Sac Fly DP')[0]),np.asarray(np.where(eventall=='Field Error')[0])))
        esc[ind3] = 3
        ind4 = np.concatenate((np.asarray(np.where(eventall =='Intent Walk')[0]),np.asarray(np.where(eventall=='Single')[0])))
        esc[ind4] = 4
        ind5 = np.concatenate((np.asarray(np.where(eventall =='Hit By Pitch')[0]),np.asarray(np.where(eventall=='Double')[0]),np.asarray(np.where(eventall=='Triple')[0]),np.asarray(np.where(eventall=='Walk')[0])))
        esc[ind5] = 5
        ind6 = np.asarray(np.where(eventall =='Home Run')[0])
        esc[ind6] = 6
        ind0 = np.asarray(np.where(eventall =='0')[0])
        esc[ind0] = 0
    return esc
    
def desscore(desall):
    if type(desall) == str:
        des = desall
        if 'In play, no out' in des or 'Hit By Pitch' in des or 'In play, run(s)' in des or 'In play, out(s)' in des:
            dsc = 1
            
        elif 'Ball' in des or 'Automatic Ball'in des or 'Ball In Dirt' in des:
            dsc = 2
            
        elif 'Foul' in des or 'Foul (Runner Going)' in des or 'Foul Bunt' in des or 'Foul Pitchout' in des or 'Foul Tip' in des or 'Intent Ball' in des or 'Pitchout' in des:
            dsc = 3
            
        elif 'Called Strike' in des or 'Missed Bunt' in des or 'Swinging Pitchout' in des or 'Swinging Strike' in des or 'Swinging Strike (Blocked)' in des:
            dsc = 4

        elif '0' in des:
            dsc = 0
        else:
            dsc = 0
    else:
        dsc = np.zeros([len(desall),1])
        #dsc = dsc + 3
        ind1 = np.concatenate((np.asarray(np.where(desall == 'In play, no out')[0]),np.asarray(np.where(desall == 'Hit By Pitch')[0]),np.asarray(np.where(desall == 'In play, run(s)')[0]),np.asarray(np.where(desall == 'In play, out(s)')[0])))
        ind2 = np.concatenate((np.asarray(np.where(desall == 'Ball')[0]),np.asarray(np.where(desall == 'Automatic Ball')[0]),np.asarray(np.where(desall == 'Ball in Dirt')[0])))
        ind3 = np.concatenate((np.asarray(np.where(desall == 'Foul')[0]),np.asarray(np.where(desall == 'Foul (Runner Going)')[0]),np.asarray(np.where(desall == 'Foul Bunt')[0]),np.asarray(np.where(desall == 'Foul Pitchout')[0]),np.asarray(np.where(desall == 'Intent Ball')[0]),np.asarray(np.where(desall == 'Pitchout')[0]),np.asarray(np.where(desall == 'Foul Tip')[0])))
        ind4 = np.concatenate((np.asarray(np.where(desall == 'Called Strike')[0]),np.asarray(np.where(desall == 'Missed Bunt')[0]),np.asarray(np.where(desall == 'Swinging Pitchout')[0]),np.asarray(np.where(desall == 'Swinging Strike')[0]),np.asarray(np.where(desall == 'Swinging Strike (Blocked)')[0])))
        ind0 = np.asarray(np.where(desall == '0'))
        dsc[ind1] = 1
        dsc[ind2] = 2
        dsc[ind3] = 3
        dsc[ind4] = 4
        dsc[ind0] = 0
    return dsc

def destoballsstrikes(desall):
    #print 'deslength ' + str(len(desall))
    if type(desall) == str:
        des = desall
        if 'In play, no out' in des or 'In play, run(s)' in des or 'In play, out(s)' in des:
                bs = 'X'
        elif 'Ball' in des or 'Automatic Ball' in des or 'Ball In Dirt' in des or 'Hit By Pitch' in des or 'Intent Ball' in des or 'Pitchout' in des:
            bs = 'B'
        elif '0' in des:
            bs = '0'
        else:
            bs = 'S'
    else:
        bs = np.empty([len(desall),1],dtype=str)
        bs[:] = 'S'
        Xinds = np.concatenate((np.asarray(np.where(desall == 'In play, no out')[0]),np.asarray(np.where(desall == 'In play, run(s)')[0]),np.asarray(np.where(desall == 'In play, out(s)')[0])))
        Binds = np.concatenate((np.asarray(np.where(desall == 'Ball')[0]),np.asarray(np.where(desall == 'Automatic Ball')[0]),np.asarray(np.where(desall == 'Ball in Dirt')[0]),np.asarray(np.where(desall == 'Hit By Pitch')[0]),np.asarray(np.where(desall == 'Intent Ball')[0]),np.asarray(np.where(desall == 'Pitchout')[0])))
        Zinds = np.asarray(np.where(desall == '0'))
        bs[Binds] = 'B'
        bs[Xinds] = 'X'
        bs[Zinds] = '0'

    """else:
        bs = np.empty([len(desall),1],dtype=str)
        for i in range(0,len(desall)):
            des = desall[i]
            if 'In play, no out' in des or 'In play, run(s)' in des or 'In play, out(s)' in des:
                bs[i] = 'X'
            elif 'Ball' in des or 'Automatic Ball' in des or 'Ball In Dirt' in des or 'Hit By Pitch' in des or 'Intent Ball' in des or 'Pitchout' in des:
                bs[i] = 'B'
            elif '0' in des:
                bs[i] = '0'
            else:
                bs[i] = 'S'"""
    return bs
    
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

def timeofday(tp,gid):
    td = np.zeros([len(tp),1])
    for i in range(0,len(tp)):
        gtemp = str(gid[i])
        ht = int(gtemp[10:12])
        if ht == 2 or ht == 10:
            adj = 6
        elif ht == 6 or ht == 7 or ht == 12 or ht == 13 or ht == 16 or ht == 17 or ht == 26:
            adj = 5
        elif ht == 1 or ht == 14 or ht == 20 or ht == 23 or ht == 24 or ht == 25:
            adj = 7
        else:
            adj = 4
        newt = (tp[i] - adj*10000)/10000

        if newt > 9 and newt < 17:
            td[i] = 1
        elif newt >= 17 and newt < 20:
            td[i] = 2
        else:
            td[i] = 3
    return td

def strikesballs(typebs):
    zInds = [i for i,s in enumerate(typebs) if '0' in s]
    zInds.append(len(typebs))
    ballcount = [0]; strikecount = [0]
    cnt = 0
    #print zInds
    for i in range(1,len(typebs)):
        #try:
        if i == zInds[cnt+1]:
            cnt += 1
            ballcount.append(0)
            strikecount.append(0)
        else:
            st = zInds[cnt]
            temp = typebs[st:i+1]
            bctemp = len([k for k,s in enumerate(temp) if 'B' in s])
            if bctemp > 3:
                ballcount.append(3)
            else:
                ballcount.append(bctemp)
            sctemp = len([p for p,s in enumerate(temp) if 'S' in s])
            if sctemp > 2:
                strikecount.append(2)
            else:
                strikecount.append(sctemp)

    return (np.asarray(ballcount),np.asarray(strikecount))

def getplaceinorder(abn):
    ord = np.zeros([len(abn),1])
    for i in range(0,len(abn)):
        if abn[i] < 10:
            ord[i] = abn[i] % 10
        elif abn[i] % 9 == 0:
            ord[i] = 9
        else:
            ord[i] = abn[i] % 9
    return ord

def findInds(lst,thing):
    if isinstance(lst[0],str):
        inds = [i for i,s in enumerate(lst) if thing in s]
    else:
        inds = [i for i,s in enumerate([str(x) for x in lst]) if thing in s]
    return inds

def gamepreturn(pitches,strikes,gameinds,batinds,battot,bcount,scount):
    outmat = np.zeros([len(pitches),49])
    bmat = np.zeros([len(pitches),7])
    countmat = np.zeros([len(pitches),7])
    for i in range(1,len(pitches)):
        bspot = sorted(set(battot)).index(battot[i])
        cbinds = batinds[bspot]
        bmat[i,:] = getcount(pitches[np.intersect1d(range(0,i),cbinds)])
    
        btemp = int(bcount[i]); stemp = int(scount[i])
        ctinds = reduce(np.intersect1d,(range(0,i),np.where(bcount == btemp)[0],np.where(scount == stemp)[0]))
    
        countmat[i,:] = getcount(pitches[ctinds])

    for game in gameinds:
        for i in range(1,len(game)):
            if i < 5:
                temp1 = getcount(pitches[game[0:i]])
                try:
                    temp1s = getcount(pitches[np.intersect1d(game[0:i],strikes)])
                except Exception as e:
                    temp1s = np.zeros([1,7])
            else:
                temp1 = getcount(pitches[game[i-5:i]])
                try:
                    temp1s = getcount(pitches[np.intersect1d(game[i-5:i],strikes)])
                except Exception as e:
                    temp1s = np.zeros([1,7])
            if i < 10:
                temp2 = getcount(pitches[game[0:i]])
                try:
                    temp2s = getcount(pitches[np.intersect1d(game[0:i],strikes)])
                except Exception as e:
                    temp2s = np.zeros([1,7])
            else:
                temp2 = getcount(pitches[game[i-10:i]])
                try:
                    temp2s = getcount(pitches[np.intersect1d(game[i-10:i],strikes)])
                except Exception as e:
                    temp2s = np.zeros([1,7])
            if i < 20:
                temp3 = getcount(pitches[game[0:i]])
                try:
                    temp3s = getcount(pitches[np.intersect1d(game[0:i],strikes)])
                except Exception as e:
                    temp3s = np.zeros([1,7])
            else:
                temp3 = getcount(pitches[game[i-20:i]])
                try:
                    temp3s = getcount(pitches[np.intersect1d(game[i-20:i],strikes)])
                except Exception as e:
                    temp3s = np.zeros([1,7])

            ovr = getcount(pitches[0:game[i]])
            outmat[game[i],:] = np.column_stack((temp1,temp2,temp3,temp1s,temp2s,temp3s,ovr))
    return np.column_stack((outmat,countmat,bmat))

def getbatterstats(bID,allbats,bpt,pInd,typebs):#strikes,balls,inplay):
    #st = time.clock()
    outmat = np.zeros([1,22])
    bInds = np.where(allbats == bID)[0]
    #print 'find batter inds' + str(time.clock() - st)
    
    s1 = np.where(typebs[bInds] == 'S')[0]
    b1 = np.where(typebs[bInds] == 'B')[0]
    ip1 = np.where(typebs[bInds] == 'X')[0]

    try:
        #st = time.clock()
        temp1 = getcount(bpt[ip1])#(bpt[np.intersect1d(inds,inplay)])
        #print 'in play count time' + str(time.clock() - st)
    except TypeError:
        temp1 = np.zeros([1,7])
    try:
        #st = time.clock()
        temp2 = getcount(bpt[s1])#(bpt[np.intersect1d(inds,strikes)])
        #print 'strike count time' + str(time.clock() - st)
    except TypeError:
        temp2 = np.zeros([1,7])
    try:
        #st = time.clock()
        temp3 = getcount(bpt[b1])#(bpt[np.intersect1d(inds,balls)])
        #print 'ball count time time' + str(time.clock() - st)
    except TypeError:
        temp3 = np.zeros([1,7])
    outmat[:,0:7] = temp1 #= np.column_stack((temp1,temp2,temp3))
    outmat[:,7:14] = temp2
    outmat[:,14:21] = temp3
    outmat[:,21] = bID

    return outmat

def getyrcount(gidgood):
    yrcount = np.zeros([7,1])
    for i in range(0,len(gidgood)):
        if gidgood[i] < 201100000000 and gidgood[i] > 201000000000:
            yrcount[0] += 1
        elif gidgood[i] < 201200000000 and gidgood[i] > 201100000000:
            yrcount[1] += 1
        elif gidgood[i] < 201300000000 and gidgood[i] > 201200000000:
            yrcount[2] += 1
        elif gidgood[i] < 201400000000 and gidgood[i] > 201300000000:
            yrcount[3] += 1
        elif gidgood[i] < 201500000000 and gidgood[i] > 201400000000:
            yrcount[4] += 1
        elif gidgood[i] < 201600000000 and gidgood[i] > 201500000000:
            yrcount[5] += 1
        elif gidgood[i] < 201700000000 and gidgood[i] > 201600000000:
            yrcount[6] += 1
    return yrcount

def loadindata():
    print 'Loading...'

    start = time.clock()
    with open('PitDataUpdate/MLBAllUpdate.pkl','rb') as input:
        Data = pickle.load(input)
    print time.clock() - start

    print 'Loaded'

    print len(Data.Inning)

    #pInds = findInds(Data.pitcher,pID)

    #print len(pInds)

    return (Data)


def makepitcherdata(Data):

    inds2014plus = np.where(Data.gameID > 201400000000)[0]
    
    inds2016 = np.where(Data.gameID > 201606000000)[0]
    
    pitcherVec = np.asarray(list(set(Data.pitcher[inds2016])))

    print len(pitcherVec)

    #print [np.max(pNums), np.min(pNums), np.mean(pNums)]

    #YearCounts = np.loadtxt('YearCounts.txt').T
    YearCounts = np.zeros([19,len(pitcherVec)])
    
    mainstart = time.clock()
    
    for k in range(0,len(pitcherVec)):
    
        p = pitcherVec[k]
        print p
    
        start = time.clock()
        
        pInds = inds2014plus[np.where(Data.pitcher[inds2014plus] == p)[0]]
        
        print 'Original length ' + str(len(pInds))

        Inningp = Data.Inning[pInds]; abnp = Data.at_bat_num[pInds]; spreadp = Data.spread[pInds]; outsp = Data.outs[pInds]; batterp = Data.batter[pInds]; stancep = fixstand(Data.stance[pInds]); bheightp = Data.bheight[pInds]; eventp = eventscore(Data.pr_event[pInds]); res_eventp = eventscore(Data.res_event[pInds]); desp = desscore(Data.pr_des[pInds]); res_desp = desscore(Data.res_des[pInds]); pnump = Data.pnum[pInds]; typebsp = Data.typebs[pInds]; res_typebsp = Data.res_typebs[pInds]; timep = timeofday(Data.tfs[pInds],Data.gameID[pInds]); breakyp = Data.breaky[pInds]; breakanglep = Data.breakangle[pInds]; breaklengthp = Data.breaklength[pInds]; on1p = Data.on1[pInds]; on2p = Data.on2[pInds]; on3p = Data.on3[pInds]; nastyp = Data.nasty[pInds]; outpitchp = pitchscore(Data.outpitch[pInds]); outcp = Data.outc[pInds]; outspdp = np.ceil(1000*(.5*np.add(Data.outstspd[pInds],Data.outenspd[pInds])))/1000; gidp = Data.gameID[pInds]; cur_zonep = Data.cur_zones[pInds]; ordernum = getplaceinorder(Data.at_bat_num[pInds])
        bscorep = on1p + 2*on2p + 3*on3p
        (ballcountp,strikecountp) = strikesballs(typebsp)

        zInds = np.where(typebsp == '0')[0]

        zt = np.asarray([0,0])
        prpitch = np.insert(outpitchp[0:len(outpitchp)-1],0,0)
        prz = np.insert(cur_zonep[0:len(outpitchp)-1],0,0)
        prspd = np.insert(outspdp[0:len(outpitchp)-1],0,0)
        prbky = np.insert(breakyp[0:len(outpitchp)-1],0,0)
        prbka = np.insert(breakanglep[0:len(outpitchp)-1],0,0)
        prbkl = np.insert(breaklengthp[0:len(outpitchp)-1],0,0)
        prnsty = np.insert(nastyp[0:len(outpitchp)-1],0,0)

        prpitch[zInds] = 0
        prz[zInds] = 0
        prspd[zInds] = 0
        prbky[zInds] = 0
        prbka[zInds] = 0
        prbkl[zInds] = 0
        prnsty[zInds] = 0

        goodinds = np.intersect1d(np.where(outcp > .8)[0],np.where(outpitchp > -1)[0])
        ovrallinds = pInds[goodinds]
        
        print 'New length ' + str(len(goodinds))

        Inninggood = Inningp[goodinds]; abngood = abnp[goodinds]; spreadgood = spreadp[goodinds]; outsgood = outsp[goodinds]; battergood = batterp[goodinds]; stancegood = stancep[goodinds]; bheightgood = bheightp[goodinds]; eventgood =  eventp[goodinds]; res_eventgood =  res_eventp[goodinds]; desgood = desp[goodinds]; res_desgood = res_desp[goodinds]; pnumgood = pnump[goodinds]; typebsgood = typebsp[goodinds]; res_typebsgood = res_typebsp[goodinds]; timegood = timep[goodinds]; breakygood = breakyp[goodinds]; breakanglegood = breakanglep[goodinds]; breaklengthgood = breaklengthp[goodinds]; on1good = on1p[goodinds]; on2good = on2p[goodinds]; on3good = on3p[goodinds]; nastygood = nastyp[goodinds]; outpitchgood = outpitchp[goodinds]; out_type_confgood = outcp[goodinds]; outspdgood = outspdp[goodinds]; gidgood = gidp[goodinds]; cur_zonegood = cur_zonep[goodinds]; ordernumgood = ordernum[goodinds]; bscoregood = bscorep[goodinds]; bcountgood = ballcountp[goodinds]; scountgood = strikecountp[goodinds]; prpitchgood = prpitch[goodinds]; przgood = prz[goodinds]; prspdgood = prspd[goodinds]; prbkygood = prbky[goodinds]; prbkagood = prbka[goodinds]; prbklgood = prbkl[goodinds]; prnstygood = prnsty[goodinds]

        gameindexes = [];
        for i,game in enumerate(sorted(set(gidgood))):
            gameindexes.append(findInds(gidgood,str(game)))
        batterindexes = [];
        for i,bat in enumerate(sorted(set(battergood))):
            batterindexes.append(findInds(battergood,str(bat)))

        yrcount = getyrcount(gidgood)
        
        s1 = np.asarray(np.where(Data.res_typebs == 'S')[0])
        b1 = np.asarray(np.where(Data.res_typebs == 'B')[0])
        ip1 = np.asarray(np.where(Data.res_typebs == 'X')[0])
        
        pitches = pitchscore(Data.outpitch)

        print 'making batter data'
        batmat = np.zeros([len(outpitchgood),22])
        #start = time.clock()
        for i in range(0,len(outpitchgood)):
            #print i
            st = time.clock()
            batmat[i,:] = getbatterstats(battergood[i],Data.batter[0:ovrallinds[i]],pitches[0:ovrallinds[i]],ovrallinds[i],Data.res_typebs[0:ovrallinds[i]])#s1[short],b1[short],ip1[short])
            if i == yrcount[0]:
                print 'year 1 done'
            elif i == np.sum(yrcount[0:2]):
                print 'year 2 done'
            elif i == np.sum(yrcount[0:3]):
                print 'year 3 done'
            elif i == np.sum(yrcount[0:4]):
                print 'year 4 done'
            elif i == np.sum(yrcount[0:5]):
                print 'year 5 done'
            elif i == np.sum(yrcount[0:6]):
                print 'year 6 done'
            elif i == np.sum(yrcount-1):
                print 'done with batter'
        #print 'Batter Made in ' + str(time.clock() - start)

        strikes = np.asarray([i for i,s in enumerate(res_typebsgood) if 'S' in s])
        balls = np.asarray([i for i,s in enumerate(res_typebsgood) if 'B' in s])
        inplay = np.asarray([i for i,s in enumerate(res_typebsgood) if 'X' in s])

        pDataMatrix = np.column_stack((np.column_stack((np.asarray(gidgood),np.asarray(Inninggood), np.asarray(outsgood), np.asarray(ordernumgood), np.asarray(abngood), np.asarray(spreadgood), np.asarray(timegood), np.asarray(stancegood), np.asarray(bheightgood), np.asarray(bcountgood), np.asarray(scountgood), np.asarray(on1good), np.asarray(on2good), np.asarray(on3good), np.asarray(bscoregood), np.asarray(pnumgood), np.asarray(eventgood), np.asarray(desgood), np.asarray(prpitchgood), np.asarray(przgood), np.asarray(prspdgood), np.asarray(prnstygood), np.asarray(prbkygood), np.asarray(prbkagood), np.asarray(prbklgood))),gamepreturn(outpitchgood,strikes,gameindexes,batterindexes,battergood,bcountgood,scountgood),batmat))

        pOutMatrix = np.column_stack((np.asarray(outpitchgood), np.asarray(outspdgood), np.asarray(cur_zonegood), np.asarray(res_desgood)))

        print [np.shape(pDataMatrix), np.shape(pOutMatrix)]
        
        YearCounts[0:7,k] = yrcount[:,0]
        YearCounts[7,k] = np.sum(yrcount)
        YearCounts[8:15,k] = getcount(outpitchgood).T[:,0]
        YearCounts[15,k] = len(balls)
        YearCounts[16,k] = len(strikes)
        YearCounts[17,k] = len(inplay)
        YearCounts[18,k] = p
        
        print YearCounts[:,k].T
        
        str1 = '%i ' * 20 + '%2.2f ' + '%i ' + '%2.1f ' * 3 + '%5.6f ' * 83 + '%5.6f ' + '%i'

        str2 = '%i ' * 8 + '%5.6f ' * 7 + '%i %i %i %i'

        np.savetxt('PitDataUpdate/' + str(p) + 'Data2014pwCut.txt',pDataMatrix,str1)
        np.savetxt('PitDataUpdate/' + str(p) + 'Outputs2014pwCut.txt',pOutMatrix,'%i %2.2f %i %i')
        np.savetxt('PitDataUpdate/YearCountStuffwCut.txt',YearCounts.T,str2)

        print str(k) + ' Saved!'

        print time.clock() - start

    print 'Done in: ' + str(time.clock() - mainstart)

#makepitcherdata(loadindata())
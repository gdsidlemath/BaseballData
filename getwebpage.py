from __future__ import division
from lxml import etree
from lxml import html
from bs4 import BeautifulSoup
from scipy import stats
import numpy as np
import requests
import re
import datetime
import cPickle as pickle
from definedataclass import GamePitchData
import time
import sys
import traceback

def save_object(obj, filename):
    with open(filename, 'wb') as output:
        pickle.dump(obj, output, -1)

def build_zone(sztop,szbot,px,py,stand): #Find what zone each pitch was thrown in
    
    maxh = np.max(py); minh = np.min(py)
    
    maxw = np.max(px); minw = np.min(px)
    
    szright = 17/2; szleft = -17/2
    
    bboxright = 29/2; bboxleft = -29/2
    
    szwsplit = (1/3)*(17)
    
    zone = []
    
    for i in range(0,len(px)):
        
        sztopt = sztop[i]
        szbott = szbot[i]
        
        pxt = px[i]
        pyt = py[i]
        
        """print stand[i]
        print [sztopt,szbott,szright,szleft]
        print [pxt,pyt]"""
        
        szhdiff = sztopt - szbott
        szhmid = (1/2)*szhdiff + szbott
        szhsplit = (1/3)*szhdiff
        
        if 'L' in stand[i]:
            if(pxt >= szleft and pxt < szleft + szwsplit and pyt <= sztopt and pyt >= sztopt - szhsplit):
                zone.append(1)
            elif(pxt >= szleft + szwsplit and pxt < szleft + 2*szwsplit and pyt <= sztopt and pyt >= sztopt - szhsplit):
                zone.append(2)
            elif(pxt >= szleft + 2*szwsplit and pxt <= szright and pyt <= sztopt and pyt >= sztopt - szhsplit):
                zone.append(3)
            elif(pxt >= szleft and pxt < szleft + szwsplit and pyt < sztopt - szhsplit and pyt >= sztopt - 2*szhsplit):
                zone.append(4)
            elif(pxt >= szleft + szwsplit and pxt < szleft + 2*szwsplit and pyt < sztopt - szhsplit and pyt >= sztopt - 2*szhsplit):
                zone.append(5)
            elif(pxt >= szleft + 2*szwsplit and pxt <= szright and pyt < sztopt - szhsplit and pyt >= sztopt - 2*szhsplit):
                zone.append(6)
            elif(pxt >= szleft and pxt < szleft + szwsplit and pyt <= sztopt - 2*szhsplit and pyt >= szbott):
                zone.append(7)
            elif(pxt >= szleft + szwsplit and pxt < szleft + 2*szwsplit and pyt <= sztopt - 2*szhsplit and pyt >= szbott):
                zone.append(8)
            elif(pxt >= szleft + 2*szwsplit and pxt <= szright and pyt <= sztopt - 2*szhsplit and pyt >= szbott):
                zone.append(9)
            elif(pxt >= bboxleft and pxt < 0 and pyt <= maxh and pyt > szhmid ):
                zone.append(10)
            elif(pxt >= 0 and pxt <= bboxright and pyt <= maxh and pyt > szhmid ):
                zone.append(11)
            elif(pxt >= bboxleft and pxt < 0 and pyt <= szhmid and pyt > 0 ):
                zone.append(12)
            elif(pxt >= 0 and pxt <= bboxright and pyt <= szhmid and pyt > 0 ):
                zone.append(13)
            elif(pxt >= minw and pxt < bboxleft and pyt <= maxh and pyt > szhmid):
                zone.append(14)
            elif(pxt > bboxright and pxt <= maxw and pyt <= maxh and pyt > szhmid):
                zone.append(15)
            elif(pxt >= minw and pxt < bboxleft and pyt <= szhmid and pyt > 0):
                zone.append(16)
            elif(pxt > bboxright and pxt <= maxw and pyt <= szhmid and pyt > 0):
                zone.append(17)
            elif(py <0):
                zone.append(18)
            else:
                zone.append(0)
    
        else:
            
            if(pxt >= szleft and pxt < szleft + szwsplit and pyt <= sztopt and pyt >= sztopt - szhsplit):
                zone.append(3)
            elif(pxt >= szleft + szwsplit and pxt < szleft + 2*szwsplit and pyt <= sztopt and pyt >= sztopt - szhsplit):
                zone.append(2)
            elif(pxt >= szleft + 2*szwsplit and pxt <= szright and pyt <= sztopt and pyt >= sztopt - szhsplit):
                zone.append(1)
            elif(pxt >= szleft and pxt < szleft + szwsplit and pyt < sztopt - szhsplit and pyt >= sztopt - 2*szhsplit):
                zone.append(6)
            elif(pxt >= szleft + szwsplit and pxt < szleft + 2*szwsplit and pyt < sztopt - szhsplit and pyt >= sztopt - 2*szhsplit):
                zone.append(5)
            elif(pxt >= szleft + 2*szwsplit and pxt <= szright and pyt < sztopt - szhsplit and pyt >= sztopt - 2*szhsplit):
                zone.append(4)
            elif(pxt >= szleft and pxt < szleft + szwsplit and pyt <= sztopt - 2*szhsplit and pyt >= szbott):
                zone.append(9)
            elif(pxt >= szleft + szwsplit and pxt < szleft + 2*szwsplit and pyt <= sztopt - 2*szhsplit and pyt >= szbott):
                zone.append(8)
            elif(pxt >= szleft + 2*szwsplit and pxt <= szright and pyt <= sztopt - 2*szhsplit and pyt >= szbott):
                zone.append(7)
            elif(pxt >= bboxleft and pxt < 0 and pyt <= maxh and pyt > szhmid ):
                zone.append(11)
            elif(pxt >= 0 and pxt <= bboxright and pyt <= maxh and pyt > szhmid ):
                zone.append(10)
            elif(pxt >= bboxleft and pxt < 0 and pyt <= szhmid and pyt > 0 ):
                zone.append(13)
            elif(pxt >= 0 and pxt <= bboxright and pyt <= szhmid and pyt > 0 ):
                zone.append(12)
            elif(pxt >= minw and pxt < bboxleft and pyt <= maxh and pyt > szhmid):
                zone.append(15)
            elif(pxt > bboxright and pxt <= maxw and pyt <= maxh and pyt > szhmid):
                zone.append(14)
            elif(pxt >= minw and pxt < bboxleft and pyt <= szhmid and pyt > 0):
                zone.append(17)
            elif(pxt > bboxright and pxt <= maxw and pyt <= szhmid and pyt > 0):
                zone.append(16)
            elif(py < 0):
                zone.append(18)
            else:
                zone.append(0)

#print zone[i]
    
    return zone

def getgameID(gid):
    teams = ['ana','nya','bal','cle','chn','was','det','cha','hou','tor','mia','col','mil','min','nyn','ari','oak','bos','pit','atl','sdn','cin','sfn','phi','sln','lan','tba','sea','tex','kca']
    teams.sort()
    myd = gid[4:8] + gid[9:11] + gid[12:14]
    ateam = gid[15:18]; hteam = gid[22:25]
    if 'flo' in ateam:
        ateam = 'mia'
    if 'flo' in hteam:
        hteam = 'mia'
    aspot = str([i for i,s in enumerate(teams) if ateam in s][0]+1)
    hspot = str([i for i,s in enumerate(teams) if hteam in s][0]+1)
    if len(aspot) < 2:
        aspot = '0' + aspot
    if len(hspot) < 2:
        hspot = '0' + hspot

    totstr = myd + aspot + hspot

    return int(totstr)

"""class GamePitchData(object):

    def __init__(self,gameID,Inning,at_bat_num,home_runs,away_runs,outs,batter,bheight,stance,
                 pitcher,pthrows,event,des,pnum,typebs,tfs,stspd,endspd,sztop,szbot,breaky,breakangle,
                 breaklength,on1,on2,on3,pr_pitch_type,pr_type_conf,nasty,outpitch,outc,outx,outy,outstspd,outenspd,
                 pr_zones,cur_zones):
        
        self.Inning = Inning; self.at_bat_num = at_bat_num; self.home_runs = home_runs; self.away_runs = away_runs
        self.outs = outs; self.batter = batter; self.bheight = bheight #self.balls = balls; self.strikes = strikes
        self.stance = stance; self.pitcher = pitcher; self.pthrows = pthrows; self.event = event; self.des = des
        self.typebs = typebs; self.tfs = tfs; self.stspd = stspd; self.endspd = endspd; self.sztop = sztop
        self.szbot = szbot; self.breaky = breaky; self.breakangle = breakangle; self.breaklength = breaklength; self.on1 = on1
        self.on2 = on2; self.on3 = on3; self.pr_pitch_type = pr_pitch_type; self.pr_type_conf = pr_type_conf; self.nasty = nasty
        self.outpitch = outpitch; self.outc = outc; self.pnum = pnum; self.outx = outx; self.outy = outy; self.outstspd = outstspd
        self.outenspd = outenspd; self.pr_zones = pr_zones; self.cur_zones = cur_zones; self.gameID = gameID"""

def mergeGameData(one,two):

    return GamePitchData(np.asarray(list(one.gameID) + list(two.gameID)),np.asarray(list(one.Inning) + list(two.Inning)),np.asarray(list(one.at_bat_num) + list(two.at_bat_num)),np.asarray(list(one.spread) + list(two.spread)),np.asarray(list(one.outs) + list(two.outs)),np.asarray(list(one.batter) + list(two.batter)),np.asarray(list(one.bheight) + list(two.bheight)),np.asarray(list(one.stance) + list(two.stance)),np.asarray(list(one.pitcher) + list(two.pitcher)),np.asarray(list(one.pthrows) + list(two.pthrows)),np.asarray(list(one.pr_event) + list(two.pr_event)),np.asarray(list(one.res_event) + list(two.res_event)),np.asarray(list(one.pr_des) + list(two.pr_des)),np.asarray(list(one.res_des) + list(two.res_des)),np.asarray(list(one.pnum) + list(two.pnum)),np.asarray(list(one.typebs) + list(two.typebs)),np.asarray(list(one.res_typebs) + list(two.res_typebs)),np.asarray(list(one.tfs) + list(two.tfs)),np.asarray(list(one.sztop) + list(two.sztop)),np.asarray(list(one.szbot) + list(two.szbot)),np.asarray(list(one.breaky) + list(two.breaky)),np.asarray(list(one.breakangle) + list(two.breakangle)),np.asarray(list(one.breaklength) + list(two.breaklength)),np.asarray(list(one.on1) + list(two.on1)),np.asarray(list(one.on2) + list(two.on2)),np.asarray(list(one.on3) + list(two.on3)),np.asarray(list(one.nasty) + list(two.nasty)),np.asarray(list(one.outpitch) + list(two.outpitch)),np.asarray(list(one.outc) + list(two.outc)),np.asarray(list(one.outx) + list(two.outx)),np.asarray(list(one.outy) + list(two.outy)),np.asarray(list(one.outstspd) + list(two.outstspd)),np.asarray(list(one.outenspd) + list(two.outenspd)),np.asarray(list(one.cur_zones) + list(two.cur_zones)))

def getgamedata(url,gameID):
    
    page = requests.get(url)
    soup = BeautifulSoup(page.content,'lxml')
    table1 = soup.game.find_all('inning')
    
    Inning = []; at_bat_num = []; spread = [];
    outs = []; batter = []; stance = []; bheight = []; pitcher = []; pthrows = []
    event = []; des = []; pnum = []; typebs = []; res_typebs = []; tfs = []; stspd = []; endspd = []
    sztop = []; szbot = []; breaky = []; breakangle = []; breaklength = []; on1 = []; on2 = []; on3 = []
    pr_pitch_type = []; pr_type_conf = []; nasty = []; outpitch = []; out_type_conf = []
    outx = []; outy = []; outstspd = []; outenspd = []; gid = []; res_event = []; res_des = [];
    #balls = []; strikes = [];

    hABct = 0
    aABct = 0
    hpct = 0
    apct = 0
    
    ovrfuckups = 0
    
    for Iind,inning in enumerate(table1):
        instr = str(inning)
        st1 = instr.index('num="') + len('num="'); ed1 = instr.index('"',st1)
        num = instr[st1:ed1]
        top = inning.find_all('top')
        bot = inning.find_all('bottom')
        holddes = '0'
        for t in top:
            table2 = t.find_all('atbat')
            for ind1,AB in enumerate(table2):
                if ind1 > 0:
                    prABstr = str(table2[ind1-1])
                else:
                    prABstr = 'event="0" o="0" '
                    if Iind == 0:
                        prABstr = prABstr + 'home_team_runs="0" away_team_runs="0"'
                    else:
                        prABstr = prABstr + 'home_team_runs="' + holdhscore +'" ' + 'away_team_runs="' + holdascore + '"'
                #print prABstr
                ABstr = str(AB)
                hABct += 1
                
                # Stuff that stays constant through the at-bat
                stbat = ABstr.index('batter="') + len('batter="'); endbat = ABstr.index('"',stbat)
                battertemp = ABstr[stbat:endbat]
                stbh = ABstr.index('b_height="') + len('b_height="'); endbh = ABstr.index('"',stbh)
                bhtemp = ABstr[stbh:endbh]
                stpit = ABstr.index('pitcher="') + len('pitcher="'); endpit = ABstr.index('"',stpit)
                pitchertemp = ABstr[stpit:endpit]
                stpth = ABstr.index('p_throws="') + len('p_throws="'); endpth = ABstr.index('"',stpth)
                pthtemp = ABstr[stpth:endpth]
                ststd = ABstr.index('stand="') + len('stand="'); endstd = ABstr.index('"',ststd)
                standtemp = ABstr[ststd:endstd]
                evst1 = ABstr.index('event="') + len('event="'); evend1 = ABstr.index('"',evst1)
                tempev1 = ABstr[evst1:evend1]
                
                # Stuff from the previous at-bat
                try:
                    sthsc = prABstr.index('home_team_runs="') + len('home_team_runs="'); endhsc = prABstr.index('"',sthsc)
                    temphsc = prABstr[sthsc:endhsc]
                    stasc = prABstr.index('away_team_runs="') + len('away_team_runs="'); endasc = prABstr.index('"',stasc)
                    tempasc = prABstr[stasc:endasc]
                except ValueError:
                    temphsc = '0'; tempasc = '0';
                evst = prABstr.index('event="') + len('event="'); evend = prABstr.index('"',evst)
                tempev = prABstr[evst:evend]
                outst = prABstr.index('o="') + len('o="'); outend = prABstr.index('"',outst)
                tempout = prABstr[outst:outend]
                
                table3 = AB.find_all('pitch')
                for ind,pit in enumerate(table3):
                    pitstr = str(pit)
                    hpct += 1
                    if ind > 0:
                        prPitstr = str(table3[ind-1])
                    else:
                        prPitstr = ' type="0" px="0" pz="0" start_speed="0" end_speed="0" break_y="0" break_angle="0" break_length="0" pitch_type="0" type_confidence="1" nasty="0" sz_top="0" sz_bot="0" des="' + holddes + '"'
                    # Stuff from the current pitch
                    try:
                        if 'tfs=""' in pitstr:
                            if len(str(Iind)) < 2:
                                t1 = '0' + str(Iind)
                            else:
                                t1 = str(Iind)
                            if len(str(hABct)) < 2:
                                t2 = '0' + str(hABct)
                            else:
                                t2 = str(hABct)
                            if len(str(hpct)) < 2:
                                t3 = '0' + str(hpct)
                            else:
                                t3 = str(hpct)
                            tfstemp = t1 + t2 + t3
                        else:
                            tfsst = pitstr.index('tfs="') + len('tfs="'); tfsend = pitstr.index('"',tfsst)
                            tfstemp = pitstr[tfsst:tfsend]
                        
                        try:
                            pitstr.index('on_1b')
                            on1temp = 1
                        except ValueError:
                            on1temp = 0
                        try:
                            pitstr.index('on_2b')
                            on2temp = 1
                        except ValueError:
                            on2temp = 0
                        try:
                            pitstr.index('on_3b')
                            on3temp = 1
                        except ValueError:
                            on3temp = 0
                        if 'pitch_type' in pitstr:
                            stopt = pitstr.index('pitch_type="') + len('pitch_type="'); endopt = pitstr.index('"',stopt)
                            outptemp = pitstr[stopt:endopt]
                            stoptc = pitstr.index('type_confidence="') + len('type_confidence="'); endoptc = pitstr.index('"',stoptc)
                            outpcontemp = pitstr[stoptc:endoptc]
                            stxp = pitstr.index('px="') + len('px="'); endxp = pitstr.index('"',stxp)
                            tempxcp = pitstr[stxp:endxp]
                            styp = pitstr.index('pz="') + len('pz="'); endyp = pitstr.index('"',styp)
                            tempycp = pitstr[styp:endyp]
                            ststspp = pitstr.index('start_speed="') + len('start_speed="'); endstspp = pitstr.index('"',ststspp)
                            tempstspdcp = pitstr[ststspp:endstspp]
                            stenspp = pitstr.index('end_speed="') + len('end_speed="'); endenspp = pitstr.index('"',stenspp)
                            tempenspdcp = pitstr[stenspp:endenspp]
                            stbkyt = pitstr.index('break_y="') + len('break_y="'); endbkyt = pitstr.index('"',stbkyt)
                            tempbky = pitstr[stbkyt:endbkyt]
                            stbkat = pitstr.index('break_angle="') + len('break_angle="'); endbkat = pitstr.index('"',stbkat)
                            tempbka = pitstr[stbkat:endbkat]
                            stbklt = pitstr.index('break_length="') + len('break_length="'); endbklt = pitstr.index('"',stbklt)
                            tempbkl = pitstr[stbklt:endbklt]
                            stnsty = pitstr.index('nasty="') + len('nasty="'); endnsty = pitstr.index('"',stnsty)
                            nstytemp = pitstr[stnsty:endnsty]
                            stsztopt = pitstr.index('sz_top="') + len('sz_top="'); endsztopt = pitstr.index('"',stsztopt)
                            tempsztop = pitstr[stsztopt:endsztopt]
                            stszbott = pitstr.index('sz_bot="') + len('sz_bot="'); endszbott = pitstr.index('"',stszbott)
                            tempszbot = pitstr[stszbott:endszbott]
                        else:
                            outptemp = 'XX'
                            outpcontemp = '1'
                            tempxcp = '0'; tempycp = '0'; tempstspdcp = '0'; tempenspdcp = '0'; tempbky = '0'; tempbka = '0'; tempbkl = '0'; nstytemp = '0'; tempsztop = '0'; tempszbot = '0'
                        stdes1 = pitstr.index('des="') + len('des="'); enddes1 = pitstr.index('"',stdes1)
                        tempdes1 = pitstr[stdes1:enddes1]
                        sttype1 = pitstr.index(' type="') + len(' type="'); endtype1 = pitstr.index('"',sttype1)
                        temptype1 = pitstr[sttype1:endtype1]

                        
                        # Stuff from the previous pitch
                        stdes = prPitstr.index('des="') + len('des="'); enddes = prPitstr.index('"',stdes)
                        tempdes = prPitstr[stdes:enddes]
                        sttype = prPitstr.index(' type="') + len(' type="'); endtype = prPitstr.index('"',sttype)
                        temptype = prPitstr[sttype:endtype]
                        
                        if ind == (len(table3) - 1):
                            sthdes = pitstr.index('des="') + len('des="'); endhdes = pitstr.index('"',sthdes)
                            holddesc = pitstr[sthdes:endhdes]
                        
                        Inning.append(int(num))
                        at_bat_num.append(int(hABct))
                        spread.append(int(temphsc) - int(tempasc))
                        outs.append(int(tempout))
                        batter.append(int(battertemp))
                        bheight.append(12*int(bhtemp[0]) + int(bhtemp[2:len(bhtemp)]))
                        stance.append(standtemp)
                        pitcher.append(int(pitchertemp))
                        pthrows.append(pthtemp)
                        event.append(tempev)
                        des.append(tempdes)
                        pnum.append(int(hpct))
                        typebs.append(temptype)
                        tfs.append(int(tfstemp))
                        sztop.append(12*float(tempsztop))
                        szbot.append(12*float(tempszbot))
                        breaky.append(float(tempbky))
                        breakangle.append(float(tempbka))
                        breaklength.append(float(tempbkl))
                        on1.append(on1temp)
                        on2.append(on2temp)
                        on3.append(on3temp)
                        nasty.append(float(nstytemp))
                        outpitch.append(outptemp)
                        out_type_conf.append(float(outpcontemp))
                        outx.append(12*float(tempxcp))
                        outy.append(12*float(tempycp))
                        outstspd.append(float(tempstspdcp))
                        outenspd.append(float(tempenspdcp))
                        gid.append(gameID)
                        res_event.append(tempev1)
                        res_des.append(tempdes1)
                        res_typebs.append(temptype1)
                    except Exception as e:
                        print pitstr
                        print traceback.print_exc()
                        print [ind, ind1, Iind]
                        continue
                
                if ind1 == (len(table2) - 1):
                    try:
                        sthsc = ABstr.index('home_team_runs="') + len('home_team_runs="'); endhsc = ABstr.index('"',sthsc)
                        holdhscore = ABstr[sthsc:endhsc]
                        stasc = ABstr.index('away_team_runs="') + len('away_team_runs="'); endasc = ABstr.index('"',stasc)
                        holdascore = ABstr[stasc:endasc]
                    except ValueError:
                        holdhscore = '0'; holdascore = '0'
        for b in bot:
            table2 = b.find_all('atbat')
            for ind1,AB in enumerate(table2):
                if ind1 > 0:
                    prABstr = str(table2[ind1-1])
                else:
                    prABstr = 'event="0" o="0" ' + 'home_team_runs="' + holdhscore +'" ' + 'away_team_runs="' + holdascore + '"'
                ABstr = str(AB)
                aABct += 1
                
                # Stuff that stays constant through the at-bat
                stbat = ABstr.index('batter="') + len('batter="'); endbat = ABstr.index('"',stbat)
                battertemp = ABstr[stbat:endbat]
                stbh = ABstr.index('b_height="') + len('b_height="'); endbh = ABstr.index('"',stbh)
                bhtemp = ABstr[stbh:endbh]
                stpit = ABstr.index('pitcher="') + len('pitcher="'); endpit = ABstr.index('"',stpit)
                pitchertemp = ABstr[stpit:endpit]
                stpth = ABstr.index('p_throws="') + len('p_throws="'); endpth = ABstr.index('"',stpth)
                pthtemp = ABstr[stpth:endpth]
                ststd = ABstr.index('stand="') + len('stand="'); endstd = ABstr.index('"',ststd)
                standtemp = ABstr[ststd:endstd]
                evst1 = ABstr.index('event="') + len('event="'); evend1 = ABstr.index('"',evst1)
                tempev1 = ABstr[evst1:evend1]
                
                # Stuff from the previous at-bat
                try:
                    sthsc = prABstr.index('home_team_runs="') + len('home_team_runs="'); endhsc = prABstr.index('"',sthsc)
                    temphsc = prABstr[sthsc:endhsc]
                    stasc = prABstr.index('away_team_runs="') + len('away_team_runs="'); endasc = prABstr.index('"',stasc)
                    tempasc = prABstr[stasc:endasc]
                except ValueError:
                    temphsc = '0'; tempasc = '0';
                evst = prABstr.index('event="') + len('event="'); evend = prABstr.index('"',evst)
                tempev = prABstr[evst:evend]
                outst = prABstr.index('o="') + len('o="'); outend = prABstr.index('"',outst)
                tempout = prABstr[outst:outend]
                
                table3 = AB.find_all('pitch')
                for ind,pit in enumerate(table3):
                    pitstr = str(pit)
                    apct += 1
                    if ind > 0:
                        prPitstr = str(table3[ind-1])
                    else:
                        prPitstr = ' type="0" px="0" pz="0" start_speed="0" end_speed="0" break_y="0" break_angle="0" break_length="0" pitch_type="0" type_confidence="1" nasty="0" sz_top="0" sz_bot="0" des="' + holddes + '"'
                    # Stuff from the current pitch
                    try:
                        if 'tfs=""' in pitstr:
                            if len(str(Iind)) < 2:
                                t1 = '0' + str(Iind)
                            else:
                                t1 = str(Iind)
                            if len(str(hABct)) < 2:
                                t2 = '0' + str(hABct)
                            else:
                                t2 = str(hABct)
                            if len(str(hpct)) < 2:
                                t3 = '0' + str(hpct)
                            else:
                                t3 = str(hpct)
                            tfstemp = t1 + t2 + t3
                        else:
                            tfsst = pitstr.index('tfs="') + len('tfs="'); tfsend = pitstr.index('"',tfsst)
                            tfstemp = pitstr[tfsst:tfsend]

                        try:
                            pitstr.index('on_1b')
                            on1temp = 1
                        except ValueError:
                            on1temp = 0
                        try:
                            pitstr.index('on_2b')
                            on2temp = 1
                        except ValueError:
                            on2temp = 0
                        try:
                            pitstr.index('on_3b')
                            on3temp = 1
                        except ValueError:
                            on3temp = 0
                        if 'pitch_type' in pitstr:
                            stopt = pitstr.index('pitch_type="') + len('pitch_type="'); endopt = pitstr.index('"',stopt)
                            outptemp = pitstr[stopt:endopt]
                            stoptc = pitstr.index('type_confidence="') + len('type_confidence="'); endoptc = pitstr.index('"',stoptc)
                            outpcontemp = pitstr[stoptc:endoptc]
                            stxp = pitstr.index('px="') + len('px="'); endxp = pitstr.index('"',stxp)
                            tempxcp = pitstr[stxp:endxp]
                            styp = pitstr.index('pz="') + len('pz="'); endyp = pitstr.index('"',styp)
                            tempycp = pitstr[styp:endyp]
                            ststspp = pitstr.index('start_speed="') + len('start_speed="'); endstspp = pitstr.index('"',ststspp)
                            tempstspdcp = pitstr[ststspp:endstspp]
                            stenspp = pitstr.index('end_speed="') + len('end_speed="'); endenspp = pitstr.index('"',stenspp)
                            tempenspdcp = pitstr[stenspp:endenspp]
                            stbkyt = pitstr.index('break_y="') + len('break_y="'); endbkyt = pitstr.index('"',stbkyt)
                            tempbky = pitstr[stbkyt:endbkyt]
                            stbkat = pitstr.index('break_angle="') + len('break_angle="'); endbkat = pitstr.index('"',stbkat)
                            tempbka = pitstr[stbkat:endbkat]
                            stbklt = pitstr.index('break_length="') + len('break_length="'); endbklt = pitstr.index('"',stbklt)
                            tempbkl = pitstr[stbklt:endbklt]
                            stnsty = pitstr.index('nasty="') + len('nasty="'); endnsty = pitstr.index('"',stnsty)
                            nstytemp = pitstr[stnsty:endnsty]
                            stsztopt = pitstr.index('sz_top="') + len('sz_top="'); endsztopt = pitstr.index('"',stsztopt)
                            tempsztop = pitstr[stsztopt:endsztopt]
                            stszbott = pitstr.index('sz_bot="') + len('sz_bot="'); endszbott = pitstr.index('"',stszbott)
                            tempszbot = pitstr[stszbott:endszbott]
                        else:
                            outptemp = 'XX'
                            outpcontemp = '1'
                            tempxcp = '0'; tempycp = '0'; tempstspdcp = '0'; tempenspdcp = '0'; tempbky = '0'; tempbka = '0'; tempbkl = '0'; nstytemp = '0'; tempsztop = '0'; tempszbot = '0'
                        stdes1 = pitstr.index('des="') + len('des="'); enddes1 = pitstr.index('"',stdes1)
                        tempdes1 = pitstr[stdes1:enddes1]
                        sttype1 = pitstr.index('" type="') + len('" type="'); endtype1 = pitstr.index('"',sttype1)
                        temptype1 = pitstr[sttype1:endtype1]
                        
                        # Stuff from the previous pitch
                        stdes = prPitstr.index('des="') + len('des="'); enddes = prPitstr.index('"',stdes)
                        tempdes = prPitstr[stdes:enddes]
                        sttype = prPitstr.index(' type="') + len(' type="'); endtype = prPitstr.index('"',sttype)
                        temptype = prPitstr[sttype:endtype]
                        
                        if ind == (len(table3) - 1):
                            sthdes = pitstr.index('des="') + len('des="'); endhdes = pitstr.index('"',sthdes)
                            holddesc = pitstr[sthdes:endhdes]
                        
                        Inning.append(int(num))
                        at_bat_num.append(int(aABct))
                        spread.append(int(temphsc) - int(tempasc))
                        outs.append(int(tempout))
                        batter.append(int(battertemp))
                        bheight.append(12*int(bhtemp[0]) + int(bhtemp[2:len(bhtemp)]))
                        stance.append(standtemp)
                        pitcher.append(int(pitchertemp))
                        pthrows.append(pthtemp)
                        event.append(tempev)
                        des.append(tempdes)
                        pnum.append(int(apct))
                        typebs.append(temptype)
                        tfs.append(int(tfstemp))
                        sztop.append(12*float(tempsztop))
                        szbot.append(12*float(tempszbot))
                        breaky.append(float(tempbky))
                        breakangle.append(float(tempbka))
                        breaklength.append(float(tempbkl))
                        on1.append(on1temp)
                        on2.append(on2temp)
                        on3.append(on3temp)
                        nasty.append(float(nstytemp))
                        outpitch.append(outptemp)
                        out_type_conf.append(float(outpcontemp))
                        outx.append(12*float(tempxcp))
                        outy.append(12*float(tempycp))
                        outstspd.append(float(tempstspdcp))
                        outenspd.append(float(tempenspdcp))
                        gid.append(gameID)
                        res_event.append(tempev1)
                        res_des.append(tempdes1)
                        res_typebs.append(temptype1)
                    except Exception as e:
                        print pitstr
                        print traceback.print_exc()
                        print [ind, ind1, Iind]
                        continue
                    
                if ind1 == (len(table2) - 1):
                    try:
                        sthsc = ABstr.index('home_team_runs="') + len('home_team_runs="'); endhsc = ABstr.index('"',sthsc)
                        holdhscore = ABstr[sthsc:endhsc]
                        stasc = ABstr.index('away_team_runs="') + len('away_team_runs="'); endasc = ABstr.index('"',stasc)
                        holdascore = ABstr[stasc:endasc]
                    except ValueError:
                        holdhscore = '0'; holdascore = '0'

    
    stop = int(len(outx))
    
    cur_zones = build_zone(sztop,szbot,outx,outy,stance)

    return GamePitchData(np.asarray(gid),np.asarray(Inning),np.asarray(at_bat_num),np.asarray(spread),np.asarray(outs),np.asarray(batter),np.asarray(bheight),np.asarray(stance),np.asarray(pitcher),np.asarray(pthrows),np.asarray(event),np.asarray(res_event),np.asarray(des),np.asarray(res_des),np.asarray(pnum),np.asarray(typebs),np.asarray(res_typebs),np.asarray(tfs),np.asarray(sztop),np.asarray(szbot),np.asarray(breaky),np.asarray(breakangle),np.asarray(breaklength),np.asarray(on1),np.asarray(on2),np.asarray(on3),np.asarray(nasty),np.asarray(outpitch),np.asarray(out_type_conf),np.asarray(outx),np.asarray(outy),np.asarray(outstspd),np.asarray(outenspd),np.asarray(cur_zones))

#def makedata(gpstruct):

def getdaydata(yr,month,day):

    #now = datetime.datetime.now()

    #yrs = range(int(sys.argv[1]),int(sys.argv[1]) + 1)

    #yr = str(2016); month = str(7); day = str(12);
    yr = str(yr)
    
    month = str(month)

    if len(month) < 2:
        month = '0' + month
    
    day = str(day)

    if len(day) < 2:
        day = '0' + day

    gameID = []; Inning = []; at_bat_num = []; spread = []; outs = []; batter = []; stance = []; bheight = []; pitcher = []; pthrows = []; event = []; des = []; pnum = []; typebs = []; tfs = []; stspd = []; endspd = []; sztop = []; szbot = []; breaky = []; breakangle = []; breaklength = []; on1 = []; on2 = []; on3 = []; pr_pitch_type = []; pr_type_conf = []; nasty = []; outpitch = []; out_type_conf = []; outx = []; outy = []; outstspd = []; outenspd = []; stop = []; gameID = []; pr_zones = []; cur_zones = []; res_event = []; res_des = []; res_typebs = [];

    BaseballData = GamePitchData(gameID,Inning,at_bat_num,spread,outs,batter,bheight,stance,pitcher,pthrows,event,res_event,des,res_des,pnum,typebs,res_typebs,tfs,sztop,szbot,breaky,breakangle,breaklength,on1,on2,on3,nasty,outpitch,out_type_conf,outx,outy,outstspd,outenspd,cur_zones)


    url1 = 'http://gd2.mlb.com/components/game/mlb/year_' + yr + '/month_' + month + '/day_' + day + '/'

    url2 = 'inning/inning_all.xml'

    page = requests.get(url1)

    soup = BeautifulSoup(page.content,'lxml')

    table = soup.find_all('a',string=re.compile('gid'))

    lst = []

    for elem in table:
        elem = str(elem)
        start = elem.index('"') + len('"')
        end = elem.index('"',start)
        lst.append(elem[start:end])

    for game in lst:
        
        try:
            name = getgameID(game)

            url = url1 + game + url2

            BaseballData = mergeGameData(BaseballData,getgamedata(url,name))
            
            #save_object(BaseballData,'MLBData2010throughNow.pkl')

        except Exception as e:
            print traceback.print_exc()
            print game
            continue

    return BaseballData

"""gameID = []; Inning = []; at_bat_num = []; spread = []; outs = []; batter = []; stance = []; bheight = []; pitcher = []; pthrows = []; event = []; des = []; pnum = []; typebs = []; tfs = []; stspd = []; endspd = []; sztop = []; szbot = []; breaky = []; breakangle = []; breaklength = []; on1 = []; on2 = []; on3 = []; pr_pitch_type = []; pr_type_conf = []; nasty = []; outpitch = []; out_type_conf = []; outx = []; outy = []; outstspd = []; outenspd = []; stop = []; gameID = []; pr_zones = []; cur_zones = []; res_event = []; res_des = []; res_typebs = [];

NewData = GamePitchData(gameID,Inning,at_bat_num,spread,outs,batter,bheight,stance,pitcher,pthrows,event,res_event,des,res_des,pnum,typebs,res_typebs,tfs,sztop,szbot,breaky,breakangle,breaklength,on1,on2,on3,nasty,outpitch,out_type_conf,outx,outy,outstspd,outenspd,cur_zones)

with open('OldtxtFiles/MLBGoodDataOD2010thruASB2016.pkl','rb') as input:
    PrevData = pickle.load(input)

print 'loaded'

print len(PrevData.Inning)

yr = 2016; month = [7,8];

for m in month:
    if m == 7:
        days = range(0,32)
    else:
        days = range(0,26)

    for d in days:

        NewData = mergeGameData(NewData,getdaydata(yr,m,d))

        print 'month: ' + str(m) + ' day: ' + str(d) + 'done'

AllData = mergeGameData(PrevData,NewData)

save_object(AllData,'MLBAllUpdate.pkl')

print 'done'"""

"""mstart = time.clock()

for yr in yrs:
    if yr == 2011 or yr == 2013 or yr == 2014:
        months = range(3,11)
    elif yr == now.year:
        months = range(4,now.month+1)
    else:
        months = range(4,11)

    yr = str(yr)

    for month in months:
        if month == 3:
            days = [31]
        elif month == 4 and int(yr) == 2010:
            days = range(4,31)
        elif month == 4 and int(yr) == 2012:
            days = range(5,31)
        elif month == 4 and int(yr) == 2015:
            days = range(5,31)
        elif month == 4 and int(yr) == 2016:
            days = range(3,31)
        elif month == 6 or month == 9:
            days = range(1,31)
        elif month == now.month and int(yr) == now.year:
            days = range(1,11)
        else:
            days = range(1,32)
        
        month = str(month)

        if len(month) < 2:
            month = '0' + month

        for day in days:

            day = str(day)

            if len(day) < 2:
                day = '0' + day

            url1 = 'http://gd2.mlb.com/components/game/mlb/year_' + yr + '/month_' + month + '/day_' + day + '/'

            url2 = 'inning/inning_all.xml'

            page = requests.get(url1)

            soup = BeautifulSoup(page.content,'lxml')

            table = soup.find_all('a',string=re.compile('gid'))

            lst = []

            for elem in table:
                elem = str(elem)
                start = elem.index('"') + len('"')
                end = elem.index('"',start)
                lst.append(elem[start:end])

            for game in lst:
                
                try:
                    name = getgameID(game)

                    url = url1 + game + url2

                    BaseballData = mergeGameData(BaseballData,getgamedata(url,name))

                    
                    #save_object(BaseballData,'MLBData2010throughNow.pkl')

                except Exception as e:
                    print traceback.print_exc()
                    print game
                    continue


            print yr + ' ' + month + ' ' + day + ' done.'

        save_object(BaseballData,'MLBData' + sys.argv[1] + '.pkl')

print time.clock() - mstart"""

#for i in range(0,gamedata.count):
#    print [gamedata.cur_zones[i], gamedata.pr_zones[i], gamedata.pr_pitch_type[i]]

#print [gamedata.outx, gamedata.outy]


"""for inning in table:
    temp = inning.findAll('pitch')
    for pitch in temp:
        print pitch['des']"""
"""print 'Loading...'
start = time.clock()
with open('MLBData2010.pkl','rb') as input:
    D10 = pickle.load(input)
print len(D10.gameID)
print '10 loaded'
with open('MLBData2011.pkl','rb') as input:
    D11 = pickle.load(input)
print len(D11.gameID)
print '11 loaded'
with open('MLBData2012.pkl','rb') as input:
    D12 = pickle.load(input)
print len(D12.gameID)
print '12 loaded'
with open('MLBData2013.pkl','rb') as input:
    D13 = pickle.load(input)
print len(D13.gameID)
print '13 loaded'
with open('MLBData2014.pkl','rb') as input:
    D14 = pickle.load(input)
print len(D14.gameID)
print '14 loaded'
with open('MLBData2015.pkl','rb') as input:
    D15 = pickle.load(input)
print len(D15.gameID)
print '15 loaded'
with open('MLBData2016.pkl','rb') as input:
    D16 = pickle.load(input)
print len(D16.gameID)
print '16 loaded'

print time.clock() - start

ten11 = mergeGameData(D10,D11)

ten12 = mergeGameData(ten11,D12)

ten13 = mergeGameData(ten12,D13)

ten14 = mergeGameData(ten13, D14)

ten15 = mergeGameData(ten14,D15)

allofit = mergeGameData(ten15,D16)

#FullData = mergeGameData(D1,BaseballData)

print len(allofit.Inning)

save_object(allofit,'MLBGoodDataOD2010thruASB2016.pkl')"""




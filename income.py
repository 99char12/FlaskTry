import tkinter as tk
from tkinter import Message ,Text,Scrollbar
import cv2,os
import shutil
import csv
import numpy as np
import pandas as pd
import tkinter.ttk as ttk
import tkinter.font as font
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn import metrics
from sklearn.linear_model import Ridge
from PIL import Image,ImageTk
import datetime
import sys
from textblob import TextBlob
import requests
from io import BytesIO
from firebase import firebase

class Income(object):
    def __init__(self,state,district,land,crop):
        self.state=state
        self.district=district
        self.land=land
        self.crop=crop
        
    def predictor(self):
        #print(self.state,self.district,self.land,self.crop) 
        #name=txt1.get()
        #acno=txt2.get()
        district=self.district#txt3.get()
        state=self.state#txt4.get()
        land_area=self.land#txt5.get()
        crop=self.crop #txt6.get()
        #own=v.get()
        own=0
        stop=0
        print("Hii")
        #some declarations
        amob=0
        rr=""
        yield_for_database=0
    
        #print(name,acno,district,state,land_area,crop,own)
        now1 = datetime.datetime.now()
        st1=state
        cr1=crop
        di1=district
        clf=Ridge(alpha=1.0)
    
        print(district)

        flag3=0
        flag1=0
        flag2=0
        try:
            #creating firebase object
            from firebase import firebase
            firebase = firebase.FirebaseApplication('https://farmsistantfinal.firebaseio.com/',None)
        #read data from firebase table
            result=firebase.get('Market_price/',None)
            l1,l2=[],[]
            for i in result.values():
                l1.append(i['name'])
                l2.append(i['price'])
        #create dataset and get current market price    
            da=pd.DataFrame(list(zip(l1,l2)),columns=['crop','price']) 
            da=da[da['crop']==crop]
            str1=list(da['price'])
            rr=str(str1[len(str1)-1])
            print("Last price is "+str(rr))
            #mprice = tk.Label(winnn, text=rr,width=60  ,height=2  ,fg="#DF744A"  ,bg="#FEDCD2" ,font=('Arial Rounded MT Bold', 15, ' bold ') )
            #mprice.place(x=400, y=100)    
    
        except ValueError:
            stop=1
            pass
    
        if stop==0:
            stop1=0
 
            try:
                l1,l2=[],[]
                l3,l4=[],[]
                #reading data from firebase
                result=firebase.get('WeatherData/',None)
                for i in result.values():
                    l1.append(i['state'])
                    l2.append(i['district'])
                    l3.append(i['year'])
                    l4.append(i['rain'])
                #creating dataset    
                da1=pd.DataFrame(list(zip(l1,l2,l3,l4)),columns=['state','district','year','rain'])
                print("-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-")
                print(da1)
                print("-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-")

                da1.replace(np.inf,np.nan)
                da1.replace(-np.inf,np.nan)
                da1.fillna(method='backfill',inplace=True)
                da1=da1[da1['state']==st1]
                da1=da1[da1['district']==di1]
                #converting strings to integer so as to allow prediction
                h=2
                for i in range(h):
                    co=0
                    for j in da1.iloc[:,i]:
                        s=0
                        for k in j:
                            s+=ord(k)    
                        da1.iloc[co,i]=s  
                        co+=1  
                #predicting rainfall for current year        
                if da1.shape[0]!=1:        
                    y=da1.rain
                    X=da1.drop('rain',1)
                    clf.fit(X,y)
                    xtr,ytr,xtes,ytes=train_test_split(X,y,test_size=0.2,random_state=10)
                    rain=clf.predict(ytr)
                    r=rain[0]
                    print("Rainfall is"+str(rain[0]))  
                    str12="Rain is"+str(r)
                else:
                    str12=str(da1['rain'])
                    pass
            except ValueError:  
                stop1=1
            
            except IndexError:    
                stop1=1
            
            if(stop1==0):
                stop2=0
                #getting soil pH required for a crop 
                try:
                    da2=pd.read_csv('https://raw.githubusercontent.com/sailendra2000/crop_prediction/master/Soil_crop_ph.csv')
                    da2.fillna(method='backfill',inplace=True)
                    da2=da2[da2['Crop']==cr1]
                    maxiph=da2['ph_max']
                    miniph=da2['ph_min']
                    soil=da2['Soil']
                    k=(maxiph.values[0])
                    l=(miniph.values[0])
                    m=(soil.values)
                except ValueError:
                    stop2=1
                except IndexError:
                    stop2=1
            
                try:
                    #finding types of soil available in a district
                    da3=pd.read_csv('https://raw.githubusercontent.com/sailendra2000/crop_prediction/master/State_soil.csv')
                    da3.fillna(method='backfill',inplace=True)
                    da3=da3[da3['State']==st1]
                    da3=da3[da3['district']==di1]
                    avai_min_ph=da3['ph_min']
                    avai_max_ph=da3['ph_max']
                    avai_soil=da3['Soil']
                    print("maxph,minph and soil is"+str(l)+" "+str(k)+" "+str(m))

        
                except ValueError:
                    stop2=1
                except IndexError:
                    stop2=1
            
                if stop2==0:
                    stop3=0
                    try: 
                        #getting minimum and maximum average temperature in a district over a year
                        da5=pd.read_csv('https://raw.githubusercontent.com/sailendra2000/crop_prediction/master/minmaxtemper.csv')
                        da5=da5[da5['State']==st1]
                        da5=da5[da5['District']==di1]
                        temp_min=da5['Min_temp'].values[0]
                        temp_max=da5['Max_temp'].values[0]
    
                        da6=pd.read_csv('https://raw.githubusercontent.com/sailendra2000/crop_prediction/master/temp_requ.csv')
                        da6=da6[da6['Crop']==crop]
                        avai_min_temp=da6['Minimum_temperature'].values[0]
                        avai_max_temp=da6['Maximum_temperature'].values[0]

                        #comparing temperature range to find if the temperature conditions support the growth of specified crop
                        flag3=0
                        flag5=1
                        if(temp_min<=avai_min_temp):
                            if(temp_max>=avai_min_temp):
                                flag3=1
                            else:
                                flag3=0
                        elif(temp_min>avai_min_temp):        
                            if(avai_max_temp>=temp_min):
                                flag3=1
                            else:
                                flag3=0
                        if flag3==0:      
                            print("@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@")
                            print("Not cultivable")
                            print("@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@")

                            #labl2 = tk.Label(winnn, text="Not Cultivable",width=60  ,height=2  ,fg="#DF744A"  ,bg="#462066" ,font=('Arial Rounded MT Bold', 15, ' bold ') )
                            #labl2.place(x=400, y=250)
    
                        #comparing pH values for supporting growth of specified crop 
                        flag=0
                        flag1=0
                        flag2=0
                        for i in avai_min_ph.values:
                            if i>=l:
                                if i<=k:
                                    flag1=1
                                    flag2=1
                            else:
                                for i in avai_max_ph.values:
                                    if i<=k:
                                        flag1=1
                                        flag2=1
                        quite=0        
                        for i in m:
                            if i in avai_soil.values:
                                quite=1
                                if flag1==1 or flag2==1:
                                    print("Cultivable")
                                    #labl2 = tk.Label(winnn, text="Cultivable",width=60  ,height=2  ,fg="#DF744A"  ,bg="#462066" ,font=('Arial Rounded MT Bold', 15, ' bold ') )
                                    #labl2.place(x=400, y=350)
                                    flag=1
                                    break
                                else:    
                                    print("No requires soil pH")
                                    #labl2 = tk.Label(winnn, text="No Required Soil pH",width=60  ,height=2  ,fg="#DF744A"  ,bg="#FEDCD2" ,font=('Arial Rounded MT Bold', 15, ' bold ') )
                                    labl2.place(x=400, y=300)
                                    flag5=0
                        if quite==0:
                            #labl2 = tk.Label(winnn, text="No soil support for Crop",width=60  ,height=2  ,fg="#DF744A"  ,bg="#FEDCD2" ,font=('Arial Rounded MT Bold', 15, ' bold ') )
                            #labl2.place(x=400, y=300)
                            flag5=0
                    except ValueError:
                        stop3=1
                    except IndexError:
                        stop3=1
    
                    try:
                        #finding the average production of the specified crop per acre in quintals using prediction
                        da4=pd.read_csv('https://raw.githubusercontent.com/karthisuresh/Income_prediction_Crop_Suggestion/master/apy.csv')
                        da4=da4[da4['crop']==cr1]
                        da4=da4[da4['statename']==st1]
                        da4=da4[da4['districtname']==di1]
                        da4.fillna(method='backfill',inplace=True)
                        da4['pbya']=da4['production']/da4['area']
                        if da4.shape[0]!=1:
                            y=da4.pbya
                            X=da4.drop('pbya',1)
                            X=X.drop('statename',1)
                            X=X.drop('districtname',1)
                            X=X.drop('season',1)
                            X=X.drop('crop',1)
                            X=X.drop('production',1)
                            clf.fit(X,y)
                            xtr,ytr,xtes,ytes=train_test_split(X,y,test_size=0.2,random_state=10)

    
                            Year=now1.year
                            print(Year)
                            Area=int(land_area)*4046.86
                            ytr=[[Year,Area]]
                            pro_per_area=clf.predict(ytr)
                            print(pro_per_area[0])
                            print("yield is"+str(pro_per_area[0]*int(land_area)))
                            z=abs(pro_per_area[0]*int(land_area))
                            yield_for_database=z
                            yi="Yield in quintals="+str(z)
        
                        else:
                            yi=str(da4['pbya'])
                        if(flag3!=0 and flag5==1):    
                            #yiel = tk.Label(winnn, text=yi,width=60  ,height=2  ,fg="#DF744A"  ,bg="#FEDCD2" ,font=('Arial Rounded MT Bold', 15, ' bold ') )
                            #yiel.place(x=400, y=400)
                            #amob=z*maxi_price[0]
                            amob=z*int(rr)*100
                            da=pd.read_csv('https://raw.githubusercontent.com/karthisuresh/farmloan_prediction/master/datafile%20(1).csv')
                            da.fillna(method='backfill',inplace=True)
                            da=da[da['crop']=='paddy']
                            temmpp = int(list(da['total'])[0])*10
                            amob =amob - temmpp
                            print("COst is " + str(temmpp))
                            '''if own==1:
                                if land_area>str(5):
                                    if amob>85000:
                                        amob=amob-38700
                                    if amob>55000:
                                        amob=amob-22000
                                    if amob>25000:
                                        amob=amob-10000'''
                            str3="Maximum amount for total yield="+str(amob)
                            #amtob = tk.Label(winnn, text=str3,width=60  ,height=2  ,fg="#DF744A"  ,bg="#FEDCD2" ,font=('Arial Rounded MT Bold', 15, ' bold ') )
                            #amtob.place(x=400, y=500)
        
                    except ValueError:
                        stop3=1
                    except IndexError:
                        stop3=1
                        
        #checking the data for suggesting crop that yields maximum income       
        da=pd.read_csv('https://raw.githubusercontent.com/karthisuresh/Income_prediction_Crop_Suggestion/master/crop_price.csv')
        da.fillna(method='backfill',inplace=True)
        da=da[da['state']==st1]
        da=da[da['district']==di1]
        print(da)
        maximuuum=0
        count=0
        index=0
        z=da.iloc[:,6:7]
        print("******************************")
        print(z)
        y=pd.Series(z['max_price'])
        print("###################################################")
        print(y)
        for i in y:
            print(i,end="&&&&&&&&")
            print()
            if i>(maximuuum):
                maximuuum=i
                index=count
            count+=1 
        print("This is"+str(maximuuum))
        
        size="Best suggested crop:"+str(da.iloc[index,2])
        #ll8 = tk.Label(winnn, text=size,width=60  ,height=2  ,fg="#DF744A"  ,bg="#FEDCD2" ,font=('Arial Rounded MT Bold', 15, ' bold ') )
        #ll8.place(x=400, y=600)
    
        z1=str(yield_for_database)
        st=str(str12)
        am=str(amob)
        si=str(da.iloc[index,2])
    
        data={
        'rain':st,
         'yield_quintals':z1,
          'overall_price':am,
            'best_crop':si
        }
        result = firebase.post('Previous/',data)
        print(result)
    
        profit=int(0.25*amob)
        profit_text="Profit is"+str(profit)
        
        #ll9 = tk.Label(winnn, text=profit_text,width=60  ,height=2  ,fg="#DF744A"  ,bg="#FEDCD2" ,font=('Arial Rounded MT Bold', 15, ' bold ') )
        #ll9.place(x=400, y=675)
    
        #if(state=='assam'):
            #ll10 = tk.Label(winnn, text="Please avail insurance",width=60  ,height=2  ,fg="#DF744A"  ,bg="#FEDCD2" ,font=('Arial Rounded MT Bold', 15, ' bold ') )
            #ll10.place(x=400, y=750)
   
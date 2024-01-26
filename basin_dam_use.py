import pandas as pd
import os
import re
import numpy as np
header=pd.DataFrame(columns=["name","Irrigation","Hydroelectricity","Water supply","Flood control","Recreation","Navigation","Fisheries","Pollution control","Livestock","Other","Blank","mainuse","affect","affectv","year.start","year.end","no"])
header.to_csv('E:out.csv')
for name in os.listdir(r'C:\\Users\\dell\\Desktop\\excel'):
	data = os.path.join('C:\\Users\\dell\\Desktop\\excel\\',name)
	data = pd.read_excel(data,usecols=[15,27,48])
	arr=pd.DataFrame(columns=["name","Irrigation","Hydroelectricity","Water supply","Flood control","Recreation","Navigation","Fisheries","Pollution control","Livestock","Other","Blank","mainuse","affect","affectv","year.start","year.end","no"])
	arr.loc[0]=0
	columnname=arr.columns.values.tolist()
	l=len(data)
	for i in range(l):
		if data.iloc[i,1]==-99:
			data=data.drop(index=[i])
	data=data.reset_index(drop=True)
	l=len(data)
#计算各种用途水库的容积
	Irrigation=Hydroelectricity=Watersupply=Floodcontrol=Recreation=Navigation=Fisheries=Pollutioncontrol=Livestock=Other=Blank=0
	time = pd.read_excel('C:\\Users\\dell\\Desktop\\area.xls')
	time.set_index('gsim', inplace=True)
	start=int(time.loc[str(name),"year.start"])
	end=int(time.loc[str(name),"year.end"])
	no=0
	for i in range(l):
		year=data.iloc[i,0]
		if year>start and year<end:
			no+=1
		else:
			continue
		if data.iloc[i,2]=="Irrigation":
			Irrigation+=data.iloc[i,1]
		elif data.iloc[i,2]=="Hydroelectricity":
			Hydroelectricity+=data.iloc[i,1]
		elif data.iloc[i,2]=="Water supply":
			Watersupply+=data.iloc[i,1]
		elif data.iloc[i,2]=="Flood control":
			Floodcontrol+=data.iloc[i,1]
		elif data.iloc[i,2]=="Recreation":
			Recreation+=data.iloc[i,1]
		elif data.iloc[i,2]=="Navigation":
			Navigation+=data.iloc[i,1]
		elif data.iloc[i,2]=="Fisheries":
			Fisheries+=data.iloc[i,1]
		elif data.iloc[i,2]=="Pollution control":
			Pollutioncontrol+=data.iloc[i,1]
		elif data.iloc[i,2]=="Livestock":
			Livestock+=data.iloc[i,1]
		elif data.iloc[i,2]=="Other":
			Other+=data.iloc[i,1]
		elif data.iloc[i,2]==" ":
			Blank+=data.iloc[i,1]
	sum=Irrigation+Hydroelectricity+Watersupply+Floodcontrol+Recreation+Navigation+Fisheries+Pollutioncontrol+Livestock+Other+Blank
	var=[Irrigation,Hydroelectricity,Watersupply,Floodcontrol,Recreation,Navigation,Fisheries,Pollutioncontrol,Livestock,Other,Blank]
	for i in range(11):
		if var[i]>0.5*sum:
			arr.iloc[0,12]=columnname[i+1]
	arr.loc[0,"name"]=name
	arr.loc[0,"Irrigation"]=Irrigation
	arr.loc[0,"Hydroelectricity"]=Hydroelectricity
	arr.loc[0,"Water supply"]=Watersupply
	arr.loc[0,"Flood control"]=Floodcontrol
	arr.loc[0,"Recreation"]=Recreation
	arr.loc[0,"Navigation"]=Navigation
	arr.loc[0,"Fisheries"]=Fisheries
	arr.loc[0,"Pollution control"]=Pollutioncontrol
	arr.loc[0,"Livestock"]=Livestock
	arr.loc[0,"Other"]=Other
	arr.loc[0,"Blank"]=Blank
#判断水坝是否建于流量观测期内
	arr.loc[0,"affectv"]=sum
	arr.loc[0,"year.start"]=start
	arr.loc[0,"year.end"]=end
	arr.loc[0,"no"]=no
	arr.to_csv('E:out.csv',header=False,mode='a')
import pandas as pd
import numpy as np
from dbfread import DBF


table = DBF('E:\\hydroriverpoint\\point.dbf', encoding='GBK')
header=pd.DataFrame(columns=["HYRIV_ID","NEXT_DOWN","MAIN_RIV","LENGTH_KM","DIST_DN_KM","DIST_UP_KM","CATCH_SKM","UPLAND_SKM","ENDORHEIC","DIS_AV_CMS","ORD_STRA","ORD_CLAS","ORD_FLOW","HYBAS_L12","Shape_Leng","sgr_dk_rav","X","Y","RA","RD","R","ID","Wshd_area"])
header.to_csv('E:out.csv')
river = pd.DataFrame(iter(table))
ll=len(river)
for m in range(ll):
	if river.loc[m,"UPLAND_SKM"]==0:
		river=river.drop(m)
dam=pd.read_excel(r'C:\\Users\\dell\\Desktop\\GOODDsnap\\alldam.xlsx')
ldam=len(dam)
for i in range(ldam):
	x=dam.loc[i,"Pour_long"]
	y=dam.loc[i,"Pour_lat"]
	jinlin=river[(abs(river.X-x)<0.2)&(abs(river.Y-y)<0.2)]
	l=len(jinlin)
	if l==0:
		continue
	if dam.loc[i,"Wshd_area"]==0:
		continue
	jinlin=jinlin.reset_index(drop=True)
	for j in range(l):
		jinlin.loc[j,"RA"]=abs((jinlin.loc[j,"UPLAND_SKM"]-dam.loc[i,"Wshd_area"]))/jinlin.loc[j,"UPLAND_SKM"]*250
		jinlin.loc[j,"RD"]=pow(pow(jinlin.loc[j,"X"]-x,2)+pow(jinlin.loc[j,"Y"]-y,2),0.5)*100
		jinlin.loc[j,"R"]=jinlin.loc[j,"RA"]+2*jinlin.loc[j,"RD"]
	id=jinlin.R.idxmin()
	result=pd.DataFrame(jinlin.loc[id])
	result.loc["ID",id]=dam.loc[i,"ID"]
	result.loc["Wshd_area",id]=dam.loc[i,"Wshd_area"]
	result.T.to_csv('E:out.csv',header=False,mode='a')


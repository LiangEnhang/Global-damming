import pandas as pd
import numpy as np
from dbfread import DBF

data=DBF(r'E:mapping\\USE_SED_DOF.dbf', encoding='GBK')
data=data.set_index('REACH_ID')
table1 = DBF(r'C:\\Users\\dell\\Desktop\\ES\\525xiangjiao\\fid1xiangjiao.dbf', encoding='GBK')
table2 = DBF(r'C:\\Users\\dell\\Desktop\\ES\\525xiangjiao\\fid2xiangjiao.dbf', encoding='GBK')
river1 = pd.DataFrame(iter(table1))
river2 = pd.DataFrame(iter(table2))
river2=river2.loc[river2.HYRIV_ID>0]
data=pd.DataFrame(iter(data))


river2.loc[:,"DOF"]=data.loc[river2.HYRIV_ID.values,"DOF"].values
river2.loc[:,"USE"]=data.loc[river2.HYRIV_ID.values,"USE"].values
river2.loc[:,"SED"]=data.loc[river2.HYRIV_ID.values,"SED"].values
river1.loc[:,"DOF"]=data.loc[river1.HYRIV_ID.values,"DOF"].values
river1.loc[:,"USE"]=data.loc[river1.HYRIV_ID.values,"USE"].values
river1.loc[:,"SED"]=data.loc[river1.HYRIV_ID.values,"SED"].values

river1.loc[:,["HYRIV_ID","ID","ORD_STRA","DOF","USE","SED"]].to_csv("E:river1.txt")
river2.loc[:,["HYRIV_ID","ID","ORD_STRA","DOF","USE","SED"]].to_csv("E:river2.txt")

river=river.loc[:,["HYRIV_ID","ID","ORD_STRA","DOF","USE","SED"]].drop_duplicates()

fenji1=river1.groupby(['ID']).mean()
fenji1.to_csv('E:out2.csv',mode='a')
fenji2=river2.groupby(['ID']).mean()
fenji2.to_csv('E:out2.csv',mode='a')








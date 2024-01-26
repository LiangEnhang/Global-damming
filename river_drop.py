import pandas as pd
import numpy as np
from dbfread import DBF


table1 = DBF(r'C:\\Users\\dell\\Desktop\\ES\\525xiangjiao\\fid1xiangjiao.dbf', encoding='GBK')
table2 = DBF(r'C:\\Users\\dell\\Desktop\\ES\\525xiangjiao\\fid2xiangjiao.dbf', encoding='GBK')
river1 = pd.DataFrame(iter(table1))
river2 = pd.DataFrame(iter(table2))
river1.loc[:,"H"]=river1.loc[:,"LENGTH_KM"]*river1.loc[:,"sgr_dk_rav"]*0.1
fenji=river1.groupby(['ID','ORD_STRA']).sum()
fenji.to_csv('E:out1.csv',mode='a')

river2.loc[:,"H"]=river2.loc[:,"LENGTH_KM"]*river2.loc[:,"sgr_dk_rav"]*0.1
fenji=river2.groupby(['ID','ORD_STRA']).sum()
fenji.to_csv('E:out2.csv',mode='a')






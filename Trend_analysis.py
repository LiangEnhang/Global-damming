import pandas as pd
import os
import re
import numpy as np
for data in os.listdir(r'E:/1'):
	data = os.path.join('E:/1',data)
	with open(data,'r') as x:
		line = x.readlines()
	name=re.findall(r"[A-Z]+_\d+",line[10])
#提取经纬度及站点名称
	latitude=re.findall(r"-?\d+\.?\d*",line[14])
	longitude=re.findall(r"-?\d+\.?\d*",line[15])
	data = pd.read_table(data,sep=',\t',skiprows=list(range(21)),usecols=[5],engine='python')
	data['index'] = data.index
	data=data.dropna(axis=0,how='any')
	data=data.reset_index(drop=True)
	l=len(data)
	if l<4:
		continue
	data1=data[0:l-1]
#计算自相关系数
	data2=data[1:]
	data_mean=data.mean()
	data_var=0
	for i in range(l):
		data_var+=pow(data.loc[i]-data_mean,2)
	auto_corr=0
	for i in range(l-1):
		temp=(data1.loc[i]-data_mean)*(data2.loc[i+1]-data_mean)/data_var
		auto_corr+=temp
	auto_corr=auto_corr.iloc[0]
	ru=(-1+1.96*pow(l-2,0.5))/(l-1)
#自相关系数显著性检验
	rd=(-1-1.96*pow(l-2,0.5))/(l-1)
	if auto_corr<ru and auto_corr>rd:
		auto_result='NS'
	else:
		auto_result='S'
#计算slope
	slopeseries={'S':[0]}
	Slopeseries=pd.DataFrame(slopeseries)
	c=0
	for i in range(l-1):
		for j in range(i+1,l):
			Slopeseries.loc[c]=(data.loc[j,'"MIN"']-data.loc[i,'"MIN"'])/(data.loc[j,'index']-data.loc[i,'index'])
			c+=1
	slope=Slopeseries.median()
	slope=slope.iloc[0]
#去除自相关项
	if auto_result=='S':
		for i in range(l):
			data.iloc[i]=data.iloc[i,0]-slope*i
		for i in range(1,l):
			data.iloc[l-i]=data.iloc[l-i,0]-auto_corr*data.iloc[l-i-1,0]
		for i in range(l):
			data.iloc[i]=data.iloc[i,0]+slope*i
	same=[]
#提取相同数据的组数和每组的样本数
	unit=[]
	tp=1
	for i in range(l-1):
		if tp>1:
			same.append(tp)
			unit.append(data.iloc[i-1,0])
			tp=1
		if data.iloc[i,0] in unit:
			continue
		for j in range(i+1,l):
			if data.iloc[i,0]==data.iloc[j,0]:
				tp+=1
	q=len(same)
	s=0
#计算s
	for i in range(l-1):
		for j in range(i+1,l):
			if data.iloc[j,0]>data.iloc[i,0]:
				s+=1
			elif data.iloc[j,0]==data.iloc[i,0]:
				s+=0
			elif data.iloc[j,0]<data.iloc[i,0]:
				s-=1
	vars=l*(l-1)*(2*l+5)
#计算vars
	for i in range(q):
		vars-=same[i]*(same[i]-1)*(2*same[i]+5)
	vars=vars/18
	if s>0:
#计算z
		z=(s-1)/pow(vars,0.5)
	elif s==0:
		z=0
	else:
		z=(s+1)/pow(vars,0.5)
	blank={'"MIN"':[name]}
#写入表头
	line=pd.DataFrame(blank)
	line.loc[1]=latitude
	line.loc[2]=longitude
	line.loc[3]=auto_corr
	line.loc[4]=auto_result
	line.loc[5]=slope
	line.loc[6]=s
	line.loc[7]=vars
	line.loc[8]=z
	line.loc[9]=q
	line.loc[10]=l
	line.loc[11]=data_mean
	line.loc[12]='***********'
	data=data.drop(columns='index')
	new=pd.concat([line,data])
#合并结果并输出
	new.T.to_csv('E:outMIN.csv',header=False,mode='a')
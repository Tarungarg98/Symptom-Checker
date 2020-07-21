import pandas as pd
import numpy as np
df=pd.read_csv('Cough_combined.csv')
dic1={}
dic2={}
for x in df['Conditions']:
	y=""
	flag=0
	for m in range(len(x)):
		a=x[m]
		if a=="'" and x[m-1]=="(" and flag==0:
			word1=""
			flag=1
			continue
			
		if a=="'" and x[m+1]=="," and flag==1:
			dic1[word1]=[]
			word1=""			
			flag=2
			continue

		if flag==1:
			word1+=a
			continue
			
		# print(a,x[m-1])
		if a=="'" and x[m-2]=="," and flag==2:
			word2=""
			flag=3
			continue
			
		if a=="'" and x[m+1]==")" and flag==3:
			dic2[word2]=[]
			if word2==" '":
				print(x)
			word2=""			
			flag=0
			continue
		if flag==3:
			word2+=a
symp1={}
symp2={}
for x in df['Symptoms']:
	y=""
	flag=0
	# print(x)
	for m in range(len(x)):
		a=x[m]
		if a=="'" and flag==0:
			word1=""
			flag=1
			continue
			
		if a=="'" and x[m+1]=="," and flag==1:
			symp1[word1]=[]
			word1=""			
			flag=2
			continue

		if flag==1:
			word1+=a
			continue
			
		if a=="'" and x[m-2]=="," and flag==2:
			word2=""
			flag=3
			continue
			
		if a=="'" and x[m+1]=="]" and flag==3:
			symp2[word2]=[]
			word2=""			
			flag=0
			continue

		if flag==3:
			word2+=a
			continue

symps=[]
for x in symp1:
	symps.append(x)
for x in symp2:
	symps.append(x)
symps=sorted(set(symps))
inp=pd.DataFrame(columns=symps)			
count=0
			
for x in df['Symptoms']:
	inp=inp.append({},ignore_index=True)
	y=""
	flag=0
	for m in range(len(x)):
		a=x[m]
		if a=="'" and flag==0:
			word1=""
			flag=1
			continue
			
		if a=="'" and x[m+1]=="," and flag==1:
			inp[word1][count]=1
			flag=2
			continue

		if flag==1:
			word1+=a
			continue
			
		if a=="'" and x[m-2]=="," and flag==2:
			word2=""
			flag=3
			continue
			
		if a=="'" and x[m+1]=="]" and flag==3:
			inp[word2][count]=1
			flag=0
			continue

		if flag==3:
			word2+=a
			continue
	count+=1
inp.replace(np.nan,0.0,inplace=True)
			
			
dis={}
count=0
for a in sorted(dic1):
	count+=1
	dis[a]=count	
match={}
count=0
match={'Low match': 1.0,'Fair match': 2.0, 'Moderate match': 3.0, 'STRONG match': 4.0}
# match={'Low match': 0.25,'Fair match': 0.5, 'Moderate match': 0.75, 'STRONG match': 1}

out=pd.DataFrame(columns=[a for a in dis])
count=0
for x in df['Conditions']:
	out=out.append({},ignore_index=True)
	y=""
	flag=0
	# print(x)
	for m in range(len(x)):
		a=x[m]
		if a=="'" and x[m-1]=="(" and flag==0:
			word1=""
			flag=1
			continue
			
		if a=="'" and x[m+1]=="," and flag==1:
			dic1[word1]=[]
			flag=2
			continue

		if flag==1:
			word1+=a
			continue
			
		if a=="'" and x[m-2]=="," and flag==2:
			word2=""
			flag=3
			continue
			
		if a=="'" and x[m+1]==")" and flag==3:
			out[word1][count]=match[word2]
			word2=""			
			flag=0
			continue
		if flag==3:
			word2+=a
	count+=1
out.replace(np.nan,0.0,inplace=True)

l=len(inp)
x_train=np.array(inp)[:int(0.8*l)]
x_validate=np.array(inp)[int(0.8*l):int(0.9*l)]
x_test=np.array(inp)[int(0.9*l):]
y_train=np.array(out)[:int(0.8*l)]
y_validate=np.array(out)[int(0.8*l):int(0.9*l)]
y_test=np.array(out)[int(0.9*l):]
# out[out.isin([4])].stack()


from tensorflow.keras.preprocessing import sequence
from tensorflow.keras.models import Sequential
from tensorflow.keras import backend as K
from tensorflow.keras.layers import Dense, Embedding, LSTM	
from tensorflow.keras.optimizers import Adam
K.clear_session()
model=Sequential()
model.add(Dense(30,activation='tanh'))
model.add(Dense(30,activation='tanh'))
# model.add(Dense(30,activation='tanh'))
model.add(Dense(81,activation='linear'))
opt=Adam(learning_rate=0.001)
model.compile(optimizer="adam", loss="mse", metrics=["accuracy"])
model.fit(x_train,y_train,validation_data=(x_validate,y_validate),verbose=1,epochs=2000)
model.predict(x_test)[y_test!=0]
# -*- coding: utf-8 -*-
"""A5_Mt19133_Q1_Regression.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1P0TUpki95vZyMHWVCRmzpliFnXE1SUsn
"""

##Cell -1 ##
###Import all library####

import pandas as pd
import numpy as np
import statistics
from sklearn import preprocessing
import math
from collections import Counter

##Cell -2 ##
#### Data Import and Test Train Split ####

##"drive/My Drive/SML_A5.csv"
data_path=input("Enter data path")
data=pd.read_csv(data_path)
data=data.drop(['No'], axis=1)
categorical=data["cbwd"].unique()
median=(statistics.median(data["pm2.5"]))
mean=(statistics.mean(data["pm2.5"]))

data["pm2.5"].fillna(value=mean,inplace = True) 
data.fillna(0,inplace = True)
print(data.shape)  ### (43824, 12)

print("year",len(data["year"].unique()))
print("month",len(data["month"].unique()))
print("day",len(data["day"].unique()))
print("hour",len(data["hour"].unique()))
print("pm2.5",len(data["pm2.5"].unique()))
print("DWEP",len(data["DEWP"].unique()))
print("TEMP",len(data["TEMP"].unique()))
print("IWS",len(data["Iws"].unique()))
print("IS",len(data["Is"].unique()))
print("IR",len(data["Ir"].unique()))




data=data.to_numpy()


Train_Data=[]
Test_Data=[]

##Training Data 2010 & 2012
##Test Data 2011 & 2014

for item in data:
  if item[0]==2010 or item[0]==2012:
    Train_Data.append(item)
  if item[0]==2011 or item[0]==2014:
    Test_Data.append(item)
  
Train_Data=np.array(Train_Data)
Test_Data=np.array(Test_Data)



print(len(Test_Data))  ### 17520
print(len(Train_Data))  ### 17544

#Cell -3 ##
### THis code performs label encoding for the "cbwd" attribute of the data ###


print(categorical)

label_encoder = preprocessing.LabelEncoder() 

categorical1= label_encoder.fit_transform(categorical)

print(categorical1)

categorical_dict={}
i=0
for item in categorical:
  categorical_dict.update({item:categorical1[i]})
  i=i+1

print(categorical_dict)

##Cell -4 ##
## features dictionary ##
features_dict={0:"year",1:"month",2:"day",3:"hour",4:"pm2.5",5:"DEWP",6:"TEMP",7:"PRES",8:"cbwd",9:"Iws",10:"Is",11:"Ir"}

features_dict1={"year":0,"month":1,"day":2,"hour":3,"pm2.5":4,"DEWP":5,"TEMP":6,"PRES":7,"cbwd":8,"Iws":9,"Is":10,"Ir":11}

##Cell -5 ##
## Label Encoder ##

from sklearn import preprocessing 

def encoder(arr):
  label_encoder = preprocessing.LabelEncoder() 

  category_col= label_encoder.fit_transform(arr[:,8:9])

  return category_col

##Cell -6 ##
### Entropy Calculator###
def rss_calc(arr):
  #print(arr)
  X1=statistics.mean(arr[:,4])
  
  RSS=0
  for item in arr:
    RSS=RSS+(pow((item[4]-X1),2))
  return RSS

##Cell -7 ##
def permutations():
  permute=[]
  permute.append(tuple([[0],[1,2,3]]))
  permute.append(tuple([[1],[0,2,3]]))
  permute.append(tuple([[2],[0,1,3]]))
  permute.append(tuple([[3],[1,2,0]]))
  
  permute.append(tuple([[1,2],[3,0]]))
  permute.append(tuple([[1,0],[3,2]]))
  permute.append(tuple([[1,3],[0,2]]))
  
  return permute

#
##Cell -8 ##
#### This function returns the best feature to split the node and the respective value of the feature ####

def split_node(features,arr):
  #print("Hi3")
  print("array ki size",len(arr))
  Best_feature=features[0]
  Breaking_condition=[]
  features_range={}
  for f in features:
    if not(isinstance(arr[0][f], (int,float))):
      features_range.update({f:encoder(arr)})
    else:
      unique=[]
      for j in range(0,len(arr)):
        if arr[j][f] not in unique:
          unique.append(arr[j][f])
      features_range.update({f:unique})
  
  min=9999999999
  Left=np.array([])
  Right=np.array([])

  for f in features:
    print("featurename:",features_dict.get(f))
    if not(isinstance(arr[0][f], (int,float))):
      permute=permutations()  ### Write some function ##

      for item in permute:
        L=item[0]
        R=item[1]
        arr1=[]
        arr2=[]
        for ITEM in L:
          for Item in arr:
            if Item[f] ==categorical_dict.get(ITEM):
              arr1.append(Item)

        arr1=np.array(arr1)

        for ITEM in R:
          for Item in arr:
            if Item[f] ==categorical_dict.get(ITEM):
              arr2.append(Item)

        arr2=np.array(arr2)
       # print("Hi4")
        if (len(arr1)!=0 and len(arr2)!=0):
          R1=rss_calc(arr1)
          R2=rss_calc(arr2)
          if min>(R1+R2):
            min=R1+R2
            Left=arr1
            Right=arr2
            Best_feature=f
            Breaking_condition=[]
            Breaking_condition.append(L)
            Breaking_condition.append(R)
          else:
            
            continue  
        
    else:
      range1=features_range.get(f)
      #print(range1)
      range1.sort()
      #print(range1)
      
      for i in range(0,len(range1)-1):
        
        if(len(range1)/100 >1):
          L=range1[0:(i+1)*50]
          R=range1[(i+1)*50:len(range1)]
          
        
        else:
          L=range1[0:(i+1)*2]
          R=range1[(i+1)*2:len(range1)]
        arr1=[]
        arr2=[]

        for ITEM in L:
          for item in arr:
            if item[f]==ITEM:
              arr1.append(item)
        arr1=np.array(arr1)

        for ITEM in R:
          for item in arr:
            if item[f]==ITEM:
              arr2.append(item)
        arr2=np.array(arr2)
        if len(arr2)==0:
          continue
        #print("Hi5")
        #if len(arr1) >0:
        R1=rss_calc(arr1)
        #if len(arr2) >0:
        R2=rss_calc(arr2)
        if min>(R1+R2):
          min=R1+R2
          Left=arr1
          Right=arr2
          Best_feature=f
          Breaking_condition=[]
          Breaking_condition.append(R[0])        
  
  return Left,Right,Best_feature,Breaking_condition

#Decision_tuple=[]
#Decision_tuple=[]
##Cell -9 ##
def DT(Decision_tuple,arr,features,Level):

  
  if len(arr) <=19:
    
    Decision_tuple.append(tuple([Level,"Leaf",statistics.mean(arr[:,4])]))
    return False
  

  LEFT,RIGHT,F,Breaking_condition=split_node(features,arr)
  print("feature selected",F)
  print("Left node",len(LEFT))
  print("Right node",len(RIGHT))
  Decision_tuple.append(tuple([Level,features_dict.get(F),Breaking_condition]))
  
  features_updt=[]
  #for fe in features:
  #if fe != F and fe!=1:
  features_updt=features
  #print("Hi1")    
  DT(Decision_tuple,LEFT,features_updt,Level+1)
  #print("Hi")
  DT(Decision_tuple,RIGHT,features_updt,Level+1)
  return Decision_tuple

##Cell 10 ##
## This function makes single regression tree ####
def make_tree():
  Decision_tuple=[]
  DTR=DT(Decision_tuple,Train_Data,[0,1,2,3,5,6,7,8,9,10,11],0)

  decision_tree=smooth_ds(DTR)
  MSE,Z=accuracy(decision_tree)
  MAE,SD=Mean_SD(decision_tree)

  print("Mean Squared Error :",MSE)
  print("Mean Absoute Error :",MAE)
  print("Standard Deviation :",SD)
  return Z

##Cell 11##
### Execute this cell to call  single regression tree
Z=make_tree()

##Cell 12##
##This function changes the stucture of each Decision tree node to a tuple ###
def smooth_ds(DTR):
  dt=[]
  for item in DTR:
    if item[1]=='Leaf':
      temp=[]
      temp.append(item[2])
      T=tuple([item[0],item[1],temp])
      dt.append(T)
    else:
      dt.append(item)
  return dt

##Cell 13 ###
### This function takes Decision tree as input and predict the output ###

def funct1(test,item,DT1):
  level=item[0]
  feature=item[1]
  val=item[2][0]
  item1=["","",""]

  while item1[1] != 'Leaf':

    if item[1]=='cbwd':
      print("JJJ")
      if test[features_dict1.get(feature)] in val[0]:
        for item1 in DT1:
          if item1[0]==level+1:
            level=item1[0]
            feature=item1[1]
            val=item1[2][0]
            break

      else:
        if test[features_dict1.get(feature)]  in val[1]:
          i=0 
          j=0
          for item1 in DT1:
            j=j+1
            if item1[0]==level+1 and i==0:
              i=i+1
            else: 
              if item1[0]==level+1 and i==1:
                DT1=DT1[j:len(DT1)]
                level=item1[0]
                feature=item1[1]
                val=item1[2][0]
                break







    ###################################################
    else:
      if test[features_dict1.get(feature)] < val:
        for item1 in DT1:
          if item1[0]==level+1:
            level=item1[0]
            feature=item1[1]
            val=item1[2][0]
            break

      else:
        if test[features_dict1.get(feature)]>= val:
          i=0 
          j=0
          for item1 in DT1:
            j=j+1
            if item1[0]==level+1 and i==0:
              i=i+1
            else: 
              if item1[0]==level+1 and i==1:
                DT1=DT1[j:len(DT1)]
                level=item1[0]
                feature=item1[1]
                val=item1[2][0]
                break
  return(item1[2][0])

##Cell 14 ###
##This function calculate the MSE (Mean squared error) ###
def accuracy(decision_tree):

  ct=0
  RES=[]
  for test in Test_Data:

    res=funct1(test,decision_tree[0],decision_tree)
    RES.append(res)
    act=test[1]
    ct=ct+((res-act)**2)
    
  return(ct/len(Test_Data)),RES

##Cell 15 ##
###This funct calculates MEan and Std Deviation###
def Mean_SD(decision_tree):
  ct=0
  Error=[]
  SD=0
  for test in Test_Data:

    res=funct1(test,decision_tree[0],decision_tree)
    Error.append(res)
    act=test[1]
    ct=ct+((res-act))
  
  MAE=(ct/len(Test_Data))
  for err in Error:
    SD=SD+((err-MAE)**2)

  SD=math.sqrt(SD/len(Error))
  return MAE,SD

##Cell 16 ##

def accuracy_bag(DTR):

  ct=[]
  for test in Test_Data:
    #print(DTR[0])
    res=funct1(test,DTR[0],DTR)
    act=test[1]
    ct.append(res)
  return ct

##Cell 17 ##


def make_bag(k):
  prediction=[]
  MSE=0
  MAE=0
  SD=0
  Range=list(range(0,len(Train_Data)))
  print(Range)
  for j in range(0,k):
    indices=np.random.choice(Range,len(Train_Data),replace=True)
    print(indices)
    sample=[]
    for i in indices:
      sample.append(Train_Data[i])
    sample=np.array(sample)
    Decision_tuple=[]
    DD= DT(Decision_tuple,sample,[0,1,2,3,5,6,7,8,9,10,11],0) 
    DTR=smooth_ds(DD)
    acc=accuracy_bag(DTR)
    prediction.append(acc)
  
  
  for k in range(0,len(Test_Data)) :
    Result=[]
    for kk in range(0,len(prediction)):
      Result.append(prediction[kk][k])
    #mode=(Counter(Result))
    #tup=((mode.most_common()))
    mean=statistics.mean(Result)
    actual=Test_Data[k][1]

    print("actual value: ",actual,"Result by each classifier: ",Result,"Mean value given by bag:",mean)
    MSE=MSE+((mean -actual)**2)
    MAE=MAE+(mean -actual)
  MSE=MSE/len(Test_Data)
  MAE=MAE/len(Test_Data)
  print("Mean Square error",MSE)  
  print("Mean absolute error",MAE)

###Cell 18###
k=int(input("enter number of decision trees to make bag"))
make_bag(k)

###Cell 19##
#### Random forest code ####


def make_forest(k):
  prediction=[]
  ct=0
  MSE=0
  MAE=0
  Range=list(range(0,len(Train_Data)))
  print(Range)
  for j in range(0,k):
    indices=np.random.choice(Range,len(Train_Data),replace=True)
    print(indices)
    sample=[]
    for i in indices:
      sample.append(Train_Data[i])
    sample=np.array(sample)
    Decision_tuple=[]
    dim_num=int(math.sqrt(len([0,1,2,3,5,6,7,8,9,10,11])))
    dim=np.random.choice([0,1,2,3,5,6,7,8,9,10,11],dim_num,replace=False)
    print("dim",dim)
    DD= DT(Decision_tuple,sample,list(dim),0) 
    DTR=smooth_ds(DD)
    acc=accuracy_bag(DTR)
    prediction.append(acc)
  
  
  for k in range(0,len(Test_Data)) :
    Result=[]
    for kk in range(0,len(prediction)):
      Result.append(prediction[kk][k])
    mean=statistics.mean(Result)
    actual=Test_Data[k][1]

    print("actual value: ",actual,"Result by each classifier: ",Result,"Mean value given by bag:",mean)
    MSE=MSE+((mean -actual)**2)
    MAE=MAE+(mean -actual)
  MSE=MSE/len(Test_Data)
  MAE=MAE/len(Test_Data)
  print("Mean Square error",MSE)  
  print("Mean absolute error",MAE)

##Cell 20###
#### Calll this function to create Forest of Decion trees , predict output, calculate MSE , MAE and STD Deviation ##4
## 
k=int(input("enter number of decision trees to make bag"))
make_forest(k)
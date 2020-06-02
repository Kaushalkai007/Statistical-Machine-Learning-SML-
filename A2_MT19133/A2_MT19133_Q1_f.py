# -*- coding: utf-8 -*-
"""f.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1b7oUB8E6-LODnS6RXiBOZAQq8ryg2LgZ
"""

import struct as st
import numpy as np               
                  
MNIST = {'MY_IMGS':'train-images.idx3-ubyte'}
train_imagesfile = open(MNIST['MY_IMGS'],'rb')
train_imagesfile.seek(0)
magic = st.unpack('>4B',train_imagesfile.read(4))
number_of_images,number_of_rows,number_of_columns=st.unpack('>III',train_imagesfile.read(12))
temp=np.asarray(st.unpack('>'+(number_of_images*number_of_rows*number_of_columns)*'B',train_imagesfile.read(number_of_images*number_of_rows*number_of_columns)))
images_array=temp.reshape(number_of_images,number_of_rows,number_of_columns)

print(images_array)

import numpy as np

R=[]
for img in images_array:
  temp=np.array(img.flatten())
  R.append(temp)

#flattend image array
R=np.array(R)

import numpy as np

R=[]
for img in images_array:
  temp2=np.array(img.flatten())
  R.append(temp2)

#flattend image array
R=np.array(R)

##Library function of Standard Scalar

from sklearn.preprocessing import StandardScaler
scaler = StandardScaler()
scaler.fit(R)

std_data=(scaler.transform(R))

y=(std_data[0].reshape(28,28))
import matplotlib.pyplot as plt
plt.imshow(y[:,:], cmap='gray')
plt.show()

from scipy.linalg import eigh
import pandas as pd
covariance_matrix=np.cov(R.T)

##For P dimensional reduction####
values, vectors = eigh(covariance_matrix)
values=np.flipud(values)
#vectors=np.flipud(vectors)

vectors=vectors.T
vectors=np.flipud(vectors)

eigen_energy=input("Enter eigen energy value in fraction")
eigen_energy=float(eigen_energy)
N=0
for i in range(0,784):
  N=N+values[i]
frac=0
p=0
for i in range(0,784):
  frac=frac+(values[i]/N)
  if frac > eigen_energy:
    p=i
    break

print(p)

vect_upd=[]
for i in range(0,p):
  vect_upd.append(vectors[i])
  
vect_upd=np.array(vect_upd)

#projected_X = np.matmul(vect_upd,std_data.T)


#projected_X=projected_X.T
print(len(vect_upd[0]))
print(len(vect_upd))

#vect_upd=vect_upd.T
import matplotlib.pyplot as plt

for i in range(0,8):
  y=(vect_upd[i].reshape(28,28))
  plt.imshow(y[:,:], cmap='gray')
  plt.show()
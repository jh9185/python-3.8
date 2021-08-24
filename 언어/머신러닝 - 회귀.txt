import tensorflow as tf
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

파일경로 = 'D:\KJH\장비백업\A3961\Table0_SendMMIData.csv'
얼라인 = pd.read_csv(파일경로)
print(얼라인.columns)
얼라인.head()

독립 = 얼라인[['X', 'Y']]
종속 = 얼라인[['T']]

print(독립.shape, 종속.shape)

# 모델의 구조 만들기
X = tf.keras.layers.Input(shape=[2]) # 독립 변수의 개수: 2 (X, Y)
Y = tf.keras.layers.Dense(1)(X) # 종속 변수의 개수: 1 (T)
model = tf.keras.models.Model(X,Y)
model.compile(loss='mse')


# 모델을 학습시키기
model.fit(독립, 종속, epochs=1000, verbose=1)
model.fit(독립, 종속, epochs=10)

#print(model.predict(독립[0:5]))
print(model.predict(독립[:-1]))


w,b = model.get_weights()

print(w, b) # Y = W1X1 + W2X2 + B

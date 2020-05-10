# -*- coding: utf-8 -*-
"""simple_NN.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1aKjr8dFMyfdY_6fTFPmiTxlqiZEoaut9
"""

import os
####*注意start*: その一行をtensorflowインポートする前に置く
os.environ['PYTHONHASHSEED']=str(1)
####*注意end*

# for irisデータ
from sklearn import datasets
from sklearn.model_selection import train_test_split

# for ニューラルネットワーク
from tensorflow.keras.models import Sequential, load_model
from tensorflow.keras.layers import Dense
from tensorflow.keras.callbacks import EarlyStopping, ModelCheckpoint

import tensorflow as tf
import numpy as np
import random
print("tensorflowのバージョン：", tf.__version__)

def reset_random_seeds():
   os.environ['PYTHONHASHSEED']=str(1)
   tf.random.set_seed(1)
   np.random.seed(1)
   random.seed(1)

reset_random_seeds()

# irisデータをロード
iris = datasets.load_iris()
X = iris.data
y = iris.target

# trainデータとvalidationデータ、testデータを作成
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3,
                                                    random_state=0,
                                                    stratify=y)
X_train, X_val, y_train, y_val = train_test_split(X_train, y_train,
                                                  test_size=0.1,random_state=1,
                                                  stratify=y_train)
print("X_train:", X_train)
print("y_train:", X_train)
print("X_test:", X_test)
print("y_test:", y_test)

# ニューラルネットワークを作成
# 定数
input_size = 4
hidden_size = 10
output_size = 3 # 3種類
batch_size = 32
epoch_size = 100
save_path = 'simple_NN_model.hdf5'

input_size = 4 # 4個の特徴量
hidden_size = 10
output_size = 3 # 3種類のアヤメ

batch_size = 32
epoch_size = 500
save_path = 'simple_NN_model.hdf5'

model = Sequential()
model.add(Dense(hidden_size, activation='relu', input_dim=input_size))
model.add(Dense(output_size, activation='softmax'))

# 訓練の継続条件：
# ①何epoch(patience)訓練しても、モデルの精度が上がらなければ訓練を終了
earlyStop = EarlyStopping(monitor='val_accuracy', verbose=1, patience=64)
# ②モデル保存の条件
# 一番精度が良いcheckpointを保存
saveBestModel = ModelCheckpoint(filepath=save_path, monitor='val_loss',
                                verbose=1, save_best_only=True)

model.compile(loss='sparse_categorical_crossentropy',
              optimizer='adam',
              metrics=['accuracy'])

history = model.fit(X_train, y_train, epochs=epoch_size, batch_size=batch_size,
            validation_data=(X_val,y_val), callbacks=[earlyStop, saveBestModel])

# 予測

# 一番良いモデルをロード
model = load_model(save_path)

y_pred = np.argmax(model.predict(X_test),axis=1)
print(y_pred)
print(y_test)

# テストデータのロスと正解率
model.evaluate(X_test, y_test)
'''Trains a simple convnet on the MNIST dataset.
Gets to 99.25% test accuracy after 12 epochs
(there is still a lot of margin for parameter tuning).
16 seconds per epoch on a GRID K520 GPU.
'''
#-- From Tensorfolw 2.0, keras.somthings --> tensorflow.keras.somethings

from __future__ import print_function

import tensorflow as tf
import tensorflow.keras
from tensorflow.keras.datasets import mnist
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Dropout, Flatten
from tensorflow.keras.layers import Conv2D, MaxPooling2D
from tensorflow.keras import backend as K
#from tensorflow.keras.utils import np_utils
import matplotlib.pyplot as plt
from PIL import Image
import numpy as np
import os

print("Tensorflow version :",tf.__version__)

batch_size = 128
num_classes = 10
epochs = 50

# input image dimensions
img_rows, img_cols = 28, 28

# the data, split between train and test sets
(x_train, y_train), (x_test, y_test) = mnist.load_data()

if K.image_data_format() == 'channels_first':
    x_train = x_train.reshape(x_train.shape[0], 1, img_rows, img_cols)
    x_test = x_test.reshape(x_test.shape[0], 1, img_rows, img_cols)
    input_shape = (1, img_rows, img_cols)
else:
    x_train = x_train.reshape(x_train.shape[0], img_rows, img_cols, 1)
    x_test = x_test.reshape(x_test.shape[0], img_rows, img_cols, 1)
    input_shape = (img_rows, img_cols, 1)

x_train = x_train.astype('float32')
x_test = x_test.astype('float32')
x_train /= 255
x_test /= 255
print('x_train shape:', x_train.shape)
print(x_train.shape[0], 'train samples')
print(x_test.shape[0], 'test samples')

# convert class vectors to binary class matrices
y_train = tensorflow.keras.utils.to_categorical(y_train, num_classes)
y_test = tensorflow.keras.utils.to_categorical(y_test, num_classes)

model = Sequential()
model.add(Conv2D(32, kernel_size=(5, 5),
                 activation='relu',
                 input_shape=input_shape))
model.add(MaxPooling2D(pool_size=(2, 2)))
model.add(Conv2D(64, (5, 5), activation='relu'))
model.add(MaxPooling2D(pool_size=(2, 2)))
model.add(Dropout(0.25))
model.add(Flatten())
model.add(Dense(1024, activation='relu'))
model.add(Dropout(0.5))
model.add(Dense(num_classes, activation='softmax'))

model.compile(loss=tensorflow.keras.losses.categorical_crossentropy,
              optimizer=tensorflow.keras.optimizers.Adadelta(),
              metrics=['accuracy'])

history=model.fit(x_train, y_train,
          batch_size=batch_size,
          epochs=epochs,
          verbose=1,
          validation_data=(x_test, y_test))
score = model.evaluate(x_test, y_test, verbose=0)
print('Test loss:', score[0])
print('Test accuracy:', score[1])

#history_dict = history.history
#print(history_dict.keys())

##-- summarize history for accuracy
plt.plot(history.history['accuracy'])
plt.plot(history.history['val_accuracy'])
plt.title('model accuracy')
plt.ylabel('accuracy')
plt.xlabel('epoch')
plt.legend(['train', 'test'], loc='upper left')
plt.show()

##-- Model Test using Test datasets 
print()
print("----Actual test for digits----")

mnist_label_file_path =  "dataset_test/testlabels/t_labels.txt"
mnist_label = open(mnist_label_file_path, "r")
cnt_correct = 0
for index in range(10):
	#-- read a label
	label = mnist_label.readline()
	print(label)
	#-- predict the input image (digit)
	img = Image.open('dataset_test/testimgs/' + str(index+1) + '.png').convert("L")
	img = img.resize((28,28))
	im2arr = np.array(img)
	im2arr = im2arr.reshape(1,28,28,1)
	
	# Predicting the Test set results
	#y_pred = model.predict(im2arr)		#<-- [0,0 .....1. 0.]
	#y_pred = model.predict_classes(im2arr)	#<-- 7 or 4
	predict_x= model.predict(im2arr)
	y_pred = np.argmax(predict_x)
    
	print(y_pred)

	#-- compute the accuracy of the preditcion
	if int(label)==y_pred:
		cnt_correct += 1

#-- Final accuracy
Final_acc = cnt_correct/10
print()
print("Final test accuray: %f" %Final_acc)



    

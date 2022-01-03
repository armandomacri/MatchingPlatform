import os
import tensorflow as tf
from tensorflow import keras
import tensorflow_datasets as tfds
import numpy as np
from matplotlib import pyplot as plt
import os
from tensorflow.keras import layers
from keras import models

# try to load the model
from tensorflow.keras.models import load_model

train_data, train_label = tfds.as_numpy(tfds.load(
    'ag_news_subset',
    split='train',
    batch_size=-1,  # return the full dataset
    as_supervised=True, # return object and label
))

dir_name ="word_ebedding_model"
if not os.path.exists(dir_name):
  os.makedirs(dir_name)


network = load_model(os.path.join(dir_name, 'model.h5'))

Xnew = []
Xnew.append("Chelsea is a great team")
Xnew.append("In war, you can only be killed once, but in politics, many times")
Xnew.append("my smartphone isn't very smart question answer")
Xnew.append("according to you who seems to be dumb the phone on the speaker why")
prova = vectorizer(np.array([[s] for s in Xnew])).numpy()
ynew = nwtwork.predict(prova)

print(ynew)
for i in range(0, len(ynew)):
  print(topic(list(ynew[i]).index(max(ynew[i]))))
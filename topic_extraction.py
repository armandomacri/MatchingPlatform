import os
import tensorflow as tf
from tensorflow import keras
import tensorflow_datasets as tfds
import numpy as np
from matplotlib import pyplot as plt
import os
from tensorflow.keras import layers
from keras import models
from tensorflow.keras.layers.experimental.preprocessing import TextVectorization
# try to load the model
from tensorflow.keras.models import load_model
import pickle
import en_core_web_md


def topic(index):
    if index==0:
        return "World"
    if index==1:
        return "Sport"
    if index==2:
        return "Business"
    if index==3:
        return "Science/Tech"

if __name__ == "__main__":

    MAX_WORDS = 10000
    MAX_LENGTH = 100

    """
    train_data, train_label = tfds.as_numpy(tfds.load(
        'ag_news_subset',
        split='train',
        batch_size=-1,  # return the full dataset
        as_supervised=True, # return object and label
    ))

    # Shuffle the data
    seed = 123
    rng = np.random.RandomState(seed)
    rng.shuffle(train_data)
    rng = np.random.RandomState(seed)
    rng.shuffle(train_label)

    # Extract a training and a validation split
    validation_split = 0.2
    num_validation_samples = int(validation_split * len(train_data))
    text_val = train_data[-num_validation_samples:]
    tmp_text_train = train_data[:-num_validation_samples]
    label_val = train_label[-num_validation_samples:]
    tmp_label_train = train_label[:-num_validation_samples]

    print(tmp_label_train[:50]) # check

    NUM_EXAMPLE = 500
    text_train = tmp_text_train[:NUM_EXAMPLE]
    label_train = tmp_label_train[:NUM_EXAMPLE]

    unique, counts = np.unique(label_train, return_counts=True)
    plt.pie(counts, labels = unique, startangle = 90)
    plt.title('Label Distribution')
    plt.show()
    NUM_CLASSES = len(unique)

    vectorizer = TextVectorization(max_tokens=MAX_WORDS,
                                   output_mode = 'int', # set different output encoding
                                   standardize='lower_and_strip_punctuation',
                                   split="whitespace",
                                   ngrams=None,
                                   output_sequence_length=MAX_LENGTH, # set max length
                                   pad_to_max_tokens=True,)
    vectorizer.adapt(text_train)

    num_tokens = len(vectorizer.get_vocabulary())
    num_tokens

    pickle.dump({'config': vectorizer.get_config(),
                 'weights': vectorizer.get_weights()}
                , open("vectorizer.pkl", "wb")) 
    
    """
 
    from_disk = pickle.load(open("vectorizer.pkl", "rb"))
    vectorizer = TextVectorization(max_tokens=from_disk['config']['max_tokens'],
                                       output_mode='int',
                                       output_sequence_length=from_disk['config']['output_sequence_length'])
    # You have to call `adapt` with some dummy data (BUG in Keras)
    vectorizer.adapt(tf.data.Dataset.from_tensor_slices(["xyz"]))
    vectorizer.set_weights(from_disk['weights'])

    dir_name = "word_embedding_model"
    if not os.path.exists(dir_name):
      os.makedirs(dir_name)

    nlp = en_core_web_md.load()
    network = load_model(os.path.join(dir_name, 'model.h5'))

    Xnew = []
    Xnew.append("Chelsea is a great team")
    Xnew.append("In war, you can only be killed once, but in politics, many times")
    Xnew.append("my smartphone isn't very smart question answer")
    Xnew.append("according to you who seems to be dumb the phone on the speaker why")
    prova = vectorizer(np.array([[s] for s in Xnew])).numpy()
    print(prova.shape)
    ynew = network.predict(prova)

    print(ynew)
    for i in range(0, len(ynew)):
        print(topic(list(ynew[i]).index(max(ynew[i]))))
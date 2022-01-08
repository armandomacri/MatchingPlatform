import os
import numpy as np
from tensorflow.keras.layers.experimental.preprocessing import TextVectorization
from tensorflow.keras.models import load_model
import tensorflow as tf
import pickle

topics = ["world", "sport", "business", "science/tech"]

class TopicExtractor:
    dir_name = "word_embedding_model"

    def __init__(self):
        if not os.path.exists(self.dir_name):
            os.makedirs(self.dir_name)

        self.network = load_model(os.path.join(self.dir_name, 'model.h5'))

        from_disk = pickle.load(open(os.path.join(self.dir_name, 'vectorizer.pkl'), "rb"))
        self.vectorizer = TextVectorization(max_tokens=from_disk['config']['max_tokens'],
                                       output_mode='int',
                                       output_sequence_length=from_disk['config']['output_sequence_length'])
        # You have to call `adapt` with some dummy data (BUG in Keras)
        self.vectorizer.adapt(tf.data.Dataset.from_tensor_slices(["xyz"]))
        self.vectorizer.set_weights(from_disk['weights'])

    def get_topic(self, str):
        v = self.vectorizer(np.array([str])).numpy()
        p = self.network.predict(v)
        return topics[np.argmax(p)], max(p[0])

import os
import numpy as np
from tensorflow.keras.layers.experimental.preprocessing import TextVectorization
from tensorflow.keras.models import load_model
import tensorflow as tf
import pickle
import xmlrpc.client
import time
import http.client


class TimeoutTransport(xmlrpc.client.Transport):
    timeout = 30.0

    def set_timeout(self, timeout):
        self.timeout = timeout

    def make_connection(self, host):
        h = http.client.HTTPConnection(host, timeout=self.timeout)
        return h


topics = ["world", "sport", "business", "science/tech"]


class TopicExtractor:
    dir_name = "word_embedding_model"

    def __init__(self):

        if not os.path.exists(self.dir_name):
            os.makedirs(self.dir_name)
        # self.classifier = pipeline('zero-shot-classification', model='facebook/bart-large-mnli')
        self.hypothesis_template = 'This text is about {}.'

    def load_local_model(self):
        self.network = load_model(os.path.join(self.dir_name, 'model.h5'))
        from_disk = pickle.load(open(os.path.join(self.dir_name, 'vectorizer.pkl'), "rb"))
        self.vectorizer = TextVectorization(max_tokens=from_disk['config']['max_tokens'],
                                            output_mode='int',
                                            output_sequence_length=from_disk['config']['output_sequence_length'])
        # You have to call `adapt` with some dummy data (BUG in Keras)
        self.vectorizer.adapt(tf.data.Dataset.from_tensor_slices(["xyz"]))
        # self.vectorizer.weights[0]=from_disk['weights'][0]
        self.vectorizer.set_weights([from_disk['weights'][0]])

    def get_topic_local(self, stringa):
        self.load_local_model()
        arrival_time = time.time()
        v = self.vectorizer(np.array([stringa])).numpy()
        p = self.network.predict(v)
        end_time = time.time()
        exec_time = end_time - arrival_time
        print("-----------------------")
        print("Time: " + str(exec_time))
        print("-----------------------")
        return topics[np.argmax(p)], max(p[0])

    def get_topic(self, str):
        try:
            t = TimeoutTransport()
            t.set_timeout(40.0)
            s = xmlrpc.client.ServerProxy('http://localhost:9000', transport=t)
            # s = xmlrpc.client.ServerProxy('http://LAPTOP-E04M55SK:9000', transport=t)
            arrival_time = time.time()
            topic, score = s.get_topic(str)
            end_time = time.time()
            print("Extract topic time")
            print(end_time - arrival_time)
            print(topic)
            print(score)
        except xmlrpc.client.Fault as timeout_expired:
            #print(type(timeout_epired))  # the exception instance
            print(timeout_expired)
            print("Timeout expired!")
            topic, score = self.get_topic_local(str)
        except:
            print("Remote server not reachable")
            topic, score = self.get_topic_local(str)

        return topic, score


if __name__ == '__main__':
    t = TopicExtractor()
    t.get_topic("ciao")
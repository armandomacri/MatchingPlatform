
from topic_extractor import TopicExtractor



if __name__ == '__main__':
    t = TopicExtractor()
    result = t.get_topic("Chelsea is a great team")

    print(result)

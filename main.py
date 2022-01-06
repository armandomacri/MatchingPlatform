
from topic_extractor import TopicExtractor
from transcriber import Transcriber
from audio_retrieval import AudioRetriever

if __name__ == '__main__':

    retriever = AudioRetriever()
    audio = retriever.retrieve()

    transcriber = Transcriber()
    transcription = transcriber.transcriptWav("file.wav")

    topic_ext = TopicExtractor()
    result = topic_ext.get_topic(transcription)

    print(result)

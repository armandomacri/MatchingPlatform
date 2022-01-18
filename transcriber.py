import speech_recognition as sr
from deep_translator import GoogleTranslator

class Transcriber:

    def __init__(self):
        self.r = sr.Recognizer()

    def transcriptWav(self, filename, language=False):
        with sr.AudioFile(filename) as source:
            try:
                # calibrates the recognizer to the noise level of the audio
                self.r.adjust_for_ambient_noise(source, 1)
                # listen for the data (load audio to memory)
                audio_data = self.r.record(source)
                # recognize (convert from speech to text)
                if language == False:
                        text = self.r.recognize_google(audio_data, language="en-EN")
                        print(text)
                        return text
                else:
                        text = self.r.recognize_google(audio_data, language="it-IT")
                        print(text)
                        translated = GoogleTranslator(source='it',target='en').translate(text)
                        print(translated)
                        return translated
            except:
                print("Error ! \t" + filename.split('/')[3])

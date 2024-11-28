import pyttsx3
import pyaudio
import datetime
import locale
import speech_recognition as sr
import spacy
import pt_core_news_sm

locale.setlocale(locale.LC_TIME, 'pt_BR.UTF-8')
nlp = spacy.load("pt_core_news_sm")

class Voice:
    def __init__(self):
        self.engine = pyttsx3.init()

    def speak(self, audio):
        self.engine.setProperty('rate', 170)
        voices = self.engine.getProperty('voices')
        self.engine.setProperty('voice', voices[1].id)
        self.engine.say(audio)
        self.engine.runAndWait()

    def microphone(self):
        r = sr.Recognizer()
        with sr.Microphone() as source:
            r.pause_threshold = 1
            audio = r.listen(source)

        try:
            print('Reconhecendo...')
            command = r.recognize_google(audio, language='pt-br')
            print("Comando recebido:", command)
            return command.lower()
        except Exception as e:
            print("Erro:", e)
            self.speak("Por favor, repita!")
            return None
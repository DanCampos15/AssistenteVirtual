import datetime
import spacy

class Intent:
    def __init__(self):
        self.nlp = spacy.load("pt_core_news_sm")

    def detect_intent(self, command):
        doc = self.nlp(command)
        intents = {
            "horas": ["hora", "horas", "tempo"],
            "data": ["data", "hoje", "dia"],
            "cumprimento": ["olá", "oi", "saudações", "alô"],
            "desligar": ["desligar", "sair", "fechar", "encerrar"],
            "clima": ["clima", "tempo", "previsão"]
        }

        for intent, keywords in intents.items():
            if any(token.lemma_ in keywords for token in doc):
                return intent
        return "desconhecido"
class Command:
    def __init__(self, voice):
        self.voice = voice
        
    def time(self):
        current_time = datetime.datetime.now().strftime('%I:%M')
        self.voice.speak('São exatamente ' + current_time)

    def date(self):
        year = int(datetime.datetime.now().year)
        month = datetime.datetime.now().strftime('%B')
        day = int(datetime.datetime.now().day)
        self.voice.speak("A data atual é: " + str(day) + " de " + str(month) + " de " + str(year))

    def greet(self):
        self.voice.speak("Olá! Como posso ajudar?")

    def shutdown(self):
        self.voice.speak("Encerrando o sistema. Até logo!")
        exit()

    def weather(self):
        self.voice.speak("A previsão do tempo de hoje é ensolarada, com temperatura máxima de 25 graus e mínima de 18 graus.")

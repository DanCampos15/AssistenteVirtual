import datetime
from voice import Voice
from intent import Intent, Command

class AssistenteVirtual:
    def __init__(self):
        self.voice = Voice()
        self.intent_detector = Intent()
        self.commands = Command(self.voice)
        
    def welcome_message(self):
        hour = datetime.datetime.now().hour
        greeting = 'Bom dia' if hour < 12 else 'Boa tarde' if hour < 18 else 'Boa noite'
        self.voice.speak("Olá mestre," + greeting + ", seja bem-vindo")
        self.voice.speak('Éllo a sua disposição, como posso ajudá-lo?')

    def run(self):
        self.welcome_message()
        while True:
            print("Escutando...")
            command = self.voice.microphone()
            if command:
                self.execute_command(command)

    def execute_command(self, command):
        intent = self.intent_detector.detect_intent(command)
        action = self.intent_actions.get(intent)
        if action:
            action()
        else:
            self.voice.speak("Desculpe, não entendi o comando.")

    @property
    def intent_actions(self):
        return {
            "horas": self.commands.time,
            "data": self.commands.date,
            "cumprimento": self.commands.greet,
            "desligar": self.commands.shutdown,
            "clima": self.commands.weather
        }



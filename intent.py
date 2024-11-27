import datetime
import spacy
import serial

class Intent:
    def __init__(self):
        self.nlp = spacy.load("pt_core_news_sm")

    def detect_intent(self, command):
        """Detecta a intenção do comando baseado em palavras-chave e contexto."""
        
        # Define as intenções e palavras-chave
        intents = {
            "horas": ["que horas são", "hora", "horas", "tempo"],
            "data": ["data", "qual a data de hoje", "hoje é que dia", "dia de hoje"],
            "cumprimento": ["olá", "oi", "bom dia", "boa tarde", "saudações"],
            "desligar": ["desligar", "sair", "fechar sistema", "encerrar"],
            "clima": ["qual a previsão do tempo", "clima", "tempo", "como está o tempo"],
            "ligar_luz_sala": ["ligar luz sala", "acender luz sala", "acender a luz da sala", "ligar a luz da sala"],
            "desligar_luz_sala": ["desligar luz sala", "apagar luz sala", "apagar a luz da sala", "desligar a luz da sala"],
            "ligar_luz_quarto": ["ligar luz quarto", "acender luz quarto", "ligar a luz do quarto", "acender a luz do quarto"],
            "desligar_luz_quarto": ["desligar luz quarto", "apagar luz quarto", "apagar a luz do quarto", "desligar a luz do quarto"],
            "ligar_luz_cozinha": ["ligar luz cozinha", "acender luz cozinha", "ligar a luz da cozinha", "acender a luz da cozinha"],
            "desligar_luz_cozinha": ["desligar luz cozinha", "apagar luz cozinha", "apagar a luz da cozinha", "desligar a luz da cozinha"],
            "abrir_portao": ["abrir portão", "abrir portao", "abrir o portão"],
            "fechar_portao": ["fechar portão", "fechar portao", "fechar o portão"]
        }

        
        # Define as palavras-chave contextuais para cada intenção
        context_keywords = {
            "fechar_portao": ["portão", "portao"],
            "desligar": ["sistema", "computador", "encerrar"]
        }

        command_lower = command.lower()

        # Primeiro, tenta encontrar as intenções comuns
        for intent, keywords in intents.items():
            for keyword in keywords:
                if keyword in command_lower:
                    # Verifica o contexto somente para intenções ambíguas
                    if intent in context_keywords:
                        if self._check_context(command_lower, intent, context_keywords):
                            return intent
                    else:
                        return intent  # Retorna diretamente a intenção quando não há ambiguidade

        return "desconhecido"
    
    def _check_context(self, command, intent, context_keywords):
        """Verifica o contexto baseado em palavras-chave adicionais."""
        if intent in context_keywords:
            for context_word in context_keywords[intent]:
                if context_word in command:
                    return True
        return False

class Command:
    def __init__(self, voice, port='COM3', baudrate=9600):
        self.voice = voice
        try:
            self.serial_connection = serial.Serial(port, baudrate, timeout=1)
            self.voice.speak("Conexão com o Arduino estabelecida.")
        except Exception as e:
            self.voice.speak("Erro ao conectar ao Arduino.")
            print(f"Erro na inicialização da porta serial: {e}")
            self.serial_connection = None

    def _send_to_arduino(self, command):
        """Envia comandos ao Arduino e lê a resposta."""
        if self.serial_connection:
            try:
                self.serial_connection.write((command + '\n').encode())  # Envia comando
                response = self.serial_connection.readline().decode().strip()  # Lê resposta
                return response
            except Exception as e:
                print(f"Erro ao comunicar com o Arduino: {e}")
                return None
        else:
            return None

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

    # Comandos para o Arduino
    def turn_on_sala(self):
        self.voice.speak("Ligando luz da sala.")
        self._send_to_arduino("LS")

    def turn_off_sala(self):
        self.voice.speak("Desligando luz da sala.")
        self._send_to_arduino("ls")

    def turn_on_quarto(self):
        self.voice.speak("Ligando luz do quarto.")
        self._send_to_arduino("LQ")

    def turn_off_quarto(self):
        self.voice.speak("Desligando luz do quarto.")
        self._send_to_arduino("lq")

    def turn_on_cozinha(self):
        self.voice.speak("Ligando luz da cozinha.")
        self._send_to
    def turn_off_cozinha(self):
        self.voice.speak("Desligando luz da cozinha.")
        self._send_to_arduino("lc")

    def open_gate(self):
        self.voice.speak("Abrindo o portão.")
        response = self._send_to_arduino("PA")
        if response:
            self.voice.speak(response)

    def close_gate(self):
        self.voice.speak("Fechando o portão.")
        response = self._send_to_arduino("PF")
        if response:
            self.voice.speak(response)

    def shutdown(self):
        """Encerrando o sistema de forma segura."""
        self.voice.speak("Encerrando o sistema. Até logo!")
        self.listening = False  # Para o processo de escuta de voz
        if self.serial_connection:
            self.serial_connection.close()
        exit()

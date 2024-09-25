import pyttsx3
import datetime
import locale
import speech_recognition as sr

# Definir a localidade para português do Brasil
locale.setlocale(locale.LC_TIME, 'pt_BR.UTF-8')

engine = pyttsx3.init()

def speak(audio):
  rate = engine.getProperty('rate')
  engine.setProperty('rate', 170)
  voices = engine.getProperty('voices')
  engine.setProperty('voice', voices[2].id) #Alteração de Voz
  engine.say(audio)
  engine.runAndWait()

def time():
   Time = datetime.datetime.now().strftime('%I:%M')
   speak('São exatamente,' + Time)

def date():
   Year = int(datetime.datetime.now().year)
   Month = datetime.datetime.now().strftime('%B')
   Day = int(datetime.datetime.now().day)
   speak("A data atual é: " + str(Day) + " de " + str(Month) + " de " + str(Year))

def welcome_message():
   speak('Olá mestre, seja bem vindo')
   time()
   date()

   Hour = datetime.datetime.now().hour

   if Hour >= 0 and Hour < 12:
    speak('Bom dia')
   elif Hour >= 12 and Hour < 18:
    speak('Boa tarde')
   else:
    speak('Boa noite')
   
   speak('Éllo a sua disposição, como posso ajudá-lo ?')

welcome_message()
def microphone():
  r = sr.Recognizer()

  with sr.Microphone() as source:
      r.pause_threshold = 1
      audio = r.listen(source)
  
  try:
      print('Reconhecendo...')
      command = r.recognize_google(audio, language='pt-br')
      print(command)
  
  except Exception as e:
      print(e)
      speak("Por favor repita!")

      return "None"
  return command

microphone()
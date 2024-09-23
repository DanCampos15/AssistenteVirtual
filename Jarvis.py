import pyttsx3
import speech_recognition as sr

engine = pyttsx3.init()

def falar(audio):
  voices = engine.getProperty('voices')
  engine.setProperty('voice', voices[0].id) #Alteração de Voz

  engine.say("teste")
  engine.runAndWait()

falar('Olá a todos, teste')

def microfone():
  r = sr.Recognizer()

  with sr.Microphone() as source:
      r.pause_threshold = 1
      audio = r.listen(source)
  
  try:
      print('Reconhecendo...')
      comando = r.recognize_google(audio, language='pt-br')
      print(comando)
  
  except Exception as e:
      print(e)
      falar("Por favor repita!")

      return "None"
  return comando

microfone()
import pyttsx3
import speech_recognition as sr
import pyaudio

texto_fala = pyttsx3.init()

def falar(audio):
  voices = texto_fala.getProperty('voices')
  texto_fala.setProperty('voice', voices[1].id) #Alteração de Voz

  texto_fala.say(audio)
  texto_fala.runAndWait()

#falar("Olá a todos, meu nome é ricardo")

def microfone():
  r = sr.Recognizer()

  with sr.Microphone() as source:
      r.pause_treshold = 1
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
# Fazer o computador enetender o que foi digitado e reproduzir por voz. 

import pyttsx3 # pip install pyttsx3

engine = pyttsx3.init() # inicia a biblioteca

engine.say("Olá Mundo.")

engine.runAndWait()

engine.stop()

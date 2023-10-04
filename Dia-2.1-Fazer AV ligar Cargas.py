# Codigo da Assistente Virtual
import serial  # pip install pyserial
import threading # usado para processamento paralelo (execuntando dois programas ao mesmo tempo)
import time
import speech_recognition as sr  # pip install SpeechRecognition
import pyttsx3 # pip install pyttsx3

engine = pyttsx3.init()

voices = engine.getProperty('voices')
contar = 0
for vozes in voices: #Listar vozes
    print(contar, vozes.name)
    contar += 1

voz = 0
engine.setProperty('voice', voices[voz].id)    

r = sr.Recognizer()

mic = sr.Microphone()

conectado = False
porta = 'COM4' # Porta COM, selecionar a mesma do Arduino
velocidadeBaud = 9600 # Velocidade também deve ser igual ao código do Arduino

mensagensRecebidas = 1;
desligarArduinoThread = False

falarTexto = False;
textoRecebido = ""
SerialArduino = serial.Serial(porta, velocidadeBaud, timeout = 0.2) # Nessa parte ativamos a comunicação com a porta serial

engine = pyttsx3.init() # inicia a biblioteca

engine.say("Olá, eu sou sua assistente virtual. Como posso ajudar?.")

engine.runAndWait()

try:
    SerialArduino = serial.Serial(porta, velocidadeBaud, timeout = 0.2)
except:
    print("Verificar porta serial ou reiniciar arduino")

def handle_data(data): # 'def' é usado para criar uma função, que é um bloco de código para executar algo especifico
    global mensagensRecebidas, engine, falarTexto, textoRecebido
    print("Recebi " + str(mensagensRecebidas) + ": " + data)

    mensagensRecebidas += 1
    textoRecebido = data
    falarTexto = True

def read_from_port():
    global conectado, desligarArduinoThread

    while not conectado:
        conectado = True

        while True: # Laço de repetição 'while' é usado para executar o código 'enquanto' uma condição ainda é verdadeira
           reading = SerialArduino.readline().decode()
           if reading != "":  # 'if' impoe uma condição 'se'
              handle_data(reading)
           if desligarArduinoThread:
              print("Desligando Arduino")
              break

lerSerialThread = threading.Thread(target=read_from_port, args=SerialArduino)
lerSerialThread.start()

print("Preparando Arduino")
time.sleep(2)
print("Arduino Pronto")

while (True):
    if falarTexto:
       engine.say(textoRecebido)
       engine.runAndWait()
       falarTexto = False
       
    try:
       with mic as fonte:
         r.adjust_for_ambient_noise(fonte)
         print("Fale alguma coisa")
         audio = r.listen(fonte)
         print("Enviando para reconhecimento")
         try:
           text = r.recognize_google(audio, language= "pt-BR").lower()
           print("Você disse: {}". format(text))
           if text == "ligar luz da cozinha" or text == "desligar luz da cozinha":
              SerialArduino.write((text + '\n').encode())

              print("Dado enviado")
           if text == "ligar luz do quarto" or text == "desligar luz do quarto":
              SerialArduino.write((text + '\n').encode())

              print("Dado enviado")
           if text == "abrir portão da garagem" or text == "fechar portão da garagem":
              SerialArduino.write((text + '\n').encode())

              print("Dado enviado")
           if(text == "desativar"):
              print("Saindo")

              desativando = "Assistente Virtual desativando."

              engine.say(desativando)
              engine.runAndWait()

              engine.stop()
              desligarArduinoThread = True
              SerialArduino.close()
              lerSerialThread.join()
              break
         except:
           print("Não entendi o que você disse.\n")  

         time.sleep(1)
    except (KeyboardInterrupt, SystemExit):
           print("Apertou Ctrl+F2")
           engine.stop()
           desligarArduinoThread = True
           SerialArduino.close()
           lerSerialThread.join()
           break              


import serial  # pip install pyserial
import threading  # usado para processamento paralelo (executando dois programas ao mesmo tempo)
import time
import speech_recognition as sr  # pip install SpeechRecognition
import pyttsx3  # pip install pyttsx3

# Inicialização do motor de voz
engine = pyttsx3.init()

voices = engine.getProperty('voices')
contar = 0
for vozes in voices:  # Listar vozes
    print(contar, vozes.name)
    contar += 1

# Selecionar a voz
voz = 0
engine.setProperty('voice', voices[voz].id)

# Inicialização do reconhecimento de fala
r = sr.Recognizer()
mic = sr.Microphone()

# Inicialização da conexão serial
porta = 'COM3'  # Porta COM, selecionar a mesma do Arduino
velocidadeBaud = 9600  # Velocidade também deve ser igual ao código do Arduino

SerialArduino = serial.Serial(porta, velocidadeBaud, timeout=0.2)  # Ativar comunicação serial

# Função para lidar com dados recebidos do Arduino
def handle_data(data):
    global engine
    print("Recebi: " + data)
    engine.runAndWait()

# Função para ler dados da porta serial
def read_from_port():
    while True:
        reading = SerialArduino.readline().decode()
        if reading:
            handle_data(reading)

# Criar thread para ler dados da porta serial
lerSerialThread = threading.Thread(target=read_from_port)
lerSerialThread.start()

print("Preparando Arduino")
time.sleep(2)
print("Arduino Pronto")

# Função para pedir o nome do usuário e armazenar
def perguntar_nome():
    while True:  # Loop para continuar tentando até obter o nome
        engine.say("Olá! Eu sou uma Assistente Robô Virtual. Qual é o seu nome?")
        engine.runAndWait()
        with mic as fonte:
            r.adjust_for_ambient_noise(fonte)
            print("Fale seu nome")
            audio = r.listen(fonte)
            try:
                nome_usuario = r.recognize_google(audio, language="pt-BR").capitalize()
                print(f"Nome recebido: {nome_usuario}")
                return nome_usuario  # Retorna o nome quando bem-sucedido
            except:
                engine.say("Desculpe, não consegui entender o nome. Vamos tentar novamente.")
                engine.runAndWait()

# Perguntar o nome do usuário
nome_usuario = perguntar_nome()

# Função para interação de conversa
def conversar():
    engine.say(f"{nome_usuario}, você gosta de estudar?")
    engine.runAndWait()
    with mic as fonte:
        r.adjust_for_ambient_noise(fonte)
        audio = r.listen(fonte)
        try:
            resposta = r.recognize_google(audio, language="pt-BR").lower()

            if "sim" in resposta:
                engine.say("Legal, e qual sua matéria favorita?")
                engine.runAndWait()
                audio = r.listen(fonte)
                materia_favorita = r.recognize_google(audio, language="pt-BR")
                engine.say(f"Eu também gosto de {materia_favorita}.")
            else:
                engine.say("Que pena, estudar é muito importante.")
            engine.runAndWait()

        except:
            engine.say("Não entendi sua resposta.")
            engine.runAndWait()

# Função para perguntar o próximo passo
def proximo_passo():
    engine.say(f"{nome_usuario}, você quer conversar, dar comandos ou desativar?")
    engine.runAndWait()
    with mic as fonte:
        r.adjust_for_ambient_noise(fonte)
        audio = r.listen(fonte)
        try:
            escolha = r.recognize_google(audio, language="pt-BR").lower()
            return escolha
        except:
            engine.say("Não entendi sua resposta.")
            engine.runAndWait()
            return proximo_passo()

# Função para encerrar o assistente
def encerrar_assistente():
    engine.say(f"Foi bom interagir com você, {nome_usuario}!")
    engine.say("Assistente Robô Virtual desativando.")
    engine.runAndWait()
    SerialArduino.close()
    lerSerialThread.join()
    engine.stop()
    print("Encerrando...")
    exit()

# Loop principal para interações
while True:
    escolha = proximo_passo()

    if "comandos" in escolha:
        # Loop para comandos
        while True:
            with mic as fonte:
                r.adjust_for_ambient_noise(fonte)
                engine.say(f"Diga um comando {nome_usuario}.")
                engine.runAndWait()
                print("Fale um comando")
                audio = r.listen(fonte)
                print("Enviando para reconhecimento")

                try:
                    text = r.recognize_google(audio, language="pt-BR").lower()
                    print("Você disse: {}".format(text))

                    # Comandos de voz para controlar o braço robótico
                    if text in ["mover base direita", "mover base esquerda",
                                "mover ombro para cima", "mover ombro para baixo",
                                "mover cotovelo para cima", "mover cotovelo para baixo",
                                "abrir garra", "fechar garra"]:
                        SerialArduino.write((text + '\n').encode())
                        engine.say(f"Claro {nome_usuario}, {text}.")
                        engine.runAndWait()
                        print("Comando enviado ao Arduino: {}".format(text))

                    # Comando para desativar a assistente
                    elif text == "desativar":
                        encerrar_assistente()

                except:
                    engine.say("Não entendi o que você disse.")
                    engine.runAndWait()

                time.sleep(1)
            
            # Após executar um comando, pergunta novamente se quer continuar ou encerrar
            escolha = proximo_passo()
            if "desativar" in escolha:
                encerrar_assistente()

    elif "conversar" in escolha:
        # Executa o modo de conversa
        conversar()

    elif "desativar" in escolha:
        encerrar_assistente()

    else:
        engine.say("Opção não reconhecida. Tente novamente.")
        engine.runAndWait()

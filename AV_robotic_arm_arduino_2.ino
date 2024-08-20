#include <Servo.h>

String inputString = ""; // Uma string para armazenar dados de entrada
bool stringComplete = false; // Para caso a string esteja completa.

Servo servoBase;     // Servo que controla a base (direita/esquerda)
Servo servoOmbro;    // Servo que controla o ombro (para cima/baixo)
Servo servoCotovelo; // Servo que controla o cotovelo (para cima/baixo)
Servo servoGarra;    // Servo que controla a garra (abrir/fechar)

// Defina os pinos onde os servos estão conectados
#define pinoServoBase 8
#define pinoServoOmbro 9
#define pinoServoCotovelo 10
#define pinoServoGarra 11

// Posições iniciais e limites dos servos
int posBaseInicial = 90;
int posBaseEsquerda = 30;
int posBaseDireita = 160;

int posOmbroInicial = 90;
int posOmbroBaixo = 60;
int posOmbroCima = 120;

int posCotoveloInicial = 60;
int posCotoveloBaixo = 100;
int posCotoveloCima = 30;

int posGarraInicial = 90;
int posGarraFechada = 120;
int posGarraAberta = 20;

// Posições variáveis dos servos
int posBase = posBaseInicial;
int posOmbro = posOmbroInicial;
int posCotovelo = posCotoveloInicial;
int posGarra = posGarraInicial;

// Tempo de espera antes de retornar à posição inicial (em milissegundos)
unsigned long tempoEspera = 3000; // 3 segundos
unsigned long tempoMovimento = 0;
bool moverParaPosInicial = false;

// Função para mover o servo suavemente para uma posição desejada
void moverServoSuavemente(Servo& servo, int& posAtual, int posFinal) {
  if (posAtual < posFinal) {
    for (int i = posAtual; i <= posFinal; i++) {
      servo.write(i);
      delay(20);  // Ajuste o valor do delay para controlar a velocidade
    }
  } else {
    for (int i = posAtual; i >= posFinal; i--) {
      servo.write(i);
      delay(20);  // Ajuste o valor do delay para controlar a velocidade
    }
  }
  posAtual = posFinal;  // Atualiza a posição atual
}

void setup() {
  // Inicia a porta serial
  Serial.begin(9600);
  // Reserva 200 bytes para a entrada da string
  inputString.reserve(200);

  // Anexando os servos aos seus respectivos pinos
  servoBase.attach(pinoServoBase);
  servoOmbro.attach(pinoServoOmbro);
  servoCotovelo.attach(pinoServoCotovelo);
  servoGarra.attach(pinoServoGarra);
  
  // Definindo a posição inicial dos servos
  servoBase.write(posBaseInicial);
  servoOmbro.write(posOmbroInicial);
  servoCotovelo.write(posCotoveloInicial);
  servoGarra.write(posGarraInicial);

  Serial.println("Servos prontos na posição inicial.");
}

void loop() {
  // Verifica se a string foi completada
  if (stringComplete) {
    // Movimento da base (direita/esquerda)
    if (inputString.startsWith("mover base direita")) {
      moverServoSuavemente(servoBase, posBase, posBaseDireita);
      Serial.println("Base movida para direita.");
    } else if (inputString.startsWith("mover base esquerda")) {
      moverServoSuavemente(servoBase, posBase, posBaseEsquerda);
      Serial.println("Base movida para esquerda.");
    }

    // Movimento do ombro (para cima/baixo)
    if (inputString.startsWith("mover ombro para cima")) {
      moverServoSuavemente(servoOmbro, posOmbro, posOmbroCima);
      Serial.println("Ombro movido para cima.");
    } else if (inputString.startsWith("mover ombro para baixo")) {
      moverServoSuavemente(servoOmbro, posOmbro, posOmbroBaixo);
      Serial.println("Ombro movido para baixo.");
    }

    // Movimento do cotovelo (para cima/baixo)
    if (inputString.startsWith("mover cotovelo para cima")) {
      moverServoSuavemente(servoCotovelo, posCotovelo, posCotoveloCima);
      Serial.println("Cotovelo movido para cima.");
    } else if (inputString.startsWith("mover cotovelo para baixo")) {
      moverServoSuavemente(servoCotovelo, posCotovelo, posCotoveloBaixo);
      Serial.println("Cotovelo movido para baixo.");
    }

    // Controle da garra (abrir/fechar)
    if (inputString.startsWith("abrir garra")) {
      moverServoSuavemente(servoGarra, posGarra, posGarraAberta);
      Serial.println("Garra aberta.");
    } else if (inputString.startsWith("fechar garra")) {
      moverServoSuavemente(servoGarra, posGarra, posGarraFechada);
      Serial.println("Garra fechada.");
    }

    // Inicia o temporizador para retornar à posição inicial
    moverParaPosInicial = true;
    tempoMovimento = millis();  // Armazena o tempo atual

    // Limpa a string após o processamento
    inputString = "";
    stringComplete = false;
  }

  // Verifica se o tempo de espera passou e se deve mover os servos para a posição inicial
  if (moverParaPosInicial && millis() - tempoMovimento >= tempoEspera) {
    moverServoSuavemente(servoBase, posBase, posBaseInicial);
    moverServoSuavemente(servoOmbro, posOmbro, posOmbroInicial);
    moverServoSuavemente(servoCotovelo, posCotovelo, posCotoveloInicial);
    moverServoSuavemente(servoGarra, posGarra, posGarraInicial);

    Serial.println("Servos retornaram à posição inicial.");

    // Reseta a flag de movimento
    moverParaPosInicial = false;
  }
}

// Captura os dados da serial
void serialEvent() {
  while (Serial.available()) {
    char inChar = (char)Serial.read();
    inputString += inChar;

    if (inChar == '\n') {
      stringComplete = true;
    }
  }
}

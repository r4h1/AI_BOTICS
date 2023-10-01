String inputString = ""; //Uma string para armazenar dados de entrada
bool stringComplete = false; //Para caso a string estija completa.

#define pinoLampadaCozinha 8
#define pinoPortaoGaragem 10
#define pinoLampadaQuarto 6


void setup() {
  // Inicia a porta serial
  Serial.begin(9600);
  // Reserva 200 bytes para a entrada da string
  inputString.reserve(200); // Até 200 bytes de caracter de entrada.
  
  pinMode(pinoLampadaCozinha, OUTPUT); 
  pinMode(pinoPortaoGaragem, OUTPUT); 
  pinMode(pinoLampadaQuarto, OUTPUT); 
}

void loop() {
  // Imprime conteudo da string quando uma nova linha chegar.
  if (stringComplete){
     if (inputString.startsWith("ligar luz da cozinha")){
       digitalWrite(pinoLampadaCozinha, HIGH);
       Serial.print("Ok. Lampada Ligada.\n");
   }else if(inputString.startsWith("desligar luz da cozinha")){
    digitalWrite(pinoLampadaCozinha, LOW);
    Serial.print("Pronto. Lampada Desligada.\n");
   }
   
    if (inputString.startsWith("ligar luz do quarto")){
       digitalWrite(pinoLampadaQuarto, HIGH);
       Serial.print("Claro. Lampada Ligada.\n");
   }else if(inputString.startsWith("desligar luz do quarto")){
    digitalWrite(pinoLampadaQuarto, LOW);
    Serial.print("Pronto. Desligada.\n");
   }

    if (inputString.startsWith("abrir portão da garagem")){
       digitalWrite(pinoPortaoGaragem, HIGH);
       Serial.print("Abrindo o portão.\n");
   }else if(inputString.startsWith("fechar portão da garagem")){
    digitalWrite(pinoPortaoGaragem, LOW);
    Serial.print("Pronto. Fechando portão.\n");
   }
   inputString = "";
   stringComplete = false;
 }
}

void serialEvent(){
  while (Serial.available()){
    char inChar = (char)Serial.read(); // Pega um novo byte
    inputString += inChar; // Adiciona ao inputString

    if (inChar == '\n'){
      stringComplete = true;
    }
  }
}

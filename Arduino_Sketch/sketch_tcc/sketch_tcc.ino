#include <Servo.h>
#include <DHT.h>

#define LED_SALA 2
#define LED_COZINHA 3
#define LED_QUARTO 4

#define DHTPIN 5
#define DHTTYPE DHT11

#define TRIG_PIN 6
#define ECHO_PIN 7

#define RELAY_PIN 8

Servo servo;
DHT dht(DHTPIN, DHTTYPE);

float TEMPERATURE_THRESHOLD = 25.0;  // Temperatura limite para acionar o relé

int pos;

void setup() {
  Serial.begin(9600);

  // Configuração dos LEDs
  pinMode(LED_SALA, OUTPUT);
  pinMode(LED_COZINHA, OUTPUT);
  pinMode(LED_QUARTO, OUTPUT);

  // Configuração do DHT
  dht.begin();

  // Configuração do Sensor de Distância
  pinMode(TRIG_PIN, OUTPUT);
  pinMode(ECHO_PIN, INPUT);

  // Configuração do Servo Motor
  servo.attach(9); // Pino do Servo
  servo.write(360); // Inicialmente fechado

  // Configuração do Relé
  pinMode(RELAY_PIN, OUTPUT);
  digitalWrite(RELAY_PIN, LOW); // Relé desligado inicialmente
}

void loop() {
  // Leitura do Sensor de Distância
  digitalWrite(TRIG_PIN, LOW);
  delayMicroseconds(2);
  digitalWrite(TRIG_PIN, HIGH);
  delayMicroseconds(10);
  digitalWrite(TRIG_PIN, LOW);

  long duration = pulseIn(ECHO_PIN, HIGH);
  float distance = (duration * 0.034) / 2;

  /*if (distance <= 15) { // Ajuste para a distância de segurança
    Serial.println("Objeto encontrado!"); // Envia a mensagem para o Python
  } else {
    Serial.println("Nenhum objeto próximo.");
  }*/

  // Leitura da temperatura
  float temp = dht.readTemperature();  // Lê a temperatura (em Celsius)

  if (isnan(temp)) {
    Serial.println("Falha ao ler o sensor DHT");
  } else {
    Serial.print(temp);
    Serial.println(" C");

    // Verifica se a temperatura atingiu o limite
    if (temp >= TEMPERATURE_THRESHOLD) {
      digitalWrite(RELAY_PIN, HIGH);  // Liga o relé
      Serial.println("Relé ligado devido à alta temperatura.");
    } else {
      digitalWrite(RELAY_PIN, LOW);  // Desliga o relé
      Serial.println("Relé desligado.");
    }
  }

  // Controle de LEDs
  if (Serial.available() > 0) {
    String command = Serial.readStringUntil('\n');
    command.trim();

    if (command == "LS") {  // ls de led sala
      digitalWrite(LED_SALA, HIGH);
    } else if (command == "ls") {
      digitalWrite(LED_SALA, LOW);
    }

    if (command == "LQ") { // lq de led quarto
      digitalWrite(LED_QUARTO, HIGH);
    } else if (command == "lq") {
      digitalWrite(LED_QUARTO, LOW);
    }

    if (command == "LC") { // lc de led cozinha
      digitalWrite(LED_COZINHA, HIGH);
    } else if (command == "lc") {
      digitalWrite(LED_COZINHA, LOW);
    }

    // Controle do Relé (que irá simular o ventilador)
    if (command == "Ligar Ventilador") {  // Comando de voz para ligar o ventilador (relé)
      digitalWrite(RELAY_PIN, HIGH);  // Liga o relé
      Serial.println("Ventilador ligado");  // Envia a confirmação de que o ventilador foi ligado
    } else if (command == "Desligar Ventilador") {  // Comando de voz para desligar o ventilador (relé)
      digitalWrite(RELAY_PIN, LOW);   // Desliga o relé
      Serial.println("Ventilador desligado");  // Envia a confirmação de que o ventilador foi desligado
    }

    // Controle portão
    if (command == "PA") {
      for (pos = pos; pos >= 100; pos -= 1) {  
        servo.write(pos); // abre o portão
        delay(15);
      }
      Serial.println("Portão aberto");
    } else if (command == "PF") {
      for (pos = pos; pos <= 360; pos += 1) {
        servo.write(pos);
        delay(15); 
      }  // Fecha o portão
      Serial.println("Portão fechado");
    }
  }
  delay(500); // Atualize conforme necessário
}
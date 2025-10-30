/*
 * ARDUINO NEMA17 CONTROLLER - VERSIÓN SIMPLE QUE FUNCIONA
 * Sistema de control para motor paso a paso NEMA17 con driver L298N
 */

// Configuración del motor paso a paso
const int STEP_PIN = 8;    // IN1 del L298N
const int DIR_PIN = 9;     // IN2 del L298N  
const int ENABLE_PIN = 10;  // IN3 del L298N
const int RESET_PIN = 11;  // IN4 del L298N

// Variables de control
int currentPosition = 0;
int targetPosition = 0;
bool isMoving = false;
unsigned long lastStepTime = 0;
const int STEP_DELAY = 2000;

void setup() {
  // Configurar pines
  pinMode(STEP_PIN, OUTPUT);
  pinMode(DIR_PIN, OUTPUT);
  pinMode(ENABLE_PIN, OUTPUT);
  pinMode(RESET_PIN, OUTPUT);
  
  // Estado inicial
  digitalWrite(ENABLE_PIN, HIGH);
  digitalWrite(RESET_PIN, HIGH);
  digitalWrite(STEP_PIN, LOW);
  digitalWrite(DIR_PIN, LOW);
  
  // Comunicación serial
  Serial.begin(115200);
  delay(2000);
  
  Serial.println("ARDUINO_NEMA17_READY");
  Serial.println("Comandos: HOME, OPEN <grados> <tiempo>, STATUS");
  Serial.println("Sistema listo");
}

void loop() {
  // Procesar comandos seriales
  if (Serial.available()) {
    String command = Serial.readStringUntil('\n');
    command.trim();
    command.toUpperCase();
    
    Serial.print("Comando recibido: ");
    Serial.println(command);
    
    if (command == "HOME") {
      homeMotor();
    }
    else if (command.startsWith("OPEN ")) {
      // Formato: OPEN <grados> <tiempo>
      int firstSpace = command.indexOf(' ');
      int secondSpace = command.indexOf(' ', firstSpace + 1);
      
      if (firstSpace != -1 && secondSpace != -1) {
        int degrees = command.substring(firstSpace + 1, secondSpace).toInt();
        int dwellTime = command.substring(secondSpace + 1).toInt();
        
        if (degrees >= 0 && degrees <= 360 && dwellTime > 0) {
          moveToPosition(degrees, dwellTime);
        } else {
          Serial.println("ERROR: Parámetros inválidos");
        }
      } else {
        Serial.println("ERROR: Formato incorrecto");
      }
    }
    else if (command == "STATUS") {
      showStatus();
    }
    else {
      Serial.println("ERROR: Comando no reconocido");
    }
  }
  
  // Control del motor
  if (isMoving) {
    moveStepper();
  }
}

void homeMotor() {
  Serial.println("Iniciando HOME...");
  moveToPosition(0, 2);
  Serial.println("HOME completado");
}

void moveToPosition(int degrees, int dwellTime) {
  if (degrees < 0 || degrees > 360) {
    Serial.println("ERROR: Grados fuera de rango");
    return;
  }
  
  // Calcular posición objetivo
  int targetSteps = degrees * 200 / 360;  // 200 pasos por vuelta
  
  Serial.print("Moviendo a ");
  Serial.print(degrees);
  Serial.print(" grados (");
  Serial.print(targetSteps);
  Serial.println(" pasos)");
  
  // Configurar dirección
  if (targetSteps > currentPosition) {
    digitalWrite(DIR_PIN, HIGH);
    Serial.println("Dirección: Horario");
  } else {
    digitalWrite(DIR_PIN, LOW);
    Serial.println("Dirección: Antihorario");
  }
  
  // Configurar movimiento
  targetPosition = targetSteps;
  isMoving = true;
  
  Serial.print("Iniciando movimiento... Tiempo: ");
  Serial.print(dwellTime);
  Serial.println(" segundos");
}

void moveStepper() {
  unsigned long currentTime = micros();
  
  if (currentTime - lastStepTime >= STEP_DELAY) {
    if (currentPosition != targetPosition) {
      // Generar pulso de paso
      digitalWrite(STEP_PIN, HIGH);
      delayMicroseconds(10);
      digitalWrite(STEP_PIN, LOW);
      
      // Actualizar posición
      if (targetPosition > currentPosition) {
        currentPosition++;
      } else {
        currentPosition--;
      }
      
      lastStepTime = currentTime;
    } else {
      // Movimiento completado
      isMoving = false;
      int currentDegrees = currentPosition * 360 / 200;
      
      Serial.print("Movimiento completado - Posición: ");
      Serial.print(currentDegrees);
      Serial.println(" grados");
      
      // Mantener posición
      if (dwellTime > 0) {
        Serial.print("Manteniendo por ");
        Serial.print(dwellTime);
        Serial.println(" segundos...");
        delay(dwellTime * 1000);
        Serial.println("Tiempo completado");
      }
    }
  }
}

void showStatus() {
  int currentDegrees = currentPosition * 360 / 200;
  
  Serial.println("=== ESTADO DEL MOTOR ===");
  Serial.print("Posición: ");
  Serial.print(currentDegrees);
  Serial.println(" grados");
  Serial.print("Pasos: ");
  Serial.println(currentPosition);
  Serial.print("Estado: ");
  Serial.println(isMoving ? "MOVIÉNDOSE" : "DETENIDO");
  Serial.println("========================");
}

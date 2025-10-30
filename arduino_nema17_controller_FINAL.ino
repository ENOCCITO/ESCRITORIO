/*
 * ARDUINO NEMA17 CONTROLLER - VERSIÓN FINAL CORREGIDA
 * Sistema de control para motor paso a paso NEMA17 con driver L298N
 * Recibe comandos por puerto serial desde Python
 * 
 * Conexiones:
 * - Pines 8-11: Control del motor NEMA17 (IN1-IN4 del L298N)
 * - Puerto Serial: Comunicación con Python (115200 baud)
 * 
 * Comandos:
 * - HOME: Mueve el motor a posición inicial (0 grados)
 * - OPEN <grados> <tiempo>: Mueve el motor a la posición especificada
 * 
 * Autor: Sistema de Dispensación Biométrica CEFA
 * Fecha: 2025
 */

// Configuración del motor paso a paso
const int STEP_PIN = 8;    // IN1 del L298N
const int DIR_PIN = 9;     // IN2 del L298N  
const int ENABLE_PIN = 10;  // IN3 del L298N
const int RESET_PIN = 11;  // IN4 del L298N

// Configuración del motor NEMA17
const int STEPS_PER_REVOLUTION = 200;  // 200 pasos por vuelta (1.8 grados por paso)
const int STEPS_PER_DEGREE = STEPS_PER_REVOLUTION / 360;  // Pasos por grado

// Variables de control
int currentPosition = 0;  // Posición actual en pasos
int targetPosition = 0;   // Posición objetivo en pasos
bool isMoving = false;
unsigned long lastStepTime = 0;
const int STEP_DELAY = 2000;  // Microsegundos entre pasos (velocidad)

// Variables para el tiempo de espera
int dwellSeconds = 0;  // Tiempo de espera en segundos
unsigned long dwellStartTime = 0;  // Tiempo de inicio de espera
bool isDwelling = false;  // Si está en período de espera

// Buffer para comandos seriales
String inputString = "";
bool stringComplete = false;

void setup() {
  // Configurar pines de salida
  pinMode(STEP_PIN, OUTPUT);
  pinMode(DIR_PIN, OUTPUT);
  pinMode(ENABLE_PIN, OUTPUT);
  pinMode(RESET_PIN, OUTPUT);
  
  // Configurar estado inicial
  digitalWrite(ENABLE_PIN, HIGH);  // Habilitar motor
  digitalWrite(RESET_PIN, HIGH);    // Reset activo
  digitalWrite(STEP_PIN, LOW);
  digitalWrite(DIR_PIN, LOW);
  
  // Configurar comunicación serial
  Serial.begin(115200);
  
  // Esperar a que se establezca la conexión
  delay(2000);
  
  Serial.println("ARDUINO_NEMA17_READY");
  Serial.println("Comandos disponibles:");
  Serial.println("  HOME - Mover a posición inicial");
  Serial.println("  OPEN <grados> <tiempo> - Mover a posición específica");
  Serial.println("  STATUS - Estado actual del motor");
  Serial.println("  RESET - Resetear posición");
  Serial.println("Sistema listo para recibir comandos");
  
  // Inicializar posición
  currentPosition = 0;
  targetPosition = 0;
}

void loop() {
  // Procesar comandos seriales
  if (stringComplete) {
    processCommand(inputString);
    inputString = "";
    stringComplete = false;
  }
  
  // Control del motor paso a paso
  if (isMoving) {
    moveStepper();
  }
  
  // Control del tiempo de espera
  if (isDwelling) {
    handleDwell();
  }
}

void serialEvent() {
  while (Serial.available()) {
    char inChar = (char)Serial.read();
    
    if (inChar == '\n' || inChar == '\r') {
      if (inputString.length() > 0) {
        stringComplete = true;
      }
    } else {
      inputString += inChar;
    }
  }
}

void processCommand(String command) {
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
        Serial.println("Uso: OPEN <grados 0-360> <tiempo_segundos>");
      }
    } else {
      Serial.println("ERROR: Formato de comando incorrecto");
      Serial.println("Uso: OPEN <grados> <tiempo>");
    }
  }
  else if (command == "STATUS") {
    showStatus();
  }
  else if (command == "RESET") {
    resetMotor();
  }
  else {
    Serial.println("ERROR: Comando no reconocido");
    Serial.println("Comandos disponibles: HOME, OPEN <grados> <tiempo>, STATUS, RESET");
  }
}

void homeMotor() {
  Serial.println("Iniciando secuencia HOME...");
  
  // Mover a posición 0 grados
  moveToPosition(0, 2);
  
  Serial.println("HOME completado - Posición: 0 grados");
}

void moveToPosition(int degrees, int dwellTime) {
  if (degrees < 0 || degrees > 360) {
    Serial.println("ERROR: Grados fuera de rango (0-360)");
    return;
  }
  
  // Calcular posición objetivo en pasos
  int targetSteps = degrees * STEPS_PER_DEGREE;
  
  Serial.print("Moviendo a ");
  Serial.print(degrees);
  Serial.print(" grados (");
  Serial.print(targetSteps);
  Serial.println(" pasos)");
  
  // Configurar dirección
  if (targetSteps > currentPosition) {
    digitalWrite(DIR_PIN, HIGH);  // Sentido horario
    Serial.println("Dirección: Horario");
  } else {
    digitalWrite(DIR_PIN, LOW);   // Sentido antihorario
    Serial.println("Dirección: Antihorario");
  }
  
  // Configurar movimiento
  targetPosition = targetSteps;
  isMoving = true;
  
  // Configurar tiempo de espera
  dwellSeconds = dwellTime;
  isDwelling = false;  // Se activará cuando termine el movimiento
  
  Serial.print("Iniciando movimiento... Tiempo de espera: ");
  Serial.print(dwellSeconds);
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
      int currentDegrees = currentPosition / STEPS_PER_DEGREE;
      
      Serial.print("Movimiento completado - Posición actual: ");
      Serial.print(currentDegrees);
      Serial.println(" grados");
      
      // Iniciar período de espera si es necesario
      if (dwellSeconds > 0) {
        isDwelling = true;
        dwellStartTime = millis();
        Serial.print("Manteniendo posición por ");
        Serial.print(dwellSeconds);
        Serial.println(" segundos...");
      }
    }
  }
}

void handleDwell() {
  unsigned long currentTime = millis();
  unsigned long elapsedTime = (currentTime - dwellStartTime) / 1000;  // Convertir a segundos
  
  if (elapsedTime >= dwellSeconds) {
    // Tiempo de espera completado
    isDwelling = false;
    dwellSeconds = 0;
    Serial.println("Tiempo de espera completado");
  }
}

void showStatus() {
  int currentDegrees = currentPosition / STEPS_PER_DEGREE;
  
  Serial.println("=== ESTADO DEL MOTOR NEMA17 ===");
  Serial.print("Posición actual: ");
  Serial.print(currentDegrees);
  Serial.println(" grados");
  
  Serial.print("Pasos actuales: ");
  Serial.println(currentPosition);
  
  Serial.print("Objetivo: ");
  Serial.print(targetPosition);
  Serial.println(" pasos");
  
  Serial.print("Estado: ");
  if (isMoving) {
    Serial.println("MOVIÉNDOSE");
  } else if (isDwelling) {
    Serial.println("ESPERANDO");
  } else {
    Serial.println("DETENIDO");
  }
  
  Serial.print("Pines L298N: ");
  Serial.print("STEP=");
  Serial.print(digitalRead(STEP_PIN));
  Serial.print(" DIR=");
  Serial.print(digitalRead(DIR_PIN));
  Serial.print(" ENABLE=");
  Serial.print(digitalRead(ENABLE_PIN));
  Serial.print(" RESET=");
  Serial.println(digitalRead(RESET_PIN));
  Serial.println("================================");
}

void resetMotor() {
  Serial.println("Reseteando motor...");
  
  // Deshabilitar motor
  digitalWrite(ENABLE_PIN, LOW);
  delay(100);
  
  // Resetear posición
  currentPosition = 0;
  targetPosition = 0;
  isMoving = false;
  isDwelling = false;
  dwellSeconds = 0;
  
  // Rehabilitar motor
  digitalWrite(ENABLE_PIN, HIGH);
  
  Serial.println("Motor reseteado - Posición: 0 grados");
}

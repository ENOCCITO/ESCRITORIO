/*
 * ARDUINO NEMA17 CONTROLLER - VERSIÓN QUE SÍ FUNCIONA
 * Sistema de control para motor paso a paso NEMA17 con driver L298N
 * 
 * CONEXIONES:
 * - Pin 8: STEP (IN1 del L298N)
 * - Pin 9: DIR (IN2 del L298N)  
 * - Pin 10: ENABLE (IN3 del L298N)
 * - Pin 11: RESET (IN4 del L298N)
 */

// Configuración del motor NEMA17
const int STEP_PIN = 8;
const int DIR_PIN = 9;
const int ENABLE_PIN = 10;
const int RESET_PIN = 11;

// Configuración del motor
const int STEPS_PER_REVOLUTION = 200;  // NEMA17 tiene 200 pasos por vuelta
const int STEPS_PER_DEGREE = STEPS_PER_REVOLUTION / 360;  // 0.556 pasos por grado

// Variables de control
int currentPosition = 0;  // Posición actual en pasos
int targetPosition = 0;   // Posición objetivo en pasos
bool isMoving = false;
unsigned long lastStepTime = 0;
const int STEP_DELAY = 2000;  // Microsegundos entre pasos

// Variables para el tiempo de espera
int dwellTime = 0;
unsigned long dwellStartTime = 0;
bool isDwelling = false;

void setup() {
  // Configurar pines
  pinMode(STEP_PIN, OUTPUT);
  pinMode(DIR_PIN, OUTPUT);
  pinMode(ENABLE_PIN, OUTPUT);
  pinMode(RESET_PIN, OUTPUT);
  
  // Estado inicial
  digitalWrite(ENABLE_PIN, HIGH);  // Habilitar motor
  digitalWrite(RESET_PIN, HIGH);   // Reset activo
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
        float degrees = command.substring(firstSpace + 1, secondSpace).toFloat();
        int dwellTimeValue = command.substring(secondSpace + 1).toInt();
        
        if (degrees >= 0 && degrees <= 360 && dwellTimeValue > 0) {
          moveToPosition(degrees, dwellTimeValue);
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
  
  // Control del tiempo de espera
  if (isDwelling) {
    handleDwell();
  }
}

void homeMotor() {
  Serial.println("Iniciando HOME...");
  moveToPosition(0, 2);
  Serial.println("HOME completado");
}

void moveToPosition(float degrees, int dwellTimeValue) {
  if (degrees < 0 || degrees > 360) {
    Serial.println("ERROR: Grados fuera de rango");
    return;
  }
  
  // Calcular posición objetivo en pasos
  int targetSteps = (int)(degrees * STEPS_PER_DEGREE);
  
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
  dwellTime = dwellTimeValue;
  isDwelling = false;
  
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
      float currentDegrees = currentPosition / STEPS_PER_DEGREE;
      
      Serial.print("Movimiento completado - Posición: ");
      Serial.print(currentDegrees);
      Serial.println(" grados");
      
      // Iniciar período de espera
      if (dwellTime > 0) {
        isDwelling = true;
        dwellStartTime = millis();
        Serial.print("Manteniendo por ");
        Serial.print(dwellTime);
        Serial.println(" segundos...");
      }
    }
  }
}

void handleDwell() {
  unsigned long currentTime = millis();
  unsigned long elapsedTime = (currentTime - dwellStartTime) / 1000;
  
  if (elapsedTime >= dwellTime) {
    isDwelling = false;
    dwellTime = 0;
    Serial.println("Tiempo completado");
  }
}

void showStatus() {
  float currentDegrees = currentPosition / STEPS_PER_DEGREE;
  
  Serial.println("=== ESTADO DEL MOTOR ===");
  Serial.print("Posición: ");
  Serial.print(currentDegrees);
  Serial.println(" grados");
  Serial.print("Pasos: ");
  Serial.println(currentPosition);
  Serial.print("Estado: ");
  if (isMoving) {
    Serial.println("MOVIÉNDOSE");
  } else if (isDwelling) {
    Serial.println("ESPERANDO");
  } else {
    Serial.println("DETENIDO");
  }
  Serial.println("========================");
}
const int PIN_POT = 34;
const unsigned long INTERVALO_MS = 500;
unsigned long ultimoEnvio = 0;

void setup() {
  Serial.begin(115200);
  delay(1000);
  analogReadResolution(12);
  pinMode(PIN_POT, INPUT);
  Serial.println("ESP32 listo. Enviando: lectura_cruda,voltaje,porcentaje");
}

void loop() {
  unsigned long ahora = millis();
  if (ahora - ultimoEnvio >= INTERVALO_MS) {
    ultimoEnvio = ahora;
    int lecturaCruda = analogRead(PIN_POT);
    float voltaje = (lecturaCruda / 4095.0) * 3.3;
    int porcentaje = map(lecturaCruda, 0, 4095, 0, 100);
    Serial.print(lecturaCruda);
    Serial.print(",");
    Serial.print(voltaje, 3);
    Serial.print(",");
    Serial.println(porcentaje);
  }
}
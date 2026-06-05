const int PIN_ADC = 34;          // GPIO34 - ADC1_CH6
const int INTERVALO_MS = 100;    // Envío cada 100 ms
const float VREF = 3.3;          // Voltaje de referencia del ESP32
const int RESOLUCION_ADC = 4095; // 12 bits -> 0 a 4095

void setup() {
  Serial.begin(115200);
  analogReadResolution(12);      // Resolución de 12 bits
  delay(500);
}

void loop() {
  unsigned long tiempo_ms = millis();
  int lectura_adc = analogRead(PIN_ADC);
  float voltaje = (lectura_adc / (float)RESOLUCION_ADC) * VREF;

  // Formato: tiempo_ms,adc,voltaje
  Serial.print(tiempo_ms);
  Serial.print(",");
  Serial.print(lectura_adc);
  Serial.print(",");
  Serial.println(voltaje, 2);

  delay(INTERVALO_MS);
}

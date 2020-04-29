typedef const uint8_t pinPort;
typedef double waveTime; // time in seconds
typedef double microWaveTime; // time in microseconds 10^-6
typedef unsigned int integerMicroWaveTime; // integer time in microseconds 10^-6
typedef unsigned int integerMilliWaveTime; // integer time in milliseconds 10^-3
typedef double distance; // distance in meters
typedef double cmDistance; // distance in cm 10^-2
typedef double velocity; // velocity in m/s

float temperature = 24.0; // room temperature between 0 C and 30 C
unsigned int serialSpeed = 9600; // bps data speed for COM-interaction
integerMilliWaveTime serialTimeout = 50; // milliseconds
integerMicroWaveTime pulseInTimeout = 10000; // microseconds
integerMilliWaveTime dataFrequency = 100; // milliseconds for the delay of measurements

size_t measurementsPerTact = 3;
integerMicroWaveTime pauseDurationPerTact = 3;
integerMicroWaveTime transmitDurationPerTact = 5;

cmDistance betweenSensorAndStart = 12.7;
cmDistance betweenSensorAndFinish = 12.6;
cmDistance distanceInOperation = 70.0;

pinPort sensorStartEcho = 9;
pinPort sensorStartTrig = 8;
pinPort sensorFinishEcho = 11;
pinPort sensorFinishTrig = 7;
cmDistance sensorThreshold = 40.0;

velocity speed_of_sound = 331.5 + 0.59 * temperature; // speed of sound for 24 C
integerMicroWaveTime noWaveCollisionsInterval = 1000 + 1000 * 10 / speed_of_sound * (distanceInOperation + betweenSensorAndStart + betweenSensorAndFinish); 

struct UltrasonicSensor{

  pinPort EchoPin;
  pinPort TrigPin;
  
};


void UltrasonicSensor_init(UltrasonicSensor p) {
  pinMode(p.EchoPin, INPUT);
  pinMode(p.TrigPin, OUTPUT);
}

void UltrasonicSensor_sendWave(UltrasonicSensor p, integerMicroWaveTime pauseDuration, integerMicroWaveTime transmitDuration) {
  digitalWrite(p.TrigPin, LOW);
  delayMicroseconds(pauseDuration);
  digitalWrite(p.TrigPin, HIGH);
  delayMicroseconds(transmitDuration);
  digitalWrite(p.TrigPin, LOW);
}

microWaveTime UltrasonicSensor_getWaveTime(struct UltrasonicSensor p) {
  microWaveTime t = pulseIn(p.EchoPin, HIGH, pulseInTimeout);
  return t;  
}

cmDistance UltrasonicSensor_getDistance(struct UltrasonicSensor p, const size_t totalMeasurements = 3,
                    integerMicroWaveTime pauseDuration = 3, integerMicroWaveTime transmitDuration = 5) {
                      
  microWaveTime count = 0.0;
  for (size_t i = 0; i < totalMeasurements; i++) {
      UltrasonicSensor_sendWave(p, pauseDuration, transmitDuration);
      count += UltrasonicSensor_getWaveTime(p);
  }
  microWaveTime avg_time = count / totalMeasurements;
  cmDistance d = speed_of_sound * avg_time / 20000.0;
  return d;
  
}

struct UltrasonicSensor sensorStart = {sensorStartEcho, sensorStartTrig};
struct UltrasonicSensor sensorFinish = {sensorFinishEcho, sensorFinishTrig};

void setup(){

  // MAYBE: get the temperature
  
  // Calculate precize speed of sound
  if ((temperature >= 0.01) && (temperature <= 30.01)) {
      speed_of_sound = 331.5 + 0.59 * temperature;
  }
  
  Serial.begin(serialSpeed);
  Serial.setTimeout(serialTimeout);

  UltrasonicSensor_init(sensorStart);
  UltrasonicSensor_init(sensorFinish);
  
}

void serialEvent() {
   String msg = Serial.readString();
    if (msg.equals("\n")) { return; }

    if (msg.startsWith("params")) {
       Serial.println(" <<< OBERBECK PENDULUM >>> ");
       Serial.println(" === COM settings === ");
       Serial.print("serialSpeed: "); Serial.print(serialSpeed); Serial.println(" bps");
       Serial.print("serialTimeout: "); Serial.print(serialTimeout); Serial.println(" microseconds");
       Serial.println(" === Physical constants === ");
       Serial.print("speed_of_sound: "); Serial.print(speed_of_sound); Serial.println(" m/s");
       Serial.print("noWaveCollisionsInterval: "); Serial.print(round(noWaveCollisionsInterval / 1000)); Serial.println(" milliseconds");
       Serial.println(" === Environmental constants === ");
       Serial.print("temperature: "); Serial.print(temperature); Serial.println(" C");
       Serial.print("betweenSensorAndStart: "); Serial.print(betweenSensorAndStart); Serial.println(" cm");
       Serial.print("betweenSensorAndFinish: "); Serial.print(betweenSensorAndFinish); Serial.println(" cm");
       Serial.print("distanceInOperation: "); Serial.print(distanceInOperation); Serial.println(" cm");
       Serial.println(" === Measurement settings === ");
       Serial.print("dataFrequency: "); Serial.print(dataFrequency); Serial.println(" milliseconds");
       Serial.print("measurementsPerTact: "); Serial.print(measurementsPerTact); Serial.println(" times");
       Serial.print("pauseDurationPerTact: "); Serial.print(pauseDurationPerTact); Serial.println(" microseconds");
       Serial.print("transmitDurationPerTact: "); Serial.print(transmitDurationPerTact); Serial.println(" microseconds");
       Serial.println(" === Sensor settings === ");
       Serial.print("sensorStartEcho: "); Serial.print(sensorStartEcho); Serial.println(" pin");
       Serial.print("sensorStartTrig: "); Serial.print(sensorStartTrig); Serial.println(" pin");
       Serial.print("sensorFinishEcho: "); Serial.print(sensorFinishEcho); Serial.println(" pin");
       Serial.print("sensorFinishTrig: "); Serial.print(sensorFinishTrig); Serial.println(" pin");
       Serial.print("pulseInTimeout: "); Serial.print(pulseInTimeout); Serial.println(" microseconds");
    
    }
    
}


cmDistance analysis(cmDistance x_1, cmDistance x_2) {

  if ((x_1 <= sensorThreshold) && (x_2 <= sensorThreshold)) {
    return (x_1 + x_2) / 2;
  }

  if (!(x_1 <= sensorThreshold) && (x_2 <= sensorThreshold)) {
    return x_2;
  }

  if ((x_1 <= sensorThreshold) && !(x_2 <= sensorThreshold)) {
    return x_1;
  }

  if (!(x_1 <= sensorThreshold) && !(x_2 <= sensorThreshold)) {
    return 0.0;
  }
  
}

void loop(){

  delay(round(noWaveCollisionsInterval / 1000));
  cmDistance x_1 = UltrasonicSensor_getDistance(sensorStart, measurementsPerTact, pauseDurationPerTact, transmitDurationPerTact) - betweenSensorAndStart;
  delay(round(noWaveCollisionsInterval / 1000));
  cmDistance x_2 = distanceInOperation - UltrasonicSensor_getDistance(sensorStart, measurementsPerTact, pauseDurationPerTact, transmitDurationPerTact) - betweenSensorAndFinish;

  Serial.println(analysis(x_1, x_2));
  
  delay(dataFrequency);
  
}

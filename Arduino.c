
typedef const uint8_t pinPort;
typedef double waveTime; // time in seconds
typedef double microWaveTime; // time in microseconds 10^-6
typedef unsigned int integerMicroWaveTime; // integer time in microseconds 10^-6
typedef double distance; // distance in meters
typedef double cmDistance; // distance in cm 10^-2
typedef double velocity; // velocity in m/s

float temperature = 24.0; // room temperature between 0 C and 30 C
unsigned int serialSpeed = 9600; // bps data speed for COM-interaction
integerMicroWaveTime delayBetweenMeasurements = 50 * 1000; // microsedonds 10^-6 to wait between taking measurements
cmDistance betweenSensorAndStart = 0.0;
cmDistance betweenSensorAndFinish = 0.0;
cmDistance distanceInOperation = 70.0;
pinPort sensorStartEcho = 2;
pinPort sensorStartTrig = 3;
pinPort sensorFinishEcho = 4;
pinPort sensorFinishTrig = 5;


velocity speed_of_sound = 331.5 + 0.59 * temperature; // speed of sound for 24 C
integerMicroWaveTime noWaveCollisionsInterval = 2 + (distanceInOperation + betweenSensorAndStart + betweenSensorAndFinish) / 100 / speed_of_sound; 

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
  microWaveTime t = pulseIn(p.EchoPin, HIGH);
  return t;  
}

cmDistance UltrasonicSensor_getDistance(struct UltrasonicSensor p, const size_t totalMeasurements = 3,
integerMicroWaveTime pauseDuration = 3, integerMicroWaveTime transmitDuration = 5) {
  UltrasonicSensor_sendWave(p, pauseDuration, transmitDuration);
  microWaveTime count = 0.0;
  for (size_t i = 0; i < totalMeasurements; i++) {
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

  UltrasonicSensor_init(sensorStart);
  UltrasonicSensor_init(sensorFinish);
  
}

void loop(){

  cmDistance x_1 = UltrasonicSensor_getDistance(sensorStart, 3, 3, 5) - betweenSensorAndStart;
  delayMicroseconds(noWaveCollisionsInterval);
  cmDistance x_2 = distanceInOperation - UltrasonicSensor_getDistance(sensorFinish, 3, 3, 5) - betweenSensorAndFinish;

  cmDistance x_avg = (x_1 + x_2) / 2.0;

  Serial.println(x_avg);
  delay(delayBetweenMeasurements);
  
}

typedef const uint8_t pinPort;
typedef double waveTime; // time in seconds
typedef double microWaveTime; // time in microseconds 10^-6
typedef unsigned int integerMicroWaveTime; // integer time in microseconds 10^-6
typedef unsigned int integerMilliWaveTime; // integer time in milliseconds 10^-3
typedef double distance; // distance in meters
typedef double cmDistance; // distance in cm 10^-2
typedef double velocity; // velocity in m/s
typedef double mass; // mass in kg
typedef double acceleration; // acceleration in m/s^2
typedef double angular_acc; // angular acceleration in rad/s^2
typedef double inertiaMoment; // inertia moment in kg * m^2
typedef double moment; // moment kg * m/s^2 * m


unsigned int serialSpeed = 9600; // bps data speed for COM-interaction
integerMilliWaveTime serialTimeout = 50; // milliseconds
integerMilliWaveTime dataFrequency = 100; // milliseconds for the delay of measurements

const mass massKaretka = 0.047;
const mass massShaiba = 0.220;
const mass massGruz = 0.408;
const cmDistance l_1 = 5.7;
const cmDistance l_0 = 2.5;
const cmDistance b = 4.0;
const cmDistance d = 4.6;
const cmDistance h_0 = 70.0;

const acceleration g = 9.81908;
const waveTime humanDelayTime = 0.13;
const inertiaMoment I_0 = 0.011541518;
const moment moments_tr [6] = {-0.00228920, 0.00998837, 0.00906186, 0.01317346, 0.01499408, 0.01614266};

const moment M_tr_a = 0.003179657;
const moment M_tr_b = 0.000950262;

moment M_tr(int n) {
  return moments_tr[n - 1];
  //return M_tr_b + M_tr_a * n;
}

cmDistance R(int n) {
    return l_1 + (n - 1) * l_0 + b / 2;
}

inertiaMoment I(int n) {
  return I_0 + 4 * massGruz * R(n) * R(n) / 10000;
}

mass m(int q) {
  return massKaretka + q * massShaiba;
}

acceleration a(int q, int n) {
  return (m(q) * (d / 100) * g / 2 - M_tr(n)) / (2 * I(n) / (d/100) + m(q) * (d/100) / 2);
}

cmDistance x(microWaveTime t, int q, int n) {
  return 100 * max(0, h_0 / 100 - a(q, n) * t * t / 2);
}

void setup() {

  Serial.begin(serialSpeed);
  Serial.setTimeout(serialTimeout);

}

microWaveTime experimentTime = 0;
int experimentalQ = 0;
int experimentalN = 0;
bool isBusy = false;

void serialEvent() {
    String msg = Serial.readString();
    if (msg.equals("\n")) { return; }

    if (msg.startsWith("throw")) {

        int q = 0;
        int n = 0;
        
        int i = 0;
        char str[255];
        msg.toCharArray(str, 255);
        char * pch;
        pch = strtok (str, " ");
        while (pch != NULL) {
          
          String token(pch);

          if (i == 0) {
              if (!(token.equals("throw"))) {
                return;
              }
          }

          if (i == 1) {
              q = token.toInt();
              if (q == 0) {
                return;
              }
              experimentalQ = q;
          }

          if (i == 2) {
              n = token.toInt();
              if (n == 0) {
                return;
              }
              experimentalN = n;
          }
          
          i++;
          pch = strtok(NULL, " ");
          
        }

        isBusy = true;
        experimentTime = 0;
        
        Serial.print("# Throw ");
        Serial.print(experimentalQ);
        Serial.print(" cargos using ");
        Serial.print(experimentalN);
        Serial.println("th distance");
    }
    
}

void loop() {

    if (isBusy) {

      microWaveTime previousTime = micros();
      //Serial.print(experimentTime / 1000 / 1000);
      //Serial.print(" ");
      cmDistance r = x(experimentTime / 1000 / 1000, experimentalQ, experimentalN);
      if (r == 0) {
          isBusy = false;
          Serial.println("# Done");
      }
      Serial.println(r);
      delay(dataFrequency);
      experimentTime += micros() - previousTime;
      
    } else {
      Serial.println("70.0");
      delay(dataFrequency);
    }
  
}

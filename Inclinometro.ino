#include <math.h>
/*Accelerometer class*/
class Accelerometer {
  
private:
  String name;
  //output pins
  int pinX=0; 
  int pinY=0;
  int pinZ=0;
  //raw values 
  int xVal=0; //Longitudinal (Sagittal) axis (X).
  int yVal=0; //Lateral (Coronal or Transverse) axis (Y).
  int zVal=0; //Normal (Perpendicular or Vertical) axis (Z). 
  //calculated angles
  double aXY=0;//YAW  psi angle (dirección, deriva o giñada)
  double aYZ=0;//ROLL phi angle (balance, escora o alabeo)
  double aXZ=0;//PITCH theta angle (elevación, inclinación o cabeceo)

public:
  /*Set init data for this sensor. Pins are considered to be contiguous to each other*/
  void set(int pin, String aName){
    pinX=pin;
    pinY=pin+1;
    pinZ=pin+2;
    name=aName;
    //print to serial the configuration
    Serial.write("\n");
    Serial.write("Nombre:");
    Serial.print(name) ;
    Serial.write("\n");
    Serial.write("Pines: [");
    Serial.print(pinX);
    Serial.write(", ");
    Serial.print(pinY);
    Serial.write(", ");
    Serial.print(pinZ);
    Serial.write("]\n");

  }

  /*Read whole data levels from this sensor and maps them as usable raw values */
  void read(){
    //read'em
    xVal = analogRead(pinX);    
    yVal = analogRead(pinY);    
    zVal = analogRead(pinZ);
    //map'em
    xVal = map(xVal, 0, 1023, -500, 500); 
    yVal = map(yVal, 0, 1023, -500, 500); 
    zVal = map(zVal, 0, 1023, -500, 500); 
  }

  /*Transforms readings into angles*/
  void angles(){
    //YAW (dirección, deriva o giñada) psi angle, turns around the Normal (Perpendicular or Vertical) axis (Z). 
    aXY = atan((double)xVal / (double)yVal);
    aXY = aXY*(57.2958);
    
    //ROLL (balance, escora o alabeo) phi angle, turns (banks) around Longitudinal axis (X).
    aYZ = atan((double)yVal / (double)zVal);
    aYZ = aYZ*(57.2958);

    //PITCH (elevación, inclinación o cabeceo) theta angle, turns around Lateral (or Transverse) axis (Y). 
    aXZ = atan((double)xVal / (double)zVal);
    aXZ = aXZ*(57.2958);
  }

  /*Send data by serial link*/
  void send(){

    Serial.print(name) ;
    Serial.write(".yz:");
    Serial.print(aYZ);
    Serial.write("\n");

    Serial.print(name) ;
    Serial.write(".xz:");
    Serial.print(aXZ);
    Serial.write("\n");

    Serial.print(name) ;
    Serial.write(".xy:");
    Serial.print(aXY);
    Serial.write("\n");
  }

} 
a1; 

void setup() {
  analogReference(EXTERNAL);
  Serial.begin(9600);
  a1.set(0, "A1");
}

void loop() {

  a1.read();
  a1.angles();
  a1.send();

  delay(100);  
}

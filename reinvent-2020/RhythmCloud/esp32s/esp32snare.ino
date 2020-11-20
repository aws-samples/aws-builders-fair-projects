/*
 This is code for a robotic drum created by Ryan Vanderwerf derived from code by Randy Sarafan.
 This runs on a Espressif ESP32s DevKitc device with a L298N H bridge motor driver

 */

int event = 0;

int strikelegnth = 80;

int incomingByte = 0;
// Motor A
int motor1Pin1 = 27; 
int motor1Pin2 = 26;
int motor2Pin1 = 32;
int motor2Pin2 = 25;

void setup() {
  
  //establish motor direction toggle pins
  pinMode(motor1Pin2, OUTPUT); //CH A -- HIGH = forwards and LOW = backwards???
  pinMode(motor1Pin1, OUTPUT); //CH B -- HIGH = forwards and LOW = backwards???
  //pinMode(14, OUTPUT); //brake (disable) CH A
  pinMode(motor2Pin1, OUTPUT); //CH A -- HIGH = forwards and LOW = backwards???
  pinMode(motor2Pin2, OUTPUT); //CH B -- HIGH = forwards and LOW = backwards???
  //pinMode(32, OUTPUT); //brake (disable) CH A
  fireChannelA();
  fireChannelB();
 
  Serial.begin(115200);
}

void fireChannelB() {

  Serial.println("Motor B forward");
  digitalWrite(motor2Pin1, HIGH);
  digitalWrite(motor2Pin2, LOW);
  
  //ledcWrite(pwmChannel, 200);
  delay(80);
    // Stop the DC motor
  //Serial.println("Motor B stopped");
  digitalWrite(motor2Pin1, LOW);
  digitalWrite(motor2Pin2, LOW);
  delay(1);
  // go backwards
  //Serial.println("Motor B backwards");
  digitalWrite(motor2Pin1, LOW);
  digitalWrite(motor2Pin2, HIGH);
  delay(40);
  //Serial.println("Motor B stopped");
  digitalWrite(motor2Pin1, LOW);
  digitalWrite(motor2Pin2, LOW);      


}

void fireChannelA() {

       
  Serial.println("Motor A forward");
  digitalWrite(motor1Pin1, HIGH);
  digitalWrite(motor1Pin2, LOW);
  
  //ledcWrite(pwmChannel, 200);
  delay(80);
    // Stop the DC motor
  //Serial.println("Motor A stopped");
  digitalWrite(motor1Pin1, LOW);
  digitalWrite(motor1Pin2, LOW);
  delay(1);
  // go backwards
  //Serial.println("Motor A backwards");
  digitalWrite(motor1Pin1, LOW);
  digitalWrite(motor1Pin2, HIGH);
  delay(40);
  //Serial.println("Motor A stopped");
  digitalWrite(motor1Pin1, LOW);
  digitalWrite(motor1Pin2, LOW);      
}

void loop() {
 //Serial.print("I received: ");
 //Serial.println(incomingByte, DEC); 
 if (Serial.available()){
    incomingByte = Serial.read();
    event = 1;
 }//end if serial available

 if(event == 1){

   if (incomingByte == 131) {
       fireChannelB();
       event = 0;
   }  
   
   
   if (incomingByte == 132) {
       fireChannelA();
       event = 0; 
   }  
   
   if (incomingByte == 160) {
       fireChannelB();
       fireChannelA();
       event = 0; 
   }  
 }
}
    

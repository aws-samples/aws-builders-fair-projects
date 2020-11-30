/*
 This is code for a robotic drum created by Ryan Vanderwerf derived from code by Randy Sarafan.

 For more information, visit:
 https://www.instructables.com/id/Arduino-Controlled-Robotic-Drum/ 
 
 This example code is in the public domain.
 */

int event = 0;

int strikelegnth = 80;

int incomingByte = 0;
// Motor A

char drum[] = "ridecymbal";
int motor1Pin1 = 13; 
int motor1Pin2 = 12;
int motor2Pin1 = 26;
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

void whoami() {
   Serial.println(drum);
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
  delay(80);
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
  delay(80);
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

   if (incomingByte == 132) {
       fireChannelB();
       event = 0;
   }  
   
   
   if (incomingByte == 131) {
       fireChannelA();
       event = 0; 
   }  
   
   if (incomingByte == 133) {
       fireChannelB();
       fireChannelA();
       event = 0; 
   }  
   if (incomingByte == 130) {
       whoami();
       event = 0;
   }

 }
}
    

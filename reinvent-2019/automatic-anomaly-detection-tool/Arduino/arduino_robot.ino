#include <Braccio.h>
#include <Servo.h>

#define maxLength 64
String inString = String(maxLength);

/*
 * used in Braccio source
 */
Servo base;
Servo shoulder;
Servo elbow;
Servo wrist_rot;
Servo wrist_ver;
Servo gripper;

/*
 * blink on board led 0.5sec
 */
void blink_led(){
  digitalWrite(LED_BUILTIN, HIGH);
  delay(500);
  digitalWrite(LED_BUILTIN, LOW);
}

/*
 * move robot
 */
void move_robot(unsigned int move_position){
  pickup();
  if(move_position == 1){
    put_to_pos1();
  }
  else if(move_position == 2){
    put_to_pos2();
  }
  else if(move_position == 3){
    put_to_pos3();
  }

  home_position();
}

/*
 * Move to Home position
 */
void home_position(){
  Braccio.ServoMovement(20,  90,  45, 180, 180, 170,  50);
}

/*
 * move to pickup sushi
 */
void pickup(){
  Braccio.ServoMovement(20,  125,  85, 180, 180,  170,  10);
  Braccio.ServoMovement(20,  125, 102, 180, 170,  170,  10);
  Braccio.ServoMovement(20,  125, 102, 180, 170,  170, 100);
  Braccio.ServoMovement(20,  125,  45, 180, 170,  170, 100);
  Braccio.ServoMovement(20,   90,  45, 180, 170,  170, 100);
}

/*
 * Move to first saucer
 */
void put_to_pos1(){
  Braccio.ServoMovement(20,   23,  45, 180, 180,  170, 100);
  Braccio.ServoMovement(20,   23,  93, 170, 180,  170, 100);
  Braccio.ServoMovement(20,   23,  93, 170, 180,  170,  10);
  Braccio.ServoMovement(20,   23,  45, 180, 180,  170,  10);
}

/*
 * Move to second saucer
 */
void put_to_pos2(){
  Braccio.ServoMovement(20,   55,  45, 180, 170,  170, 100);
  Braccio.ServoMovement(20,   55,  99, 165, 175,  170, 100);
  Braccio.ServoMovement(20,   55,  99, 165, 175,  170,  10);
  Braccio.ServoMovement(20,   55,  45, 170, 180,  170,  10);
}

/*
 * Move to third saucer
 */
void put_to_pos3(){
  Braccio.ServoMovement(20,   88,  45, 180, 170,  170, 100);
  Braccio.ServoMovement(20,   88, 112, 152, 170,  170, 100);
  Braccio.ServoMovement(20,   88, 112, 152, 170,  170,  10);
  Braccio.ServoMovement(20,   88,  45, 170, 170,  170,  10);
}

/**************************************************************/


/*
 * Initial Setup
 */
void setup() {
  Serial.begin(9600);
  pinMode(LED_BUILTIN, OUTPUT);
  inString = "";
  
  Braccio.begin();

  home_position();
  
  Serial.println(F("setup done."));

}

/*
 * main loop
 */
void loop() {
  if (Serial.available() > 0) {
    char inChar = Serial.read();
    inString.concat(String(inChar));
    if (inChar == '\n') {
      digitalWrite(LED_BUILTIN, HIGH);
      if (inString.startsWith("POS1")) {
        Serial.println("MS1");
        move_robot(1);
        Serial.println("MF");
      } else if (inString.startsWith("POS2")) {
        Serial.println("MS2");
        move_robot(2);
        Serial.println("MF");
      } else if (inString.startsWith("POS3")) {
        Serial.println("MS3");
        move_robot(3);
        Serial.println("MF");
      }
      else{
        Serial.println("NM");
      }
      digitalWrite(LED_BUILTIN, LOW);
      inString = "";
    }
  }
  else{
    blink_led();
  }
}

#include <Servo.h>

Servo  rightServo;
Servo  leftServo;

#define MAXLINE  200		// biggest line of data that can be read from serial port

#define ROBOTS	4
#define ME	0		// I am robot zero, the first robot
//#define ME	1		// I am robot one, the second robot
//#define ME	2		// I am robot two, the third robot
//#define ME	3		// I am robot three, the fourth robot

#define SERVO_OFF	127	 	// relative to 0 to 255

//
// the left and right settings here are from 0 to 255
//
typedef struct servoSettings {
     int	left;
     int	right;
} servoSettings;

//
// This global array is where the serial routines will write the
// incoming servo settings that are received from BLE2.  This array
// is initialized in init().
//
servoSettings robotSettings[ROBOTS];

//
// servoInit() - initialize (attach) the two servos to the globals
//		 declared above.
//
void servoInit()
{
     leftServo.attach(9);
     rightServo.attach(10);
}

//
// servoSet() - sets the speed of the servos for this robot.  Note
//		that the servos for the Arduino library are set from 0
//		to 180, where "off" is 90.  This routine maps the
//		incoming 0 to 255 to that range.
// SERVO NOTES
//
// After using "servo explore" - it appears that the Parallax CR servos have useful
// differentiaion of speed from 1350 to 1650 where 1500 is the center.
//
void servoSet(int left, int right)
{
#define MIN_MS	1350
#define MAX_MS	1650

     // note that the leftServo is reversed from the right

     leftServo.writeMicroseconds(map(left,0,255,MIN_MS,MAX_MS));
     rightServo.writeMicroseconds(map(right,0,255,MAX_MS,MIN_MS));

}

void servoSetFromSettings(int me)
{
     servoSet(robotSettings[me].left,robotSettings[me].right);
}

//
// serialInit() - initialize the serial connection to the BLE2 module.
//
void serialInit()
{
  // first, put the serial port at the right speed
  // tell the BLE2 to start receiving broadcasts
  
  Serial.begin(38400);

  serialInputFlush();

  Serial.write("J,1\n");  // puts the BLE2 in Observer role

  // we wait for the AOK or ERR, but don't do anything if it is an ERR
  // there's not much we can do anyway

  serialReadline();

  // set BLE2 to scan every 50ms for 30ms each time
  // Serial.write("F,0032,001D\n");	// seems to error
  // set BLE2 to scan every 100ms for 75ms each time
  //Serial.write("F,0064,004b\n");
  // now go 50,50 - seems to do best
  Serial.write("F,0032,0032\n");

  serialReadline();

  // at this point the serial buffer should be clear and will start
  // receiving broadcasts
}

// 
// serialReadline() - read an entire "line" from the serial port.
//              And by "line" we mean characters up to the newline from
//		from the BLE.  This code knows, too, that the BLE will
//		return "\r\n" at the end of every line.  The number of
//		characters received will NOT include the \n or \r.
//		NOTE - this routine just does a data read from
//		the serial port - THEREFORE - it is possible that
//		'\0' characters can be in the mix.  So this routine
//		does NOT try to terminate the incoming data with
//		a '\0' - the caller should deal with incoming data including
//		NULL termination of desired.
//
int serialReadline(char *buffer,int max)
{
  char  c;
  int   i;
  
  for(i=0; i < max; i++) {
       while(Serial.available() <= 0) {		// wait for data available
       }
       c = Serial.read();
       if (c == '\n') {		// wait for the newline
	    break;
       }
       *buffer++ = c;
  }

  // at this point we are sitting at max or on top of the newline

  if(i != 0 && *(buffer-1) == '\r') {	// punt the return if it's there
       i--;
  }

  return(i);
}

//
// serialReadline() - special form of serialReadline that simply
//			reads a line from the input and dumps it.
//
void serialReadline()
{
     char	lineBuffer[MAXLINE];

     serialReadline(lineBuffer,MAXLINE);
}

//
// serialInputFlush() - flush out any data that is currently sitting in
//			the input queue - or lands there during this routine's
//			operation.
//
void serialInputFlush()
{
     while(Serial.peek() != -1) {
	  Serial.read();
     }
}

//
// hex2int() - get the hex value of a string.  This was found
//              at http://forum.arduino.cc/index.php?topic=105227.0
//
unsigned long hex2int(char *a, unsigned int len)
{
   int i;
   unsigned long val = 0;

   for(i=0;i<len;i++)
      if(a[i] <= 57)
       val += (a[i]-48)*(1<<(4*(len-1-i)));
      else
       val += (a[i]-55)*(1<<(4*(len-1-i)));
   return val;
}

//
// serialGetServoSettings() - get the settings of the servos from the
//			      BLE2 module on the serial port.  Returns
//			      TRUE if the returned values were good, or
//			      FALSE otherwise (the values should be
//			      ignored, and may have been overwritten).
//			      Normally this routine will sit and wait
//			      for a message, so normally it will return
//			      TRUE.  The values for the servos are written
//			      into the global array robotSettings().
//
int serialGetServoSettings()
{
     char	lineBuffer[MAXLINE];
     char	MACID[13];
     int	addressType;
     long	RSSI;
     int	i;
     int	wasNegativeRSSI;
    
     // format of the data is (for example):
     //
     // 001EC02495D1,0,-3A,Brcst:AABBCC
     // 0000000000111111111122222222222
     // 0123456789012345678901234567890
     //
     // <48bit MAC address>,<1bit Address Type>,
     //   <8bit RSSI value>,Brcst:<broadcast message>
  
     // we have to get messages of at least 24 bytes, or it
     // is definitely NOT a broadcast message  
  
     if(serialReadline(lineBuffer,MAXLINE) > 24) {
    
	  strncpy(MACID,lineBuffer,12);

	  if(strncmp(MACID,"001EC02495D1",12) == 0) { 
    
	       addressType = lineBuffer[13] - '0';
    
	       if(lineBuffer[15] == '-') {
		    wasNegativeRSSI = true;
		    RSSI = -hex2int(lineBuffer+16,2);
	       } else {
		    wasNegativeRSSI = false;
		    RSSI = hex2int(lineBuffer+15,2);
	       }
      
	       // at this point the servo settings are in the "message"
	       // portion of the broadcast.  Currently there are four
	       // robots defined, each with two servos, starting at
	       // byte 25 or 24 (depending upon negative RSSI):
	       //
	       //  pos  0  1   2  3   4  5   6  7   8  9  10 11  12 13  14 15
	       //  byte   0      1      2      3      4      5      6      7
	       //  robot  1      1      2      2      3      3      4      4
	       //  servo left  right   left  right   left  right   left  right

	       int position = (wasNegativeRSSI?25:24);
	       for(int i=0; i < ROBOTS; i++, position += 4) {
		    robotSettings[i].left = hex2int(lineBuffer+position,2);
		    robotSettings[i].right = hex2int(lineBuffer+position+2,2);
	       }
	
	       return(true);
	  }
     }

     return(false);
}

void setup()
{
     pinMode(8,OUTPUT);
     digitalWrite(8,LOW);

     for(int i = 0; i < ROBOTS; i++) {
	  robotSettings[i].left = SERVO_OFF;
	  robotSettings[i].right = SERVO_OFF;
     }

     servoInit();
     serialInit();
}

void loop()
{
     if(serialGetServoSettings()) {
	  servoSetFromSettings(ME);
     }
}


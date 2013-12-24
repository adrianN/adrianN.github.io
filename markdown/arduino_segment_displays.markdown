% Segment displays with an Arduino
% Adrian Neumann (adrian_neumann@gmx.de)

Things You Will Need
====================

* Your Arduino
* A breadboard
* A segment display
* 4 Resistors (at least 110Ohms)
* (optional) a button

Testing things (Optional)
===================

First I like to use buttons and my fingers instead of logic on the Arduino to make segments glow. I use the Arduino only as a power source.

I download the data sheet for my segment display from [here](http://www.lumex.com/specs/LDQ-M516RI.pdf). From there I learn that it takes 1.8V and 30mA. Since my Arduino puts out 5V, I need a resistor. I want to have the resistor and the LED of a segment in series, so I need a (5V-1.8V)/30mA=107Ohm resistor. Since I don't really trust my math and less power never fries LEDs, I choose a big resistor with 1kOhm.

My segment display has a common anode for all LEDs in a digit. I want to start with the rightmost digit, so I connect pin 6 with +, with my resistor in series. As the dot is the least important part of my segment display and I worry least about frying it, I will try to get the dot to light up. The dot is connected to pin 3. So I connect pin three with ground via a push button.

Indeed, when I push the button, the dot glows. Decently bright, even though I used a large resistor. Now I feel confident to replace the button with software control.

Displaying a single digit
=========================

I wire up all the segments with IO pins on my Arduino, starting with pin 12. Now it is time to program the Arduino. Let's first check whether we can light up each segment one after the other. So I fire up my Arduino software. I write the following code

	const int segments[] = {12,11,10,9,8,7,6};

	void setup() {
	  for(int i=0; i<7; ++i) {
	    pinMode(segments[i], OUTPUT);
	  }
	}

	void loop() {
	  for(int i=0; i<7; ++i) {
	    int led = segments[i];
	    digitalWrite(led, LOW);
	    delay(500);
	    digitalWrite(led, HIGH);
	  }
	}

Note that I have to set the output to LOW to turn the segment on, because it has a common anode. If the output is HIGH, eg. +5V, no current will flow.

It seems that I wired things up correctly. Time to display some digit. I make an array that contains the LOW HIGH patterns for each digit. I also write a function that loops over the array and sets the pins. The code now looks like this.

	const int segments[] = {12,11,10,9,8,7,6};
	const int digit[10][7] = {
	  {LOW, LOW, LOW, LOW, LOW, LOW, HIGH},
	  {HIGH, LOW, LOW, HIGH, HIGH, HIGH, HIGH},
	  {LOW, LOW, HIGH, LOW, LOW, HIGH, LOW},
	  {LOW, LOW, LOW, LOW, HIGH, HIGH, LOW},
	  {HIGH, LOW, LOW, HIGH, HIGH, LOW, LOW},
	  {LOW, HIGH, LOW, LOW, HIGH, LOW, LOW},
	  {HIGH, HIGH, LOW, LOW, LOW, LOW, LOW},
	  {LOW, LOW, LOW, HIGH, HIGH, HIGH, HIGH},
	  {LOW, LOW, LOW, LOW, LOW, LOW, LOW},
	  {LOW, LOW, LOW, HIGH, HIGH, LOW, LOW}
	};

	void  display_digit(int which) {
	  for(int i=0; i<7; ++i) {
	    digitalWrite(segments[i], digit[which][i]);
	  }
	}

	void setup() {
	  for(int i=0; i<7; ++i) {
	    pinMode(segments[i], OUTPUT);
	  }
	}

	void loop() {
	 for(int i=0; i<10; ++i) {
	    display_digit(i);
	    delay(500);
	  } 
	}

After I turn in on, my Arduino now counts from 0 to 9. Since I wired up the anode for the first digit of my segment display, the first digit lights up.

Displaying more digits
======================

Okay, now I want to display more than one digit. To do so, I will wire up the anodes of each digit with a pin on my Arduino. I don't forget to add a resistor there too. Then I can display digits in quick succession and make it look like I display them simultaniously. Now the code looks like this.

	const int segments[] = {12,11,10,9,8,7,6};
	const int digit[] = {2,3,4,5};
	const int digit_pattern[10][7] = {
	  {LOW, LOW, LOW, LOW, LOW, LOW, HIGH},
	  {HIGH, LOW, LOW, HIGH, HIGH, HIGH, HIGH},
	  {LOW, LOW, HIGH, LOW, LOW, HIGH, LOW},
	  {LOW, LOW, LOW, LOW, HIGH, HIGH, LOW},
	  {HIGH, LOW, LOW, HIGH, HIGH, LOW, LOW},
	  {LOW, HIGH, LOW, LOW, HIGH, LOW, LOW},
	  {HIGH, HIGH, LOW, LOW, LOW, LOW, LOW},
	  {LOW, LOW, LOW, HIGH, HIGH, HIGH, HIGH},
	  {LOW, LOW, LOW, LOW, LOW, LOW, LOW},
	  {LOW, LOW, LOW, HIGH, HIGH, LOW, LOW}
	};

	void  display_digit(int which, int pos) {
	  for(int i=0; i<4; ++i) {
	    digitalWrite(digit[i], LOW);
	  }
	  for(int i=0; i<7; ++i) {
	    digitalWrite(segments[i], digit_pattern[which][i]);
	  }
	  digitalWrite(digit[pos], HIGH);
	}

	void setup() {
	  for(int i=0; i<7; ++i) {
	    pinMode(segments[i], OUTPUT);
	  }
	  for(int i=0; i<4; ++i) {
	    pinMode(digit[i], OUTPUT);
	  }
	}

	void loop() {
	    display_digit(0,0);
	    display_digit(1,1);
	    display_digit(2,2);
	    display_digit(3,3);
	}

It is important that I first turn the digit off, then set the output segments and then turn the digit on in the `display_digit` function. Otherwise things don't look right because the old digit is changed before it is switched off, or the new digit displays the wrong things before it is changed to the right values.

I notice that the display is much darker than before. That makes sense because now every digit is on only a quarter of the time. I therefore replace the resistors. I also notice that numbers that light up more segments are darker. Again this makes sense since the current is divided among more LEDs. I could fix that by using the PWM pins on my Arduino as anodes and adjust brightness depending on how many segments are on, but I decide against that.

Doing something while displaying digits
=======================================

To do something else besides displaying digits, I use the timer functions. I count occasionally and at all other times I display the number. The final code looks like this

	const int segments[] = {12,11,10,9,8,7,6};
	const int digit[] = {2,3,4,5};
	const int digit_pattern[10][7] = {
	  {LOW, LOW, LOW, LOW, LOW, LOW, HIGH},
	  {HIGH, LOW, LOW, HIGH, HIGH, HIGH, HIGH},
	  {LOW, LOW, HIGH, LOW, LOW, HIGH, LOW},
	  {LOW, LOW, LOW, LOW, HIGH, HIGH, LOW},
	  {HIGH, LOW, LOW, HIGH, HIGH, LOW, LOW},
	  {LOW, HIGH, LOW, LOW, HIGH, LOW, LOW},
	  {HIGH, HIGH, LOW, LOW, LOW, LOW, LOW},
	  {LOW, LOW, LOW, HIGH, HIGH, HIGH, HIGH},
	  {LOW, LOW, LOW, LOW, LOW, LOW, LOW},
	  {LOW, LOW, LOW, HIGH, HIGH, LOW, LOW}
	};

	void  display_digit(int which, int pos) {
	  for(int i=0; i<4; ++i) {
	    digitalWrite(digit[i], LOW);
	  }
	  for(int i=0; i<7; ++i) {
	    digitalWrite(segments[i], digit_pattern[which][i]);
	  }
	  digitalWrite(digit[pos], HIGH);
	}

	void setup() {
	  for(int i=0; i<7; ++i) {
	    pinMode(segments[i], OUTPUT);
	  }
	  for(int i=0; i<4; ++i) {
	    pinMode(digit[i], OUTPUT);
	  }
	}

	void count(int number[]) {
	  number[0]++;
	  for(int i=0; i<3; ++i) {
	    if (number[i]==10) {
	      number[i]=0;
	      number[i+1]++;
	    }
	  }
	  if (number[3]==10) {
	    number[3]=0;
	  }
	}

	void loop() {
	  unsigned long time = millis();
	  int number[4] = {0};
	  while(true) {
	    if (millis()-time>100) {
	      count(number);
	      time=millis();
	    }
	    for(int i=0; i<4; ++i) {
	      display_digit(number[i],i);
	    }
	  }
	}
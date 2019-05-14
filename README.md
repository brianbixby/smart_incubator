![alt text](https://raw.githubusercontent.com/brianbixby/smart_incubator/master/Images/final.jpg "Smart Incubator")
**WHO**

I lead a team of **42 Robotics Lab students** that teamed up with **Stanford Bioengineering researchers** in the [Endy Lab](https://openwetware.org/wiki/Endy_Lab) to create a smart-incubator for their mushroom-related research.

**WHAT**

My team created an **open-source intelligent robotic system** for distributed bioproduction research. Our system automatically tracks the progress of research experiments in a regulated environment that users can change in real time at the click of a button, and can view the real time results via an online dashboard. Building costs are roughly **5-10 times less** than the price of commercially available versions, and up to **100 times less** than higher-end models.

**WHY**

Mycelium (the vegetative portion of mushrooms) materials are at the **forefront of sustainability** because of the wide variety of applications: from textiles in the form of leather replacements to building materials to pharmaceuticals to mycoremediation (using fungi-based technology for environmental decontamination.)  So my team developed an easy-to-use, cost-effective smart incubator that automates much of the labor-intensive work.
IMG_0463.JPG
**HARDWARE COMPONENTS:**
* 12V Power Supply
* DC DC Converter
* Raspberry Pi (0W)
* 2 Peltier Modules (thermoelectric heaters)
* DHT 11 (temperature and humidity sensor)
* USB Camera
* LED light strip
* Arduino Mega 2560
* Ramps 1.4 (Arduino shield used to control the stepper motor)
* Stepper Motor
* Stepper Motor Driver
* ESP-8266 (WI-FI module used to control backup system)
* Temperature sensor
* 8 Channel Relay
* DB25-M2 Connector (repurposed printer cable)

**TECHNICAL OVERVIEW:**
+ **Raspberry Pi:** runs the Temperature Uploader script which monitors the temperature and humidity (pin GCKLO4) with a DHT11 thermometer/humidity sensor and regulates the temperature (GPIO17) by controlling the Peltier Modules. The Pi is also responsible for sending GRBL commands that rotate the stepper motor it does this by creating a serial (UART) connection (5v, gnd, GPIO14, GPIO15) with the Arduino Mega through Ramps, which controlls the stepper motor. The Raspberry Pi also controls the LED lights (PWMO18), and camera through the microusb port.

+ **Arduino Mega and Ramps:** have one sole purpose: rotating the stpper motor. Again, the Pi sends GRBL commands via a serial connection to the Arduino, which utilizes Ramps to rotate the stepper motor and then sends a notification back to the Pi when it's done.

+ **8 Channel Relay:** acts as a switch to turn on and off the Peltier Modules (heaters), LED lights and also the emergency shut-off to the Pi itself.

+ **ESP8266:** runs the backup system, incase the incubator surpasses a preset threshold (which turns the Pi off). The backup system sends users a text message notification (this is set up by using twilio in conjunction with thingspeak) alerting them. Because the ESP8266 comes equipped with it's own thermometer, once the temperature is back within range the Raspberry Pi will automatically boot back up. 

+ **DB25-M2 Connector:** is a repurposed printer cable that is used to create an easily detachable compartmentalized "Brain Box" that is separate from the incubator itself. This way if there is something goes wrong or needs fixing all you have to do is disconnect the "Brain Box" from the rest of the incubator to troubleshoot.

**MY CONTRIBUTIONS**

I was the 2nd generation of 42 RoboLab Students to work on this project. With that said, I was only given a broken prototype with zero documentation and told to fix the bugs and improve the project in some way (what I was given is pictured below).

![alt text](https://raw.githubusercontent.com/brianbixby/smart_incubator/master/Images/IMG_0463.JPG "Broken Prototype")

I had 5 teammates come and go during the coure of this project, but I was involved in every aspect of the project except for 3D printing custom plastic pieces. I debugged and fixed the initial prototype, redesigned/simplified the system's wiring and hardware layout. Added new functionality, including a detachable "Brain Box", a second stepper motor that works in unison with the first (doubling the number of samples that the incubator can hold). Lastly, I actually built out and assembled the incubator itself and created documentation (howto.txt) for future generations of 42 Students so knowledge loss in minimized and they are able to improve upon my design.

**DETAILED INSTRUCTIONS**

For detailed instructions on how to recreate this project yourself please read the HOWTO.md.
              
              
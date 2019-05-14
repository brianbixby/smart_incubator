**PROJECT LAYOUT**

* app - HTML app. Host it anywhere to have the web UI.

* ArduinoMega-2560 - Goes on the mega, used to drive RAMPS.

* ESP-8266 - Backup system goes on the ESP8266.

* RaspberryPi-0W - Goes on the raspi. Shoud be in the home folder, i.e. /home/pi/Pycotronics.

**USER/PASSWORD**

* If you use the recommended OS link below(a working clone of the Raspberry Pi used for this project)

    - user/password for the `recommended` raspi is pi/raspberry
    
    You can access it with ssh pi@raspberrypizzle2.local
    
    [Raspi Copy Link (Recommended)](https://drive.google.com/file/d/1eDRG-dHGEy0Bqikq-4YRSVNHcihzqKau/view?usp=sharing)

    - user/password for the `generic` raspi is pi/raspberry
    
    You can access it with ssh pi@raspberrypi.local
    
    [Raspbian 0S Link (Generic)](https://drive.google.com/file/d/1VSevMT91YZMNc5AJt7uOJ1KNMEJVltwO/view?usp=sharing)

**SOFTWARE HOW TO (for MAC):**
##### Step 1: Install OS to SD card: 
* wipe sd card: 
    * use sdformatter or Disk Utility to wipe card, needs to be MS-DOS (FAT32) then unmount.
* unzip then flash the g-zipped file with the raspberry Pi OS onto a micro SD card:
    * ```sudo dd bs=1m if=path/to/raspberrypicopy of=/path/sd/card conv=sync```
        ###### hint: run diskutil list to get path to sd card (ex. output /dev/disk2) 
* Enable WIFI and SSH(your computer will need to be on the same WIFI as the Pi to SSH in!!!) with SD card still in computer.
    * add empty ssh file to root of sd card (/Volumes/boot)
                (ex. touch /Volumes/boot/ssh)
    * add wpa_supplicant.conf file to root of sd card (ex. /Volumes/boot/wpa_supplicant.conf) with text below:
        ```
            ctrl_interface=DIR=/var/run/wpa_supplicant GROUP=netdev
            update_config=1
            country=US

            network={
                ssid="wifi_networkname"
                psk="wifi_password"
                key_mgmt=WPA-PSK
                scan_ssid=1
            }
        ```
        ###### hint: [click here](https://www.howtogeek.com/214053/how-to-turn-your-mac-into-a-wi-fi-hotspot/) to make your own hot spot from an imac with ethernet.

* safely eject sd card from your MAC and insert it into the Pi and turn the pi on.
* ssh pi@raspberrypi.local (if raspberryPi name is different then ssh pi@differentname.local)
    ###### hint: ssh pi@raspberrypizzle2.local
* ssh-keygen -R raspberrypi.local (first time only)
* ssh pi@raspberrypi.local -> yes -> raspberry
        from now on connecting is easy (ssh pi@raspberrypi.local-> yes -> password: raspberry)

#### ONLY COMPLETE STEP 2 IF YOU ARE NOT USING THE RECOMMENDED OS FILE.

##### Step 2: First time SSHing into Pi(update config settings)
* unzip and upload Mycotronics project to OS
    ```scp path/to/Mycotronics-backup pi@raspberrypi.local:~```
* ```sudo raspi-config```
    - enable camera
    - enable wifi (wpa_supplicant file only works the first time)
    - enable ssh
    - interfacing options => serial => no => yes
    ###### hint: you might need to modify more config settings later

* Follow RaspberryPi-0W Instructions for installing dependencies (pip install will take over night)
* compile init_Random (ex. ```gcc -o init_random init_random.c```)
    ```bash
    sudo apt update
    sudo apt upgrade -y
    sudo apt install -y python-dev pip screen python-opencv
    sudo pip install Adafruit_DHT pyserial firebase-admin gpiozero
    ```
    ###### hint: screen -d then screen -r will be helpful to view logs when running tempuploader.py, but detach the screen similarly for the overnight pip install**
    
* code below is actual working code to add to etc/rc.local file, below that is code to run the demo script. Comment one of these out!!!
    ```
    /home/pi/init_random && sudo -u pi screen -dmS uploader python /home/pi/temperatureUploader.py
    
    sudo -u pi screen -dmS uploader python /home/pi/demo.py
    ```

    ###### hint: sudo vim /etc/rc.local (this file runs commands on boot, (screen -d, screen -r processid to see print statements of background programs running.))
    ###### READ https://github.com/firebase/firebase-admin-python/issues/234 comments by Alexdrean
    
##### Step 3: Install grbl script to Arduino Mega
* follow instructions on grbl for cyclone
    - link to original repo https://github.com/carlosgs/grblForCyclone 
* Install Arduino Ide to your mac
    - https://www.arduino.cc/en/Main/Donate
    - There is a weird bug with arduino ide, every time you restart the program go to preferences then check or uncheck the display line numbers (I submitted a bug report, but am unsure if it's fixed)
    * connect arduino to mac via usb
    * click on tools,board choose Arduino/Genuino Mega
    * click on tools then choose port
    * file, examples, eeprom, eeprom clear, upload to arduino
    * now you will open the grblforcyclone file and try to upload that to the Arduino
    * from the arduino ide you can use the serial monitor to set the default GRBL values per the grblforcyclone instructions.

##### Step 4: Install Mycotronics onto esp8266
* download platformio for atom
    - install the silabsusbdriverdisk.dmg for the esp8266
* Open Atom and create a new platformio project with the board: NodeMCU 1.0 (ESP-12E Module), framework: esp8266 non-os sdk
    - the framework could be different, but I believe this is correct
        open the files for the project or copy them over and flash it.

**HARDWARE SUMMARY:**
The **Raspberry Pi** runs the temperature uploader script which monitors the temperature and humidity (pin GCKLO4) with a DHT11 thermometer/humidity sensor and regulates the temperature (GPIO17) by controlling the heaters. The Pi is also responsible for sending the command that rotates the carousel it does this by creating a serial uart connection (5v, gnd, gpio14, gpio15) with the Aruino Mega 8550 through ramps, which controlls the stepper motor. The Raspberry Pi also controls the lights (PWMO18), and camera through the microusb usb port.

The **Arduino Mega and Ramps 1.4** have one sole responsibility controlling the carousel. There is an end stop or limit switch (please Google and watch a video on how the end stop works, and when it should be triggered aka 1.5x max distanced traveled 539 degrees and when it should be triggered does it hit the end stop once or twice?). There is also the x control axis which is wired directly to the stepper motor. Very importantly there is a small chip that sits next to the x control axis, this chip is the stepper driver. *** PLEASE GOOGLE *** There is a bunch of potential energy that can be released or bottled by tightening or loosening the screw on this chip. Tightening the stepper driver allows you to compensate for an increase in resistance (ex. increase in length of wires or a 2nd stepper added). If your stepper is making a hissing sound or shakes violently/only homes then this should be adjusted. There is a great Youtube video on it https://www.youtube.com/watch?v=XU6lgFeZ7ZQ.

The **relay** acts as a switch with input pins and corresping outputs, each output has 3 sockets: normally open, normally closed and common. There is a little drawing on the high voltage/output/socket side of the relay which describes the sockets. A closed connection is a complete connection meaning if there is no input then both normally closed and common are active. If there is a input then normally closed becaomes inactive and normally open creates a closed circuit with common.

The **adapter's** purpose is to create an easily detachable compartmentalized "Brain Box" that is separate from the incubator itself. This way if there is something that goes wrong or needs fixing we are able to disconnect the brain box from the rest of the incubator and we can leave Rolando with the incubator itself.

The **ESP8266** is the emergency cutoff system for the Raspberry Pi if the temperature in the incubator surpasses a preset threshold. It will send users a text message (this is set up by using twilio in conjunction with thingspeak) alerting them. Because the ESP8266 comes equipped with it's own thermometer, once the temperature is back within range the Raspberry Pi will automatically boot back up.

**HARDWARE CONNECTIONS:**
##### Power supply
- **outputs:**
    - 12v => 12v hub
    - GND => DC DC Converter

##### DC DC Converter
- **inputs:**
    - 12v <= 12v hub
    - gnd <= Powersupply
- **outputs:**
    - 5v => 5v hub
    - gnd => gnd hub
##### 5v hub
- **inputs:**
    - 5v <= 5v dc dc converter
- **outputs:**
    - 5v => relay vcc
    - 5v => relay raspberry pi output
    - 5v => adapter to power dht11 thermometer
    - 5v => adapter to power humidifier
    - 5v => adapter to power backup thermometer
    - 5v => vin esp8266
##### 12v hub
- **inputs:**
    - 12v <= 12v power supply
- **outputs:**
    - 12v => ramps (2x)
    - 12v => relay light output
    - 12v => relay heaters output
    - 12v => dcdc input
##### ground hub
- **inputs:**
    - gnd <= dc dc output
- **outputs:**
    - all grounds
##### ramps
- **inputs:**
    - 12v(2x) <= 12v hub
    - gnd(2x) <= gnd hub
- **outputs:**
    - x axis labeled in link below(4 wires for stepper motor) => adapter
        http://domoticx.com/wp-content/uploads/2017/05/RAMPS-Shield-1.4-bovenkant-legenda.jpg
    - aux 1(4x)(5v, gnd, a3, a4) => raspberry pi(5v, gnd, gpio14, gpio15) (uart serial connection to Raspberry Pi)
        ###### hint: uart tx and rx pins for pi and ramps
    - x end stop data => adapter
        http://3d.robbroek.nl/wp-content/uploads/2014/08/untitled-50242.jpg
##### relay
- **inputs:**
    - vcc <= 5v hub
    - gnd <= gnd hub
    - lights input <= raspi PWMO18
    - heater input <= raspi GPIO17
    - raspi input <= esp8266 gpio16
- **outputs:**
    - lights output (12v) => adapter(2x)
    - heaters output (12v) => adapter(4x)
    - raspi output (5v) => raspi microusb power
##### esp8266
- **inputs:**
    - vin <= 5v hub
    - gnd <= gnd hub
- **outputs:**
    - gpio16 => relay raspberry pi input
    - gpio5 => adapter backup thermometer data
##### raspberry pi
- **inputs:**
    - 5v <= microusb power from relay output that controls Raspberry pi
- **outputs:**
    - camera => microusb usb to camera or dongle if there are multiple cameras
    - PWMO18 => relay input to control the lights
    - GPIO17 => relay input to control heaters
    - GCKLO4 => adapter for dht11 data
    - 5v, gnd, gpio14, gpio15(4x) => ramps aux 1(5v, gnd, a3, a4) uart serial connection
    ###### hint: uart tx and rx pins for pi and ramps **
##### adapter
- **inputs:**
    - dht 11 data <= dht11 data
    - all ground (dht 11, backup thermometer, both fans, both heaters, lights, humidifier) <= gnd hub
- **outputs:**
    - 4 gnd, 4 12v => heaters
    - 1 gnd, 1 5v, 1 dht data => dht11
    - 1gnd 1 5v => humidifier
    - 2 12v 2 gnd ???=> fans
    - 1 12v, 1 gnd => lights
    - 1 gnd, 1 x end stop data => x end stop
    - data, gnd, 5v => backup thermometer

# Pycotronics

## How to install
raspi:
```bash
sudo apt update
sudo apt upgrade -y
sudo apt install -y python-dev pip screen python-opencv
sudo pip install Adafruit_DHT pyserial firebase-admin gpiozero
git clone https://github.com/BullCheat/Pycotronics.git /home/pi/Pycotronics
```

Add `sudo -u pi screen -dmS uploader python /home/pi/Pycotronics/temperatureUploader.py` to /etc/rc.local
Don't forget https://github.com/BullCheat/mycotronics_dms on the esp

Firebase:

![Default firebase settings](https://raw.githubusercontent.com/BullCheat/Pycotronics/master/default_database_settings.png)
# used gps hat
- https://www.waveshare.com/wiki/GSM/GPRS/GNSS_HAT

# links
- https://austinsnerdythings.com/2021/09/29/millisecond-accurate-chrony-ntp-with-a-usb-gps-for-12-usd/

# todos
- timeserver
  - testing
- HW button(s)
  - power on off GPS module
  - retrieve time via GPS
- LED(s)
  - showing status, blinking,...
- how long power up with all connected hardware

# testing
## gps modul install steps on rapsberry 2
- use standard raspberian OS
- update repos
- enable serial port
- LOCALE einstellungen zu DE
  - zur not: sudo dpkg-reconfigure locales
- add user to "dialout" group
  - sudo usermod -a -G dialout $(whoami)
- python dependencies
  - sudo apt install python3-serial

# raspberry pi zero 2 W

- credentials for ssh: login: time, pw: machine
- name of device (in LAN): timemachine

apt-key list
sudo apt-key export 7FA3303E | sudo gpg --dearmor -o /tmp/raspi.gpg (take correct name of filename from 1. command)
file /tmp/raspi.gpg
sudo apt-key del 7FA3303E
sudo mv /tmp/raspi.gpg /etc/apt/trusted.gpg.d/
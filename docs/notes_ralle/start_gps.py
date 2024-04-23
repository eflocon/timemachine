import RPi.GPIO as GPIO
import serial
import time
from datetime import datetime
import subprocess

PWRKEY: int
ser: serial.Serial


def initialize():
    global ser, PWRKEY
    ser = serial.Serial('/dev/serial0', 9600, timeout=1)
    PWRKEY = 4
    GPIO.setmode(GPIO.BCM)


# this works, dont ask me why
def power_toggle_module():
    print("----------- power_toggle_module start")
    GPIO.setup(PWRKEY, GPIO.IN)
    time.sleep(4)

    GPIO.setup(PWRKEY, GPIO.OUT)
    time.sleep(4)
    print("----------- power_toggle_module end\n")


def gpio_cleanup():
    print("----------- gpio_cleanup start")
    GPIO.cleanup()
    time.sleep(4)
    print("----------- gpio_cleanup end\n")


def power_on_gps():
    print("----------- power_on_gps start")
    ser.write(b'AT+CGNSPWR?\r\n')
    time.sleep(1)
    response = ser.read_all()
    print(response)

    if "CGNSPWR: 0" in response.decode():
        print("POWER is up, but internally is set to 0, will POWER UP")
        ser.write(b'AT+CGPSPWR=1\r\n')
        time.sleep(1)
        response2 = ser.read_all()
        print(response2)
    elif "CGNSPWR: 1" in response.decode():
        print("POWER is internally up")

    print("----------- power_on_gps end\n")


def is_gps_module_powered_up() -> bool:
    print("----------- is_gps_module_powered_up start")
    is_powered_up: bool
    ser.write(b'AT+CGNSPWR?\r\n')
    time.sleep(1)
    response = ser.read_all()
    print(response)

    if "NORMAL POWER DOWN" in response.decode():
        print("NORMAL POWER DOWN")
        is_powered_up = False
    elif len(response.decode()) == 0:
        print("b'' in response")
        is_powered_up = False
    elif "CGNSPWR: 0" in response.decode():
        print("POWER is up, but internally is set to 0")
        is_powered_up = True
    else:
        is_powered_up = True

    print("returning: ", is_powered_up)
    print("----------- is_gps_module_powered_up end\n")
    return is_powered_up


def get_gps_data():
    ser.write(b'AT+CGPSINF=0\r\n')
    time.sleep(1)
    response = ser.read_all()
    return response


def parse_date_time(response) -> datetime:
    try:
        date_time_str = response.decode().split(',')[4]
        date_time_obj = datetime.strptime(date_time_str, '%Y%m%d%H%M%S.%f')
        print(date_time_obj)
        return date_time_obj
    except ValueError:
        print(f"Could not parse date and time from '{date_time_str}'")
    except IndexError:
        print("The expected data was not found in the response. Is GPS module switched on?")


def setDate():
    is_date_plausible: bool = False
    temp_time: datetime

    while not is_date_plausible:
        response = get_gps_data()
        temp_time = parse_date_time(response)
        if temp_time is not None and temp_time.year == 2024:
            is_date_plausible = True
            print(f"Plausible date and time: {temp_time}")

    command = f"date -s '{temp_time}'"
    subprocess.run(command, shell=True, check=True)


def main():
    initialize()

    if not is_gps_module_powered_up():
        power_toggle_module()
        power_on_gps()
    else:
        power_on_gps()

    # start actual work
    setDate()
    # end actual work

    power_toggle_module()
    gpio_cleanup()
    ser.close()


if __name__ == "__main__":
    main()

import os
import time
import signal
import sys
import RPi.GPIO as GPIO

FAN_PIN = 12
BATTERY_PIN = 18

TARGET_TEMPERATURE = 45
PWM_FREQUENCY = 50

INITIAL_FAN_SPEED = 100
CONTROL_PERIOD = 2

P_FACTOR = 15
I_FACTOR = 0.75
D_FACTOR = 0.25

TOTAL_LIMIT = 30
FAN_SPEED_LIMIT = 40


# fetches the current CPU temperature as a float.
def fetch_temperature():
    result = os.popen("vcgencmd measure_temp").readline()
    temperature = result.replace("temp=", "").replace("'C\n", "")
    return float(temperature)


def handle_fan(pwm):
    total = 0
    diff_diff = 0
    old_diff = 0

    while True:
        temperature = fetch_temperature()
        diff = temperature - TARGET_TEMPERATURE
        total = total + diff
        diff_diff = diff - old_diff
        old_diff = diff

        pDiff = diff * P_FACTOR
        iDiff = total * I_FACTOR
        kDiff = diff_diff * D_FACTOR

        fan_speed = pDiff + iDiff + kDiff

        fan_speed = 100 if fan_speed > 100 else FAN_SPEED_LIMIT if fan_speed < FAN_SPEED_LIMIT else fan_speed
        total = TOTAL_LIMIT if total > TOTAL_LIMIT else -TOTAL_LIMIT if total < -TOTAL_LIMIT else total

        print(f"Fan speed is {fan_speed}.")
        pwm.ChangeDutyCycle(fan_speed)
        time.sleep(CONTROL_PERIOD)


def initialize_pwm():
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(FAN_PIN, GPIO.OUT)
    pwm = GPIO.PWM(FAN_PIN, PWM_FREQUENCY)
    pwm.start(INITIAL_FAN_SPEED)
    GPIO.setup(BATTERY_PIN, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    GPIO.setwarnings(False)
    return pwm


def main():
    pwm = initialize_pwm()
    try:
        handle_fan(pwm)
    except KeyboardInterrupt:
        pwm.ChangeDutyCycle(0)
        GPIO.cleanup()


if __name__ == "__main__":
    main()

import RPi.GPIO as GPIO
from time import time, localtime
from dev_prototype import DevPrototype

class LED(DevPrototype):
    def __init__(self, pin=17, interval=1, start_time=0, end_time=17):
        self.pin = pin
        self.interval = interval
        self.start_time = start_time
        self.end_time = end_time
        self.state = False
        self.last_time = time()
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.pin, GPIO.OUT)
        print(f"LED on pin {self.pin} has been initialized.")

    def on(self):
        GPIO.output(self.pin, GPIO.HIGH)
        self.state = True

    def off(self):
        GPIO.output(self.pin, GPIO.LOW)
        self.state = False

    def within_time_range(self):
        current_time = localtime().tm_hour
        return self.start_time <= current_time < self.end_time

    def loop(self):
        if self.within_time_range():
            current_time = time()
            if current_time - self.last_time >= self.interval:
                if self.state:
                    self.off()
                    print(f"LED ({self.pin})가 꺼졌습니다!")
                else:
                    self.on()
                    print(f"LED ({self.pin})가 켜졌습니다!")
                self.last_time = current_time
        else:
            if self.state:
                self.off()
                print(f"LED ({self.pin})가 시간 범위 밖이라 꺼졌습니다!")

        self.share()

    def cleanup(self):
        GPIO.cleanup(self.pin)
        print(f"LED on pin {self.pin} has been cleaned up.")


class FAN(DevPrototype):
    def __init__(self, pin=27, interval=2, start_time=6, end_time=18):
        self.pin = pin
        self.interval = interval
        self.start_time = start_time
        self.end_time = end_time
        self.state = False
        self.last_time = time()
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.pin, GPIO.OUT)
        print(f"FAN on pin {self.pin} has been initialized.")

    def on(self):
        GPIO.output(self.pin, GPIO.HIGH)
        self.state = True

    def off(self):
        GPIO.output(self.pin, GPIO.LOW)
        self.state = False

    def within_time_range(self):
        current_time = localtime().tm_hour
        return self.start_time <= current_time < self.end_time

    def loop(self):
        if self.within_time_range():
            current_time = time()
            if current_time - self.last_time >= self.interval:
                if self.state:
                    self.off()
                    print(f"FAN ({self.pin})가 꺼졌습니다!")
                else:
                    self.on()
                    print(f"FAN ({self.pin})가 켜졌습니다!")
                self.last_time = current_time
        else:
            if self.state:
                self.off()
                print(f"FAN ({self.pin})가 시간 범위 밖이라 꺼졌습니다!")

        self.share()

    def cleanup(self):
        GPIO.cleanup(self.pin)
        print(f"FAN on pin {self.pin} has been cleaned up.")


class PUMP(DevPrototype):
    def __init__(self, pin=22, interval=3, start_time=9, end_time=21):
        self.pin = pin
        self.interval = interval
        self.start_time = start_time
        self.end_time = end_time
        self.state = False
        self.last_time = time()
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.pin, GPIO.OUT)
        print(f"PUMP on pin {self.pin} has been initialized.")

    def on(self):
        GPIO.output(self.pin, GPIO.HIGH)
        self.state = True

    def off(self):
        GPIO.output(self.pin, GPIO.LOW)
        self.state = False

    def within_time_range(self):
        current_time = localtime().tm_hour
        return self.start_time <= current_time < self.end_time

    def loop(self):
        if self.within_time_range():
            current_time = time()
            if current_time - self.last_time >= self.interval:
                if self.state:
                    self.off()
                    print(f"PUMP ({self.pin})가 꺼졌습니다!")
                else:
                    self.on()
                    print(f"PUMP ({self.pin})가 켜졌습니다!")
                self.last_time = current_time
        else:
            if self.state:
                self.off()
                print(f"PUMP ({self.pin})가 시간 범위 밖이라 꺼졌습니다!")

        self.share()

    def cleanup(self):
        GPIO.cleanup(self.pin)
        print(f"PUMP on pin {self.pin} has been cleaned up.")
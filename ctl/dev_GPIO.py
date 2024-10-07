import RPi.GPIO as GPIO
from time import time, localtime
from dev_prototype import DevPrototype

import RPi.GPIO as GPIO
from time import time, localtime
from dev_prototype import DevPrototype


class dev_GPIO(DevPrototype):
    def __init__(self, pin, on_time, off_time, name="GPIO", start_time=(0, 0), end_time=(23, 59)):
        self.pin = pin
        self.on_time = on_time  # 켜진 상태 지속 시간
        self.off_time = off_time  # 꺼진 상태 지속 시간
        self.name = name
        self.start_time = start_time  # 시작 시간 (시, 분 튜플로 받음)
        self.end_time = end_time  # 종료 시간 (시, 분 튜플로 받음)
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.pin, GPIO.OUT)
        self.last_time = time()
        self.state = False
        print(f"{self.name} on pin {self.pin} has been initialized.")

    def on(self):
        GPIO.output(self.pin, GPIO.HIGH)
        self.state = True  # 상태를 ON으로 저장

    def off(self):
        GPIO.output(self.pin, GPIO.LOW)
        self.state = False  # 상태를 OFF로 저장

    def within_time_range(self):
        """ 현재 시간이 시작-종료 시간 범위 내에 있는지 확인 """
        current_time = localtime()
        current_hour, current_minute = current_time.tm_hour, current_time.tm_min
        start_hour, start_minute = self.start_time
        end_hour, end_minute = self.end_time

        # 시작 시간과 종료 시간 사이에 있는지 확인
        if (start_hour, start_minute) <= (current_hour, current_minute) <= (end_hour, end_minute):
            return True
        return False

    def loop(self):
        """ GPIO 상태 제어 (시간 범위에 따라 ON/OFF) """
        if self.within_time_range():
            current_time = time()
            if self.state:
                if current_time - self.last_time >= self.on_time:  # 켜진 시간이 on_time을 넘으면
                    self.off()
                    print(f"{self.name} ({self.pin})가 꺼졌습니다!")
                    self.last_time = current_time
            else:
                if current_time - self.last_time >= self.off_time:  # 꺼진 시간이 off_time을 넘으면
                    self.on()
                    print(f"{self.name} ({self.pin})가 켜졌습니다!")
                    self.last_time = current_time
        else:
            if self.state:
                self.off()
                print(f"{self.name} ({self.pin})가 시간 범위 밖이라 꺼졌습니다!")

        self.share()

    def cleanup(self):
        GPIO.cleanup(self.pin)
        print(f"{self.name} on pin {self.pin} has been cleaned up.")

class LED(dev_GPIO):
    def __init__(self, pin=17, on_time=2, off_time=2, start_time=0, end_time=24):
        super().__init__(pin, on_time, off_time, name="LED", start_time=start_time, end_time=end_time)

class FAN(dev_GPIO):
    def __init__(self, pin=27, on_time=2, off_time=2, start_time=6, end_time=18):
        super().__init__(pin, on_time, off_time, name="FAN", start_time=start_time, end_time=end_time)

class PUMP(dev_GPIO):
    def __init__(self, pin=22, on_time=3, off_time=3, start_time=9, end_time=21):
        super().__init__(pin, on_time, off_time, name="PUMP", start_time=start_time, end_time=end_time)
import RPi.GPIO as GPIO
from time import time, localtime
from dev_prototype import DevPrototype

import RPi.GPIO as GPIO
from time import time, localtime
from dev_prototype import DevPrototype

class GPIODevice(DevPrototype):
    def __init__(self, pin, on_time=1, off_time=1, start_time="0:0", end_time="23:59", name="Device"):
        self.pin = pin
        self.on_time = on_time  # 켜짐 시간
        self.off_time = off_time  # 꺼짐 시간
        self.name = name
        self.start_time = self.convert_time(start_time)  # 시작 시간
        self.end_time = self.convert_time(end_time)  # 종료 시간
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.pin, GPIO.OUT)
        self.last_time = time()  # 기준 시간 저장
        self.state = False  # 현재 상태 (ON/OFF)
        print(f"{self.name} on pin {self.pin} has been initialized.")

    def convert_time(self, time_str):
        """시:분 형식을 초 단위로 변환"""
        hours, minutes = map(int, time_str.split(":"))
        return hours * 3600 + minutes * 60

    def within_time_range(self):
        """현재 시간이 설정된 시간 범위 내에 있는지 확인"""
        current_time = localtime().tm_hour * 3600 + localtime().tm_min * 60  # 현재 시와 분을 초로 변환
        return self.start_time <= current_time < self.end_time

    def on(self):
        GPIO.output(self.pin, GPIO.HIGH)
        self.state = True

    def off(self):
        GPIO.output(self.pin, GPIO.LOW)
        self.state = False

    def loop(self):
        """GPIO 상태 제어 (시간 범위에 따라 ON/OFF)"""
        if self.within_time_range():
            current_time = time()
            interval = self.on_time if self.state else self.off_time  # ON/OFF 상태에 따라 타이머 결정
            if current_time - self.last_time >= interval:
                if self.state:
                    self.off()
                    print(f"{self.name} ({self.pin})가 꺼졌습니다!")
                else:
                    self.on()
                    print(f"{self.name} ({self.pin})가 켜졌습니다!")
                self.last_time = current_time  # 기준 시간 업데이트
        else:
            if self.state:
                self.off()
                print(f"{self.name} ({self.pin})가 시간 범위 밖이라 꺼졌습니다!")

        self.share()  # 상태 공유

    def cleanup(self):
        """GPIO 핀 정리"""
        GPIO.cleanup(self.pin)
        print(f"{self.name} on pin {self.pin} has been cleaned up.")

class LED(GPIODevice):
    def __init__(self, pin=17, on_time=2, off_time=2, start_time=0, end_time=24):
        super().__init__(pin, on_time, off_time, name="LED", start_time=start_time, end_time=end_time)

class FAN(GPIODevice):
    def __init__(self, pin=27, on_time=2, off_time=2, start_time=6, end_time=18):
        super().__init__(pin, on_time, off_time, name="FAN", start_time=start_time, end_time=end_time)

class PUMP(GPIODevice):
    def __init__(self, pin=22, on_time=3, off_time=3, start_time=9, end_time=21):
        super().__init__(pin, on_time, off_time, name="PUMP", start_time=start_time, end_time=end_time)
import RPi.GPIO as GPIO
from time import time, sleep, localtime
from dev_prototype import DevPrototype

class dev_GPIO(DevPrototype):
    def __init__(self, pin, interval=2, name="Device", start_time=0, end_time=24):
        self.pin = pin
        self.interval = interval  # ON/OFF 간격
        self.name = name
        self.start_time = start_time  # 작동 시작 시간 (24시간 형식, 예: 12 = 오전 12시)
        self.end_time = end_time  # 작동 종료 시간 (24시간 형식, 예: 17 = 오후 5시)
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.pin, GPIO.OUT)  # GPIO 핀 설정
        self.last_time = time()  # 기준 시간 저장
        self.state = False  # 현재 핀 상태 저장 (ON/OFF)
        print(f"{self.name} on pin {self.pin} has been initialized.")

    def on(self):
        GPIO.output(self.pin, GPIO.HIGH)
        self.state = True  # 상태를 ON으로 저장

    def off(self):
        GPIO.output(self.pin, GPIO.LOW)
        self.state = False  # 상태를 OFF로 저장

    def within_time_range(self):
        """ 현재 시간이 설정된 시간 범위 내에 있는지 확인 """
        current_time = localtime().tm_hour  # 현재 시간의 시(hour)를 가져옴
        return self.start_time <= current_time < self.end_time

    def loop(self):
        """ GPIO 상태 제어 (시간 범위에 따라 ON/OFF) """
        if self.within_time_range():
            current_time = time()
            if current_time - self.last_time >= self.interval:  # 설정된 interval마다 작업 실행
                if self.state:  # 현재 상태가 ON이면 OFF로 전환
                    self.off()
                    print(f"{self.name} ({self.pin})가 꺼졌습니다!")
                else:  # 현재 상태가 OFF이면 ON으로 전환
                    self.on()
                    print(f"{self.name} ({self.pin})가 켜졌습니다!")

                self.last_time = current_time  # 기준 시간 업데이트
        else:
            # 시간 범위 밖에 있으면 항상 OFF 상태 유지
            if self.state:
                self.off()
                print(f"{self.name} ({self.pin})가 시간 범위 밖이라 꺼졌습니다!")

        self.share()  # 상태 공유

    def cleanup(self):
        """ GPIO 핀 정리 """
        try:
            GPIO.cleanup(self.pin)
            print(f"{self.name} on pin {self.pin} has been cleaned up.")
        except RuntimeError as e:
            print(f"Cleanup failed for {self.name} on pin {self.pin}: {e}")
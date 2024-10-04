import os
from picamera2 import Picamera2
from time import sleep, time
from datetime import datetime

from dev_prototype import DevPrototype

class Camera(DevPrototype):
    def __init__(self, interval=10, name="Camera", sht31_callback=None):
        self.interval = interval  # 사진 촬영 간격
        self.name = name
        self.sht31_callback = sht31_callback  # 온습도 센서 데이터 콜백 함수 (DI)
        self.picam2 = Picamera2()

        # 카메라 설정 및 준비
        camera_config = self.picam2.create_still_configuration()
        self.picam2.configure(camera_config)
        self.picam2.start()
        sleep(2)  # 카메라 준비 대기 시간
        self.last_time = time()  # 기준 시간 설정
        print(f"{self.name} has been initialized with interval {self.interval} seconds.")

    def capture(self):
        # 현재 날짜 (연도/월/일 형식)로 디렉토리 생성
        current_year = datetime.now().strftime("%Y")
        current_month = datetime.now().strftime("%m")
        current_day = datetime.now().strftime("%d")
        
        # 디렉토리 경로 설정 (연/월/일)
        dirname = f"../static/images/{current_year}/{current_month}/{current_day}"

        # 디렉토리가 없으면 생성
        if not os.path.exists(dirname):
            os.makedirs(dirname)

        # 파일명 설정 (현재 시간 기반)
        filename = f"{dirname}/image_{int(time())}.png"

        # 사진 저장
        self.picam2.capture_file(filename)
        print(f"Image captured: {filename}")

        # 온습도 센서 데이터 콜백 함수가 주입된 경우 실행
        if self.sht31_callback:
            temp, hum = self.sht31_callback()
            print(f"Temperature: {temp:.2f} °C, Humidity: {hum:.2f} % - Recorded with image.")

    def loop(self):
        """ 주기적으로 사진 촬영 및 온습도 데이터 기록 """
        current_time = time()
        if current_time - self.last_time >= self.interval:
            self.capture()  # 사진 촬영 및 온습도 기록
            self.last_time = current_time  # 기준 시간 업데이트

        self.share()  # 상태 공유

    def cleanup(self):
        """ 카메라 정리 """
        self.picam2.stop()
        print(f"{self.name} has been cleaned up.")
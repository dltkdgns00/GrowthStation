import os
from picamera2 import Picamera2
from time import sleep, time
from datetime import datetime
from dev_prototype import DevPrototype
import json

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
        
        # 이전 상태를 복구
        self.restore_previous_status()

        print(f"{self.name} has been initialized with interval {self.interval} seconds.")

    def restore_previous_status(self):
        """ 프로그램 재시작 시, 이전 상태 복원 """
        filepath = "/dev/shm/station/Camera"
        if os.path.exists(filepath):
            try:
                with open(filepath, "r") as f:
                    previous_status = json.load(f)
                    self.latest_image = previous_status.get("latest_image", None)
                    self.latest_temp = previous_status.get("temperature", None)
                    self.latest_hum = previous_status.get("humidity", None)
                    print(f"Restored previous camera state: image={self.latest_image}, temperature={self.latest_temp}, humidity={self.latest_hum}")
            except (IOError, json.JSONDecodeError):
                print("Failed to restore previous camera state, starting fresh.")
                self.latest_image = None
                self.latest_temp = None
                self.latest_hum = None
        else:
            print("No previous camera state found, starting fresh.")
            self.latest_image = None
            self.latest_temp = None
            self.latest_hum = None

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
        self.latest_image = filename  # 최근 촬영된 이미지 경로 업데이트
        # filename에서 맨 앞의 ../를 제거
        self.latest_image = self.latest_image[3:]
        print(f"Image captured: {self.latest_image}")

        # 온습도 센서 데이터 콜백 함수가 주입된 경우 실행
        if self.sht31_callback:
            self.latest_temp, self.latest_hum = self.sht31_callback()
            print(f"Temperature: {self.latest_temp:.2f} °C, Humidity: {self.latest_hum:.2f} % - Recorded with image.")
        else:
            print("No SHT31 callback provided; temperature and humidity are not available.")

    def loop(self):
        """ 주기적으로 사진 촬영 및 온습도 데이터 기록 """
        current_time = time()
        if current_time - self.last_time >= self.interval:
            print(f"Capturing image after {self.interval} seconds...")
            self.capture()  # 사진 촬영 및 온습도 기록
            self.last_time = current_time  # 기준 시간 업데이트

        self.share()  # 상태 공유

    def share(self):
        """ 카메라 상태 및 온습도 정보 공유 """
        # 상태 정보를 구성
        status_data = {
            "timestamp": time(),
            "dev_name": self.name,
            "interval": self.interval,
            "latest_image": self.latest_image,  # 최근 촬영된 이미지
            "temperature": self.latest_temp,  # 최근 온도
            "humidity": self.latest_hum  # 최근 습도
        }

        # 상태를 저장할 경로
        sharepath = "/dev/shm/station/"
        if not os.path.exists(sharepath):
            os.makedirs(sharepath)
        filepath = os.path.join(sharepath, self.name)

        # 파일에 JSON 형식으로 상태 저장
        try:
            with open(filepath, "w") as f:
                json.dump(status_data, f, indent=4)
            print(f"{self.name} 상태가 {filepath}에 저장되었습니다.")
        except Exception as e:
            print(f"Error to write status {self.name}: {e}")

    def cleanup(self):
        """ 카메라 정리 """
        self.picam2.stop()
        print(f"{self.name} has been cleaned up.")
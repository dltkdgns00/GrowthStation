from picamera2 import Picamera2
from time import sleep

# Picamera2 객체 생성
picam2 = Picamera2()

# 카메라 설정 가져오기
camera_config = picam2.create_still_configuration()

# 설정 적용
picam2.configure(camera_config)

# 카메라 미리보기 시작
picam2.start()

# 2초 대기 (카메라 준비 시간)
sleep(2)

# 사진 촬영 및 저장
picam2.capture_file("./image.png")

# 카메라 중지
picam2.stop()

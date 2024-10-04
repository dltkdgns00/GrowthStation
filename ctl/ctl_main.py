import os
from time import sleep, time
import threading
import dev_GPIO as gpio
from dev_camera import Camera
from dev_sht31 import SHT31
from dotenv import load_dotenv

LED_INTERVAL = os.getenv('LED_INTERVAL', 1)
LED_START_TIME = os.getenv('LED_START_TIME', 0)
LED_END_TIME = os.getenv('LED_END_TIME', 17)

FAN_INTERVAL = os.getenv('FAN_INTERVAL', 2)
FAN_START_TIME = os.getenv('FAN_START_TIME', 6)
FAN_END_TIME = os.getenv('FAN_END_TIME', 18)

PUMP_INTERVAL = os.getenv('PUMP_INTERVAL', 3)
PUMP_START_TIME = os.getenv('PUMP_START_TIME', 9)
PUMP_END_TIME = os.getenv('PUMP_END_TIME', 21)

CAMERA_INTERVAL = os.getenv('CAMERA_INTERVAL', 10)

# 시스템 모니터링 프로세스 구성
def collect_status(devices, stop_event):
    while not stop_event.is_set():  # stop_event가 설정되지 않은 동안 루프
        for device in devices:
            device.loop()  # 각 장치의 loop 호출
        sleep(0.1)  # 0.1초 간격으로 loop 호출

if __name__ == "__main__":
    # .env 파일 로드
    load_dotenv()

    # GPIO 장치 생성 (환경 변수 값으로 생성)
    led = gpio.dev_GPIO(
        pin=17,
        interval=int(LED_INTERVAL),
        name="LED",
        start_time=int(LED_START_TIME),
        end_time=int(LED_END_TIME)
    )
    fan = gpio.dev_GPIO(
        pin=27,
        interval=int(FAN_INTERVAL),
        name="FAN",
        start_time=int(FAN_START_TIME),
        end_time=int(FAN_END_TIME)
    )
    pump = gpio.dev_GPIO(
        pin=22,
        interval=int(),
        name="PUMP",
        start_time=int(PUMP_START_TIME),
        end_time=int(PUMP_END_TIME)
    )

    # 온습도 센서 인스턴스 생성
    sht31_sensor = SHT31()

    # 카메라 생성 (온습도 센서 데이터 콜백 주입)
    camera_interval = int(CAMERA_INTERVAL)
    camera = Camera(
        interval=camera_interval,
        sht31_callback=sht31_sensor.read_sht31  # DI 방식으로 온습도 데이터 주입
    )

    devices = [led, fan, pump, camera]  # 모든 장치 리스트

    # 스레드 종료 이벤트 설정
    stop_event = threading.Event()

    # 시스템 모니터링 시작
    try:
        # 스레드 시작 (stop_event를 전달하여 제어)
        thread = threading.Thread(target=collect_status, args=(devices, stop_event))
        thread.start()
        thread.join()  # 스레드가 종료될 때까지 대기

    except KeyboardInterrupt:
        print("프로그램이 종료 중입니다...")
        stop_event.set()  # 스레드를 안전하게 종료

    finally:
        # 모든 장치에 대해 cleanup 호출
        for device in devices:
            device.cleanup()

        # 온습도 센서 정리
        sht31_sensor.cleanup()
        print("프로그램이 안전하게 종료되었습니다.")
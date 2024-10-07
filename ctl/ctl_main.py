import os
from time import sleep, time
import threading
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from dev_GPIO import LED, FAN, PUMP
from dev_camera import Camera
from dev_sht31 import SHT31
from dev_WebSocket import WSOCKET
from dotenv import load_dotenv

# .env 파일을 처음 로드
load_dotenv()

# 환경 변수 로드 함수 (필요할 때마다 호출하여 최신 값을 반영)
def load_env_variables():
    global LED_ON, LED_OFF, LED_START_TIME, LED_END_TIME
    global FAN_ON, FAN_OFF, FAN_START_TIME, FAN_END_TIME
    global PUMP_ON, PUMP_OFF, PUMP_START_TIME, PUMP_END_TIME
    global CAMERA_INTERVAL
    
    LED_ON = os.getenv('LED_ON', 1)
    LED_OFF = os.getenv('LED_OFF', 0)
    LED_START_TIME = os.getenv('LED_START_TIME', 0)
    LED_END_TIME = os.getenv('LED_END_TIME', 23)
    
    FAN_ON = os.getenv('FAN_ON', 1)
    FAN_OFF = os.getenv('FAN_OFF', 0)
    FAN_START_TIME = os.getenv('FAN_START_TIME', 6)
    FAN_END_TIME = os.getenv('FAN_END_TIME', 23)
    
    PUMP_ON = os.getenv('PUMP_ON', 1)
    PUMP_OFF = os.getenv('PUMP_OFF', 0)
    PUMP_START_TIME = os.getenv('PUMP_START_TIME', 9)
    PUMP_END_TIME = os.getenv('PUMP_END_TIME', 23)
    
    CAMERA_INTERVAL = os.getenv('CAMERA_INTERVAL', 10)

# .env 파일이 변경될 때 호출되는 핸들러 클래스
class EnvFileChangeHandler(FileSystemEventHandler):
    def on_modified(self, event):
        if event.src_path.endswith('.env'):
            print(".env 파일이 변경되었습니다. 새로 로드합니다.")
            load_dotenv()  # .env 파일 다시 로드
            load_env_variables()  # 환경 변수 다시 로드

# 시스템 모니터링 프로세스 구성
def collect_status(devices, stop_event):
    while not stop_event.is_set():  # stop_event가 설정되지 않은 동안 루프
        for device in devices:
            device.loop()  # 각 장치의 loop 호출
        sleep(1)  # 1초 간격으로 loop 호출

if __name__ == "__main__":
    # 환경 변수 처음 로드
    load_env_variables()

    # .env 파일 감시 설정
    path_to_watch = os.path.dirname(os.path.abspath('.env'))
    event_handler = EnvFileChangeHandler()
    observer = Observer()
    observer.schedule(event_handler, path=path_to_watch, recursive=False)
    observer.start()

    # GPIO 장치 생성 (환경 변수 값으로 생성)
    led = LED(
        pin=17,
        on_time=int(LED_ON),
        off_time=int(LED_OFF),
        start_time=int(LED_START_TIME),
        end_time=int(LED_END_TIME)
    )
    fan = FAN(
        pin=27,
        on_time=int(FAN_ON),
        off_time=int(FAN_OFF),
        start_time=int(FAN_START_TIME),
        end_time=int(FAN_END_TIME)
    )
    pump = PUMP(
        pin=22,
        on_time=int(PUMP_ON),
        off_time=int(PUMP_OFF),
        start_time=int(PUMP_START_TIME),
        end_time=int(PUMP_END_TIME)
    )

    # 온습도 센서 인스턴스 생성
    sht31_sensor = SHT31()

    # 카메라 생성 (온습도 센서 데이터 콜백 주입)
    camera = Camera(
        interval=int(CAMERA_INTERVAL),
        sht31_callback=sht31_sensor.read_sht31
    )

    wSocket = WSOCKET()

    devices = [led, fan, pump, camera, wSocket]

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

        # 파일 감시 종료
        observer.stop()
        observer.join()
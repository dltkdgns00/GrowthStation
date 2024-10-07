import os
import json
from dotenv import load_dotenv

def get_env():
    env_path = "/home/pi/GrowthStation/ctl/.env"
    
    # .env 파일 로드
    load_dotenv(env_path)

    # 각 장치의 환경 변수 가져오기
    env = {
        "LED": {
            "start_time": os.getenv('LED_START_TIME', "0:0"),
            "end_time": os.getenv('LED_END_TIME', "23:59"),
            "on_time": os.getenv('LED_ON_TIME', "1"),
            "off_time": os.getenv('LED_OFF_TIME', "1")
        },
        "FAN": {
            "start_time": os.getenv('FAN_START_TIME', "0:0"),
            "end_time": os.getenv('FAN_END_TIME', "23:59"),
            "on_time": os.getenv('FAN_ON_TIME', "1"),
            "off_time": os.getenv('FAN_OFF_TIME', "1")
        },
        "PUMP": {
            "start_time": os.getenv('PUMP_START_TIME', "0:0"),
            "end_time": os.getenv('PUMP_END_TIME', "23:59"),
            "on_time": os.getenv('PUMP_ON_TIME', "1"),
            "off_time": os.getenv('PUMP_OFF_TIME', "1")
        },
        "CAMERA": {
            "interval": os.getenv('CAMERA_INTERVAL', "10")
        }
    }

    return env

if __name__ == "__main__":
    print(json.dumps(get_env()))

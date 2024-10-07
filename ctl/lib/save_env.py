import json
import sys
from dotenv import set_key, load_dotenv

def update_env(data):
    env_path = "/home/pi/GrowthStation/ctl/.env"
    
    # .env 파일 로드
    load_dotenv(env_path)

    # JSON 문자열을 딕셔너리로 변환
    data = json.loads(data)  # JSON 문자열을 딕셔너리로 변환    

    # 'LED' 설정 접근
    if 'LED' in data:
        if 'on_time' in data['LED']:
            set_key(env_path, 'LED_ON_TIME', str(data['LED']['on_time']))
        if 'off_time' in data['LED']:
            set_key(env_path, 'LED_OFF_TIME', str(data['LED']['off_time']))
        if 'start_time' in data['LED']:
            set_key(env_path, 'LED_START_TIME', str(data['LED']['start_time']))
        if 'end_time' in data['LED']:
            set_key(env_path, 'LED_END_TIME', str(data['LED']['end_time']))

    # 'FAN' 설정 접근
    if 'FAN' in data:
        if 'on_time' in data['FAN']:
            set_key(env_path, 'FAN_ON_TIME', str(data['FAN']['on_time']))
        if 'off_time' in data['FAN']:
            set_key(env_path, 'FAN_OFF_TIME', str(data['FAN']['off_time']))
        if 'start_time' in data['FAN']:
            set_key(env_path, 'FAN_START_TIME', str(data['FAN']['start_time']))
        if 'end_time' in data['FAN']:
            set_key(env_path, 'FAN_END_TIME', str(data['FAN']['end_time']))

    # 'PUMP' 설정 접근
    if 'PUMP' in data:
        if 'on_time' in data['PUMP']:
            set_key(env_path, 'PUMP_ON_TIME', str(data['PUMP']['on_time']))
        if 'off_time' in data['PUMP']:
            set_key(env_path, 'PUMP_OFF_TIME', str(data['PUMP']['off_time']))
        if 'start_time' in data['PUMP']:
            set_key(env_path, 'PUMP_START_TIME', str(data['PUMP']['start_time']))
        if 'end_time' in data['PUMP']:
            set_key(env_path, 'PUMP_END_TIME', str(data['PUMP']['end_time']))

    # 'CAMERA' 설정 접근
    if 'CAMERA' in data:
        if 'interval' in data['CAMERA']:
            set_key(env_path, 'CAMERA_INTERVAL', str(data['CAMERA']['interval']))

if __name__ == "__main__":
    try:
        raw_data = sys.argv[1]
        update_env(raw_data)
        print("Environment variables updated")
    except Exception as e:
        print(f"Error: {e}")
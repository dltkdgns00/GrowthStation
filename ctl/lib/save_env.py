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
        if 'interval' in data['LED']:
            set_key(env_path, 'LED_INTERVAL', str(data['LED']['interval']))
        if 'start_time' in data['LED']:
            set_key(env_path, 'LED_START_TIME', str(data['LED']['start_time']))
        if 'end_time' in data['LED']:
            set_key(env_path, 'LED_END_TIME', str(data['LED']['end_time']))

    # 'FAN' 설정 접근
    if 'FAN' in data:
        if 'interval' in data['FAN']:
            set_key(env_path, 'FAN_INTERVAL', str(data['FAN']['interval']))
        if 'start_time' in data['FAN']:
            set_key(env_path, 'FAN_START_TIME', str(data['FAN']['start_time']))
        if 'end_time' in data['FAN']:
            set_key(env_path, 'FAN_END_TIME', str(data['FAN']['end_time']))

    # 'PUMP' 설정 접근
    if 'PUMP' in data:
        if 'interval' in data['PUMP']:
            set_key(env_path, 'PUMP_INTERVAL', str(data['PUMP']['interval']))
        if 'start_time' in data['PUMP']:
            set_key(env_path, 'PUMP_START_TIME', str(data['PUMP']['start_time']))
        if 'end_time' in data['PUMP']:
            set_key(env_path, 'PUMP_END_TIME', str(data['PUMP']['end_time']))

if __name__ == "__main__":
    try:
        # 명령줄 인자로 전달받은 JSON 문자열을 딕셔너리로 변환 후 함수 호출
        raw_data = sys.argv[1]
        update_env(raw_data)
        print("Environment variables updated")
    except Exception as e:
        print(f"Error: {e}")
import os
import json
from dotenv import load_dotenv, set_key
import sys

def errlog(a):
    sys.stderr.write(a+"\n")

def logfmt(func, istack):
    fmt = f"[{func}] in [{istack[0][3]}]@{istack[1][3]}"
    errlog(fmt)
    return  fmt

def resp(msg, status="error"):
    return {"data":msg, "status":status}


def func_status(data):
    # 파일들이 저장된 디렉토리
    directory = '/dev/shm/station'
    camera_directory = '/home/pi/GrowthStation/static/images'  # 카메라 이미지가 저장된 경로 (수정 필요)

    # JSON으로 변환할 데이터
    status_data = {}

    try:
        # 디렉토리 내 모든 파일을 순차적으로 읽기
        for filename in os.listdir(directory):
            file_path = os.path.join(directory, filename)

            # 파일이 존재하고 읽기 가능한 경우
            if os.path.isfile(file_path):
                with open(file_path, 'r') as f:
                    try:
                        # 파일 내용이 JSON 형식일 경우 파싱
                        file_content = f.read()
                        try:
                            content = json.loads(file_content)
                        except json.JSONDecodeError:
                            # JSON 형식이 아닐 경우 그대로 문자열로 저장
                            content = file_content
                        
                        status_data[filename] = content
                    except IOError as e:
                        # 파일을 읽는 중에 오류 발생 시 에러 메시지 기록
                        status_data[filename] = f"Error reading file: {str(e)}"
        
        # 성공적으로 파일을 읽고 JSON으로 반환
        return {"data": status_data, "status": "success"}
    
    except Exception as e:
        # 디렉토리 접근이나 다른 에러 발생 시 처리
        return {"data": f"Error: {str(e)}", "status": "fail"}


def func_save_env(data):
    """
    POST로 받은 데이터를 바탕으로 .env 파일을 업데이트하는 함수
    """

    # .env 파일 경로 설정
    env_path = ".env"

    # .env 파일 로드
    load_dotenv(env_path)
    
    try:
        # 데이터가 비어있으면 오류 처리
        if not data:
            return {"status": "error", "message": "No data provided"}

        # LED 설정
        if 'LED_INTERVAL' in data['env']:
            set_key(env_path, 'LED_INTERVAL', data['env']['LED_INTERVAL'])
        if 'LED_START_TIME' in data['env']:
            set_key(env_path, 'LED_START_TIME', data['env']['LED_START_TIME'])
        if 'LED_END_TIME' in data['env']:
            set_key(env_path, 'LED_END_TIME', data['env']['LED_END_TIME'])

        # FAN 설정
        if 'FAN_INTERVAL' in data['env']:
            set_key(env_path, 'FAN_INTERVAL', data['env']['FAN_INTERVAL'])
        if 'FAN_START_TIME' in data['env']:
            set_key(env_path, 'FAN_START_TIME', data['env']['FAN_START_TIME'])
        if 'FAN_END_TIME' in data['env']:
            set_key(env_path, 'FAN_END_TIME', data['env']['FAN_END_TIME'])

        # PUMP 설정
        if 'PUMP_INTERVAL' in data['env']:
            set_key(env_path, 'PUMP_INTERVAL', data['env']['PUMP_INTERVAL'])
        if 'PUMP_START_TIME' in data['env']:
            set_key(env_path, 'PUMP_START_TIME', data['env']['PUMP_START_TIME'])
        if 'PUMP_END_TIME' in data['env']:
            set_key(env_path, 'PUMP_END_TIME', data['env']['PUMP_END_TIME'])

        # 카메라 설정
        if 'CAMERA_INTERVAL' in data['env']:
            set_key(env_path, 'CAMERA_INTERVAL', data['env']['CAMERA_INTERVAL'])

        # 온습도 센서 설정
        if 'SHT31_ENABLED' in data['env']:
            set_key(env_path, 'SHT31_ENABLED', data['env']['SHT31_ENABLED'])

        # 변경된 .env 파일 로드
        load_dotenv(env_path)

        return {"status": "success", "message": "Environment variables updated successfully"}

    except Exception as e:
        return {"status": "error", "message": str(e)}
import os
import json
import sys
import subprocess
import base64

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
        return resp(status_data, "success")
    
    except Exception as e:
        # 디렉토리 접근이나 다른 에러 발생 시 처리
        return resp(str(e))

def func_save_env(data):
    """
    POST로 받은 데이터를 바탕으로 .env 파일을 업데이트하는 함수
    """

    # 데이터가 비어있는지 확인
    if not data:
        return resp("No data received")

    try:
        # env 데이터를 JSON 문자열로 변환
        env_data = json.dumps(data['env'])  # dict -> JSON 문자열로 변환

        # save_env.py 파일을 sudo로 실행
        result = subprocess.run(
            ['sudo', 'python3', 'ctl/lib/save_env.py', env_data], 
            text=True,  # 문자열로 출력 및 입력을 처리
            capture_output=True  # 표준 출력과 오류를 캡처
        )

        if result.returncode != 0:
            return resp(f"Error: {result.stderr}")
        else:
            return resp(result.stdout, "success")

    except Exception as e:
        return resp(str(e))


def func_get_timelapse_videos(data):
    # 타임랩스 비디오가 저장된 경로
    directory = '/home/pi/GrowthStation/static/timelapse'
    video_data = []

    try:
        # 디렉토리 내 모든 파일을 순차적으로 읽기
        for filename in os.listdir(directory):
            file_path = os.path.join('/static/timelapse', filename)
            # 파일이 존재하고 읽기 가능한 경우
            if os.path.isfile(os.path.join(directory, filename)):
                video_data.append({"name": filename, "path": file_path})
        
        # 성공적으로 파일을 읽고 JSON으로 반환
        return resp(video_data, "success")
    
    except Exception as e:
        # 디렉토리 접근이나 다른 에러 발생 시 처리
        return resp(str(e), "fail")
import os
import json
import sys
import subprocess
import csv

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
        # 웹에서 받은 data['env']는 JSON 문자열로 되어있을 수 있음
        # 이를 Python 딕셔너리로 변환해줌
        env_data = json.loads(data['env'])

        # 다시 JSON 문자열로 변환하여 저장할 준비
        env_data_str = json.dumps(env_data)  # dict -> JSON 문자열로 변환

        # save_env.py 파일을 sudo로 실행
        result = subprocess.run(
            ['sudo', 'python3', 'ctl/lib/save_env.py', env_data_str], 
            text=True,  # 문자열로 출력 및 입력을 처리
            capture_output=True  # 표준 출력과 오류를 캡처
        )

        if result.returncode != 0:
            return resp(f"Error: {result.stderr}")
        else:
            return resp(result.stdout, "success")

    except Exception as e:
        return resp(str(e))

def func_get_env(data):
    try:
        # get_env.py 파일을 sudo로 실행
        result = subprocess.run(
            ['sudo', 'python3', 'ctl/lib/get_env.py'], 
            text=True,  # 문자열로 출력 및 입력을 처리
            capture_output=True  # 표준 출력과 오류를 캡처
        )

        print(result.stdout)

        if result.returncode != 0:
            return resp(f"Error: {result.stderr}")
        else:
            return resp(result.stdout, "success")
        
    except Exception as e:
        return resp(str(e))


def func_get_timelapse_data(data):
    # 타임랩스 비디오와 온습도 로그 파일이 저장된 경로
    video_directory = '/home/pi/GrowthStation/static/timelapse'
    csv_directory = '/home/pi/GrowthStation/static/data'
    video_data = []

    try:
        # 디렉토리 내 모든 파일을 순차적으로 읽기
        for filename in os.listdir(video_directory):
            file_path = os.path.join('/static/timelapse', filename)
            
            # 파일이 존재하고 읽기 가능한 경우
            if os.path.isfile(os.path.join(video_directory, filename)):
                # 파일 이름에서 날짜를 추출 (가정: 파일명에 날짜 포함됨)
                try:
                    # 예: video_20241005.mp4에서 날짜 추출
                    date_str = filename.split('_')[1].split('.')[0]

                    # 해당 날짜에 맞는 온습도 CSV 파일 경로 설정
                    csv_filename = f"temperature_humidity_log_{date_str}.csv"
                    csv_path = os.path.join('/static/data', csv_filename)
                    
                    # 해당 날짜에 CSV 파일이 존재하는지 확인
                    if os.path.exists(os.path.join(csv_directory, csv_filename)):
                        video_data.append({
                            "date": date_str,  # 날짜를 date으로 사용
                            "path": file_path,
                            "csv_path": csv_path
                        })
                    else:
                        video_data.append({
                            "date": date_str,
                            "path": file_path,
                            "csv_path": None  # CSV가 없을 경우 None
                        })
                except Exception as e:
                    # 날짜 추출 또는 파일명 처리 오류가 있을 때 예외 처리
                    continue

            print(video_data)   
        
        # 성공적으로 파일을 읽고 JSON으로 반환
        return resp(video_data, "success")
    
    except Exception as e:
        # 디렉토리 접근이나 다른 에러 발생 시 처리
        return resp(str(e), "fail")

def func_get_temperature_humidity_data(data):
    csv_path = data.get('csv_path')

    csv_path = '/home/pi/GrowthStation' + csv_path
    
    if not csv_path or not os.path.exists(csv_path):
        return resp("CSV file not found", "fail")

    try:
        with open(csv_path, mode='r', encoding='utf-8') as file:
            csv_reader = csv.DictReader(file)
            csv_data = [row for row in csv_reader]

        print(csv_data)
        
        # JSON으로 변환
        return resp(csv_data, "success")
    
    except Exception as e:
        return resp(f"Error reading CSV: {str(e)}", "fail")


if __name__ == "__main__":
    func_get_temperature_humidity_data({'csv_path': '/static/data/temperature_humidity_log_20241007.csv'})
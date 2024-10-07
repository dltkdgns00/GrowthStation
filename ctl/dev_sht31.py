import smbus2
import time
import os
import csv
from datetime import datetime
from dev_prototype import DevPrototype

class SHT31(DevPrototype):
    I2C_BUS = 1
    SHT31_ADDRESS = 0x44
    CMD_MEASURE_HIGHREP = [0x2C, 0x06]

    def __init__(self, name="SHT31"):
        self.name = name
        self.bus = smbus2.SMBus(self.I2C_BUS)
        self.current_csv_file = self.get_csv_filename()
        self.initialize_csv(self.current_csv_file)  # CSV 초기화
        print(f"{self.name} sensor has been initialized.")

    def get_csv_filename(self):
        """ 현재 날짜에 맞는 CSV 파일 이름을 생성 """
        current_date = datetime.now().strftime("%Y%m%d")
        return f"/home/pi/GrowthStation/static/data/temperature_humidity_log_{current_date}.csv"

    def initialize_csv(self, file_path):
        """ CSV 파일이 존재하지 않으면 새로 생성하고, 헤더를 추가 """
        directory = os.path.dirname(file_path)
        
        # 디렉토리가 없으면 생성
        if not os.path.exists(directory):
            os.makedirs(directory)
        
        # 파일이 없으면 헤더를 추가하여 새로 생성
        if not os.path.exists(file_path):
            with open(file_path, mode='w', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(["Timestamp", "Temperature (°C)", "Humidity (%)"])

    def log_data_to_csv(self, temperature, humidity):
        """ 온습도 데이터를 CSV 파일에 기록 """
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        file_path = self.get_csv_filename()  # 현재 날짜에 맞는 파일 경로
        
        # 만약 날짜가 변경되었으면 새로운 파일을 생성
        if self.current_csv_file != file_path:
            self.current_csv_file = file_path
            self.initialize_csv(self.current_csv_file)

        # 데이터 기록
        with open(self.current_csv_file, mode='a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([timestamp, temperature, humidity])

    def read_sht31(self):
        """ 온습도 데이터를 읽는 함수 """
        self.bus.write_i2c_block_data(self.SHT31_ADDRESS, self.CMD_MEASURE_HIGHREP[0], self.CMD_MEASURE_HIGHREP[1:])
        time.sleep(0.5)  # 측정 대기 시간 (500ms)
        data = self.bus.read_i2c_block_data(self.SHT31_ADDRESS, 0, 6)

        # 온도 데이터 계산
        temperature_raw = data[0] << 8 | data[1]
        temperature = -45 + (175 * temperature_raw / 65535.0)
        temperature = round(temperature, 1)  # 소수점 첫째 자리까지 반올림

        # 습도 데이터 계산
        humidity_raw = data[3] << 8 | data[4]
        humidity = 100 * humidity_raw / 65535.0
        humidity = round(humidity, 1)  # 소수점 첫째 자리까지 반올림

        # CSV 파일에 데이터 기록
        self.log_data_to_csv(temperature, humidity)

        return temperature, humidity

    def cleanup(self):
        """ 센서 정리 """
        self.bus.close()
        print(f"{self.name} has been cleaned up.")
import smbus2
import time
from dev_prototype import DevPrototype

class SHT31(DevPrototype):
    I2C_BUS = 1
    SHT31_ADDRESS = 0x44
    CMD_MEASURE_HIGHREP = [0x2C, 0x06]

    def __init__(self, name="SHT31"):
        self.name = name
        self.bus = smbus2.SMBus(self.I2C_BUS)
        print(f"{self.name} sensor has been initialized.")

    def read_sht31(self):
        """ 온습도 데이터를 읽는 함수 """
        self.bus.write_i2c_block_data(self.SHT31_ADDRESS, self.CMD_MEASURE_HIGHREP[0], self.CMD_MEASURE_HIGHREP[1:])
        time.sleep(0.5)  # 측정 대기 시간 (500ms)
        data = self.bus.read_i2c_block_data(self.SHT31_ADDRESS, 0, 6)

        # 온도 데이터 계산
        temperature_raw = data[0] << 8 | data[1]
        temperature = -45 + (175 * temperature_raw / 65535.0)

        # 습도 데이터 계산
        humidity_raw = data[3] << 8 | data[4]
        humidity = 100 * humidity_raw / 65535.0

        return temperature, humidity

    def cleanup(self):
        """ 센서 정리 """
        self.bus.close()
        print(f"{self.name} has been cleaned up.")
import smbus2
import time

# I2C 버스 번호 (Raspberry Pi에서는 보통 1번 버스)
I2C_BUS = 1
# SHT31의 I2C 주소 (일반적으로 0x44 또는 0x45)
SHT31_ADDRESS = 0x44

# SHT31 명령
CMD_MEASURE_HIGHREP = [0x2C, 0x06]

def read_sht31():
    bus = smbus2.SMBus(I2C_BUS)
    
    # 측정 명령 전송
    bus.write_i2c_block_data(SHT31_ADDRESS, CMD_MEASURE_HIGHREP[0], CMD_MEASURE_HIGHREP[1:])
    
    time.sleep(0.5)  # 측정 대기 시간 (500ms)
    
    # 6바이트의 데이터 읽기 (온도와 습도 정보)
    data = bus.read_i2c_block_data(SHT31_ADDRESS, 0, 6)

    # 온도 데이터 계산
    temperature_raw = data[0] << 8 | data[1]
    temperature = -45 + (175 * temperature_raw / 65535.0)

    # 습도 데이터 계산
    humidity_raw = data[3] << 8 | data[4]
    humidity = 100 * humidity_raw / 65535.0

    return temperature, humidity

if __name__ == "__main__":
    while True:
        temp, hum = read_sht31()
        print(f"Temperature: {temp:.2f} °C, Humidity: {hum:.2f} %")
        time.sleep(2)  # 2초 대기 후 다시 측정
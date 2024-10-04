import RPi.GPIO as GPIO
from time import sleep

# GPIO 핀 번호 설정 (여기서는 BCM 모드 사용)
LED_PINS = [17, 27, 22]  # 각각의 GPIO 핀 번호

# GPIO 설정
GPIO.setmode(GPIO.BCM)
GPIO.setup(LED_PINS, GPIO.OUT)  # LED 핀을 출력 모드로 설정

# LED 제어 함수
def control_leds(state):
    for pin in LED_PINS:
        GPIO.output(pin, state)

try:
    while True:
        # LED 켜기
        control_leds(GPIO.HIGH)
        print("LED가 켜졌습니다!")
        sleep(2)  # 2초 동안 켜짐

        # LED 끄기
        control_leds(GPIO.LOW)
        print("LED가 꺼졌습니다!")
        sleep(2)  # 2초 동안 꺼짐

finally:
    # 종료 시 GPIO 클린업
    GPIO.cleanup()
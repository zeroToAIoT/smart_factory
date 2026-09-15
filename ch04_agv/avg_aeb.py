# file name: agv_aeb_system.py
# 전후방 초음파 센서 기반 긴급 제동(AEB) 및 후방 경보 시스템

from gpiozero import Motor, DistanceSensor, TonalBuzzer, LED, Robot
from time import sleep
from signal import pause

# 1. 하드웨어 객체 생성
# 모터 설정 (이전 절에서 조립한 핀 번호)
motor1 = Motor(26, 19)
motor2 = Motor(27, 22)
motor3 = Motor(20, 21)
motor4 = Motor(24, 23)

# 오른쪽 축 및 왼쪽 축 설정
right_wheel = Robot(motor1, motor2)
left_wheel = Robot(motor3, motor4)

# 초음파 센서 설정 (threshold_distance: 이벤트가 발생하는 기준 거리 설정)
# 전방은 20cm(0.2m), 후방은 15cm(0.15m)로 설정
front_ultra = DistanceSensor(echo=12, trigger=13, max_distance=1.0, threshold_distance=0.2)
rear_ultra = DistanceSensor(echo=17, trigger=4, max_distance=1.0, threshold_distance=0.15)

# 경고용 출력 장치
buzzer = TonalBuzzer(25)
led = LED(16)

speed = 0.5  # AGV 기본 주행 속도 (50%)

# 2. 로봇 제어 통합 함수 정의
def stop_all_motors():
    right_wheel.stop()
    left_wheel.stop()

def drive_forward():
    right_wheel.forward(speed)
    left_wheel.forward(speed)

# 3. 센서 이벤트 발생 시 실행될 안전 로직(콜백 함수) 정의
def aeb_activation():
    """전방에 장애물 감지 시 긴급 제동"""
    stop_all_motors()
    led.on()
    buzzer.play('A4')
    print(f'\n[긴급 제동] 전방 작업자 감지! 충돌 방지 시스템 작동!')

def resume_driving():
    """전방 장애물이 사라지면 주행 재개"""
    led.off()
    buzzer.stop()
    print(f'\n[전방 안전 확보] AGV 물류 이송을 재개합니다.')
    drive_forward()

def rear_warning_on():
    """후방에 무언가 접근하면 짧은 경고음 발생 (주행은 유지)"""
    buzzer.play('E4')
    print(f'\n[주의] 후방 접근자 감지!')

def rear_warning_off():
    """후방 안전거리 확보 시 경고음 해제"""
    buzzer.stop()
    print(f'\n[후방 안전 확보] 후방 안전 확보.')

# 4. 센서와 이벤트 함수 연결 (이벤트 구동 방식)
front_ultra.when_in_range = aeb_activation
front_ultra.when_out_of_range = resume_driving

rear_ultra.when_in_range = rear_warning_on
rear_ultra.when_out_of_range = rear_warning_off

# 5. 메인 실행부
print('=============================================')
print(' 스마트 팩토리 AGV 안전 주행 시스템 가동 시작')
print(' 전방 20cm 감지 시 정지 / 후방 15cm 감지 시 경보')
print(' 종료하려면 Ctrl+C 를 누르세요.')
print('=============================================')

try:
    # 최초 주행 시작
    drive_forward()
    
    # 프로그램이 종료되지 않고 백그라운드에서 센서 이벤트를 계속 감지하도록 무한 대기
    pause()

except KeyboardInterrupt:
    print('\n관리자에 의해 AGV 시스템이 종료되었습니다.')

finally:
    # 프로그램 종료 시 AGV가 폭주하지 않도록 모든 하드웨어 자원 정지 및 반환
    stop_all_motors()
    buzzer.stop()
    led.off()
    print('모터 및 안전 시스템의 전원을 안전하게 차단했습니다.')
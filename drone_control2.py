import cv2
import threading
import pygame
from datetime import datetime

# MockTello 클래스를 정의해 실제 드론 없이 명령을 출력하게 처리
class MockTello:
    def connect(self):
        print("Pretending to connect to the drone!")
        return True  # 항상 연결된 것으로 처리

    def get_battery(self):
        return 100  # 테스트용 배터리 값

    def takeoff(self):
        print("Pretending drone is taking off!")

    def land(self):
        print("Pretending drone is landing!")

    def emergency(self):
        print("Pretending emergency stop is activated!")

    def move_up(self, distance):
        print(f"Pretending drone is moving up by {distance} cm")

    def move_down(self, distance):
        print(f"Pretending drone is moving down by {distance} cm")

    def rotate_clockwise(self, angle):
        print(f"Pretending drone is rotating clockwise by {angle} degrees")

    def rotate_counter_clockwise(self, angle):
        print(f"Pretending drone is rotating counter clockwise by {angle} degrees")

    def send_rc_control(self, left_right, forward_backward, up_down, yaw):
        # 모든 값이 0일 때 출력을 생략
        if left_right != 0 or forward_backward != 0 or up_down != 0 or yaw != 0:
            print(f"Pretending to send RC control: Left/Right: {left_right}, Forward/Backward: {forward_backward}, Up/Down: {up_down}, Yaw: {yaw}")

    def flip(self, direction):
        print(f"Pretending to flip {direction}")

    def get_flight_time(self):
        return 120  # 테스트용 비행 시간

    def get_height(self):
        return 50  # 테스트용 높이

    def get_temperature(self):
        return 30  # 테스트용 온도

    def query_attitude(self):
        return "Attitude: pitch=0, roll=0, yaw=0"

    def query_barometer(self):
        return 10  # 테스트용 기압계 값

    def query_acceleration(self):
        return "x=0, y=0, z=0"

    def stop(self):
        print("Pretending stop command activated!")

# Pygame 초기화
pygame.init()
pygame.display.set_mode((400, 300))  # 필요 없는 윈도우지만 pygame을 시작하기 위해 필요

# MockTello 객체 초기화 및 연결
tello = MockTello()
tello.connect()
print(f"Battery: {tello.get_battery()}%")


# 플립, 상태 정보 등 한 번만 실행되도록 처리할 키 상태 저장
pressed_keys = {
    pygame.K_1: False,
    pygame.K_2: False,
    pygame.K_3: False,
    pygame.K_4: False,
    pygame.K_5: False,
    pygame.K_6: False,
    pygame.K_7: False,
    pygame.K_8: False,
    pygame.K_9: False,
    pygame.K_0: False,
    pygame.K_MINUS: False,
    pygame.K_SPACE: False,
    pygame.K_RETURN: False
}

# 드론 이륙
tello.takeoff()

# 메인 루프 - 키 입력 감지 및 드론 조작
running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # 키 눌림 상태 확인
    keys = pygame.key.get_pressed()

    # ESC 누르면 종료
    if keys[pygame.K_ESCAPE]:
        running = False

    # 상태 정보 및 명령 실행 (한 번만 실행되도록)
    if keys[pygame.K_5] and not pressed_keys[pygame.K_5]:
        pressed_keys[pygame.K_5] = True
        print(f"Battery: {tello.get_battery()}%")
    elif not keys[pygame.K_5]:
        pressed_keys[pygame.K_5] = False

    if keys[pygame.K_6] and not pressed_keys[pygame.K_6]:
        pressed_keys[pygame.K_6] = True
        print(f"Flight Time: {tello.get_flight_time()}s")
    elif not keys[pygame.K_6]:
        pressed_keys[pygame.K_6] = False

    if keys[pygame.K_7] and not pressed_keys[pygame.K_7]:
        pressed_keys[pygame.K_7] = True
        print(f"Height: {tello.get_height()}cm")
    elif not keys[pygame.K_7]:
        pressed_keys[pygame.K_7] = False

    if keys[pygame.K_8] and not pressed_keys[pygame.K_8]:
        pressed_keys[pygame.K_8] = True
        print(f"Temperature: {tello.get_temperature()}°C")
    elif not keys[pygame.K_8]:
        pressed_keys[pygame.K_8] = False

    if keys[pygame.K_9] and not pressed_keys[pygame.K_9]:
        pressed_keys[pygame.K_9] = True
        attitude = tello.query_attitude()
        print(f"Attitude: {attitude}")
    elif not keys[pygame.K_9]:
        pressed_keys[pygame.K_9] = False

    if keys[pygame.K_0] and not pressed_keys[pygame.K_0]:
        pressed_keys[pygame.K_0] = True
        print(f"Barometer: {tello.query_barometer()}cm")
    elif not keys[pygame.K_0]:
        pressed_keys[pygame.K_0] = False

    if keys[pygame.K_MINUS] and not pressed_keys[pygame.K_MINUS]:
        pressed_keys[pygame.K_MINUS] = True
        acceleration = tello.query_acceleration()
        print(f"Acceleration: {acceleration}")
    elif not keys[pygame.K_MINUS]:
        pressed_keys[pygame.K_MINUS] = False

    if keys[pygame.K_SPACE] and not pressed_keys[pygame.K_SPACE]:
        pressed_keys[pygame.K_SPACE] = True
        print("Emergency stop activated!")
        tello.emergency()
    elif not keys[pygame.K_SPACE]:
        pressed_keys[pygame.K_SPACE] = False

    if keys[pygame.K_RETURN] and not pressed_keys[pygame.K_RETURN]:
        pressed_keys[pygame.K_RETURN] = True
        print("Stop command activated!")
        tello.stop()
    elif not keys[pygame.K_RETURN]:
        pressed_keys[pygame.K_RETURN] = False

    # 플립 동작 (한 번만 실행되도록)
    if keys[pygame.K_1] and not pressed_keys[pygame.K_1]:
        pressed_keys[pygame.K_1] = True
        tello.flip('l')  # 왼쪽 플립
    elif not keys[pygame.K_1]:
        pressed_keys[pygame.K_1] = False

    if keys[pygame.K_2] and not pressed_keys[pygame.K_2]:
        pressed_keys[pygame.K_2] = True
        tello.flip('r')  # 오른쪽 플립
    elif not keys[pygame.K_2]:
        pressed_keys[pygame.K_2] = False

    if keys[pygame.K_3] and not pressed_keys[pygame.K_3]:
        pressed_keys[pygame.K_3] = True
        tello.flip('f')  # 앞쪽 플립
    elif not keys[pygame.K_3]:
        pressed_keys[pygame.K_3] = False

    if keys[pygame.K_4] and not pressed_keys[pygame.K_4]:
        pressed_keys[pygame.K_4] = True
        tello.flip('b')  # 뒤쪽 플립
    elif not keys[pygame.K_4]:
        pressed_keys[pygame.K_4] = False

    # 기본 조작 및 속도 설정 (조이스틱 명령은 지속적)
    speed = 25
    rotation_speed = 30

    # Shift가 눌린 경우 더 빠르게, Ctrl이 눌린 경우 더 느리게, Alt가 눌린 경우 최대 속도
    mods = pygame.key.get_mods()
    if mods & pygame.KMOD_SHIFT:
        speed = 50  # 빠른 속도
        rotation_speed = 60
    elif mods & pygame.KMOD_CTRL:
        speed = 10  # 느린 속도
        rotation_speed = 15
    elif mods & pygame.KMOD_ALT:
        speed = 100 # 최대 속도
        rotation_speed = 100

    # 방향과 회전 제어
    left_right = 0
    forward_backward = 0
    up_down = 0
    yaw = 0

    if keys[pygame.K_w]:
        forward_backward = speed  # 전진
    if keys[pygame.K_s]:
        forward_backward = -speed  # 후진
    if keys[pygame.K_a]:
        left_right = -speed  # 왼쪽으로 이동
    if keys[pygame.K_d]:
        left_right = speed  # 오른쪽으로 이동

    if keys[pygame.K_UP]:
        forward_backward = speed  # 전진
    if keys[pygame.K_DOWN]:
        forward_backward = -speed  # 후진
    if keys[pygame.K_LEFT]:
        left_right = -speed  # 왼쪽으로 이동
    if keys[pygame.K_RIGHT]:
        left_right = speed  # 오른쪽으로 이동

    if keys[pygame.K_r]:
        up_down = speed  # 상승
    if keys[pygame.K_f]:
        up_down = -speed  # 하강
    if keys[pygame.K_e]:
        yaw = rotation_speed  # 시계 방향 회전
    if keys[pygame.K_q]:
        yaw = -rotation_speed  # 반시계 방향 회전

    # 모든 값을 send_rc_control로 보내기
    tello.send_rc_control(left_right, forward_backward, up_down, yaw)

# 드론 착륙 및 자원 해제
tello.land()

# Pygame 종료
pygame.quit()

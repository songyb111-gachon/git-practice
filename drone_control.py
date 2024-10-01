from djitellopy import Tello
import cv2
import threading
import inputs  # Xbox 컨트롤러 입력을 위한 라이브러리
from datetime import datetime

# MockTello 클래스를 정의해 실제 드론 없이 명령을 출력하게 처리
class MockTello(Tello):
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
        print(f"Pretending drone is rotating counterclockwise by {angle} degrees")

    def send_rc_control(self, left_right, forward_backward, up_down, yaw):
        # 모든 값이 0일 때 출력을 생략
        if left_right != 0 or forward_backward != 0 or up_down != 0 or yaw != 0:
            print(
                f"Pretending to send RC control: Left/Right: {left_right}, Forward/Backward: {forward_backward}, Up/Down: {up_down}, Yaw: {yaw}")

    # 플립 동작 처리 추가
    def flip_forward(self):
        print("Pretending drone is flipping forward")

    def flip_back(self):
        print("Pretending drone is flipping backward")

    def flip_left(self):
        print("Pretending drone is flipping left")

    def flip_right(self):
        print("Pretending drone is flipping right")

# 드론 객체 초기화 및 연결 (MockTello 사용)
tello = MockTello()
tello.connect()
print(f"Pretending battery level is: {tello.get_battery()}%")

# 드론 이륙
tello.takeoff()

# 버튼 입력에 따른 동작을 처리하는 함수
def handle_button_press(tello, button_code, state):
    if button_code == 'BTN_SOUTH':  # A 버튼
        print("A button (land) pressed")
        tello.land()
    elif button_code == 'BTN_EAST':  # B 버튼
        print("B button (emergency) pressed")
        tello.emergency()
    elif button_code == 'BTN_WEST':  # X 버튼
        print("X button (move up) pressed")
        tello.move_up(30)
    elif button_code == 'BTN_NORTH':  # Y 버튼
        print("Y button (move down) pressed")
        tello.move_down(30)
    elif button_code == 'ABS_HAT0Y':  # DPAD 위/아래 플립 처리
        if state == -1:  # 위쪽 눌림
            print("DPAD UP (flip forward) pressed")
            tello.flip_forward()
        elif state == 1:  # 아래쪽 눌림
            print("DPAD DOWN (flip backward) pressed")
            tello.flip_back()
    elif button_code == 'ABS_HAT0X':  # DPAD 왼쪽/오른쪽 플립 처리
        if state == -1:  # 왼쪽 눌림
            print("DPAD LEFT (flip left) pressed")
            tello.flip_left()
        elif state == 1:  # 오른쪽 눌림
            print("DPAD RIGHT (flip right) pressed")
            tello.flip_right()
    elif button_code == 'BTN_TL':  # Left bumper
        print("Left Bumper (rotate counterclockwise) pressed")
        tello.rotate_counter_clockwise(30)
    elif button_code == 'BTN_TR':  # Right bumper
        print("Right Bumper (rotate clockwise) pressed")
        tello.rotate_clockwise(30)
    elif button_code == 'BTN_THUMBL':  # 왼쪽 조이스틱 클릭 -> 이륙
        print("Left joystick click (takeoff) pressed")
        tello.takeoff()
    elif button_code == 'BTN_THUMBR':  # 오른쪽 조이스틱 클릭 -> 착륙
        print("Right joystick click (land) pressed")
        tello.land()

# 컨트롤러 입력 처리 함수
def process_controller_input(tello):
    normal_speed = 50
    fast_speed = 100
    slow_speed = 10

    # 초기 조이스틱 위치와 버튼 상태를 중립(0)으로 설정
    lx, ly, rx, ry = 0, 0, 0, 0
    last_buttons = {}

    while True:
        events = inputs.get_gamepad()
        for event in events:
            if event.ev_type == 'Absolute':  # 조이스틱 및 트리거 처리
                if event.code in ['ABS_X', 'ABS_Y', 'ABS_RX', 'ABS_RY']:
                    speed = get_speed(last_buttons)  # 트리거 상태에 따른 속도 계산
                    if event.code == 'ABS_X':
                        lx = scale_input(event.state, speed)
                    elif event.code == 'ABS_Y':
                        ly = scale_input(event.state, speed)
                    elif event.code == 'ABS_RX':
                        rx = scale_input(event.state, speed)
                    elif event.code == 'ABS_RY':
                        ry = scale_input(event.state, speed)
                elif event.code in ['ABS_HAT0X', 'ABS_HAT0Y']:  # DPAD 처리
                    handle_button_press(tello, event.code, event.state)
                else:
                    last_buttons[event.code] = event.state  # 트리거 입력 처리 (좌측, 우측 트리거)

            elif event.ev_type == 'Key':  # 버튼 입력 처리
                last_buttons[event.code] = event.state  # 버튼 상태 업데이트
                if event.state == 1:  # 버튼이 눌릴 때
                    handle_button_press(tello, event.code, event.state)

        # 조이스틱 입력에 따라 드론 제어
        tello.send_rc_control(lx, ly, ry, rx)

# 트리거 버튼 상태에 따른 속도 조정
def get_speed(last_buttons):
    if last_buttons.get('ABS_RZ', 0) > 128:  # 우측 트리거 50% 이상
        return 100
    elif last_buttons.get('ABS_Z', 0) > 128:  # 좌측 트리거 50% 이상
        return 10
    return 50

# 조이스틱 입력을 스케일링하는 함수
def scale_input(value, max_speed):
    deadzone = int(32767 * 0.2)  # 20% 데드존
    if -deadzone < value < deadzone:
        return 0
    if value == 32767 or value == -32767:
        return max_speed * (1 if value > 0 else -1)
    return int(value / 32767 * max_speed)

# 컨트롤러 입력을 별도의 스레드에서 처리
controller_thread = threading.Thread(target=lambda: process_controller_input(tello))
controller_thread.start()

# 프로그램 종료 대기
try:
    controller_thread.join()
except KeyboardInterrupt:
    print("Program interrupted, exiting.")

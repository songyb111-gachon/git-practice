from djitellopy import Tello
import cv2
import threading
import pygame
from datetime import datetime

# Pygame 초기화
pygame.init()
pygame.display.set_mode((400, 300))  # 필요 없는 윈도우지만 pygame을 시작하기 위해 필요

# 드론 객체 초기화 및 연결
tello = Tello()
tello.connect()
print(f"Battery: {tello.get_battery()}%")

# 드론 스트림 시작
tello.streamon()
frame_read = tello.get_frame_read()

# 비디오 저장 설정 (압축률이 낮은 MJPG 코덱 사용)
width = 960
height = 720
fourcc = cv2.VideoWriter_fourcc(*'MJPG')  # 코덱 변경: MJPG
current_time = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
video_filename = f'tello_video_{current_time}.avi'
out = cv2.VideoWriter(video_filename, fourcc, 30.0, (width, height))  # 비디오 파일 이름, 코덱, FPS, 프레임 크기

# 비디오 스트리밍 처리 함수
def video_stream():
    while True:
        img = frame_read.frame
        if img is not None:
            cv2.imshow("drone", img)
            out.write(img)  # 프레임을 비디오 파일에 저장

        if cv2.waitKey(1) & 0xFF == 27:  # ESC 키 감지
            break

    cv2.destroyAllWindows()

# 비디오 스트리밍을 별도의 스레드에서 실행
video_thread = threading.Thread(target=video_stream)
video_thread.start()

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
tello.streamoff()  # 스트림 중지
out.release()  # 비디오 파일 저장 종료

# 비디오 스레드 종료 대기
video_thread.join()
cv2.destroyAllWindows()
pygame.quit()

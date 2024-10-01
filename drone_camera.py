from djitellopy import tello
import cv2

drone = tello.Tello()
drone.connect()
print(f"Battery: {drone.get_battery()}%")

drone.streamon()

while True:
    img = drone.get_frame_read().frame
    img = cv2.resize(img, (960, 720))
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    cv2.imshow("Tello Camera", img)
    cv2.waitKey(1)

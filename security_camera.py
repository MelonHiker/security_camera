import cv2
from time import strftime, localtime, time


fourcc = cv2.VideoWriter_fourcc(*"mp4v")
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")

RECORD_GAP = 5
recording = False
record_stop_time = None


cap = cv2.VideoCapture(0)
frame_size = (int(cap.get(3)), int(cap.get(4)))

while True:
    _, frame = cap.read()

    gary_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gary_frame, 1.2, 5)

    if len(faces) > 0:
        if not recording and (record_stop_time is None or (time() - record_stop_time) > RECORD_GAP):
            recording = True
            cur_time = strftime("%Y_%m_%d_%H.%M.%S", localtime())
            out = cv2.VideoWriter(f"{cur_time}.mp4", fourcc, 20, frame_size)
            print("Recording...")
    elif recording:
        out.release()
        record_stop_time = time()
        recording = False
        print("Stop!")

    if recording:
        out.write(frame)

    for (x, y, width, height) in faces:
        cv2.rectangle(frame, (x, y), (x + width, y + height), (255, 0, 0), 3)

    cv2.imshow("Camera", frame)

    if cv2.waitKey(1) == ord('q'):
        break

out.release()
cap.release()
cv2.destroyAllWindows()
import cv2
import apriltag

cap = cv2.VideoCapture(0)
detector = apriltag.Detector(apriltag.DetectorOptions(families='tag36h11'))
font = cv2.FONT_HERSHEY_SIMPLEX

while True:
    ret, orig_frame = cap.read()
    gray_frame = cv2.cvtColor(orig_frame, cv2.COLOR_BGR2GRAY)
    tags = detector.detect(gray_frame)

    for tag in tags:
        for i in range(4):
            point = [int(x) for x in tag.corners[i]]
            cv2.circle(orig_frame, point, 2, (255, 0, 0), 10)
            cv2.putText(orig_frame, str(tag.tag_id), [x + 7 for x in point], font, 0.8, (255, 0, 0), 1)

    cv2.imshow('Apriltags:', orig_frame)
    if cv2.waitKey(1) & 0xFF == ord('e'):
        cap.release()
        cv2.destroyAllWindows()

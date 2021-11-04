#!/usr/bin/env python3
import cv2
import rospy
from sensor_msgs.msg import Image

class CameraNode:
    def __init__(self):
        self.cap = cv2.VideoCapture(0)
        self.pub = rospy.Publisher("/camera/image_rect", Image, queue_size=10)
        rospy.init_node('camera_pub', anonymous=True)
        self.rate = rospy.Rate(30)
        self.width = self.cap.get(cv2.CAP_PROP_FRAME_WIDTH)
        self.height = self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT)

    def frame_capture(self):
        self.ret, self.frame = self.cap.read()
        if self.ret:
            self.pub.publish(Image(data=self.frame))
        self.rate.sleep()

    def __del__(self):
        self.cap.release()


if __name__ == '__main__':
    cam = CameraNode()
    while not rospy.is_shutdown():
        cam.frame_capture()

#!/usr/bin/env python2

# Node that captures Image frames from a topic and saves them

import rospy
from std_msgs.msg import String
from sensor_msgs.msg import Image
import cv2
import time
from datetime import datetime
from cv_bridge import CvBridge, CvBridgeError

counter = 0
time_elapsed = 0
last_time = int(round(time.time() * 1000))
bridge = CvBridge()

def image_callback(msg):
    global time_elapsed
    global counter
    global last_time

    if time_elapsed > 125: #8fps
        time_elapsed = 0
        print("Received an image!")
        try:
            # Convert your ROS Image message to OpenCV2
            cv2_img = bridge.imgmsg_to_cv2(msg, "bgr8")
        except CvBridgeError, e:
            print(e)
        else:
            # Save your OpenCV2 image as a jpeg
            cv2.imwrite('/home/nimbus/friday_dataset/' + str(time.time()) + '.jpeg', cv2_img)
            counter += 1

    time_elapsed += int(round(time.time() * 1000)) - last_time
    last_time = int(round(time.time() * 1000))
    
def listener():
    rospy.init_node('listener', anonymous=True)

    rospy.Subscriber("/camera/image_raw", Image, image_callback)

    rospy.spin()

if __name__ == '__main__':
    listener()

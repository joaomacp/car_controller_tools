#!/usr/bin/env python2

# Node that reads darknet_ros recognitions, and plays sounds accordingly (or, in the future, displays visual feedback)

import rospy

from darknet_ros_msgs.msg import BoundingBoxes, BoundingBox

from playsound import playsound

SOUNDS_DIR = '/home/nimbus/catkin_ws/src/car_controller_tools/sounds/'
FRAMES_TO_RECOGNIZE = 2 # TODO when we have more FPS, increase this number

traffic_sign_counters = {}

def object_callback(msg):
  signs_found = []

  for box in msg.bounding_boxes:
    traffic_sign = box.Class
    signs_found.append(traffic_sign)

    if traffic_sign not in traffic_sign_counters:
      traffic_sign_counters[traffic_sign] = 0

    traffic_sign_counters[traffic_sign] += 1
    if traffic_sign_counters[traffic_sign] >= FRAMES_TO_RECOGNIZE:
      traffic_sign_counters[traffic_sign] = 0
      playsound(SOUNDS_DIR + traffic_sign + '.ogg')

  for sign in traffic_sign_counters:
    if sign not in signs_found:
      traffic_sign_counters[sign] = 0

def listener():
    rospy.init_node('traffic_recognizer', anonymous=True)
    rospy.Subscriber("/darknet_ros/bounding_boxes", BoundingBoxes, object_callback)
    rospy.spin()

if __name__ == '__main__':
    listener()
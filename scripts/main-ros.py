#!/usr/bin/env python

###############################
######### 2021/07/31 ##########
#### WebRTC + ROS Melodic #####
#### Author: Moon Seokjun  ####
###############################


from selenium import webdriver
import cv2
import platform
from multiprocessing import Process, Manager
import time
import os
# from pathlib import path
import json
import ast

import rospy
from std_msgs.msg import String
from sensor_msgs.msg import LaserScan
from geometry_msgs.msg import Twist


# Setup webdriver & network
options = webdriver.ChromeOptions()                                     # Webdriver option
# options.add_argument("--disable-infobars")                            # Don't use infobar
options.add_argument('--start-fullscreen')                              # Start at F11; Full screan
options.add_argument("--disable-extensions")                            # Disable Chrome extension program
options.add_experimental_option("prefs", { \
    "profile.default_content_setting_values.media_stream_mic": 1,       # Able Media Mike
    "profile.default_content_setting_values.media_stream_camera": 1,    # Able Media Camera
    "profile.default_content_setting_values.geolocation": 1,            # Able Location
    "profile.default_content_setting_values.notifications": 1           # Able Alert
})

try:
    current_os = platform.system()

    if current_os == "Windows":  # Driver for window
        driver = webdriver.Chrome(executable_path='./Windows/chromedriver', options=options)
    elif current_os == "Linux":  # Driver for Linux
        driver = webdriver.Chrome(executable_path='./Linux/chromedriver', options=options)
except:
    driver = webdriver.Chrome(options=options)


def ScanData(data):
    #rospy.loginfo(rospy.get_caller_id() + 'Lidar LaserScan data:%s', data)

    # Sensing Data & Robot parameters
    ''' sensor_msgs/LaserScan Message Definition
    std_msgs/Header header
    float32 angle_min
    float32 angle_max
    float32 angle_increment
    float32 time_increment
    float32 scan_time
    float32 range_min
    float32 range_max
    float32[] ranges
    float32[] intensities '''
    LIDAR_data = data.ranges

    #if LIDAR_data is not None:
    send_json = json.dumps({'LIDAR_data': LIDAR_data})
    driver.execute_script('sendData('+send_json+')')        # Send data

def ControlData():
    pub = rospy.Publisher('remote_message', String, queue_size=1)

    msg_dict = {}
    while not rospy.is_shutdown():
        remote_message = driver.execute_script("return getData()")

        if type(remote_message) != type(None):
            # type of remote message is unicode
            msg_dict = json.loads(remote_message)
            rospy.loginfo(rospy.get_caller_id() + ' remote message:%s', msg_dict)

            pub.publish(remote_message)


if __name__=="__main__":
    abs_path = os.path.abspath("./")
    driver.get(url='file:///'+abs_path+'/rail.html')        # Connect to web site

    # Setup ROS node
    rospy.init_node('webrtc_main');
    rospy.Subscriber('/scan', LaserScan, ScanData)
    ControlData()

    # Start running
    rospy.spin()

    # driver.quit()

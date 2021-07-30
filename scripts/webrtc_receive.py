#!/usr/bin/env python

## Base : https://github.com/JeonHyeongJunKW/WebRTC-RAIL.git

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

import rospy
from std_msgs.msg import String
from sensor_msgs.msg import Image
from sensor_msgs.msg import LaserScan


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

current_os = platform.system()

try:
    current_os = platform.system()

    if current_os == "Windows":  # Driver for window
        driver = webdriver.Chrome(executable_path='./Windows/chromedriver', options=options)
    elif current_os == "Linux":  # Driver for Linux
        driver = webdriver.Chrome(executable_path='./Linux/chromedriver', options=options)
except:
    driver = webdriver.Chrome(options=options)


def ReceiveData(lidar_que, camera_que):
    remote_message = []
    while True:
        remote_message = driver.execute_script("return getData()")
        if remote_message is not None:
            print(remote_message)


if __name__=="__main__":
    abs_path = os.path.abspath("./")
    driver.get(url='file:///'+abs_path+'/rail.html')  # Connect to web site

    # Setup ROS node
    rospy.init_node('webrtc_receive');

    # Start running
    rospy.spin()

    # driver.quit()

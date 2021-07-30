#!/usr/bin/env python

## Base : https://github.com/JeonHyeongJunKW/WebRTC-RAIL.git

###############################
######### 2021/07/26 ##########
#### WebRTC + ROS Melodic #####
#### Author: Moon Seokjun  ####
###############################


from selenium import webdriver
import cv2
import platform
from multiprocessing import Process, Manager, Queue, Pool
import time
import os
# from pathlib import path
import json

import rospy
from std_msgs.msg import String
from sensor_msgs.msg import LaserScan
from sensor_msgs.msg import Image


def ScanData(data):
    #rospy.loginfo(rospy.get_caller_id() + 'Lidar LaserScan data:%s', data.ranges[:3])

    # Sensing Data & Robot parameters
    #current_location = [1,1,0]
    LIDAR_data = data
    lidar_que.put(LIDAR_data)

def ImageData(data):
    # Camera image data
    CAMERA_data = data
    camera_que.put(CAMERA_data)

def TransData(lidar_que, camera_que):
    while True:
        LIDAR_data = lidar_que.get()
        CAMERA_data = camera_que.get()

        if LIDAR_data is not None and CAMERA_data is not None:
            #print(LIDAR_data)
            send_json = json.dumps({'LIDAR data': LIDAR_data, 'CAMERA_data': CAMERA_data})
            driver.execute_script('sendData('+send_json+')')                # Send Data
            print(send_json)


if __name__=="__main__":
    lidar_que = Queue()
    camera_que = Queue()

    # Parallel process
    pool = Pool(2, TransData, (lidar_que, camera_que))

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

    if current_os == "Windows":  # Driver for window
        driver = webdriver.Chrome(executable_path='./Windows/chromedriver', options=options)
    elif current_os == "Linux":  # Driver for Linux
        driver = webdriver.Chrome(executable_path='./Linux/chromedriver', options=options)

    abs_path = os.path.abspath("./")

    driver.get(url='file:///'+abs_path+'/rail.html')  # Connect to web site


    # Setup ROS node
    rospy.init_node('webrtc_transmit');
    rospy.Subscriber('/scan', LaserScan, ScanData)
    rospy.Subscriber('/jetbot_camera/raw', Image, ImageData)


    # Start running
    rospy.spin()

    # driver.quit()

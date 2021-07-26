#!/usr/bin/env python

###############################
### 2021/07/26 ################
### WebRTC + ROS Melodic ######
### Author: Moon Seokjun  #####
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


def Lidar_subscriber(data):
    rospy.loginfo(rospy.get_caller_id() + 'Lidar data:%s', data)

if __name__=="__main__":
    # Setup webdriver & network
    options = webdriver.ChromeOptions()             # 옵션을 추가합니다.
    # options.add_argument("--disable-infobars")    #infobar를 안씁니다.
    options.add_argument('--start-fullscreen')      # F11풀화면으로 시작합니다.
    options.add_argument("--disable-extensions")    # 크롬 확장 프로그램을 안씁니다.
    options.add_experimental_option("prefs", { \
        "profile.default_content_setting_values.media_stream_mic": 1,       # 미디어 마이크 허용
        "profile.default_content_setting_values.media_stream_camera": 1,    # 미디어 카메라 허용
        "profile.default_content_setting_values.geolocation": 1,            # 현재위치 파악허용
        "profile.default_content_setting_values.notifications": 1           # 알림허용
    })

    current_os = platform.system()

    if current_os == "Windows":  # 현재 os가 윈도우라면, 윈도우용 드라이버를 쓴다.
        driver = webdriver.Chrome(executable_path='./Windows/chromedriver', options=options)
    elif current_os == "Linux":  # 현재 os가 리눅스라면, 리눅스용
        driver = webdriver.Chrome(executable_path='./Linux/chromedriver', options=options)

    abs_path = os.path.abspath("./")

    driver.get(url='file:///'+abs_path+'/rail.html')  # 사이트에 접속합니다.


    # Setup ROS node
    rospy.init_node('webrtc_ros');
    rospy.Subscriber('''LIDAR Data, LIDAR Data type, Lidar_subscriber''')


    ##로봇 파라미터
    current_location = [1,1,0]
    LIDAR_data = [1,2,3]
    remote_message = []
    while True:
        send_json = json.dumps({'current_location': current_location, 'LIDAR_data': LIDAR_data})
        driver.execute_script('sendData('+send_json+')')#보내기
        remote_message = driver.execute_script("return getData()")
        print(remote_message)


    # Start running
    rospy.spin()

    # driver.quit()

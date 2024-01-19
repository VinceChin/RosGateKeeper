#!/usr/bin/env python
# -*- coding: utf-8 -*-

import rospy
from std_msgs.msg import String
import subprocess
import threading
import os
import cv2
import random
import json
import requests
import base64

DEFAULT_FACE_SERVICE_URL = "https://01bc-103-18-0-18.ngrok-free.app/face_detect"
DEFAULT_VIDEO_DEVICE = "/dev/video0"

class VideoRecorder:
    def __init__(self):
        self.video_file = 'output.mp4'
        self.frame_numbers = []
        self.facerecognition_service_url = rospy.get_param('~facial_recognition_url', DEFAULT_FACE_SERVICE_URL)
        self.video_device = rospy.get_param('~video_device', DEFAULT_VIDEO_DEVICE)

        self.keyword_sub = rospy.Subscriber("recognition_result", String, self.keyword_callback)
        self.pub = rospy.Publisher('/speech_topic', String, queue_size=10)

    def keyword_callback(self, msg):
        # to record faces
        if msg.data.lower() ==  "start recording":
            rospy.loginfo("Someone try to add a new face.")
            self.pub.publish("name") # ask for real name
        elif msg.data.lower().startswith("my name is"): # get the name for face respectively
            start_index = len("My name is")
            # slice the sentecne to get the name
            name = msg.data[start_index:].strip()

            rospy.loginfo('Start Recording Face.')
            self.start_recording()
            files = self.images_to_files()
            self.delete_recording()

            data = {
                'state': 1,
                'name': name,
            }

            # 将数据转换为 JSON 字符串
            json_data = json.dumps(data)
            response = requests.post(self.facerecognition_service_url, files=files, data=data)
            # check status code
            if response.status_code == 200:
                # retrieve data
                data = response.json() 
                rospy.loginfo(data)
                result_code = data.get('result') 

                if result_code == 0:
                    rospy.loginfo("Successfully recorded the face.")
                    self.pub.publish("record success")
                else:
                    rospy.loginfo("Failed to record face")
                    self.pub.publish("record failure")
                return
            else:
                rospy.logerr("HTTP error " + str(response.status_code) + " : " + response.text.encode('utf-8'))
                self.pub.publish("record failure")
                return 
        elif "unlock" in msg.data.lower() :
            rospy.loginfo('Start Facial Recognition.')
            self.start_recording()
            files = self.images_to_files()
            self.delete_recording()

            data = {
                'state' : 0
            }
            response = requests.post(self.facerecognition_service_url, files=files, data=data)

            if response.status_code == 200:
                # retrieve data
                data = response.json() 
                result_code = data.get('result') 
                rospy.loginfo(data)

                if result_code == 0:
                    name = data.get('name')
                    rospy.loginfo("Successfully unlock people is %s." %name)
                    self.pub.publish(name)
                else:
                    rospy.loginfo("Failed to recognize face")
                    self.pub.publish("unlock failure")
                return
            else:
                rospy.logerr("HTTP error " + str(response.status_code) + " : " + response.text.encode('utf-8'))
                self.pub.publish("unlock failure")
                return 

            return

    def images_to_files(self):
        files = []

        for i in range(len(self.frame_numbers)):
            output_image = 'output_%d.jpeg' % self.frame_numbers[i]
            with open(output_image, 'rb') as image_file:
                image_data = image_file.read() 
                image_base64 = base64.b64encode(image_data)
                files.append(('image_%d' % i, (output_image, image_base64, 'image/jpeg')))

        json_file_path = 'files.json'
        with open(json_file_path, 'w') as json_file:  
            json.dump(files, json_file)

        return files

    def start_recording(self):
        rospy.loginfo("Starting video recording...")
        self.record_video()

    def delete_recording(self):
        current_directory = os.getcwd()
        rospy.loginfo('Current Directory: %s' %current_directory)

        try:
            os.remove(self.video_file)
            rospy.loginfo('Delete output.mp4 successfully')
            for frame_number in self.frame_numbers:
                output_image = 'output_%d.jpeg' % frame_number
                os.remove(output_image)
                rospy.loginfo('Delete %s successfully' %output_image)
            rospy.loginfo("Related Information is successfully deleted.")
        except OSError as e:
            rospy.logerr("An error occured while deleting the video & frames: %s" %e)

    def record_video(self):
        # use ffmpeg to reocord this video
        try:
            record_command = 'ffmpeg -f v4l2 -i '+self.video_device +'-t 2 ' + self.video_file
            subprocess.call(record_command, shell=True)
            rospy.loginfo("Video recording stopped.")
            # select 5 random frames
            video = cv2.VideoCapture('output.mp4')
            fps = video.get(cv2.CAP_PROP_FPS)
            video.release()
            rospy.loginfo("Video fps is %s", str(fps))
            total_frames = 2 * fps
        
            self.frame_numbers = random.sample(range(int(total_frames)), 5)
            for frame_number in self.frame_numbers:
                output_image = 'output_%d.jpeg' % frame_number
                command = 'ffmpeg -i %s -vf "select=\'eq(n\\,%d)\'" -vframes 1 %s' % (self.video_file, frame_number, output_image)
                subprocess.call(command, shell=True)

        except subprocess.CalledProcessError as e:
            # ffmpeg execution failed
            rospy.logerr("Failed to record video: ffmpeg command failed with return code: %s" % format(e.returncode))
        except Exception as e:
            # other exception
            rospy.logerr("An error occurred while recording video: %s" %e)


if __name__ == '__main__':
    rospy.init_node('custom_cam_node')
    recorder = VideoRecorder()
    rospy.spin()

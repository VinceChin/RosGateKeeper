#!/usr/bin/env python2
# -*- coding: utf-8 -*-

import rospy
from std_msgs.msg import String
import subprocess
import threading
import os

class VideoRecorder:
    def __init__(self):
        self.keyword_sub = rospy.Subscriber("recognition_result", String, self.keyword_callback)

    def keyword_callback(self, msg):
        self.start_recording()
        # to record faces
        if msg.data.lower() == "start recording":
            #TODO replace with uploading to the cloud and get response
            return 
        elif msg.data.lower() == "unlock":
            #TODO replace with uploading to the cloud and get response
            return

    def start_recording(self):
        rospy.loginfo("Starting video recording...")
        recording_thread = threading.Thread(target=self.record_video)
        recording_thread.start()

    def record_video(self):
        # use ffmpeg to reocord this video
        try:
            record_command = "ffmpeg -f v4l2 -i /dev/video0 -t 3 output.mp4"
            subprocess.call(record_command, shell=True)
            rospy.loginfo("Video recording stopped.")
        except subprocess.CalledProcessError as e:
            # ffmpeg execution failed
            rospy.logerr("Failed to record video: ffmpeg command failed with return code: %s" % format(e.returncode))
        except Exception as e:
            # other exception
            rospy.logerr("An error occurred while recording video: %s" %e)


if __name__ == '__main__':
    rospy.init_node('video_recorder_node')
    recorder = VideoRecorder()
    rospy.spin()
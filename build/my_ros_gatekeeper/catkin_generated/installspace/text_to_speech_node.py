#!/usr/bin/env python2
# -*- coding: utf-8 -*-

import rospy
from std_msgs.msg import String
from gtts import gTTS
import os
import tempfile

def callback(data):
    rospy.loginfo("Speech msg: %s", data.data)
    if "name" in data.data:
        text = "Hello! what is your name?"
    elif "record success" in data.data:
        text = "Successfully recorded your face.."
    elif "record failure" in data.data:
        text = "Failed to record your face. Please try again"
    elif "unlock failure" in data.data:
        text = "Failed to unlock. Please try again!"
    else:
        text = "Welcome back %s" % data.data 

    tts = gTTS(text, lang='en')
    with tempfile.NamedTemporaryFile(delete=True, suffix='.mp3') as fp:
        tts.save(fp.name)
        os.system('mpg123 ' + fp.name)

def speech():
    rospy.init_node('text_to_speech_node')
    rospy.Subscriber("speech_topic", String, callback)
    rospy.spin()

if __name__ == '__main__':
    speech()

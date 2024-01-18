#!/usr/bin/env python
# -*- coding: utf-8 -*-

import rospy
from std_msgs.msg import String
import speech_recognition as sr
import requests


DEFAULT_VOICEPRINT_SERVICE_URL = "http://google.com"

def recognize_voiceprint(audio_data, service_url):
    files = {'audio': audio_data.get_wav_data()}
    response = requests.post(service_url, files=files)
    if response.status_code == 200:
        return response.json()  
    else:
        rospy.logerr("Failed to contact the voiceprint recognition service")
        return None

def recognize_speech(recognizer, source):
    audio_data = recognizer.listen(source)
    #use google transformation for default
    return recognizer.recognize_google(audio_data)

def speech_recognition_node():
    rospy.init_node('speech_recognition_node', anonymous=True)
    
    # get params for voice print server
    voiceprint_recognition_enabled = rospy.get_param('~voiceprint_recognition_enabled', False)
    voiceprint_service_url = rospy.get_param('~voiceprint_service_url', DEFAULT_VOICEPRINT_SERVICE_URL)

    pub = rospy.Publisher('/recognition_result', String, queue_size=10)
    recognizer = sr.Recognizer()
    
    with sr.Microphone() as source:
        rospy.loginfo("Speech recognition node is listening...")
        while not rospy.is_shutdown():
            try:
                if voiceprint_recognition_enabled:
                    # voice print recognition
                    result = recognize_voiceprint(recognize_speech(recognizer, source), voiceprint_service_url)
                    if result and result['match']:
                        rospy.loginfo("Owner has been recognized.")
                        pub.publish("Owner recognized")
                    else:
                        rospy.loginfo("Owner not recognized.")
                        pub.publish("Owner not recognized")
                else:
                    # only voice recognition
                    text = recognize_speech(recognizer, source)
                    rospy.loginfo("Recognized speech: %s " % text )
                    pub.publish(text)
            except sr.UnknownValueError:
                rospy.logwarn("Could not understand audio")
            except sr.RequestError as e:
                rospy.logerr("Could not request results; %s " %e )

if __name__ == '__main__':
    try:
        speech_recognition_node()
    except rospy.ROSInterruptException:
        pass

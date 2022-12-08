#! /usr/bin/env python3
from numpy import diff
import rospy
from std_msgs.msg import String
import time
import simpleaudio
import roslib
from std_srvs.srv import SetBool, SetBoolResponse, SetBoolRequest
roslib.load_manifest('zundam_orne')
import os
import re
import speech_recognition as sr

class speakNode():
    def __init__(self):
        self.sub = rospy.Publisher('speak_txt',String,1)
        self.srv = rospy.Service('test_speak', SetBool, self.callback_srv) 
        self.goal_sound =simpleaudio.WaveObject.from_wave_file(roslib.packages.get_pkg_dir('zundam_orne')+'/voice/goal.wav')
        self.white_sound =simpleaudio.WaveObject.from_wave_file(roslib.packages.get_pkg_dir('zundam_orne') +'/voice/white.wav')
        self.akete_sound =simpleaudio.WaveObject.from_wave_file(roslib.packages.get_pkg_dir('zundam_orne') +'/voice/akete.wav')
        self.auto_sound =simpleaudio.WaveObject.from_wave_file(roslib.packages.get_pkg_dir('zundam_orne')+'/voice/auto.wav')
        self.word = String()
    # def set_txt(txtfile):
    #     if os.path.exists(txtfile) == True:
    #         os.remove(txtfile)
    #     else:
    #         pass

    def listen_and_speak(self):
        r = sr.Recognizer()
        txt = "audio.txt"
        # set_txt(txt)

        while True:
            with sr.Microphone() as source:
                r.adjust_for_ambient_noise(source)
                print("Listening...")
                voice = r.listen(source)
                print("OK!")

                try:
                    print("Loading...")

                    pick_word = r.recognize_google(voice, language='ja-JP')
                    if ("あ"or"あー") in pick_word:
                        print(pick_word)
                        
                        # with open(txt,'a') as f:
                        #     f.write(pick_word + "\n")

                    elif "ストップ" in pick_word:
                        print("end")
                        break

                    else:
                        print("もう一回話して？")

                except Exception:
                    print("Error")
if __name__ == '__main__':
    rospy.init_node('listen_and_speak')

    time.sleep(1.0)
    speak_node = speakNode()
    print("ready")
    while not rospy.is_shutdown():
        speak_node.listen_and_speak()       
        rospy.sleep(1.0)
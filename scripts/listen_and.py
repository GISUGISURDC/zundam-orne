#! /usr/bin/env python3
from numpy import diff
import rospy
from std_msgs.msg import String
from std_srvs.srv import SetBool
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
        self.text_pub = rospy.Publisher('speak_txt',String,1)
        self.srv = rospy.Service('test_speak', SetBool, self.callback_srv) 
        self.re_sound =simpleaudio.WaveObject.from_wave_file(roslib.packages.get_pkg_dir('zundam_orne')+'/voice/re_hiro.wav')
        self.auto_sound =simpleaudio.WaveObject.from_wave_file(roslib.packages.get_pkg_dir('zundam_orne')+'/voice/auto_hiro.wav')
        self.word = String()
        self.start_call = rospy.ServiceProxy("/move",SetBool)
    # def set_txt(txtfile):
    #     if os.path.exists(txtfile) == True:
    #         os.remove(txtfile)
    #     else:
    #         pass
    # def callback_srv(self,data):
    #     resp = SetBoolResponse()
    #     if data.data == True:
    #         play_sound = self.auto_sound.play()
    #         play_sound.wait_done()

    def speak_function(self,data):
        if data == "re":
            play_sound = self.re_sound.play()
            play_sound.wait_done()
        if data == "stop":
            play_sound = self.stop_sound.play()
            play_sound.wait_done()
        if data == "auto":
            play_sound = self.auto_sound.play()
            play_sound.wait_done()


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
                if ("Alexa"or"アレクサ") in pick_word: #特定の単語を認識したら反応
                    print(pick_word) #聞き取った文章
                    #remove_pick_word = pick_word.replace("Alexa"or"アレクサ","") #特定の単語をテキストから削除
                    #remove_space = remove_pick_word.lstrip() #削除した単語の後のスペースを削除
                    if ("持ってきて"or"もってきて") in pick_word: #認識した音声に「持ってきて」と文字があったらサーバー側に処理を投げる
                       self.start_call(True)
                       self.speak_function("auto")
                    with open(txt,'a') as f:
                        f.write(pick_word + "\n")

                elif "ストップ" in pick_word: #「ストップ」といったらテキスト化するコードの終了
                    print("end")
                    break

                else:

                    print("もう一回話して？") #特定の単語がなかったらリトライ
                    self.speak_function("re")

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
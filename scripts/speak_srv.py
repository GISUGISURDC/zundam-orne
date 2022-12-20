#!/usr/bin/env python3

import os
import re
import speech_recognition as sr
from std_srvs.srv import SetBool, SetBoolResponse
import rospy

def set_txt(txtfile):
    if os.path.exists(txtfile) == True:
        os.remove(txtfile)
    else:
        pass

def StartCall_client(data):
    rospy.wait_for_service('move')
    move = rospy.ServiceProxy('move', SetBool)
    move(True)
    # try:
    #     move = rospy.ServiceProxy('move', SetBool)
    #     move(True)
    # except rospy.ServiceException, e:
    #     print("Service call failed: %s")

if __name__ == "__main__":
    r = sr.Recognizer()
    txt = "audio.txt"
    set_txt(txt)

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
                        StartCall_client()

                    with open(txt,'a') as f:
                        f.write(pick_word + "\n")

                elif "ストップ" in pick_word: #「ストップ」といったらテキスト化するコードの終了
                    print("end")
                    break

                else:
                    print("もう一回話して？") #特定の単語がなかったらリトライ

            except Exception:
                print("Error")
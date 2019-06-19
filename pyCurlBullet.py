# reference from sample coding from the tutorial
import requests
import os
import json


class pyCurlBullet:
    # constructor
    def __init__(self, token, message):
        self.__token = token
        self.__title = ""
        self.__message = message

    # send notification using PushBullet
    def __sendNotification(self):
        data_send = {"type": "note",
                     "title": self.__title,
                     "body": self.__message}

        resp = requests.post('https://api.pushbullet.com/v2/pushes',
                             data=json.dumps(data_send),
                             headers={'Authorization': 'Bearer '+self.__token,
                                      'Content-Type': 'application/json'})
        if resp.status_code != 200:
            raise Exception('Something wrong')
        else:
            print('complete sending')

    # execution function for the class
    def run(self):
        self.__title = os.popen('hostname -I').read()
        self.__sendNotification()

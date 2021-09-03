import json
import requests
import os
from time import sleep
from threading import Thread, Lock
from dotenv import load_dotenv

load_dotenv()


def get_method(url):
    return requests.get(url)


def post_method(url, data):
    return requests.get(url, data).json()


class TelegramBot:
    def __init__(self, token):
        self.url = {
            'url': 'https://api.telegram.org/bot{}/'.format(token),
            'lock': Lock()
        }

    def get_update(self):
        self.url['lock'].acquire()
        res = get_method(self.url['url']+"getUpdates")
        self.url['lock'].release()
        return res

    def delete_update(self, data):
        id = data['update_id'] + 1
        data = {
            'offset': id
        }
        self.url['lock'].acquire()
        res = post_method(self.url['url']+"getUpdates", data)
        self.url['lock'].release()
        return res

    def send_message(self, data, msg):
        id = data['message']['chat']['id']
        data_ = {
            'chat_id': id,
            'text': str(msg)
        }
        self.url['lock'].acquire()
        res = post_method(self.url['url']+"sendMessage", data_)
        self.url['lock'].release()
        return res

    def get_file(self, data):
        file_id = data['file_id']
        data_ = json.loads(post_method(
            self.url['url']+"getFile?file_id={}".format(file_id)).text)
        print(data)
        json_ = data_['result']['file_path']
        self.url['lock'].acquire()
        res = get_method(self.url['url']+f'{json_}').content
        self.url['lock'].release()
        return res


if __name__ == '__main__':
    token = os.environ.get("TOKEN")
    telegram = TelegramBot(token)
    # print(res)

    while True:
        while True:
            try:
                res = telegram.get_update().text
                x = json.loads(res)
                break
            except Exception as e:
                x = {'result': []}
                raise e
                # print(e.text)
        if 'result' in x and len(x['result']) > 0:
            for data in x['result']:
                Thread(target=telegram.delete_update, args=(data, )).start()
                if 'text' in data['message']:
                    if (data['message']['text'] == "/start"):
                        Thread(target=telegram.send_message,
                               args=(data, 'OK')).start()
                    if (data['message']['text'] == "Oi"):
                        Thread(target=telegram.send_message,
                               args=(data, 'Olá')).start()
                    # print(json.dumps(data, indent=1))
                    if 'message' in data and 'text' in data['message']:
                        print(data['message']['text'])   
                if 'document' in data['message']:
                    print(json.dumps(data['message']['document'], indent=1))
                if 'photo' in data['message']:
                    a = {}
                    for i in data['message']['photo'][0]:
                        a.update({i: data['message']['photo'][0][i]})
                    file = telegram.get_file(a)
                    print(json.dumps(a, indent=1))
                    # print(json.dumps(data['message']['photo'], indent=1))
                else:
                    print(json.dumps(data, indent=1))
                    pass
            sleep(1)

a = {
    'update_id': 703052441,
    'message': {
        'message_id': 111,
        'from': {
            'id': 515489999,
            'is_bot': False,
            'first_name': 'Josué',
            'last_name': 'Lopes',
            'username': 'JosueLopes598',
            'language_code': 'pt-br'
        },
        'chat': {
            'id': 515489999,
            'first_name': 'Josué',
            'last_name': 'Lopes',
            'username': 'JosueLopes598',
            'type': 'private'
        },
        'date': 1630671869,
        'photo': [{
            'file_id': 'AgACAgEAAxkBAANvYTIT_ZzVlH__LuRWi5SQD_eTQPsAAlCpMRtj7pBFbVbtdMYphM0BAAMCAANzAAMgBA',
            'file_unique_id': 'AQADUKkxG2PukEV4',
            'file_size': 2728,
            'width': 90,
            'height': 90
        },
            {
            'file_id': 'AgACAgEAAxkBAANvYTIT_ZzVlH__LuRWi5SQD_eTQPsAAlCpMRtj7pBFbVbtdMYphM0BAAMCAANtAAMgBA',
            'file_unique_id': 'AQADUKkxG2PukEVy',
            'file_size': 29224,
            'width': 320,
            'height': 320
        },
            {
            'file_id': 'AgACAgEAAxkBAANvYTIT_ZzVlH__LuRWi5SQD_eTQPsAAlCpMRtj7pBFbVbtdMYphM0BAAMCAAN4AAMgBA',
            'file_unique_id': 'AQADUKkxG2PukEV9',
            'file_size': 45832,
            'width': 512,
            'height': 512
        }
        ]
    }
}

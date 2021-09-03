import json, requests, os
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
        file_id = data['message']['document']['file_id']
        data_ = json.loads(post_method(self.url['url']+"getFile?file_id={}".format(file_id)).text)
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
                x =  json.loads(res)
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
                        Thread(target=telegram.send_message, args=(data, 'OK')).start()
                    if (data['message']['text'] == "Oi"):
                        Thread(target=telegram.send_message, args=(data, 'Olá')).start()
                    # print(json.dumps(data, indent=1))
                    if 'message' in data and 'text' in data['message']:
                        print(data['message']['text'])
                else:
                    print(data)
            sleep(1)
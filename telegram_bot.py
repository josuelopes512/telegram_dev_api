import json, requests, os
from time import sleep
from threading import Thread, Lock
from dotenv import load_dotenv

load_dotenv()

global config
token = os.environ.get("TOKEN")
config = {
    'url': 'https://api.telegram.org/bot{}'.format(token),
    'lock': Lock()
}
res = requests.get(config['url']+'/getUpdates').text

def delete_update(data):
    global config
    config['lock'].acquire()
    json = {
        'offset':data['update_id']+1
    }
    res = requests.post(config['url']+'/getUpdates', {'offset':data['update_id']+1})
    config['lock'].release()

def send_message(data, msg):
    global config
    json = {
        'chat_id': data['message']['chat']['id'],
        'text': str(msg)
    }
    config['lock'].acquire()
    res = requests.post(config['url']+'/sendMessage', json)
    config['lock'].release()

def get_file(file_path):
    global config

while True:
    while True:
        try:
            res = requests.get(config['url']+'/getUpdates').text
            x = json.loads(res)
            break
        except Exception as e:
            x = {'result': []}
            print(e)
    if 'result' in x and len(x['result']) > 0:
        for data in x['result']:
            Thread(target=delete_update, args=(data, )).start()
            if 'text' in data['message']:
                if (data['message']['text'] == "/start"):
                    Thread(target=send_message, args=(data, 'OK')).start()
                if (data['message']['text'] == "Oi"):
                    Thread(target=send_message, args=(data, 'Olá')).start()
                # print(json.dumps(data, indent=1))
                if 'message' in data and 'text' in data['message']:
                    print(data['message']['text'])
            else:
                print(data)
        sleep(0.5)

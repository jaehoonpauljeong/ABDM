import hashlib
import random
import threading as th
import time
import keyboard
from strgen import StringGenerator
from pymongo import MongoClient

### Insert your configuration for MongoDB Atlas ###
# user = ''
# password = ''
# hosts = []

clients = {}
key_database_num = 2

# MongoDB URI
URI = 'mongodb+srv://' + user + ':' + password + hosts[0]
clients['identity'] = MongoClient(URI)

URI = 'mongodb+srv://' + user + ':' + password + hosts[1]
clients['key_1'] = MongoClient(URI)

URI = 'mongodb+srv://' + user + ':' + password + hosts[2]
clients['key_2'] = MongoClient(URI)

URI = 'mongodb+srv://' + user + ':' + password + hosts[3]
clients['healthcare'] = MongoClient(URI)

def insert_document_for_hash(name, input_document):
    healthcare_hash_value = ''
    try:
        identity_hash_value = clients['identity']['identity_database']['identity'].find({'name': name})[0][
            'identity_hash_value']
        healthcare_hash_value += identity_hash_value
        for i in range(1, key_database_num + 1):
            key_hash_value = \
                clients['key_' + str(i)]['key_database']['key'].find({'identity_hash_value': identity_hash_value})[0][
                    'key_hash_value']
            healthcare_hash_value += key_hash_value

        healthcare_hash_value = hashlib.blake2b(healthcare_hash_value.encode('utf-8'), digest_size=64).hexdigest()
    except:
        is_collided = False
        while True:
            identity_data = {}
            nounce = str(StringGenerator("[\l\d]{" + str(64) + "}"))
            identity_data['name'] = name
            identity_data['identity_hash_value'] = hashlib.blake2b(nounce.encode('utf-8'), digest_size=64).hexdigest()

            if check_collision_for_hash('identity_hash_value', identity_data['identity_hash_value']):
                is_collided = True

            healthcare_hash_value += identity_data['identity_hash_value']
            clients['identity']['identity_database']['identity'].insert_one(identity_data)

            key_data = {}
            key_data['identity_hash_value'] = identity_data['identity_hash_value']
            for i in range(1, key_database_num+1):
                nounce = str(StringGenerator("[\l\d]{" + str(64) + "}"))
                key_data['key_hash_value'] = hashlib.blake2b(nounce.encode('utf-8'), digest_size=64).hexdigest()
                healthcare_hash_value += key_data['key_hash_value']
                clients['key_' + str(i)]['key_database']['key'].insert_one(key_data)

            healthcare_hash_value = hashlib.blake2b(healthcare_hash_value.encode('utf-8'), digest_size=64).hexdigest()
            if check_collision_for_hash('healthcare_hash_value', healthcare_hash_value):
                is_collided = True

            if is_collided:
                is_collided = False
            else:
                break

    input_document['healthcare_hash_value'] = healthcare_hash_value
    clients['healthcare']['healthcare_database']['healthcare'].insert_one(input_document)
    print('[{0}] Body Temperature: {1}, BPM:{2}'.format(name, input_document['body_temperature'], input_document['bpm']))
    print('')

def select_document_for_hash(name):
    healthcare_hash_value = ''
    try:
        identity_hash_value = clients['identity']['identity_database']['identity'].find({'name': name})[0]['identity_hash_value']
        healthcare_hash_value += identity_hash_value
        for i in range(1, key_database_num+1):
            key_hash_value = clients['key_' + str(i)]['key_database']['key'].find({'identity_hash_value': identity_hash_value})[0]['key_hash_value']
            healthcare_hash_value += key_hash_value

        healthcare_hash_value = hashlib.blake2b(healthcare_hash_value.encode('utf-8'), digest_size=64).hexdigest()
        for data in list(clients['healthcare']['healthcare_database']['healthcare'].find({'healthcare_hash_value': healthcare_hash_value})):
            print('[{0}] Body Temperature: {1}, BPM:{2}'.format(name, data['body_temperature'], data['bpm']))
    except:
        print('[{0}] 환자의 데이터는 존재하지 않습니다.'.format(name))
    print('')

def check_collision_for_hash(type, hash_value):
    collision_result = ''
    if type == 'identity_hash_value':
        collision_result = list(clients['identity']['identity_database']['identity'].find({'identity_hash_value': hash_value}))
    elif type == 'healthcare_hash_value':
        collision_result = list(clients['healthcare']['healthcare_database']['healthcare'].find({'healthcare_hash_value': hash_value}))

    if len(collision_result) == 0:
        return False
    else:
        return True

def delete_collection_for_hash():
    clients['identity']['identity_database']['identity'].drop()
    for i in range(1, key_database_num+1):
        clients['key_' + str(i)]['key_database']['key'].drop()
    clients['healthcare']['healthcare_database']['healthcare'].drop()


def create_input_document():
    input_document = {'body_temperature': random.uniform(36, 39), 'bpm': random.uniform(110, 140)}
    return input_document

def key_capture_thread():
    global keep_going
    keyboard.read_key() # enter input
    keyboard.read_key()
    keep_going = False

while True:
    print('')
    print('원하시는 옵션을 선택해주세요.')
    print('')
    print('[1] 헬스케어 데이터 저장')
    print('[2] 헬스케어 데이터 검색')
    print('[3] 헬스케어 데이터 삭제')
    print('[4] 종료')
    print('')
    input_option = input('Input: ')
    print('')

    if input_option == '1':
        keep_going = True
        name = input('환자의 이름을 입력해주세요: ')
        th.Thread(target=key_capture_thread, args=(), name='key_capture_thread', daemon=True).start()
        while keep_going:
            print('still going...')
            time.sleep(1)
            input_document = create_input_document()
            insert_document_for_hash(name, input_document)
    elif input_option == '2':
        name = input('환자의 이름을 입력해주세요: ')
        select_document_for_hash(name)
    elif input_option == '3':
        delete_collection_for_hash()
        print('데이터 삭제 완료')
    elif input_option == '4':
        break

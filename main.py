from encryption import AESCipher
from encryption import DESCipher
from encryption import TripleDESCipher
from pymongo import MongoClient
import time
import hashlib
from strgen import StringGenerator
import csv


### Insert your configuration for MongoDB Atlas ###
user = ''
password = ''
host = ''
database_name = ''
collection_name = ''

# MongoDB URI
URI = 'mongodb+srv://'
URI += user + ':'
URI += password
URI += host

client = MongoClient(URI)

aes_key = [0x10, 0x01, 0x15, 0x1B, 0xA1, 0x11, 0x57, 0x72, 0x6C, 0x21, 0x56, 0x57, 0x62, 0x16, 0x05, 0x3D,
        0xFF, 0xFE, 0x11, 0x1B, 0x21, 0x31, 0x57, 0x72, 0x6B, 0x21, 0xA6, 0xA7, 0x6E, 0xE6, 0xE5, 0x3F]
des_key = [0x10, 0x01, 0x15, 0x1B, 0xA1, 0x11, 0x57, 0x72]
triple_des_key = [0x10, 0x01, 0x15, 0x1B, 0xA1, 0x11, 0x57, 0x72, 0x6C, 0x21, 0x56, 0x57, 0x62, 0x16, 0x05, 0x3D]

def insert_document_for_encryption(input_document, database_name, collection_name, algorithm, encryption_key, result):
    start_time = time.time()
    documents = []
    for document in input_document:
        data = {}
        for key in document:
            if key == 'text':
                if algorithm.upper() == 'DES':
                    encrypted_data = DESCipher(bytes(encryption_key)).encrypt(document[key])
                elif algorithm.upper() == '3DES':
                    encrypted_data = TripleDESCipher(bytes(encryption_key)).encrypt(document[key])
                elif algorithm.upper() == 'AES':
                    encrypted_data = AESCipher(bytes(encryption_key)).encrypt(document[key])
                data[key] = encrypted_data
            else:
                data[key] = document[key]
        documents.append(data)
    client[database_name][collection_name].insert_many(documents)
    print('[' + algorithm + '] ' + "Storage Time:", time.time() - start_time)
    result.append(time.time() - start_time)

def select_document_for_encryption(database_name, collection_name, algorithm, encryption_key, result):
    start_time = time.time()
    for document in client[database_name][collection_name].find():
        data = {}
        for key in document:
            if key == 'text':
                if algorithm.upper() == 'DES':
                    decrypted_data = DESCipher(bytes(encryption_key)).decrypt(document[key]).decode('utf-8')
                elif algorithm.upper() == '3DES':
                    decrypted_data = TripleDESCipher(bytes(encryption_key)).decrypt(document[key]).decode('utf-8')
                elif algorithm.upper() == 'AES':
                    decrypted_data = AESCipher(bytes(encryption_key)).decrypt(document[key]).decode('utf-8')
                data[key] = decrypted_data
            else:
                data[key] = document[key]
        # print(data)
    print('[' + algorithm + '] ' + "Retrieval Time:", time.time() - start_time)
    result.append(time.time() - start_time)

def delete_collection_for_encryption():
    client['DES'][collection_name].drop()
    client['3DES'][collection_name].drop()
    client['AES'][collection_name].drop()


def insert_document_for_hash(input_document, database_name, collection_name, result):
    start_time = time.time()
    is_collided = False
    while True:
        identity_data = {}
        healthcare_hash_value = ''
        name = 'kjy'
        nounce = str(StringGenerator("[\l\d]{" + str(64) + "}"))
        identity_data['name'] = name
        identity_data['identity_hash_value'] = hashlib.blake2b(nounce.encode('utf-8'), digest_size=64).hexdigest()
        if check_collision_for_hash('identity_database', 'identity', 'identity_hash_value', identity_data['identity_hash_value']):
            is_collided = True

        healthcare_hash_value += identity_data['identity_hash_value']
        client['identity_database']['identity'].insert_one(identity_data)

        key_data = {}
        key_data['identity_hash_value'] = identity_data['identity_hash_value']
        for i in range(0, 3):
            nounce = str(StringGenerator("[\l\d]{" + str(64) + "}"))
            key_data['key_hash_value'] = hashlib.blake2b(nounce.encode('utf-8'), digest_size=64).hexdigest()
            healthcare_hash_value += key_data['key_hash_value']
            client['key_database']['key_' + str(i)].insert_one(key_data)

        healthcare_hash_value = hashlib.blake2b(healthcare_hash_value.encode('utf-8'), digest_size=64).hexdigest()
        if check_collision_for_hash('HASH', 'comments', 'healthcare_hash_value', healthcare_hash_value):
            is_collided = True

        if is_collided:
            is_collided = False
        else:
            break

    documents = []
    for document in input_document:
        document['healthcare_hash_value'] = healthcare_hash_value
        documents.append(document)
    client[database_name][collection_name].insert_many(documents)

    print('[CHBDMA] ' + "Storage Time:", time.time() - start_time)
    result.append(time.time() - start_time)

def select_document_for_hash(database_name, collection_name, result):
    start_time = time.time()
    healthcare_hash_value = ''
    identity_hash_value = client['identity_database']['identity'].find({'name': 'kjy'})[0]['identity_hash_value']
    healthcare_hash_value += identity_hash_value
    for i in range(0, 3):
        key_hash_value = client['key_database']['key_' + str(i)].find({'identity_hash_value': identity_hash_value})[0]['key_hash_value']
        healthcare_hash_value += key_hash_value

    healthcare_hash_value = hashlib.blake2b(healthcare_hash_value.encode('utf-8'), digest_size=64).hexdigest()
    data = list(client[database_name][collection_name].find({'healthcare_hash_value': healthcare_hash_value}))
    print('[CHBDMA] ' + "Retrieval Time:", time.time() - start_time)
    result.append(time.time() - start_time)

def check_collision_for_hash(database_name, collection_name, type, hash_value):
    collision_result = ''
    if type == 'identity_hash_value':
        collision_result = list(client[database_name][collection_name].find({'identity_hash_value': hash_value}))
    elif type == 'key_hash_value':
        collision_result = list(client[database_name][collection_name].find({'key_hash_value': hash_value}))
    elif type == 'healthcare_hash_value':
        collision_result = list(client[database_name][collection_name].find({'healthcare_hash_value': hash_value}))

    if len(collision_result) == 0:
        return False
    else:
        return True

def delete_collection_for_hash():
    client['identity_database']['identity'].drop()
    for i in range(0, 3):
        client['key_database']['key_' + str(i)].drop()
    client['HASH']['comments'].drop()


def insert_document_for_plaintext(input_document, database_name, collection_name, result):
    start_time = time.time()
    client[database_name][collection_name].insert_many(input_document)
    print('[PLAIN_TEXT] ' + "Storage Time:", time.time() - start_time)
    result.append(time.time() - start_time)

def select_document_for_plaintext(database_name, collection_name, result):
    start_time = time.time()
    data = list(client[database_name][collection_name].find())
    print('[PLAIN_TEXT] ' + "Retrieval Time:", time.time() - start_time)
    result.append(time.time() - start_time)

def delete_collection_for_plaintext():
    client['PLAIN_TEXT']['comments'].drop()


def create_input_document(document_num):
    input_document = []
    sample_documents = list(client[database_name][collection_name].find())
    for i in range(0, 20):
        for sample_document in sample_documents:
            temp_document = {}
            for key in sample_document:
                if key != '_id':
                    temp_document[key] = sample_document[key]
            input_document.append(temp_document)

    return input_document[0: document_num]


for i in range(1, 8):
    data_num = 100000*i
    input_document = create_input_document(data_num)
    print('Data Num:', len(input_document))
    f = open('data_num_' + str(data_num) + '.csv', 'w', newline='')
    wr = csv.writer(f)
    wr.writerow(
        ['', 'des-insert', 'des-select', '3des-insert', '3des-select', 'aes-insert', 'aes-select', 'hash-insert',
         'hash-select', 'plain-insert', 'plain-select'])
    for j in range(1, 11):
        result = [j]
        ##########################################################################################
        insert_document_for_encryption(input_document, 'DES', collection_name, 'DES', des_key, result)
        select_document_for_encryption('DES', collection_name, 'DES', des_key, result)
        delete_collection_for_encryption()

        insert_document_for_encryption(input_document, '3DES', collection_name, '3DES', triple_des_key, result)
        select_document_for_encryption('3DES', collection_name, '3DES', triple_des_key, result)
        delete_collection_for_encryption()

        insert_document_for_encryption(input_document, 'AES', collection_name, 'AES', aes_key, result)
        select_document_for_encryption('AES', collection_name, 'AES', aes_key, result)
        delete_collection_for_encryption()
        ##########################################################################################

        print('')

        ##########################################################################################
        insert_document_for_hash(input_document, 'HASH', collection_name, result)
        select_document_for_hash('HASH', collection_name, result)
        delete_collection_for_hash()
        ##########################################################################################

        print('')

        #########################################################################################
        insert_document_for_plaintext(input_document, 'PLAIN_TEXT', collection_name, result)
        select_document_for_plaintext('PLAIN_TEXT', collection_name, result)
        delete_collection_for_plaintext()
        #########################################################################################

        print('')

        ##########################################################################################
        delete_collection_for_encryption()
        delete_collection_for_hash()
        delete_collection_for_plaintext()
        ##########################################################################################

        print('')
        print('')

        wr.writerow(result)

    f.close()

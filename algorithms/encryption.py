from utils.encryption import AESCipher
from utils.encryption import DESCipher
from utils.encryption import TripleDESCipher
from utils.mongodb import client
from utils.mem_usage import mem_usage
import time

async def insert_document_for_encryption(input_document, algorithm, encryption_key, results):
    start_time = time.time()
    input_data = []
    for document in input_document:
        data = {}
        for key in document:
            if key == 'heartrate':
                if algorithm == 'des':
                    data[key] = DESCipher(bytes(encryption_key)).encrypt(document[key])
                elif algorithm == '3des':
                    data[key] = TripleDESCipher(bytes(encryption_key)).encrypt(document[key])
                elif algorithm == 'aes':
                    data[key] = AESCipher(bytes(encryption_key)).encrypt(document[key])
            else:
                data[key] = document[key]
        input_data.append(data)

    await client['encryption'][algorithm].insert_many(input_data)
    print('[' + algorithm + '] ' + "Storage Time:", time.time() - start_time)
    results.append(time.time() - start_time)
    results.append(mem_usage())

async def select_document_for_encryption(condition, algorithm, encryption_key, results):
    start_time = time.time()
    selected_data = []
    for document in await client['encryption'][algorithm].find({'name': condition['name']}).to_list(length=None):
        data = {}
        for key in document:
            if key == '_id':
                continue
            elif key == 'heartrate':
                if algorithm == 'des':
                    decrypted_data = DESCipher(bytes(encryption_key)).decrypt(document[key]).decode('utf-8')
                elif algorithm == '3des':
                    decrypted_data = TripleDESCipher(bytes(encryption_key)).decrypt(document[key]).decode('utf-8')
                elif algorithm == 'aes':
                    decrypted_data = AESCipher(bytes(encryption_key)).decrypt(document[key]).decode('utf-8')
                data[key] = decrypted_data
            else:
                data[key] = document[key]
        if condition['name'] == data['name']:
            selected_data.append(data)
        # print(data)
    print('[' + algorithm + '] ' + "Retrieval Time:", time.time() - start_time)
    print('num:', len(selected_data))
    results.append(time.time() - start_time)
    results.append(mem_usage())

async def delete_collection_for_encryption(algorithm):
    await client['encryption'][algorithm].drop()

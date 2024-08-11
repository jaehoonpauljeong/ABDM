import time
import hashlib
from strgen import StringGenerator
import asyncio
from copy import deepcopy
from utils.mem_usage import mem_usage
from utils.mongodb import client

async def insert_document_for_abdm(input_document, algorithm, results):
    start_time = time.time()
    hash_data = {}
    input_data = []
    for document in input_document:
        data = {}
        for key in document:
            data[key] = document[key]

        if document['name'] in hash_data:
            data['healthcare_hash_value'] = hash_data[document['name']]['healthcare_hash_value']
            input_data.append(data)
            continue

        identity_data = deepcopy(document)

        if await client['identity_database']['identity'].find_one({'name': document['name']}) is None:
            healthcare_hash_value = ''
            nounce = str(StringGenerator("[\l\d]{" + str(64) + "}"))

            identity_data['identity_hash_value'] = hashlib.blake2b(nounce.encode('utf-8'), digest_size=64).hexdigest()

            healthcare_hash_value += identity_data['identity_hash_value']
            await client['identity_database']['identity'].insert_one(identity_data)

            result = await make_create_key_hash_value_coroutine(identity_data['identity_hash_value'])

            for key_hash_value in result:
                healthcare_hash_value += key_hash_value
            healthcare_hash_value = hashlib.blake2b(healthcare_hash_value.encode('utf-8'), digest_size=64).hexdigest()

        else:
            healthcare_hash_value = ''
            identity_data = await client['identity_database']['identity'].find_one({'name': document['name']})['identity_hash_value']
            healthcare_hash_value += identity_data['identity_hash_value']

            result = await make_find_key_hash_value_coroutine(identity_data['identity_hash_value'])

            for key_hash_value in result:
                healthcare_hash_value += key_hash_value

            healthcare_hash_value = hashlib.blake2b(healthcare_hash_value.encode('utf-8'), digest_size=64).hexdigest()
        hash_data[document['name']] = {
            'identity_hash_value': identity_data['identity_hash_value'],
            'healthcare_hash_value': healthcare_hash_value
        }
        data['healthcare_hash_value'] = healthcare_hash_value
        input_data.append(data)
    await client[algorithm][algorithm].insert_many(input_data)
    print('[ABDM] ' + "Storage Time:", time.time() - start_time)
    results.append(time.time() - start_time)
    results.append(mem_usage())

async def create_key_hash_value(i, identity_hash_value):
    nounce = str(StringGenerator("[\l\d]{" + str(64) + "}"))
    key_hash_value = hashlib.blake2b(nounce.encode('utf-8'), digest_size=64).hexdigest()
    client['key_database']['key_' + str(i)].insert_one({'identity_hash_value': identity_hash_value, 'key_hash_value': key_hash_value})
    return key_hash_value

async def make_create_key_hash_value_coroutine(identity_hash_value):
    key_database_list = [0, 1, 2]
    futures = [asyncio.ensure_future(create_key_hash_value(i, identity_hash_value)) for i in key_database_list]
    result = await asyncio.gather(*futures)
    return result

async def select_document_for_abdm(condition, algorithm, results):
    start_time = time.time()

    document = await client['identity_database']['identity'].find_one({'name': condition['name']})

    healthcare_hash_value = ''
    identity_hash_value = document['identity_hash_value']
    healthcare_hash_value += identity_hash_value

    result = await make_find_key_hash_value_coroutine(identity_hash_value)

    for key_hash_value in result:
        healthcare_hash_value += key_hash_value

    healthcare_hash_value = hashlib.blake2b(healthcare_hash_value.encode('utf-8'), digest_size=64).hexdigest()

    data = await client[algorithm][algorithm].find({'healthcare_hash_value': healthcare_hash_value}).to_list(length=None)
    print('[ABDM] ' + "Retrieval Time:", time.time() - start_time)
    print('num:', len(data))
    results.append(time.time() - start_time)
    results.append(mem_usage())

async def find_key_hash_value(i, identity_hash_value):
    key_database = await client['key_database']['key_' + str(i)].find_one({'identity_hash_value': identity_hash_value})
    return key_database['key_hash_value']

async def make_find_key_hash_value_coroutine(identity_hash_value):
    key_database_list = [0, 1, 2]
    futures = [asyncio.ensure_future(find_key_hash_value(i, identity_hash_value)) for i in key_database_list]
    result = await asyncio.gather(*futures)
    return result

async def delete_collection_for_abdm(algorithm):
    await client['identity_database']['identity'].drop()
    for i in range(0, 3):
        await client['key_database']['key_' + str(i)].drop()
    await client[algorithm][algorithm].drop()
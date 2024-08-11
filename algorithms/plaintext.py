import time
from utils.mongodb import client
from utils.mem_usage import mem_usage

async def insert_document_for_plaintext(input_document, algorithm, results):
    start_time = time.time()
    await client[algorithm][algorithm].insert_many(input_document)
    print('[PLAIN_TEXT] ' + "Storage Time:", time.time() - start_time)
    results.append(time.time() - start_time)
    results.append(mem_usage())

async def select_document_for_plaintext(condition, algorithm, results):
    start_time = time.time()
    data = await client[algorithm][algorithm].find({'name': condition['name']}).to_list(length=None)
    print('[PLAIN_TEXT] ' + "Retrieval Time:", time.time() - start_time)
    print('num:', len(data))
    results.append(time.time() - start_time)
    results.append(mem_usage())

async def delete_collection_for_plaintext(algorithm):
    await client[algorithm][algorithm].drop()

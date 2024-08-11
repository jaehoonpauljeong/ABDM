import csv
import asyncio
import gc
from utils.data_generator import create_input_document
from algorithms.encryption import select_document_for_encryption
from algorithms.abdm import select_document_for_abdm
from algorithms.plaintext import select_document_for_plaintext


keys = {
    'des': [0x10, 0x01, 0x15, 0x1B, 0xA1, 0x11, 0x57, 0x72],
    'aes': [0x10, 0x01, 0x15, 0x1B, 0xA1, 0x11, 0x57, 0x72, 0x6C, 0x21, 0x56, 0x57, 0x62, 0x16, 0x05, 0x3D,
        0xFF, 0xFE, 0x11, 0x1B, 0x21, 0x31, 0x57, 0x72, 0x6B, 0x21, 0xA6, 0xA7, 0x6E, 0xE6, 0xE5, 0x3F],
    '3des': [0x10, 0x01, 0x15, 0x1B, 0xA1, 0x11, 0x57, 0x72, 0x6C, 0x21, 0x56, 0x57, 0x62, 0x16, 0x05, 0x3D]
}

async def main():

    algorithm = 'plaintext'   # des, aes, 3des, abdm, plaintext
    data_num = 100000   # 100000, 200000, 300000, 400000, 500000, 600000, 700000

    condition = {
        'name': 'bobby jackson',
    }

    input_document = create_input_document(data_num)
    print('Data Num:', len(input_document))

    f = open('results/' + algorithm + '/' + algorithm + '_data_num_' + str(data_num) + '_select_test.csv', 'w', newline='')
    wr = csv.writer(f)
    wr.writerow(
        ['', 'select-time', 'select-memory'])

    for j in range(1, 11):  # seed 1~10
        results = [j]

        if algorithm in ['des', 'aes', '3des']:

            print('')
            ##########################################################################################
            gc.collect()
            await select_document_for_encryption(condition, algorithm, keys[algorithm], results)
            gc.collect()
            ##########################################################################################

        elif algorithm in ['abdm']:

            print('')
            ##########################################################################################
            gc.collect()
            await select_document_for_abdm(condition, algorithm, results)
            gc.collect()
            ##########################################################################################

        elif algorithm in ['plaintext']:

            print('')

            #########################################################################################
            gc.collect()
            await select_document_for_plaintext(condition, algorithm, results)
            gc.collect()
            #########################################################################################

        wr.writerow(results)

    f.close()

loop = asyncio.get_event_loop()
loop.run_until_complete(main())
loop.close()
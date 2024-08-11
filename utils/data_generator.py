import csv

def create_input_document(document_num):
    index = 0
    data = []
    with open('data/original.csv', 'r') as file:
        csv_reader = csv.reader(file)
        next(csv_reader)
        for healthcare_data in csv_reader:
            if index == document_num:
                return data
            healthcare_data = {
                'datetime': healthcare_data[0],
                'name': healthcare_data[1],
                'age': healthcare_data[2],
                'gender': healthcare_data[3],
                'heartrate': healthcare_data[4],
            }
            data.append(healthcare_data)
            index += 1
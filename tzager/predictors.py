import pandas as pd
import json
import requests

def from_xls(password, file_path):

    df = pd.read_excel(file_path)
    data = df.to_dict('dict')
    columns = df.columns
    entities = df['Entities']
    samples_dict = {}
    for c in columns:
        if 'Sample' in c:
            samples_dict[c] = {}
            samples = df[c]
            for i, s in enumerate(samples):
                if s > 0:
                    samples_dict[c][entities[i]] = s
    
    response = requests.post('http://127.0.0.1:5000/predictors/' + password , json=json.dumps(samples_dict))
    if response.status_code == 200:
        data = dict(response.json())
    else:
        data = {'error': response.status_code}
        data = dict(data)
    return data


def from_csv(password, file_path):

    df = pd.read_csv(file_path)
    data = df.to_dict('dict')
    columns = df.columns
    entities = df['Entities']
    samples_dict = {}
    for c in columns:
        if 'Sample' in c:
            samples_dict[c] = {}
            samples = df[c]
            for i, s in enumerate(samples):
                if s > 0:
                    samples_dict[c][entities[i]] = s
    
    response = requests.post('https://cloud.bolooba.com:25556/predictors/' + password , json=json.dumps(samples_dict))
    if response.status_code == 200:
        data = dict(response.json())
    else:
        data = {'error': response.status_code}
        data = dict(data)
    return data


data_dict = from_xls("$biomedicine$", '/home/user/Desktop/txtpreprocess/g_cloud_bollooba/app/xls_microbiomes/test.xlsx')
print(data_dict.keys())
for s in data_dict['predictors_per_instance']:
    print('===', s, '===\n')
    for categ in data_dict['predictors_per_instance'][s]:
        print(categ, data_dict['predictors_per_instance'][s][categ])
        print()

print('--------------')
for categ in data_dict['overall_predictors']:
    print(categ, data_dict['overall_predictors'][categ])
    print()
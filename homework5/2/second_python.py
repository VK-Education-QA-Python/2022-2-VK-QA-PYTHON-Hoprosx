import re
import argparse
import json

parser = argparse.ArgumentParser()
parser.add_argument('--json', action='store_true')
args = parser.parse_args()

print("Общее количество запросов по типу, например: GET - 20, POST - 10")
path = input("Введите путь к файлу: ")

with open(path, 'r', encoding='utf-8') as log_file:
    log_file = log_file.read()
    get_count = str(len(re.findall('"GET', log_file)))
    delete_count = str(len(re.findall('"DELETE', log_file)))
    post_count = str(len(re.findall('"POST', log_file)))
    put_count = str(len(re.findall('"PUT', log_file)))

if args.json:
    dict = {
        'GET': get_count,
        'DELETE': delete_count,
        'POST': post_count,
        'PUT': put_count
    }

    json = json.dumps(dict)
    result_file_name = 'counted_requests.json'
    with open(result_file_name, 'w', encoding='utf-8') as result_file:
        result_file.write(json)
else:
    get = "GET: " + get_count
    delete = "DELETE: " + delete_count
    post = "POST: " + post_count
    put = "PUT: " + put_count

    result_file_name = 'counted_requests.txt'
    with open(result_file_name, 'w', encoding='utf-8') as result_file:
        result_file.write(get + '\n')
        result_file.write(delete + '\n')
        result_file.write(post + '\n')
        result_file.write(put + '\n')

print('Успешно, результат сохранен в файле:', result_file_name)

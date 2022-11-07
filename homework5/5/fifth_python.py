from collections import Counter
import argparse
import json

parser = argparse.ArgumentParser()
parser.add_argument('--json', action='store_true')
args = parser.parse_args()

print("Топ 5 пользователей по количеству запросов, которые завершились серверной (5ХХ) ошибкой")
path = input("Введите путь к файлу: ")

with open(path, 'r', encoding='utf-8') as log_file:
    log_file = log_file.readlines()
    result_list = []
    for row in log_file:
        splitted_row = row.split()
        if str(splitted_row[8]).startswith('5'):
            result_list.append(splitted_row[0])

result_list = dict(Counter(result_list))
result_list = sorted(result_list.items(), key=lambda item: item[1], reverse=True)

if args.json:
    result_file_name = 'ip_requests_with_status_code_5xx.json'
    dict = {id: None for id in range(1, 6)}
    with open(result_file_name, 'w', encoding='utf-8') as result_file:
        for i in range(1, 6):
            dict_with_data = {
                'ip': result_list[i][0],
                'amount': str(result_list[i][1])
            }
            dict[i] = dict_with_data
        json = json.dumps(dict)
        result_file.write(json)
else:
    result_file_name = 'ip_requests_with_status_code_5xx.txt'
    with open(result_file_name, 'w', encoding='utf-8') as result_file:
        for i in range(5):
            row = 'ip: ' + result_list[i][0] + ' amount ' + str(result_list[i][1]) + '\n'
            result_file.write(row)

print('Успешно, результат сохранен в файле: ' + result_file_name)

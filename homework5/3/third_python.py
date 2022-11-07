from collections import Counter
import argparse
import json

parser = argparse.ArgumentParser()
parser.add_argument('--json', action='store_true')
args = parser.parse_args()

print("Топ 10 самых частых запросов")
path = input("Введите путь к файлу: ")

with open(path, 'r', encoding='utf-8') as log_file:
    log_file = log_file.readlines()
    result_list = []
    for row in log_file:
        splitted_row = row.split()
        result_list.append(splitted_row[6])

result_list = dict(Counter(result_list))
result_list = sorted(result_list.items(), key=lambda item: item[1], reverse=True)

if args.json:
    result_file_name = 'top_requested_urls.json'
    dict = {id: None for id in range(1, 11)}
    with open(result_file_name, 'w', encoding='utf-8') as result_file:
        for i in range(1, 11):
            dict_with_data = {
                'url': result_list[i][0],
                'amount': str(result_list[i][1])
            }
            dict[i] = dict_with_data
        json = json.dumps(dict)
        result_file.write(json)
else:
    result_file_name = 'top_requested_urls.txt'
    with open(result_file_name, 'w', encoding='utf-8') as result_file:
        for i in range(10):
            row = 'url: ' + result_list[i][0] + ' | amount ' + str(result_list[i][1]) + '\n'
            result_file.write(row)

print('Успешно, результат сохранен в файле: ' + result_file_name)

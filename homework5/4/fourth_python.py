import argparse
import json

parser = argparse.ArgumentParser()
parser.add_argument('--json', action='store_true')
args = parser.parse_args()

print("Топ 5 самых больших по размеру запросов, которые завершились клиентской (4ХХ) ошибкой")
path = input("Введите путь к файлу: ")

with open(path, 'r', encoding='utf-8') as log_file:
    log_file = log_file.readlines()
    result_list = []
    for row in log_file:
        splitted_row = row.split()
        if str(splitted_row[8]).startswith('4'):
            result_list.append(splitted_row)

result_list = sorted(result_list, key=lambda key: int(key[11]), reverse=True)

if args.json:
    dict = {id: None for id in range(1, 6)}
    result_file_name = 'size_requests_with_4xx_status_code.json'
    with open(result_file_name, 'w', encoding='utf-8') as result_file:
        for i in range(1, 6):
            dict_with_data = {
                "url": result_list[i][6],
                "code": result_list[i][8],
                "size": result_list[i][9],
                "ip": result_list[i][0]
            }
            dict[i] = dict_with_data
        json = json.dumps(dict)
        result_file.write(json)
else:
    result_file_name = 'size_requests_with_4xx_status_code.txt'
    with open(result_file_name, 'w', encoding='utf-8') as result_file:
        for i in range(5):
            url = 'url: ' + result_list[i][6]
            result_file.write(url + '\n')
            code = 'status code: ' + str(result_list[i][8])
            result_file.write(code + '\n')
            size = 'size: ' + result_list[i][9]
            result_file.write(size + '\n')
            ip = 'ip: ' + result_list[i][0]
            result_file.write(ip + '\n')
            result_file.write('\n')

print('Успешно, результат сохранен в файле: ' + result_file_name)


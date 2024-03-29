import os.path
import re
import json
from collections import Counter

path = os.path.join(os.path.abspath(os.path.join(__file__, os.path.pardir)), 'access.txt')


def count_all_requests():
    with open(path, 'r', encoding='utf-8') as log_file:
        log_file = log_file.read()
        get_count = str(len(re.findall('^[0-9]', log_file)))

    dict = {
        'AMOUNT': get_count,
    }

    return dict


def types_of_requests():
    with open(path, 'r', encoding='utf-8') as log_file:
        log_file = log_file.read()
        get_count = str(len(re.findall('"GET', log_file)))
        delete_count = str(len(re.findall('"DELETE', log_file)))
        post_count = str(len(re.findall('"POST', log_file)))
        put_count = str(len(re.findall('"PUT', log_file)))

    dict = {
        'GET': get_count,
        'DELETE': delete_count,
        'POST': post_count,
        'PUT': put_count
    }

    return dict


def top_ten_popular_requests():
    with open(path, 'r', encoding='utf-8') as log_file:
        log_file = log_file.readlines()
        result_list = []
        for row in log_file:
            splitted_row = row.split()
            result_list.append(splitted_row[6])

    result_list = dict(Counter(result_list))
    result_list = sorted(result_list.items(), key=lambda item: item[1], reverse=True)

    main_dict = {id: None for id in range(1, 11)}
    for i in range(1, 11):
        dict_with_data = {
            'url': result_list[i][0],
            'amount': str(result_list[i][1])
        }
        main_dict[i] = dict_with_data

    return main_dict


def top_five_big_requests_with_4xx_status_code():
    with open(path, 'r', encoding='utf-8') as log_file:
        log_file = log_file.readlines()
        result_list = []
        for row in log_file:
            splitted_row = row.split()
            if str(splitted_row[8]).startswith('4'):
                result_list.append(splitted_row)

    result_list = sorted(result_list, key=lambda key: int(key[9]), reverse=True)

    dict = {id: None for id in range(1, 6)}

    for i in range(1, 6):
        dict_with_data = {
            "url": result_list[i][6],
            "code": result_list[i][8],
            "size": result_list[i][9],
            "ip": result_list[i][0]
        }
        dict[i] = dict_with_data

    return dict

def top_five_users_with_5xx_status_code_requests():
    with open(path, 'r', encoding='utf-8') as log_file:
        log_file = log_file.readlines()
        result_list = []
        for row in log_file:
            splitted_row = row.split()
            if str(splitted_row[8]).startswith('5'):
                result_list.append(splitted_row[0])

    result_list = dict(Counter(result_list))
    result_list = sorted(result_list.items(), key=lambda item: item[1], reverse=True)

    result_dict = {id: None for id in range(1, 6)}

    for i in range(1, 6):
        dict_with_data = {
            'ip': result_list[i][0],
            'amount': str(result_list[i][1])
        }
        result_dict[i] = dict_with_data

    return result_dict

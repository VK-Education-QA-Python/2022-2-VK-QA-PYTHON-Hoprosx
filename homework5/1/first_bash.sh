#!/bin/bash

echo -n 'Общее кол-во запросов: ' > number_of_requests.txt
grep -E '^[0-9]' $1 | wc -l >> number_of_requests.txt
echo 'Результат сохранен в number_of_requests.txt'
cat number_of_requests.txt


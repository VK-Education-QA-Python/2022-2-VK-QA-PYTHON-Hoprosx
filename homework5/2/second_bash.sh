#!/bin/bash

echo -n "GET - " > sorted_requests.txt
grep -E '"GET' $1 | wc -l >> sorted_requests.txt
echo -n "POST - " >> sorted_requests.txt
grep -E '"POST' $1 | wc -l >> sorted_requests.txt
echo -n "PUT - "  >> sorted_requests.txt
grep -E '"PUT' $1 | wc -l >> sorted_requests.txt
echo -n "DELETE - " >> sorted_requests.txt
grep -E '"DELETE' $1 | wc -l >> sorted_requests.txt
echo 'Результат сохранен в sorted_requests.txt'
cat sorted_requests.txt


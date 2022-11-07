#!/bin/bash

echo ' Кол-во | запрос' > top_requests.txt
awk '{print $7}'| sort | uniq -c | sort -rn | head >> top_requests.txt
echo 'Результат сохранен в top_requests.txt'
cat top_requests.txt

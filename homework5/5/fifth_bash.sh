#!/bin/bash

echo '   AMOUNT     IP' > 'top_5XX_requests.txt'
grep -E ' [5][0-9][0-9] ' $1 | awk '{print $1}' | sort | uniq -c | sort -rn | head -5 >> top_5XX_requests.txt
echo 'Результат сохранен в top_5XX_requests.txt'
cat top_5XX_requests.txt
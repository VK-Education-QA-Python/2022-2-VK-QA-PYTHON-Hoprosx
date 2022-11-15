#!/bin/bash

grep -E ' [4][0-9][0-9] ' $1 | awk '{print "url:", $7, "status_code:", $9 ,"size:", $10, "ip:", $1}'| sort -rnk6 | head -5 > 4XX_big_size.txt
echo 'Результат сохранен в 4XX_big_size.txt'
cat 4XX_big_size.txt


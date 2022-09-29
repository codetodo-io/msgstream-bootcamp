#!/bin/bash

# bash batch_test.sh

array=(1 10 100 1000 10000 100000)
for i in ${array[*]}
do
    python3 client.py $i
    python3 server.py
done

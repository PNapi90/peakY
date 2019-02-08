#!bin/bash

for i in {1..10}
do
    en=$(($i*25))
    ./peakY -t 2 -E $en
    echo $en done
done

#./peakY -t 2
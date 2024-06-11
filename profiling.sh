#!/bin/bash

# iterate over list of functions ['constant', 'linear', 'linear_close_resources']
for function in 'constant' 'linear' 'linear_close_resources'
do
    echo "Running $function"
    # runs functions one by one
    mprof run python facemesh_profiling.py $function
    # plots profiling results   
    mprof plot -o plots/$function.png
    # removes dat files
    rm *.dat
done

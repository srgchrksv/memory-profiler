#!/bin/bash

echo "Testing functions for same result"
mprof run python facemesh_profiling.py test
rm logs/*


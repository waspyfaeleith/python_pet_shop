#!/bin/sh

cd tests
for file in *test.py; do python3 $file; done
cd ..

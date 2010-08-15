#!/bin/sh

find . -name "*.pyc" -exec rm {} \;
find . -name "*.pyo" -exec rm {} \;
rm -rf screencast
rm -rf scripts
rm -rf build
rm -rf dist
rm -rf debian
rm MANIFEST
rm -rf pyarm_logs
rm -rf pyarm_figs

#!/bin/sh

egrep "class |def |return " $(find . -name "*.py")

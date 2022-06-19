#!/bin/bash
cd "$(dirname "$0")"

pybabel init -i ./messages.pot -d ./preklady -l $1

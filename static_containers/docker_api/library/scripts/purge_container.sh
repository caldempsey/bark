#!/usr/bin/env bash

if [ -z "$1" ]
  then
    echo "A container name must be specified as the first parameter."
    exit 0
fi

docker rm --force "$1"
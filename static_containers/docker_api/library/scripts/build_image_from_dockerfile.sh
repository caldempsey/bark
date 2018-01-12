#!/usr/bin/env bash

if [ -z "$1" ]
  then
    echo "No dockerfile directory supplied. You must supply the location directory of a dockerfile."
    exit 0
fi

if [ -z "$2" ]
  then
    echo "No image name supplied. You must supply the image name of the dockerfile."
    exit 0
fi

docker build -t "$2" "$1"

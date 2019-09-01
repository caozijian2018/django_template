#!/usr/bin/env bash

INFO_NEW_TAG=1

INFO_IMAGE_NAME=template


echo "=> just start build image ${INFO_IMAGE_NAME}:${INFO_NEW_TAG}"
docker build -t ${INFO_IMAGE_NAME}:${INFO_NEW_TAG} .
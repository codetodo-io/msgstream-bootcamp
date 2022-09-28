#!/bin/bash

if [ "${1-}" = "up" ]; then
    mkdir -p "${MSGSTREAM_BOOTCAMP_ROOT_DIR:-.}/volumes/vscode-extensions"
    chmod -R 777 "${MSGSTREAM_BOOTCAMP_ROOT_DIR:-.}/volumes"

    docker-compose -f ${MSGSTREAM_BOOTCAMP_ROOT_DIR:-.}/docker-compose-devcontainer.yml up -d
fi

if [ "${1-}" = "down" ]; then
    docker-compose -f ${MSGSTREAM_BOOTCAMP_ROOT_DIR:-.}/docker-compose-devcontainer.yml down
    rm -rf "${MSGSTREAM_BOOTCAMP_ROOT_DIR:-.}/volumes"
fi

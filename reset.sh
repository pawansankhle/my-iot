#!/bin/bash

FILES_PATH='/home/ist/private-workspace/iot/micropython/dev/common'
FIRMWARE_FILE_PATH='/home/ist/private-workspace/iot/micropython/'
TOOLS_PATH='/home/ist/private-workspace/iot/micropython/tools/'

remove_logs(){
    echo "Removing logs...."
    ampy --port /dev/ttyUSB0 rm micro.log 2>> /dev/null
    ampy --port /dev/ttyUSB0 rm micro.log.1 2>> /dev/null
}

init(){
    param=${1}
    if [ "${param}" == "firmware" ]; then
        python ${TOOLS_PATH}esptool.py --port /dev/ttyUSB0 erase_flash
        python ${TOOLS_PATH}esptool.py --port /dev/ttyUSB0 --baud 460800 write_flash --flash_size=detect -fm dio 0 ${FIRMWARE_FILE_PATH}esp8266-20171101-v1.9.3.bin
    fi

    if [ "${param}" == "files" ]; then
        remove_logs;
        OLD_PATH=${pwd};
        cd ${FILES_PATH}
        echo "coping main.py..."
        ampy --port /dev/ttyUSB0 put ../esp8266_525a8a00/main.py
        echo "coping config.py..."
        ampy --port /dev/ttyUSB0 put config.py
        echo "coping wifi.py..."
        ampy --port /dev/ttyUSB0 put wifi.py
        echo "coping mqtt_writer.py..."
        ampy --port /dev/ttyUSB0 put mqtt_writer.py
        echo "coping logger.py..."
        ampy --port /dev/ttyUSB0 put logger.py
        echo "coping update.py..."
        ampy --port /dev/ttyUSB0 put update.py
        cd ${OLD_PATH}
    fi


}

if [ "${1}" != "" ]; then
	init $1
else
	echo "not Enough Arguments!!"
    echo "usage: ./reset.sh {reset || files}"
	echo "Exiting!!"
    exit 1
fi

#!/bin/bash
# This script install aliyun SDK

function install_aliyun_sdk() {
    echo "please waiting for install aliyun-sdk for python..."
    sleep 1
    yum -y install python-devel &> /dev/null
    pip install aliyun-python-sdk-core &> /dev/null
    if [[ $? -eq 0 ]]; then
        echo "aliyun-sdk install successfully"
    else
        echo "aliyun-sdk install failed."
    fi
}

function get_pip_tool() {
    echo "please waiting for install pip tool"
    sleep 1
    python ./get-pip.py &> /dev/null 
    if [[ $? -eq 0 ]]; then
        echo "pip tool install successfully."
    else
        echo "pip tool install failed."
    fi
}

#check pip tool
pip --version &> /dev/null
if [[ $? -eq 0 ]]; then
    install_aliyun_sdk
else
    get_pip_tool
    install_aliyun_sdk 
fi

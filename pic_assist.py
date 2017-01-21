# !/usr/bin/env python3.5
# -*- coding: utf-8 -*-
"""
pic_assist
http://www.lewisjin.coding.me
~~~~~~~~~~~~~~~
This script implement by Jin Fagang.
: copyright: (c) 2017 Didi-Chuxing.
: license: Apache2.0, see LICENSE for more details.
"""
from random import sample
import re
import subprocess
import sys
import pickle
import time
import os
import platform
from importlib import util
qiniu = util.find_spec('qiniu')
clipboard = util.find_spec('clipboard')
tqdm = util.find_spec('tqdm')

if not qiniu:
    print('installing qiniu...')
    os.system('sudo pip3 install qiniu')
if not clipboard:
    print('installing clipboard...')
    os.system('sudo pip3 install clipboard')
if not tqdm:
    print('installing tqdm...')
    os.system('sudo pip3 install tqdm')
from qiniu import Auth, put_file, etag, urlsafe_base64_encode
import qiniu.config
import clipboard
from tqdm import tqdm


def upload(access_key, secret_key, bucket_name, local_file, save_name):
    try:
        for i in tqdm(range(800)):
            time.sleep(0.001)
            q = Auth(access_key=access_key, secret_key=secret_key)
            token = q.upload_token(bucket_name, key=save_name, expires=3600)

        ret, info = put_file(token, key=save_name, file_path=local_file)
        print('Upload Success!')
        return ret
    except ConnectionError:
        print('Connection Error! Upload failed!')
        exit()


def save_history(history_file, upload_link):
    with open(history_file, 'a') as f:
        f.write(upload_link + '\n')
        print('Link also saved to local history.md file.')


def write_to_clipboard(output):
    if is_linux():
        clipboard.copy(output)
    elif is_mac():
        process = subprocess.Popen(
            'pbcopy', env={'LANG': 'en_US.UTF-8'}, stdin=subprocess.PIPE)
        process.communicate(output.encode('utf-8'))


def is_windows():
    return 'Windows' in platform.system()


def is_linux():
    return 'Linux' in platform.system()


def is_mac():
    return 'Darwin' in platform.system()


def judge_type(file_path):
    all_type = ['jpg', 'jpeg', 'png', 'gif']
    if is_mac():
        split_list = file_path.split('\\')
        file_name = split_list[-1]
        type = str(file_name).split('.')[-1]
        if str(type) in all_type:
            return file_path
        else:
            return None
    if is_windows():
        split_list = file_path.split('/')
        type = split_list[-1]
        if str(type) in all_type:
            return file_path
        else:
            return None
    if is_linux():
        if file_path.startswith("'"):
            split_list = file_path.split('/')
            file_path = file_path.split("'")[1]
            file_name = split_list[-1].split("'")[0]
            type = str(file_name).split('.')[-1]
            if str(type) in all_type:
                return file_path
            else:
                return None
        else:
            split_list = file_path.split('/')
            file_name = split_list[-1]
            type = str(file_name).split('.')[-1]
            if str(type) in all_type:
                return file_path
            else:
                return None


def drag_file():
    local_file = input('\33[32;43m Drag your picture directly to terminal: \33[0m')
    local_file = str(local_file).rstrip()
    file_path = judge_type(local_file)
    if file_path:
        save_name = ''.join(sample('AaBbCcDdEeFfGgHhIiJjKkLlMmNnOoPpQqRrSsTtUuVvWwXxYyZz0123456789', 16))
        save_name = str(save_name + '.png')
        result_dict = upload(access_key=Access_Key, secret_key=Secret_Key, bucket_name=Bucket_Name,
                             local_file=file_path, save_name=save_name)
        picture_address = 'http://' + Bucket_Domin + '/' + result_dict['key']
        md_format_address = '![Picture](' + picture_address + ')'
        print(md_format_address)
        write_to_clipboard(md_format_address)
        save_history('history.md', md_format_address)
        print('Now address is on your pasteboard with MarkDown format, just paste to your MarkDown file.')
    else:
        print('\33[41m Ops, seems not a picture file. \33[0m')


if __name__ == '__main__':
    print('\33[30;43m ---Welcome to [final up]-your blog picture upload assistant © Jin Tian.--- \33[0m')
    try:
        user_info = open('user_info.pkl', 'rb')
        info_dict = pickle.load(user_info)
        Access_Key = info_dict['access_key']
        Secret_Key = info_dict['secret_key']
        Bucket_Name = info_dict['bucket_name']
        Bucket_Domin = info_dict['bucket_domin']
    except FileNotFoundError:
        print(''''Please Setup For First Run. If you want edit later, just delete 'user_info.pkl' file and run again.''')
        Access_Key = input('\33[31;47m 1. Paste your Qiniu Access Key from Qiniu Yun Developer Center: \33[0m')
        Secret_Key = input('\33[31;47m 2. Paste your Qiniu Secret Key: \33[0m')
        Bucket_Name = input('\33[31;47m 3. Paste your Bucket Name where you want save picture: \33[0m')
        Bucket_Domin = input('\33[31;47m 4. Paste your Bucket Dominate(*.bkt.clouddn.com): \33[0m')
        info_dict = {
            'access_key': Access_Key,
            'secret_key': Secret_Key,
            'bucket_name': Bucket_Name,
            'bucket_domin': Bucket_Domin
        }

        confirm = input('Are you sure to save this local info: (Y/n)')
        if confirm == 'y' or confirm == 'yes' or confirm == 'Y':
            user_info = open('user_info.pkl', 'wb')
            pickle.dump(info_dict, user_info)
            print('Local info saved!')
        else:
            print('Aborted!')
    time.sleep(1.5)
    if is_mac():
        os.system('clear')
    elif is_windows():
        os.system('cls')
    elif is_linux():
        os.system('clear')

    is_next = 'y'
    while is_next == 'y' or is_next == 'yes' or is_next == 'Y':
        drag_file()
        is_next = input('move on upload pictures?(y/n):')

    print('Bye!')





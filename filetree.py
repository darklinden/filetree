#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'darklinden'

import subprocess
import os
import shutil
import ntpath
import sys

def run_cmd(cmd):
    # print("run cmd: " + " ".join(cmd))
    p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out, err = p.communicate()
    if err:
        print(err)
    return out

def self_install(file, des):
    file_path = os.path.realpath(file)

    filename = file_path

    pos = filename.rfind("/")
    if pos:
        filename = filename[pos + 1:]

    pos = filename.find(".")
    if pos:
        filename = filename[:pos]

    to_path = os.path.join(des, filename)

    print("installing [" + file_path + "] \n\tto [" + to_path + "]")
    if os.path.isfile(to_path):
        os.remove(to_path)

    shutil.copy(file_path, to_path)
    run_cmd(['chmod', 'a+x', to_path])

def dir_content(folder):
    fList = os.listdir(folder)
    dirs = []
    files = []
    for f in fList:
        fPath = os.path.join(folder, f)
        if os.path.isfile(fPath):
            files.append(fPath)
        elif os.path.isdir(fPath):
            dirs.append(fPath)

    return dirs, files

def indent_tab_name(root, path):
    folder = root.rstrip("/")
    folder = folder + "/"
    path = path[len(folder):]
    list = path.strip("/").split("/")
    count = 0
    if len(list) > 0:
        count = len(list) - 1
    spaces = ""
    idx = 0
    while idx < count:
        spaces = spaces + "\t"
        idx = idx + 1

    head, tail = ntpath.split(path)
    fileName = tail or ntpath.basename(head)

    return spaces + fileName

def file_size(path):
    if os.path.isdir(path):
        result = run_cmd(["du", "-hs", path])
        results = result.split("\t")
        return results[0].strip()
    elif os.path.isfile(path):
        num = os.path.getsize(path)
        for unit in ['','K','M','G','T','P','E','Z']:
            if abs(num) < 1024.0:
                return "%3.1f%s" % (num, unit)
            num /= 1024.0
        return "%.1f%s" % (num, 'Y')

def list_dir_content(root, folder):
    tab_name = indent_tab_name(root, folder)
    if root.strip(" \t\n/") == folder.strip(" \t\n/"):
        print(". - " + file_size(folder))
    else:
        print(tab_name + " - " + file_size(folder))

    dirs, files = dir_content(folder)
    for f in files:
        tab_name = indent_tab_name(root, f)
        print(tab_name + " - " + file_size(f))

    for f in dirs:
        list_dir_content(root, f)

def __main__():

    # self_install
    if len(sys.argv) > 1 and sys.argv[1] == 'install':
        self_install("filetree.py", "/usr/local/bin")
        return

    if len(sys.argv) > 1:
        path = sys.argv[1]
    else:
        path = os.getcwd()

    if not str(path).startswith("/"):
        path = os.path.join(os.getcwd(), path)

    if os.path.isfile(path):
        fileLen = os.path.getsize(path)
        head, tail = ntpath.split(path)
        fileName = tail or ntpath.basename(head)
        print(fileName + "\t" + str(fileLen))

    elif os.path.isdir(path):
        print("list file tree:")
        print(path)
        print("\n")
        list_dir_content(path, path)

__main__()

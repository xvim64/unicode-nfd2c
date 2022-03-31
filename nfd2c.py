#!/usr/bin/env python3
# coding=utf-8

import os
import unicodedata
import shutil
import sys

def do_main(argv=sys.argv):
    msg = ''

    inputs = []
    wrongInputs = []

    items = []
    item_bDir = False
    item_Name = ''
    bItem     = True

    bRecursive = False
    bRename    = False

    bDir  = False
    bFile = False

    bDirOnly  = False
    bFileOnly = False

    bChangeInputDir = True

    currentDir = os.getcwd()

    argc = len(argv)
    n    = 1

    duplications = []

    def help_exit(n=0):
        print(
'''\
Converts NFD Unicode filenames to NFC.

USAGE: nfd2c [options] [dir(s)|file(s)]
    -x, --execute      rename on
    -r, --recursive    sub-directories on
    -d, --dir-only     directory only
    -f, --file-only    file only
    -h, --help         help\
''')
        sys.exit(n)

    def print_msg(s):
        nonlocal bItem
        if bItem:
            print('{1}\n{0}\n{1}'.format(item_Name,'-'*30))
            bItem = False
        print(s)

    if argc > 1:
        while n < argc:
            op = argv[n].lower()
            if   op in ['-x', '--execute']:
                bRename = True
            elif op in ['-r', '--recursive']:
                bRecursive = True
            elif op in ['-d', '--dir-only']:
                bDirOnly = True
            elif op in ['-f', '--file-only']:
                bFileOnly = True
            elif op in ['-h', '--help']:
                help_exit(0)
            else:
                if not argv[n] in duplications:
                    inputs.append(argv[n])
                    duplications.append(op)
            n+=1
    else:
        help_exit(0)

    for i in inputs:
        if os.path.isdir(i):
            items.append([1,i])
        elif os.path.isfile(i):
            items.append([0,i])
        else:
            wrongInputs.append(i)

    if wrongInputs:
        msg = 'ERROR : wrong inputs ...\n{}'.format('\n'.join(wrongInputs))
        print(msg)
        sys.exit(1)

    if not items:
        help_exit(0)

    for item in items:
        item_bDir  = item[0]
        item_Name = item[1]

        if item_bDir:
            bDir = True
            bFile = True
        else:
            bDir = False
            bFile = True

        if bDirOnly:
            bFile = False
        if bFileOnly:
            bDir = False
        if bDirOnly and bFileOnly:
            bFile = True
            bDir  = True

        macs    = []
        macwins = []

        macDirs = []
        macwinDirs = []

        bItem = True

        if bFile:
            if item_bDir:
                if bRecursive:
                    for p, ds, fs in os.walk(item_Name):
                        for f in fs:
                            macs.append((p,f))
                else:
                    for p, ds, fs in os.walk(item_Name):
                        for f in fs:
                            macs.append((p,f))
                        break
            else:
                macs.append(os.path.split(item_Name))
            if macs:
                for mac in macs:
                    # NFD only
                    win = unicodedata.normalize('NFC', mac[1])
                    if win != mac[1]:
                        macwins.append([mac[0],mac[1],win])
                # NFD to NFC
                if macwins:
                    if bRename:
                        # File : rename NFD to NFC
                        for macwin in macwins:
                            shutil.move(os.path.join(macwin[0],macwin[1]),os.path.join(macwin[0],macwin[2]))
                        msg = [ '[C] {:15}  {}'.format(macwin[2],os.path.join(macwin[0],macwin[1])) for macwin in macwins ]
                    else:
                        # Print only
                        msg = [ '{:15}  {}'.format(macwin[2],os.path.join(macwin[0],macwin[1])) for macwin in macwins ]
                    print_msg('\n'.join(msg))

        if bDir:
            if bRecursive:
                for p, ds, fs in os.walk(item_Name):
                    for d in ds:
                        macDirs.append((p,d))
            else:
                for p, ds, fs in os.walk(item_Name):
                    for d in ds:
                        macDirs.append((p,d))
                    break
            # Rename from the lowest directory
            macDirs.reverse()
            for macDir in macDirs:
                # NFD Only
                win = unicodedata.normalize('NFC', macDir[1])
                if macDir[1] != win:
                    macwinDirs.append([macDir[0],macDir[1],win])
            if macwinDirs:
                if bRename:
                    # Directory : rename NFD to NFC
                    for macwinDir in macwinDirs:
                        shutil.move(os.path.join(macwinDir[0],macwinDir[1]),os.path.join(macwinDir[0],macwinDir[2]))
                    # Reverse again for print
                    macwinDirs.reverse()
                    msg = [ '[C] *{:14}  {}'.format(macwinDir[2],os.path.join(macwinDir[0],macwinDir[1])) for macwinDir in macwinDirs ]
                else:
                    # Reverse again for print
                    macwinDirs.reverse()
                    msg = [ '*{:14}  {}'.format(macwinDir[2],os.path.join(macwinDir[0],macwinDir[1])) for macwinDir in macwinDirs ]
                print_msg('\n'.join(msg))
            if bChangeInputDir:
                # Current working directory
                if currentDir.find(os.path.abspath(item_Name)) + 1:
                    _, currentDir_d = os.path.split(currentDir)
                    win = unicodedata.normalize('NFC', currentDir_d)
                    if currentDir_d != win:
                        msg = 'WARNING: CWD: {}'.format(currentDir)
                        print_msg(msg)
                else:
                    # NFD to NFC
                    p, d = os.path.split(item_Name)
                    win = unicodedata.normalize('NFC', d)
                    if d != win:
                        dirNFC = os.path.join(p,win)
                        if bRename:
                            msg = '[C] *{:14}  {}'.format(dirNFC,os.path.join(p,item_Name))
                        else:
                            msg = '*{:14}  {}'.format(dirNFC,os.path.join(p,item_Name))
                        print_msg(msg)
                        if bRename:
                            # Directory : rename NFD to NFC
                            shutil.move(os.path.join(p,d),dirNFC)

if __name__ == '__main__':
    do_main()


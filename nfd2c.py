# coding=utf-8

import os
import unicodedata
import shutil
import sys

msg = ''

# 도움말
msg_help = '''\
Converts Unicode NFD filename to NFC.

USAGE: python {} [options] [dir(s)|file(s)]
    -x, --execute      rename on
    -r, --recursive    sub-directories on
    -d, --dir-only     directory only
    -f, --file-only    file only
    -h, --help         help\
'''.format(os.path.basename(sys.argv[0]))

inputs = []
wrongInputs = []

items = []
itemDir  = False
itemName = ''
bItem    = True

bRecursive = False
bRename    = False
bPrint     = False

bDir  = False
bFile = False

bDirOnly  = False
bFileOnly = False

bChangeInputDir = True

currentDir = os.getcwd()

argv = sys.argv[1:]
argc = len(argv)
n    = 0

duplications = []

def print_msg(s):
    global bItem
    if bItem:
        print('{1}\n{0}\n{1}'.format(itemName,'-'*30))
        bItem = False
    print(s)

# 옵션
if argc:
    while n < argc:
        op = argv[n].lower()
        if   op in ['-x', '--execute']:
            # NFD to NFC 변환 적용
            bRename = True
        elif op in ['-r', '--recursive']:
            # 하위 디렉토리 on
            bRecursive = True
        elif op in ['-d', '--dir-only']:
            # 디렉토리만
            bDirOnly = True
        elif op in ['-f', '--file-only']:
            # 파일만
            bFileOnly = True
        elif op in ['-h', '--help']:
            # 도움말
            print(msg_help)
            sys.exit(0)
        else:
            if not argv[n] in duplications:
                inputs.append(argv[n])
                duplications.append(op)
        n+=1

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
    print(msg_help)
    sys.exit(0)

for item in items:
    itemDir  = item[0]
    itemName = item[1]

    if itemDir:
        bDir = True
        bFile = True
    else:
        bDir = False
        bFile = True

    # 디렉토리만
    if bDirOnly:
        bFile = False
    # 파일만
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

    # 파일
    if bFile:
        # 입력 디렉토리
        if itemDir:
            if bRecursive:
                # 하위 디렉토리 포함
                for p, ds, fs in os.walk(itemName):
                    for f in fs:
                        macs.append((p,f))
            else:
                # 하위 디렉토리 포함 안 함
                for p, ds, fs in os.walk(itemName):
                    for f in fs:
                        macs.append((p,f))
                    break
        else:
            # 입력 파일
                macs.append(os.path.split(itemName))
        if macs:
            # 파일 NFD 만 선택
            for mac in macs:
                # NFD 만 선택
                win = unicodedata.normalize('NFC', mac[1])
                if win != mac[1]:
                    macwins.append([mac[0],mac[1],win])
            # 파일 NFD to NFC 변환
            if macwins:
                if bRename:
                    # 파일 NFD to NFC 변환 적용
                    for macwin in macwins:
                        shutil.move(os.path.join(macwin[0],macwin[1]),os.path.join(macwin[0],macwin[2]))
                    msg = [ '[C] {:15}  {}'.format(macwin[2],os.path.join(macwin[0],macwin[1])) for macwin in macwins ]
                else:
                    # 출력만 함
                    msg = [ '{:15}  {}'.format(macwin[2],os.path.join(macwin[0],macwin[1])) for macwin in macwins ]
                print_msg('\n'.join(msg))

    # 디렉토리
    if bDir:
        if bRecursive:
            # 하위 디렉토리 포함
            for p, ds, fs in os.walk(itemName):
                for d in ds:
                    macDirs.append((p,d))
        else:
            # 하위 디렉토리 포함 안 함
            for p, ds, fs in os.walk(itemName):
                for d in ds:
                    macDirs.append((p,d))
                break
        # 하위 디렉토리부터 변경을 위해 리버스 적용
        macDirs.reverse()
        # 디렉토리 NFD 만 선택
        for macDir in macDirs:
            # NFD 만 선택
            win = unicodedata.normalize('NFC', macDir[1])
            if macDir[1] != win:
                macwinDirs.append([macDir[0],macDir[1],win])
        # 디렉토리 NFD to NFC 변환
        if macwinDirs:
            if bRename:
                # 디렉토리 NFD to NFC 변환 적용
                for macwinDir in macwinDirs:
                    shutil.move(os.path.join(macwinDir[0],macwinDir[1]),os.path.join(macwinDir[0],macwinDir[2]))
                # 출력 순서를 위해 다시 리버스 적용
                macwinDirs.reverse()
                msg = [ '[C] *{:14}  {}'.format(macwinDir[2],os.path.join(macwinDir[0],macwinDir[1])) for macwinDir in macwinDirs ]
            else:
                # 출력만 함
                # 출력 순서를 위해 다시 리버스 적용
                macwinDirs.reverse()
                msg = [ '*{:14}  {}'.format(macwinDir[2],os.path.join(macwinDir[0],macwinDir[1])) for macwinDir in macwinDirs ]
            print_msg('\n'.join(msg))
        # 입력 디렉토리 NFD to NFC 변환
        if bChangeInputDir:
            if currentDir.find(os.path.abspath(itemName)) + 1:
                # 현재 디렉토리가 입력 디렉토리에 있을 경우 출력만 함
                currentDir_p, currentDir_d = os.path.split(currentDir)
                win = unicodedata.normalize('NFC', currentDir_d)
                if currentDir_d != win:
                    msg = 'WARNING: CWD: {}'.format(currentDir)
                    print_msg(msg)
            else:
                # 입력 디렉토리 NFD to NFC 변환
                p, d = os.path.split(itemName)
                win = unicodedata.normalize('NFC', d)
                if d != win:
                    dirNFC = os.path.join(p,win)
                    if bRename:
                        msg = '[C] *{:14}  {}'.format(dirNFC,os.path.join(p,itemName))
                    else:
                        msg = '*{:14}  {}'.format(dirNFC,os.path.join(p,itemName))
                    print_msg(msg)
                    if bRename:
                        # NFD to NFC 변환 적용
                        shutil.move(os.path.join(p,d),dirNFC)


# nfd2c

mac 에서 분리된 한글 자소를 결합합니다.

폴더나 파일 이름에 유니코드 NFD 를 포함하는 경우 NFC 로 변경합니다.


# 주의사항

nfd2c-rename.cmd 를 실행하거나 nfd2c.py 나 nfd2c.cmd 실행시
-r (하위 디렉토리 포함) 옵션을
-x (분리된 한글 자소 결합 실행) 옵션과 같이 사용할 경우
디렉토리 지정시 하위 디렉토리까지 일괄적으로 NFD 에서 NFC 로 변경합니다.

설정에서 NFD 경로명을 참조하는 경우
해당 디렉토리나 파일을 찾지 못하는 문제가 발생할 수 있습니다.

NFD 에서 NFC 로 변경되어도 괜찮은 디렉토리나 파일에만 '-x' 옵션을 적용하세요.


# 도움말

```
사용법: nfd2c.py [options] [디렉토리 | 파일]
    -x, --execute      분리된 한글 자소 결합 실행
	                   '-x' 미사용시 결합은 하지 않고 목록만 출력
    -r, --recursive    하위 디렉토리 포함
	-d, --dir-only     디렉토리만 포함
	-f, --file-only    파일만 포함
    -h, --help         도움말


[ 예 ]

# C:\TEST 디렉토리에서 분리된 한글 자소 목록을 출력합니다. (하위 디렉토리를 포함하지 않습니다.)
python nfd2c.py C:\TEST

# C:\TEST 디렉토리에서 분리된 한글 자소를 결합(-x)합니다. (하위 디렉토리를 포함하지 않습니다.)
python nfd2c.py -x C:\TEST


# C:\TEST 디렉토리에서 하위(-r) 디렉토리를 포함해서 분리된 한글 자소 목록을 출력합니다.
python nfd2c.py -r C:\TEST

# C:\TEST 디렉토리에서 하위(-r) 디렉토리를 포함해서 분리된 한글 자소를 결합(-x)합니다.
python nfd2c.py -r -x C:\TEST


# 현재 작업중인 디렉토리(\.)에서 하위(-r) 디렉토리를 포함해서 분리된 한글 자소 목록을 출력합니다.
python nfd2c.py -r .

# 현재 작업중인 디렉토리(\.)에서 하위(-r) 디렉토리를 포함해서 분리된 한글 자소를 결합(-x)합니다.
python nfd2c.py -r -x .
```


# 지원 OS

nfd2c.py 는 파이썬3가 설치되어있다면 어떤 OS 에서도 사용이 가능합니다.

그 외의 구성 파일은 윈도우 전용입니다.


# 파일 설명

파일 설명
```
python\              윈도우용 임베디드 파이썬 디렉토리
nfd2c.py             nfd2c 파이썬 스크립트
nfd2c.cmd            nfd2c.py 실행
nfd2c-help.cmd       도움말
nfd2c-print.cmd      분리된 한글 자소 목록 출력
nfd2c-rename.cmd     분리된 한글 자소 결합 실행
dirs.txt             작업 디렉토리 기록 (절대경로로 기입)
```

nfd2c-rename.cmd 실행시
dirs.txt 파일에
```
C:\A
C:\B
C:\C
```
절대경로가 기입되어 있으면
C:\A, C:\B, C:\C 디렉토리를 대상으로 하위 디렉토리 및 파일을 포함해
분리된 한글 자소를 결합니다.

nfd2c-print.cmd 실행시
dirs.txt 에 있는 경로를 대상으로
분리된 한글 자소 목록을 출력합니다.


# 라이선스

GPL-2.0 License



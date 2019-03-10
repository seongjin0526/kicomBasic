import sys
import os
import hashlib

MalewareDB = []
PatternDB = [] # Malware 패턴 저장됨.
SizeDB =[] # Malware를 Size로 판단하기 위함

def LoadMalwareDB():
    fp =open('MalwareDB.db','rb')

    while True:
        line = fp.readline()
        if not line : break

        line = line.strip() # remove \r\n
        MalewareDB.append(line)

    fp.close()


# VirusDB를 PatternDB로 변환
def MakePatternDB() :
    for pattern in MalewareDB :
        t = []
        v = pattern.split(b':')
        t.append(v[0])
        t.append(v[1])
        PatternDB.append(t)

        size = int(v[2])
        if SizeDB.count(size) == 0:
            SizeDB.append(size)

# Virus Detect
def SearchVDB(fmd5):
    for t in PatternDB :
        if t[0] == fmd5 :
            return True, t[1]
    return False, ''

# main
if __name__ == '__main__' :
    LoadMalwareDB()
    MakePatternDB()

    if len(sys.argv) != 2:
        print('Usage : KicomBasic.py [File]')
        exit(0)

    fname = sys.argv[1]

    size = os.path.getsize(fname)
    if SizeDB.count(size):
        fp = open(fname, 'rb')
        buf = fp.read()
        fp.close()

        m = hashlib.md5()
        m.update(buf)
        fmd5 = m.hexdigest()
        
        ret, vname = SearchVDB(bytes(fmd5,"utf-8"))
        if ret == True :
            print('{} : {}'.format(fname, vname))
            os.remove(fname)
            print('Complete to delete Malware File!')
        else :
            print('{} : ok'.format(fname))
            print('Thanks')
    else :
        print('{} : ok'.format(fname))
        print('Thanks')
       
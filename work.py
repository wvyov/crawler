from get import getSchool
from get import getProfession
from get import getExaminations
from get import getSs
from get import makeParams


from db import writeSchool
from db import writeProfession
from db import writeExaminations
from db import writeSs
from db import selectnotProfession

import json
import sqlite3
import requests

# 由传入学校参数，生成完整参数
def makeParamsFromSchool(school):
    id = school[0]
    name = school[1]
    sscode = school[2]
    params = {'ssdm': sscode, 'dwmc' : name, 'school_id':id}
    return makeParams(params) 

def writejson(filename, data):
    json.dump(tmp, open(filename, 'w'))
    return
    tmp = []
    try:
        tmp = json.load(open(filename, 'r'))
    except:
        tmp = []
    finally:
        tmp.extend(data)
        json.dump(tmp, open(filename, 'w'))

def isNull(data):
    if not data:
        return data
    for row in data:
        if not row:
            return row

    return data








# --- get examinations from profession


# 消费考试范围信息

# 消费专业信息, 生产考试范围信息


# -- get professions from school --

errorschool = []

integrityschool = []


# 消费学校信息, 生产专业信息

def cSchoolpProfession(c):
    schooldata = {}
    n = 0
    total = []
    while True:
        school = yield schooldata
        params = makeParamsFromSchool(school)
        try:
            professions = getProfession(params)
            k = len(professions)
            n = n + k
            print(k)
            print(n)

            #addjson('profession.json', professions)
            writeProfession(professions)
            #print('end')

        except sqlite3.IntegrityError as e:
            print('inserted: ' + school[1])
            integrityschool.append(school)
            continue
        except requests.exceptions.RequestException as e:
            # 发生异常, 已加入errorschool
            print('error ' + school[1])
            errorschool.append(school)
        except:
            print('other error')
            errorschool.append(school)


        
# 生产学校信息
def pSchool(c):
    c.send(None)
    #schools = getSchool()
    schools = selectnotProfession()
    print('total: ' + str(len(schools)))

    for i in range(0, len(schools)):
        school = schools[i]
        print(str(i) + ' ' + school[1])

        c.send(school)

        print('')
        i = i +1
    
    global errorschool

    while errorschool :
        print('error school : ' + str(len(errorschool)))

        schools = errorschool
        errorschool = []

        for i in range(0, len(schools)):
            school = schools[i]
            print(str(i) + ' ' + school[1])
            c.send(school)
            print('')
            i = i +1

    c.close()


# --- init ---

#def initdb():


def initSs():
    sss = getSs()
    try:
        writeSs(sss)
    except sqlite3.IntegrityError as e:
        return

def initSchool():
    schools = getSchool()
    #print(schools)
    try:
        writeSchool(schools)
    except sqlite3.IntegrityError as e:
        return

# --- main ---

if __name__ == '__main__':
   
    #initSs()
    print('write Ss')

    initSchool()
    print('write school')

    c = cSchoolpProfession(None)
    pSchool(c)
    print('write profession')

    if integrityschool :
        writejson('integrityschool.json', integrityschool)
        print(integrityschool)




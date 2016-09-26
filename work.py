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
from db import pageingQueryProfession

import json
import sqlite3
import requests
from multiprocessing.dummy import Pool as ThreadPool

# 由传入学校参数，生成完整参数
def makeParamsFromSchool(school):
    id = school[0]
    name = school[1]
    sscode = school[2]
    params = {'ssdm': sscode, 'dwmc' : name, 'school_id':id}
    return makeParams(params) 

# 由传入专业参数，生成查询考试范围的参数 
def makeParamsFromProfession(profession):
    data = {}
    professionid = profession[1] + profession[3] + profession[5] + profession[7]
    id = profession[12]
    dwmc = '(' + profession[1] + ')' + profession[2]
    yxsmc = '(' + profession[3] + ')' + profession[4]
    zymc = '(' + profession[5] + ')' + profession[6]
    yjfxmc = '(' + profession[7] + ')' + profession[8]

    data['professionid'] = professionid
    data['id'] = id
    data['dwmc'] = dwmc
    data['yxsmc'] = yxsmc
    data['zymc'] = zymc
    data['yjfxmc'] = yjfxmc

    return data


# -- get professions from school --

errorschool = []


# 消费学校信息, 生产专业信息(从网络获取)

def cSchoolpProfession():
    schooldata = {}
    n = 0
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
        print('error schools : ' + str(len(errorschool)))

        schools = errorschool
        errorschool = []

        for i in range(0, len(schools)):
            school = schools[i]
            print(str(i) + ' ' + school[1])
            c.send(school)
            print('')
            i = i +1

    c.close()


# --- get examinations from profession ---


# 分批获取数据，并写入
def cProfessionpExaminations():
    professiontotal = pageingQueryProfession() 
    i = 0
    k = 0
    n = 0
    for professions in professiontotal:
        print(str(i) + ':')
        #pool.map(cProfessionpExaminations, professions)
        pool = ThreadPool(10)
        result = pool.map(getExaminationsByProfession, professions)
        
        pool.close()
        pool.join()


        exams = []
        for resultitem in result:
            if resultitem:
                exams.extend(resultitem)

        writeExaminations(exams)

        k = len(exams)
        n = n + k
        i = i + 1
        print(k)
        print(n)
        print('')

# 获取profession, 构造参数，发起请求，返回数据
def getExaminationsByProfession(profession):
    params = makeParamsFromProfession(profession)
    exams = []
    try:
        #print(params)
        exams = getExaminations(params)
    except requests.exceptions.RequestException as e:
        print(e)
        pass
    except:
        pass
    return exams



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
    
    # 获取专业信息，并写入数据库
    c = cSchoolpProfession()
    pSchool(c)
    print('write profession')


    # 获取考试范围信息, 并写入数据库 
    cProfessionpExaminations()
    print('write examinations')




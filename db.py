import sqlite3
import json

# --- private ---

dbfilename = 'yz.db'

insertschool = 'insert into school values (?, ?, ?, ?, ?, ?, ?, ?, ?)'
inserts_p = 'insert into school_profession values (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)'
insertp_e = 'insert into profession_examinations values (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)'
insertss = 'insert into ss values(?, ?)'
tabmap = {'school': insertschool, 'school_profession': inserts_p, 'profession_examinations': insertp_e, 'ss': insertss}



# 将数据一个一个存入数据库
def writedbitem(tablename, data):
    if not data:
        return
    conn = sqlite3.connect(dbfilename)
    cursor = conn.cursor()
    sql = tabmap[tablename]
    errordata = []
    e = None
    i = 0
    for row in data:
        try:
            cursor.execute(sql, row)
        except sqlite3.IntegrityError as e:
            i = i + 1
            #errordata.append(row)
            print(e)
            #print(row)
            #raise e
            #continue
            pass

    conn.commit()
    conn.close()
    #print(i)



# 将数据存入数据库
def writedb(tablename, data):
    if not data:
        return
    conn = sqlite3.connect(dbfilename)
    cursor = conn.cursor()
    sql = tabmap[tablename]
    try:
        cursor.executemany(sql, data)
    except sqlite3.IntegrityError as e:
        conn.rollback()
        raise e
    finally:
        conn.commit()
        conn.close()
    #wirtedbitem(tablename, data)

# --- public ---

# 将数据写入school表
def writeSchool(data):
    writedb('school', data)

# 将数据写入school_profession表
def writeProfession(data):
    writedb('school_profession', data)

# 将数据写入profession_examinations表
def writeExaminations(data):
    writedb('profession_examinations', data)

# 将数据写入ss表
def writeSs(data):
    writedb('ss', data)

# 查询未写入专业信息的学校
def selectnotProfession():
    conn = sqlite3.connect(dbfilename)
    cursor = conn.cursor()
    sql = 'select * from school where name not in(select school_name from school_profession group by school_code)'
    cursor.execute(sql)
    results = cursor.fetchall()
    return results


# 将查询所有未写入考试范围的专业信息，分批返回

oncenum = 500

''' 
因为数据量太大，179155条， 
所以，分批返回数据, 每批数据oncenum条
'''

def pageingQueryProfession():
    while True:
        results = []
        conn = sqlite3.connect(dbfilename)
        cursor = conn.cursor()
        sql = 'select * from school_profession where id not in (select profession_id from profession_examinations) limit 0,' + str(oncenum)
        cursor.execute(sql)
        results = cursor.fetchall()
        #print(results)
        if not results:
            return 
        yield results
    


'''
# 查询某学校的专业信息


# 查询某学校未写入考试范围的专业
def selectnotExaminations(school_code):
    conn = sqlite3.connect(dbfilename)
    cursor = conn.cursor()
    sql = 'select * from school_profession where school_code = ' + school_code + ' and examinations not in (select id from profession_examinations)'
    cursor.execute(sql)
    results = cursor.fetchall()
    return results
'''

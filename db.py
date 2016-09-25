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
def wirtedbitem(tablename, data):
    if not data:
        return
    conn = sqlite3.connect(dbfilename)
    cursor = conn.cursor()
    sql = tabmap[tablename]
    errordata = []
    e = None
    for row in data:
        cursor.execute(sql, row)
        #try:
            #cursor.execute(sql, row)
        #except sqlite3.IntegrityError as e:
            #errordata.append(row)
            #print(e)
            #continue

    conn.commit()
    conn.close()
    print('errordata')
    print(errordata)



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

# 查寻未写入专业信息的学校
def selectnotProfession():
    conn = sqlite3.connect(dbfilename)
    cursor = conn.cursor()
    sql = 'select * from school where name not in(select school_name from school_profession group by school_code)'
    cursor.execute(sql)
    results = cursor.fetchall()
    return results

# 查询未写入考试范围的专业


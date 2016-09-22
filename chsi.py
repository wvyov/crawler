import requests
from bs4 import BeautifulSoup
import re
import sqlite3
import json

host = 'http://yz.chsi.com.cn'


# 给定省、直辖市获取学校信息
def getSchool(r, params):

    result = []

    # 解析响应, 将数据封装进result中
    s = BeautifulSoup(r.text, 'lxml')


    div = s.find(id='sch_list')
    table = div('table')[0];
    body = table('tbody')[0]('tr')
    
    if body[0]('td')[0].text == '很抱歉，没有找到您要搜索的数据！':
        print('error: 暂时无法获取数据')
        return result

    
    #提取学校信息的正则表达式
    pattern = re.compile(r'\((?P<id>[0-9]+)\)(?P<name>.+)')

    #数据
    for tr in body:
        tds = tr('td')
        row = []

        # 学校
        schoolstr = tds[0]('a')[0].text
        g = re.match(pattern, schoolstr)
        id = g.group('id')
        name = g.group('name')
        row.append(id)
        row.append(name)
        # 所在地
        addressstr= tds[1].text
        g = re.match(pattern, addressstr)
        id = g.group('id')
        name = g.group('name')
        row.append(id)
        row.append(name)

        # 985,211
        spans = tds[2]('span')
        if len(spans) > 0:
            #985
            flag = '0'
            if not spans[0].text.isspace():
                flag = '1'
            row.append(flag)
            # 211
            flag = '0'
            if not spans[1].text.isspace():
                flag = '1'
            row.append(flag)
        else:
            flag = '0'
            row.append(flag)
            row.append(flag)


        # 是否研究生院
        flag = '0'
        if not tds[3].text.isspace():
            flag = '1'
        row.append(flag)
        # 是否自主划线
        flag = '0'
        if not tds[4].text.isspace():
            flag = '1'
        row.append(flag)
        # 是否博士点
        flag = '0'
        if not tds[5].text.isspace():
            flag = '1'
        row.append(flag)

        result.append(row)

    return result;





# 给定学校获取专业信息
def getProfession(r, params):
    result = []
    

    SCHOOL_CODE = params['school_id'] 
    SCHOOL_NAME = params['dwmc']


    # 解析响应, 将数据封装进result中
    s = BeautifulSoup(r.text, 'lxml')

    div = s.find(id='sch_list')
    table = div('table')[0];
    body = table('tbody')[0]('tr')

    if body[0]('td')[0].text == '很抱歉，没有找到您要搜索的数据！':
        print('error: 暂时无法获取数据')
        return result
    
    #提取信息的正则表达式
    pattern = re.compile(r'[^\']+\'(?P<info>[^\']+)?\'.*')
    numpattern = re.compile(r'[^0-9]+(?P<total>[0-9]+)?[^0-9]+(?P<among>[0-9]+)?.*', re.DOTALL)
    idnamepattern = re.compile(r'\((?P<id>\w+)\)(?P<name>.+)')
    exampattern = re.compile(r'[^0-9]+id=(?P<id>[^&]+)&.*')

    #数据
    for tr in body:
        tds = tr('td')
        row = []
        # 主键
        rowid = SCHOOL_CODE

        # 院系所名称
        strs = tds[0].text
        g = re.match(idnamepattern, strs)
        id = g.group('id')
        name = g.group('name')
        row.append(id)
        row.append(name)

        
        rowid += id
        
        # 专业代码名称
        strs = tds[1].text
        g = re.match(idnamepattern, strs)
        id = g.group('id')
        name = g.group('name')
        row.append(id)
        row.append(name)
        
        rowid += id
        
        # 研究方向
        strs = tds[2].text
        g = re.match(idnamepattern, strs)
        id = g.group('id')
        name = g.group('name')
        row.append(id)
        row.append(name)
        
        rowid += id
        
        # 指导教师
        teacher = re.match(pattern, tds[3].text)
        row.append(teacher.group('info'))

        # 拟招生人数
        pnumgroup = re.match(numpattern, tds[4].text)
        # 总人数
        total = pnumgroup.group('total')
        row.append(total)
        # 推免
        row.append(pnumgroup.group('among'))

        # 考试范围
        path = tds[5]('a')[0].get('href')
        g = re.match(exampattern, path)
        id = g.group('id')
        row.append(id)
        
        # 跨专业
        path = tds[6]('a')[0].get('href')
        link = host + path
        row.append(link)
        # 备注
        remark = re.match(pattern, tds[7].text)
        row.append(remark.group('info'))
        
        # 学校名字
        row.insert(0, SCHOOL_NAME)
        # 学校代码
        row.insert(0, SCHOOL_CODE)
        # 主键
        row.insert(0, rowid) 

        result.append(row)

    return result;


# 获取考试范围
def getExaminations(r, params):
    result = []
    
    professionid = params['professionid'] 

    # 解析响应, 将数据封装进result中
    s = BeautifulSoup(r.text, 'lxml')

    div = s.find(id='result_list')


    #print(div('table'))
    table = div('table')[0];
    body = table('tbody')[0]('tr')

    if len(body) == 0:
        print(PROFESSIONID + '暂无考试范围数据')
        return result
    
    # 提取信息的正则表达式
    idnamepattern = re.compile(r'\((?P<id>[-0-9a-zA-z]+)\)(?P<name>.+)')
    # 数据
    for tr in body:
        tds = tr('td')
        row = []
        
        # 序号
        seq = tds[0].text
        id = params['id'] + seq
        row.append(id)
        # 政治
        strs = tds[1].text
        g = re.match(idnamepattern, strs)
        id = g.group('id')
        name = g.group('name')
        row.append(id)
        row.append(name)
        # 外语
        strs = tds[2].text
        g = re.match(idnamepattern, strs)
        id = g.group('id')
        name = g.group('name')
        row.append(id)
        row.append(name)
        # 业务课一
        strs = tds[3].text
        g = re.match(idnamepattern, strs)
        id = g.group('id')
        name = g.group('name')
        row.append(id)
        row.append(name)
        # 业务课二
        strs = tds[4].text
        g = re.match(idnamepattern, strs)
        id = g.group('id')
        name = g.group('name')
        row.append(id)
        row.append(name)

        row.insert(1, professionid)
        
        result.append(row)
    return result
        



# 用给定参数爬取网页, 并用给定方法处理
def getData(path, params, fun):
    # 先找出总页数, 再遍历并解析每一页
    result = []


    # 请求地址
    url = host + path
    #print(url)

    # 查询数据的页数
    page_total = 1

    # 发起请求, 获得响应
    r = requests.post(url, params=params)
    # 解析响应
    s = BeautifulSoup(r.text, 'lxml')
    # 获取总页数
    num = s.find(id='page_total')
    if num:
        p = re.compile(r'[0-9]+/(?P<num>[0-9]+)')
        g = re.match(p, num.text)
        page_totalstr = g.group('num')
        page_total = int(page_totalstr)


    #print('共有 ' + str(page_total) + ' 页')

    # 遍历每一页
    for pageno in range(1, page_total + 1):

        #print('当前，第 ' + str(pageno) + ' 页')

        params['pageno'] = pageno
        
        # 发起请求, 获得响应
        r = requests.post(url, params=params)

        # 处理响应
        resultpage = fun(r, params)
        # 将每一页的结果集加入总结果集中
        result.extend(resultpage)

    return result




# 将数据保存值数据库
def writedb(tablename, data):
    if not data:
        return

    conn = sqlite3.connect('chsi.db')
    cursor = conn.cursor()

    insertschool = 'insert into school values (?, ?, ?, ?, ?, ?, ?, ?, ?)'
    inserts_p = 'insert into school_profession values (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)'
    insertp_e = 'insert into profession_examinations values (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)'
    tabmap = {'school': insertschool, 'school_profession': inserts_p, 'profession_examinations': insertp_e}
   
    sql = tabmap[tablename]

    try:
        cursor.executemany(sql, data)
    except sqlite3.IntegrityError:
        #print('写入数据库异常 ' + tablename + ' ')
        map = {}

        for i in range(0,len(data)):
            try:
                map[data[i][0]] = ''
                cursor.execute(sql, data[i])
            except sqlite3.IntegrityError as e:
                print('该条记录写入出错:' + str(i))
                #print(data[3])
                #print(e)
        print(len(map.keys()))

    conn.commit()
    conn.close()


# 省市名称与代码
def getSs():
    sspath = '/zsml/pages/getSs.jsp'
    url = host + sspath
    r = requests.post(url)
    return r.json()
    
    result = {}
    for item in rjson:
        code = item['dm']
        name = item['mc']
        result[code] = name
    return result

# 学科门类
def getMl():
    mlpath = '/zsml/pages/getMl.jsp'
    url = host + mlpath
    r = requests.post(url)
    rjson = r.json()
    result = {}
    for item in rjson:
        code = item['dm']
        name = item['mc']
        result[code] = name
    return result

# 学科专业
def getZy():
    zypath = '/zsml/pages/getZy.jsp'
    url = host + zypath
    r = requests.post(url)
    rjson = r.json()
    result = {}
    for item in rjson:
        code = item['dm']
        name = item['mc']
        result[code] = name
    return result

# 清除参数值
def clearParams(params):
    for key in params.keys():
        params[key] = ''




def run():
    # 查询学校
    spath = '/zsml/queryAction.do'

    # 查询专业
    ppath = '/zsml/querySchAction.do'

    # 查询考试范围
    epath = '/zsml/kskm.jsp'
    
    ssdm=''
    dwmc=''
    mldm=''
    mlmc=''
    yjxkdm=''
    zymc=''
    pageno=1

    school_id = '10001' 

    # 查询数据的页数
    page_total = 1

    #封装请求参数
    data = {'ssdm': ssdm, 'dwmc': dwmc, 'mldm': mldm, 'mlmc': mlmc, 'yjxkdm': yjxkdm, 'zymc': zymc, 'pageno': pageno, 'school_id': school_id}

    # 获取省市代码
    sss = getSs()
    
    schoolall = []
    
    print(str(len(sss)) + ' 个省市')

    # 遍历省市, 获取每个省市的学校 
    for i in range(len(sss)):
        break

        key = sss[i]['dm']
        value = sss[i]['mc']

        print(str(i) + ' ' + value)

        clearParams(data)
        data['ssdm'] = key
        try:
            schoolss = getData(spath, data, getSchool)
        except:
            while not schoolss:
                schoolss = getData(spath, data, getSchool)
        schoolall.extend(schoolss)

        print(value + '共有 ' + str(len(schoolss)) + ' 所\n')

    if schoolall:
        print('全国' + ' 共有 ' + str(len(schoolall)) + ' 所\n')
        json.dump(schoolall, open('school.json', 'w'))
        writedb('school', schoolall)



    #schoolall = json.load(open('school.json', 'r'))

    print(str(len(schoolall)) + '个')

    professionall = []

    k = 0

    # 遍历该省市的每个学校, 获取每个学校的专业
    for i in range(0, len(schoolall)):
        school = schoolall[i]

        print(str(i) + ' ' + school[1])

        clearParams(data)
        data['school_id'] = school[0]
        data['dwmc'] = school[1]
        professions = []
        try:
            professions = getData(ppath, data, getProfession)
        except:
            while not professions:
                professions = getData(ppath, data, getProfession)

        professionall.extend(professions)
        print(school[1] + '共有 ' + str(len(professions)) + ' 个专业\n')

        if len(professionall) > 2000:
            #json.dump(professionall, open('profession'+ str(k) + '.json', 'w'))
            k += len(professionall)
            writedb('school_profession', professionall)
            professionall = []

    if professionall:
        print('全国' + '共有 ' + str(k + len(professionall)) + ' 个专业\n')
        json.dump(professionall, open('profession.json', 'w'))
        writedb('school_profession', professionall)

    
    return


    professionall= json.load(open('profession.json', 'r'))
    #print(professionall)

    examinationsall = []

    # 遍历每个专业, 获取每个专业的考试范围
    for profession in professionall:

        print(profession[8])

        clearParams(data)
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


        examinations = getData(epath, data, getExaminations)

        examinationsall.extend(examinations)

        print(profession[8] + '共有 ' + str(len(examinations)) + '个考试范围')
        
        
    if examinationsall:
        print(profession[8] + '共有 ' + str(len(examinations)) + '个考试范围')
        json.dump(open('examinations.json', 'w'))


        #writedb('profession_examinations', examinations)

        #print(profession[8] + ' end')

        #id = '106942100103040101'
        #dwmc = '(10694)西藏大学'
        #yxsmc = '(001)文学院'
        #zymc = '(030401)民族学'
        #yjfxmc = '(01)民族与宗教文化'

if __name__ == '__main__':
    run()





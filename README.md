# yz
研招网（ http://yz.chsi.com.cn/ ） **2017**考研数据，  
包括：学校，专业，考试范围  

## 数据格式：
参考yz.sql
```sql
-- 省市
drop table ss;
create table ss(
    id text primary key not null, -- 省市代码
    name text not null -- 省市名称
);

-- 学校
drop table school;
create table school(
    id text primary key not null, -- 学校代码
    name text not null, -- 学校名字
    address_code text not null, -- 地区代码
    address_name text not null, -- 地区名称
    type_985 text not null, -- 是否是985
    type_211 text not null, -- 是否是211
    type_graduate text not null, -- 是否研究生院
    type_autonomous text not null, -- 是否自主划线
    type_doctoral text not null -- 是否博士点
);

-- 学校-专业
drop table school_profession;
create table school_profession(
    id text primary key not null, -- 拼接主键, 拼接策略: 学校代码 + 院系所代码 + 专业代码 + 研究方向代码
    school_code text not null, -- 学校代码
    school_name text not null, -- 学校名称
    faculties_code text not null, -- 院系所代码
    faculties_name text not null, -- 院系所名称
    profession_code text not null, -- 专业代码
    profession_name text not null, -- 专业名称
    research_direction_code text not null, -- 研究方向代码
    research_direction_name text not null, -- 研究方向名称
    teacher text , -- 指导老师
    num_total text not null, -- 拟招生总人数
    num_among text, -- 拟招生中推免人数
    examinations text not null, -- 考试范围
    multi_disciplinary text, -- 跨专业
    remark text -- 备注
);

-- 专业-考试范围
drop table profession_examinations;
create table profession_examinations(
    id text primary key not null, -- school_profession.examinations + 序号
    profession_id text not null, --  专业id, school_profession外建,
    political_code text not null, -- 政治课代码
    political_name text not null, -- 政治课
    foreign_language_code text not null, -- 外语课代码
    foreign_language_name text not null, -- 外语课
    business_class_1_code text not null, -- 业务课一代码
    business_class_1_name text not null, -- 业务课一
    business_class_2_code text not null, -- 业务课二代码
    business_class_2_name text not null -- 业务课二
);
```


## 运行环境（参考） 
Ubuntu 16.04 LTS  
Python3.5  
sqlite3

## Python依赖库：  
requests2  
bs4  
lxml  

## 运行步骤：
0. 处理好各种依赖库
1. 将yz.sql导入sqlite3, 创建表
2. 运行work.py, 等待结果

## 附
已爬取数据的sqlite3数据库，爬取时间：*2016.09.26 - 2016.09.27*   
链接: https://pan.baidu.com/s/1qYkxAHI 密码: tdwr

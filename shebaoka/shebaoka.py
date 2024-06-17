import pymysql
import xlrd2
import os


STARTTIME = "2023-07-09"
ENDTIME = "2023-08-08"


class Sbk():
    def __init__(self, khmc,cardId, sfzID, kkdata, zkdata, yxjgh, yxr, jbjgh,jbr):
        self.khmc = khmc
        self.cardId = cardId
        self.sfzID = sfzID
        self.kkdata = kkdata
        self.zkdata = zkdata
        self.yxjgh = yxjgh
        self.yxr = yxr
        self.jbjgh = jbjgh
        self.jbr = jbr

    # self.shanghudanhao = shanghudanhao
    def showdetiles(self):
        print(
            f'客户名称：{self.khmc}   卡号：{self.cardId}   身份证：{self.sfzID} '
            f'  开卡日期：{self.kkdata}  制卡日期：{self.zkdata}  '
            f' 营销机构号：{self.yxjgh}  营销人：{self.yxr} 经办机构号：{self.jbjgh}  经办人：{self.jbr}')

class Jgh():
    def __init__(self, jgmc, jgid):
        self.jgmc = jgmc
        self.jgid = jgid

db = pymysql.connect(
    host='localhost',
    user='root',
    password='lichking54321',
    port=3306,
    db='test',
    charset='utf8')

sql_creat_sbk = """ create table lich_sbk(
			id int NOT NULL AUTO_INCREMENT primary key,
			客户名称 char(20),
			卡号 char(20),
			身份证 char(20),
			开卡日期 date,
			制卡日期 date,
			营销机构号 char(20),
			营销人 char(20),
			经办机构号 char(20),
			经办人 char(20)
			)
			"""

sql_creat_jgh = """ create table lich_base_jgh (
    id int NOT NULL AUTO_INCREMENT primary key,
    机构名称 char(20),
    机构号 char(20)
)
			"""


sql_insert_lich_sbk = """
		insert into lich_sbk(
		客户名称,卡号,身份证,开卡日期,制卡日期,营销机构号,营销人,经办机构号,经办人)
		values
		(%s,%s,%s,%s,%s,%s,%s,%s,%s)
		"""
sql_insert_lich_jgh = """
		insert into lich_base_jgh(
		机构名称,机构号)
		values
		(%s,%s)
		"""


select_all_lich_sbk = """
    select count(*) from lich_sbk 
        where 制卡日期 between %s and %s;
		"""
select_yxjgh_lich_sbk = """
	select count(*),营销机构号 from lich_sbk 
	    where 制卡日期 between %s and %s
        group by 营销机构号
        order by 营销机构号 ;
		"""
select_yxr_lich_sbk = """
    select count(*),营销机构号,营销人 from lich_sbk 
        where 制卡日期 between %s and %s
        group by 营销机构号,营销人
        order by 营销机构号;
		"""


def dataFormate(str):
    #print(str)
    if "." in str:
        strs = str.split(".")
        datetime = strs[0] + "/" + strs[1] + "/" + strs[2]
    elif "-" in str:
        strs = str.split("-")
        datetime = strs[0] + "/" + strs[1] + "/" + strs[2]
    else:
        datetime = str[0:4] + "/" + str[4:6] + "/" + str[6:8]
    return datetime

def readJghExcle(exclePath):
    lichxls = xlrd2.open_workbook(exclePath)
    sht =lichxls.sheet_by_index(0)
    row_all = sht.nrows
    col_all = sht.ncols

    jgh_sht = []

    for row_i in range(row_all):
        rows_value = sht.row_values(row_i, 0, col_all)
        #print(rows_value)
        jgmc= rows_value[0]
        jgid = rows_value[1]
        jgh = Jgh(jgmc,jgid)
        jgh_sht.append(jgh)
    return jgh_sht

def writesql_jgh(jgh_sht):
    cursor = db.cursor()
    cursor.execute("drop table if exists lich_base_jgh")
    try:
        cursor.execute(sql_creat_jgh)
    except:
        print("error to create_table ! ")
    try:
        # insert sql
        for jgh in jgh_sht:
            cursor.execute(sql_insert_lich_jgh, (
                jgh.jgmc,jgh.jgid
            ))
        db.commit()
    except:
        # 异常回滚
        db.rollback()
        print("error to insert1 fullback! ")

def readSbkExcle(exclePath):
    lichxls = xlrd2.open_workbook(exclePath)
    #print(exclePath)
    sht =lichxls.sheet_by_index(2)
    print(sht.name)
    row_all = sht.nrows
    col_all = sht.ncols

    sbk_sht = []
    for row_i in range(row_all):
        rows_value = sht.row_values(row_i, 0, col_all)
        if len(rows_value[2])==19 :
            kkmc = rows_value[1]
            cardId = rows_value[2]
            sfzID = rows_value[3]

            datatype = sht.cell(row_i, 4).ctype
            #print("datatype" ,datatype)
            if datatype == 2 :
                kkdata = int(rows_value[4])
                kkdata =str(kkdata)
                kkdata = dataFormate(kkdata)
            elif datatype == 3:
                t1 = sht.cell_value(row_i,4)
                kkdata = xlrd2.xldate.xldate_as_datetime(t1, 0)
                #print(kkdata)
            else:
                kkdata = str(rows_value[4])
                kkdata = dataFormate(kkdata)

            datatype = sht.cell(row_i, 5).ctype
            #print("datatype",datatype)
            if datatype == 2:
                zkdata = int(rows_value[5])
                zkdata = str(zkdata)
                zkdata = dataFormate(zkdata)
            elif datatype == 3:
                t1 = sht.cell_value(row_i,5)
                #print(t1)
                zkdata = xlrd2.xldate.xldate_as_datetime(t1, 0)
                #print(zkdata)
            else:
                zkdata = str(rows_value[5])
                zkdata = dataFormate(zkdata)

            yxjgh = rows_value[6]
            if type(yxjgh) == float:
                yxjgh = int(rows_value[6])
            else:
                yxjgh = rows_value[6]
            if type(yxjgh) == str:
                print(yxjgh)

            yxr = rows_value[7]
            yxr = ''.join(yxr.split())
            jbjgh = rows_value[8]
            if type(jbjgh) == float:
                jbjgh = int(rows_value[8])
            else:
                jbjgh = rows_value[8]

            jbr = rows_value[9]
            sbk = Sbk(kkmc,cardId,sfzID,kkdata,zkdata,yxjgh,yxr,jbjgh,jbr)
            #sbk.showdetiles()

            sbk_sht.append(sbk)
    return  sbk_sht

def writesql(sbk_all):

    cursor = db.cursor()
    cursor.execute("drop table if exists lich_sbk")
    try:
        cursor.execute(sql_creat_sbk)
    except:
        print("error to create_table ! ")

    try:
        # insert sql
        for sbk_sht in sbk_all:
            for sbk in sbk_sht:
                #sbk.showdetiles()
                cursor.execute(sql_insert_lich_sbk, (
                    sbk.khmc, sbk.cardId, sbk.sfzID, sbk.kkdata, sbk.zkdata, sbk.yxjgh, sbk.yxr, sbk.jbjgh, sbk.jbr))
        db.commit()
    except:
        # 异常回滚
        db.rollback()
        print("error to insert1 fullback! ")

sbk_all = []
jgh_sht = []


'''
path = '../shebaoka/shebaoka'
files = os.listdir(path)

for file in files:
    print(path + '/' + file)
    sbk_sht = readSbkExcle(path + '/' + file)
    sbk_all.append(sbk_sht)

'''

path = '../shebaoka/每日'
files = os.listdir(path)
print(files)

for file in files:
    print(path + '/' + file)
    path1 = path + '/' + file
    files1 = os.listdir(path1)
    for fle1 in files1:
        print(path1 + '/' + fle1)
        sbk_sht = readSbkExcle(path1 + '/' + fle1)
        sbk_all.append(sbk_sht)


writesql(sbk_all)

'''
cursor = db.cursor()
for sbk_sht in sbk_all:
    for sbk in sbk_sht:
        #sbk.showdetiles()
        cursor.execute(sql_insert_lich_sbk, (
            sbk.khmc, sbk.cardId, sbk.sfzID, sbk.kkdata, sbk.zkdata, sbk.yxjgh, sbk.yxr, sbk.jbjgh, sbk.jbr))
    db.commit()
'''




'''

cursor = db.cursor()
cursor.execute(select_all_lich_sbk,(STARTTIME,ENDTIME));
results1 = cursor.fetchall();
print(results1)

cursor.execute(select_yxjgh_lich_sbk,(STARTTIME,ENDTIME));
results2 = cursor.fetchall();
print(results2)


cursor.execute(select_yxr_lich_sbk,(STARTTIME,ENDTIME));
results3 = cursor.fetchall();
print(results3)

'''


#增加数据库机构号
jgh_sht = readJghExcle("机构号.xls")
writesql_jgh(jgh_sht)


db.close()

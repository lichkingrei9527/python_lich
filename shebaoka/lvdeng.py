import pymysql
import xlrd2
import os


STARTTIME = "2023-07-09"
ENDTIME = "2023-08-08"
path_all = '../shebaoka/lvdeng8'

class lvdeng():
    def __init__(self, anli,miaoshu, jigou):
        self.anli = anli
        self.miaoshu = miaoshu
        self.jigou = jigou


    # self.shanghudanhao = shanghudanhao
    def showdetiles(self):
        print(
            f'案例名称：{self.anli}   描述：{self.miaoshu}   机构：{self.jigou} ')



db = pymysql.connect(
    host='localhost',
    user='root',
    password='lichking54321',
    port=3306,
    db='test',
    charset='utf8')

sql_creat_lvdeng = """ create table lich_lvdeng(
			id int NOT NULL AUTO_INCREMENT primary key,
			anli char(200),
			miaoshu char(200),
			jigou char(20)
			)
			"""

sql_insert_lich_lvdeng = """
		insert into lich_lvdeng(
		anli,miaoshu,jigou)
		values
		(%s,%s,%s)
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




#单个文件处理
def readldExcle(exclePath):
    lichxls = xlrd2.open_workbook(exclePath)
    sht =lichxls.sheet_by_name("县级机构汇总")
    row_all = sht.nrows
    col_all = sht.ncols
    ld_list = []
    for row_i in range(row_all):
        rows_value = sht.row_values(row_i, 0, col_all)
        #print(rows_value[1],1)
        #print(rows_value[2],2)
        #print(rows_value[3],3)
        #print(rows_value[4],4)


        if len(rows_value[4])>1 and "问题描述" not in rows_value[4] and "日期：" not in rows_value[4]:
            anli1=rows_value[1]
            miaoshu1 = rows_value[4]

            if "忻州" in exclePath:
                ld = lvdeng(anli1,miaoshu1,"忻州")
            if "定襄" in exclePath:
                ld = lvdeng(anli1, miaoshu1, "定襄")
            if "五台" in exclePath:
                ld = lvdeng(anli1, miaoshu1, "五台")
            if "原平" in exclePath:
                ld = lvdeng(anli1, miaoshu1, "原平")
            if "代县" in exclePath:
                ld = lvdeng(anli1, miaoshu1, "代县")
            if "繁峙" in exclePath:
                ld = lvdeng(anli1, miaoshu1, "繁峙")
            if "宁武" in exclePath:
                ld = lvdeng(anli1, miaoshu1, "宁武")
            if "静乐" in exclePath:
                ld = lvdeng(anli1, miaoshu1, "静乐")
            if "神池" in exclePath:
                ld = lvdeng(anli1, miaoshu1, "神池")
            if "五寨" in exclePath:
                ld = lvdeng(anli1, miaoshu1, "五寨")
            if "岢岚" in exclePath:
                ld = lvdeng(anli1, miaoshu1, "岢岚")
            if "河曲" in exclePath:
                ld = lvdeng(anli1, miaoshu1, "河曲")
            if "保德" in exclePath:
                ld = lvdeng(anli1, miaoshu1, "保德")
            if "偏关" in exclePath:
                ld = lvdeng(anli1, miaoshu1, "偏关")
            #ld.showdetiles()
            ld_list.append(ld)
    return  ld_list

#遍历所有县的案例
def wirteld (list_all):
    for xian in lich_all:
        for anli in xian:
            anli.showdetiles()

#写数据库
def write_sql_ld(list_all):

    cursor = db.cursor()
    cursor.execute("drop table if exists lich_lvdeng")
    try:
        cursor.execute(sql_creat_lvdeng)
    except:
        print("error to create_table ! ")

    try:
        for xian in lich_all:
            for anli1 in xian:
                anli1.showdetiles()
                cursor.execute(sql_insert_lich_lvdeng,(
                    anli1.anli,anli1.miaoshu,anli1.jigou
                ))
        db.commit()
    except:
        # 异常回滚
        db.rollback()
        print("error to insert1 fullback! ")

#遍历读取路径下所有文件
def readall(path):
    files = os.listdir(path)
    lich_all_ld = []
    lvdeng_exlce = []
    for file in files:
        #print(path + '/' + file)
        path1 = path + '/' + file
        files1 = os.listdir(path1)
        for fle1 in files1:
            #print(path1 + '/' + fle1)
            #sbk_sht = readSbkExcle(path1 + '/' + fle1)
            #sbk_all.append(sbk_sht)
            if "xls" in fle1:
                str1 = path1 + '/' + fle1
                #print(str1)
                lvdeng_exlce.append(str1)
                lich_xian = readldExcle(str1)
                lich_all_ld.append(lich_xian)
    return lich_all_ld

lich_all = readall(path_all)

write_sql_ld(lich_all)

'''
cursor = db.cursor()

cursor.execute("drop table if exists lich_lvdeng")
cursor.execute(sql_creat_lvdeng)
for xian in lich_all:
    for anli1 in xian:
        anli1.showdetiles()
        cursor.execute(sql_insert_lich_lvdeng,(
                    anli1.anli,anli1.miaoshu,anli1.jigou
                ))

db.commit()
'''

db.close()



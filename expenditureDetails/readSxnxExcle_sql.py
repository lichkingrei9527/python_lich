import pymysql
import xlrd2


class Jiaoyi():
    def __init__(self, jiaoyiriqi, jiaoyishijian, jiaoyileixing, jiaoyishouzhi,
                 jiaoyifangshi, jiaoyijine, jiaoyiduifang, jiaoyiqudao):
        # self.jiaoyidanhao = jiaoyidanhao
        self.jiaoyiriqi = jiaoyiriqi
        self.jiaoyishijian = jiaoyishijian
        self.jiaoyileixing = jiaoyileixing
        self.jiaoyishouzhi = jiaoyishouzhi
        self.jiaoyifangshi = jiaoyifangshi
        self.jiaoyijine = jiaoyijine
        self.jiaoyiduifang = jiaoyiduifang
        self.jiaoyiqudao = jiaoyiqudao

    # self.shanghudanhao = shanghudanhao
    def showdetiles(self):
        print(
            f'交易日期：{self.jiaoyiriqi}   交易时间：{self.jiaoyishijian}   交易类型：{self.jiaoyileixing}   交易收支：{self.jiaoyishouzhi}  交易方式：{self.jiaoyifangshi}   交易金额：{self.jiaoyijine}  交易对方：{self.jiaoyiduifang}')


#weixintxts = ['2020weixin.txt', '2021weixin.txt']
sxnxExcle= "山西农信.xlsx"

db = pymysql.connect(
    host='localhost',
    user='root',
    password='lichking54321',
    port=3306,
    db='test',
    charset='utf8')
'''
# 微信账单
sql_creat_weixin =""" create table lich_weixin(
			id int NOT NULL AUTO_INCREMENT primary key,
			交易日期 char(20),
			交易时间 char(20),
			交易类型 char(20),
			交易收支 char(20),
			交易方式 char(20),
			交易金额 int,
			交易对方 char(80),
			交易渠道 char(10)
			)
			"""
'''
# sxnx明细
sql_creat_sxnx = """ create table lich_sxnx(
			id int NOT NULL AUTO_INCREMENT primary key,
			交易日期 date,
			交易时间 char(20),
			交易类型 char(20),
			交易收支 char(20),
			交易方式 char(20),
			交易金额 double ,
			交易对方 char(80),
			交易渠道 char(10)
			)
			"""

sql_insert_lich_sxnx = """
		insert into lich_sxnx(
		交易日期,交易时间,交易类型,交易收支,交易方式,交易金额,交易对方,交易渠道)
		values
		(%s,%s,%s,%s,%s,%s,%s,%s)
		"""
sql_update_lich_sxnx_shouzhi = """
        update lich_sxnx set 交易收支 = '支出' where 交易金额 <= 0
        """ 
sql_update_lich_sxnx_jine = """
        update lich_sxnx set 交易金额 = 0-交易金额 where 交易收支 = '支出'
        """ 


def readSxnxExcle(exclePath):
    lichxls = xlrd2.open_workbook(exclePath)
    shts_count = lichxls.nsheets
    jiaoyi_all = []
    for sht_i in range(shts_count):
        print (f'此处为第{sht_i}工作簿：{lichxls.sheet_by_index(sht_i).name}')
        sht = lichxls.sheet_by_index(sht_i)
        row_all = lichxls.sheet_by_index(sht_i).nrows
        col_all = lichxls.sheet_by_index(sht_i).ncols
        jiaoyi_sht = []
        for row_i in range(row_all):
            rows_value = sht.row_values(row_i,0,col_all)
            t1 =  sht.cell_value(row_i,0)
            date1 = xlrd2.xldate.xldate_as_datetime(t1,0)
            jiaoyiriqi = date1.strftime("%Y/%m/%d")
            jiaoyishijian = ''
            jiaoyileixing = rows_value[3]
            jiaoyishouzhi = '收入'
            jiaoyijine = rows_value[4]
            jiaoyifangshi = rows_value[7]
            jiaoyiduifang = ''
            jiaoyiqudao = '山西农信'
            anyone = Jiaoyi(jiaoyiriqi, jiaoyishijian, jiaoyileixing, jiaoyishouzhi, jiaoyifangshi, jiaoyijine,
                            jiaoyiduifang, jiaoyiqudao)
            jiaoyi_sht.append(anyone)
        for jy in jiaoyi_sht:
            jiaoyi_all.append(jy)
        #print(jiaoyi_all[0].jiaoyiriqi)
    return jiaoyi_all


#jiaoyi_weixin = readweixintxt(weixintxts)
jiaoyi_sxnx = readSxnxExcle(sxnxExcle)
'''
for j in jiaoyi_sxnx:
    print(j.jiaoyiqudao,j.jiaoyiduifang,j.jiaoyijine,j.jiaoyiriqi,j.jiaoyifangshi,j.jiaoyileixing,j.jiaoyishijian,j.jiaoyishouzhi)
'''

# 建立游标
cursor = db.cursor()
# 如果表存在则删掉表
cursor.execute("drop table if exists lich_sxnx")

# 执行sql
try:
    cursor.execute(sql_creat_sxnx)
except:
    print("error to create_table ! ")


try:
    # insert sql
    for one in jiaoyi_sxnx:
    	#print(one.jiaoyijine)
    	cursor.execute(sql_insert_lich_sxnx,(one.jiaoyiriqi,one.jiaoyishijian,one.jiaoyileixing,one.jiaoyishouzhi,one.jiaoyifangshi,one.jiaoyijine,one.jiaoyiduifang,one.jiaoyiqudao))
    db.commit()
except:
    # 异常回滚
    db.rollback()
    print("error to insert1 fullback! ")


try:
    cursor.execute(sql_update_lich_sxnx_shouzhi)
    db.commit()
except:
    print("error to update_table ! ")
try:
    cursor.execute(sql_update_lich_sxnx_jine)
    db.commit()
except:
    print("error to update_table ! ")


db.close()
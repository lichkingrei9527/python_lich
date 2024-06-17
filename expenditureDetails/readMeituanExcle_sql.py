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
MeituanExcle= "工资分析.xlsx"

db = pymysql.connect(
    host='localhost',
    user='root',
    password='lichking',
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
sql_creat_lich_meituan = """ create table lich_meituan(
			id int NOT NULL AUTO_INCREMENT primary key,
			交易日期 date,
			交易时间 char(20),
			交易类型 char(20),
			交易收支 char(20),
			交易方式 char(20),
			交易金额 float,
			交易对方 char(80),
			交易渠道 char(10)
			)
			"""

sql_insert_lich_meituan = """
		insert into lich_meituan(
		交易日期,交易时间,交易类型,交易收支,交易方式,交易金额,交易对方,交易渠道)
		values
		(%s,%s,%s,%s,%s,%s,%s,%s)
		"""


def readMeituanExcle(exclePath):
    lichxls = xlrd2.open_workbook(exclePath)

    sht = lichxls.sheet_by_name('美团')
    row_all = sht.nrows
    col_all = sht.ncols
    jiaoyi_all = [] 
    for row_i in range(row_all):
    	t1 =  sht.cell_value(row_i,1)
    	date1 = xlrd2.xldate.xldate_as_datetime(t1,0)
    	jiaoyiriqi = date1.strftime("%Y/%m/%d")
    	jiaoyijine = sht.cell_value(row_i,2)
    	jiaoyiduifang = sht.cell_value(row_i,3)
    	anyone = Jiaoyi(jiaoyiriqi,'','','支出','',jiaoyijine,jiaoyiduifang,'美团')
    	jiaoyi_all.append(anyone)

    return jiaoyi_all


#jiaoyi_weixin = readweixintxt(weixintxts)
jiaoyi_sxnx = readMeituanExcle(MeituanExcle)

# 建立游标
cursor = db.cursor()
# 如果表存在则删掉表
cursor.execute("drop table if exists lich_meituan")

# 执行sql
try:
    cursor.execute(sql_creat_lich_meituan)
except:
    print("error to create_table ! ")


try:
    # insert sql
    for one in jiaoyi_sxnx:
    	#print(one.jiaoyijine)
    	cursor.execute(sql_insert_lich_meituan,(one.jiaoyiriqi,one.jiaoyishijian,one.jiaoyileixing,one.jiaoyishouzhi,one.jiaoyifangshi,one.jiaoyijine,one.jiaoyiduifang,one.jiaoyiqudao))
    db.commit()
except:
    # 异常回滚
    db.rollback()
    print("error to insert1 fullback! ")

db.close()
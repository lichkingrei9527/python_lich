import pymysql
import xlrd


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
        print(f'交易日期：{self.jiaoyiriqi}   交易时间：{self.jiaoyishijian}   交易类型：{self.jiaoyileixing}   交易收支：{self.jiaoyishouzhi}  交易方式：{self.jiaoyifangshi}   交易金额：{self.jiaoyijine}  交易对方：{self.jiaoyiduifang} 交易渠道:{self.jiaoyiqudao}')


#weixintxts = ['2020weixin.txt', '2021weixin.txt']
zhifubaoExcle = "支付宝.xlsx"

db = pymysql.connect(
    host='localhost',
    user='root',
    password='lichking',
    port=3306,
    db='test',
    charset='utf8')

# zhifubao明细
sql_creat_zfb = """ create table lich_zfb(
			orderID_zhifubao int NOT NULL AUTO_INCREMENT primary key,
			交易日期 date,
			交易时间 char(20),
			交易类型 char(100),
			交易收支 char(20),
			交易方式 char(20),
			交易金额 float,
			交易对方 char(200),
			交易渠道 char(10)
			)
			"""

sql_insert_lich_zfb = """
		insert into lich_zfb(
		交易日期,交易时间,交易类型,交易收支,交易方式,交易金额,交易对方,交易渠道)
		values
		(%s,%s,%s,%s,%s,%s,%s,%s)
		"""
'''
sql_update_lich_sxnx_shouzhi = """
        update lich_sxnx set 交易收支 = '支出' where 交易金额 <= 0
        """ 
sql_update_lich_sxnx_jine = """
        update lich_sxnx set 交易金额 = 0-交易金额 where 交易收支 = '支出'
        """ 
'''


def readZhiFuBaoExcle(exclePath):
    lichxls = xlrd.open_workbook(exclePath)
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
            t1 =  sht.cell_value(row_i,11)
            '''
            print(t1)
            date1 = xlrd.xldate.xldate_as_datetime(t1,0)
            print(date1)
            jiaoyiriqi = date1.strftime("%Y/%m/%d")
            print(jiaoyiriqi)
            jiaoyishijian = date1.strftime("%H:%M")
            print(jiaoyishijian)
            '''

            '''
            date1 =xlrd.xldate_as_tuple(t1,0)
            print(date1)
            jiaoyiriqi = str(date1[0]) + "-" + str(date1[1]) + "-" + str(date1[2])
            print(jiaoyiriqi)
            jiaoyishijian = str(date1[3]) + ":" + str(date1[4])
            print(jiaoyishijian)
            '''
            jiaoyiriqi = rows_value[10]
            jiaoyiriqi = jiaoyiriqi.replace('/','-')
            jiaoyishijian = rows_value[11]
            jiaoyileixing = rows_value[4]
            jiaoyishouzhi = rows_value[0]
            jiaoyijine = rows_value[5]
            jiaoyifangshi = ""
            jiaoyiduifang = rows_value[1]+":"+rows_value[3]
            jiaoyiqudao = '支付宝'
            anyone = Jiaoyi(jiaoyiriqi, jiaoyishijian, jiaoyileixing, jiaoyishouzhi, jiaoyifangshi, jiaoyijine,
                            jiaoyiduifang, jiaoyiqudao)
            jiaoyi_sht.append(anyone)
            #anyone.showdetiles()
        for jy in jiaoyi_sht:
            jiaoyi_all.append(jy)
        #print(jiaoyi_all[0].showdetiles())
    return jiaoyi_all


#jiaoyi_weixin = readweixintxt(weixintxts)
jiaoyi_zhifubao = readZhiFuBaoExcle(zhifubaoExcle)

# 建立游标
cursor = db.cursor()
# 如果表存在则删掉表
cursor.execute("drop table if exists lich_zfb")

# 执行sql
try:
    cursor.execute(sql_creat_zfb)
except:
    print("error to create_table ! ")


try:
    # insert sql
    for one in jiaoyi_zhifubao:
        one.showdetiles()
        #print(one.jiaoyijine)
        cursor.execute(sql_insert_lich_zfb,(one.jiaoyiriqi,one.jiaoyishijian,one.jiaoyileixing,one.jiaoyishouzhi,one.jiaoyifangshi,one.jiaoyijine,one.jiaoyiduifang,one.jiaoyiqudao))
    db.commit()
except pymysql.InternalError as error:
    code,message = error.args
    print(code,message)
'''    
except:
    # 异常回滚
    db.rollback()
    print("error to insert1 fullback! ")
'''

'''
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
'''

db.close()
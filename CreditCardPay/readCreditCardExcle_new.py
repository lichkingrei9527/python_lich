import pymysql
import xlrd2

'''
使用说明：
将Excel按格式复制到根目录下，多个sheet时，每个sheet模板保持一致，无其他废弃数据
'''
CCDS_PATH= "信用卡营销.xlsx"
STARTDATE = '2023-04-01'
ENDDATE = '2023-05-31'
WORK_ID = '335776'

class CreditCards():
    def __init__(self, riqi,customer,phoneNo,staff,type1,jobNo):
        self.riqi = riqi
        self.customer = customer
        self.phoneNo = phoneNo
        self.staff = staff
        self.type1 = type1
        self.jobNo = jobNo

    def showdetiles(self):
        print(f'办理日期：{self.riqi}   姓名：{self.customer}   联系方式：{self.phoneNo}   营销人：{self.staff}  类型：{self.type1}   工号：{self.jobNo} ')

db = pymysql.connect(
    host='localhost',
    user='root',
    password='lichking54321',
    port=3306,
    db='test',
    charset='utf8')


sql_creat_creditCard = """ create table lich_creditCard(
			id int NOT NULL AUTO_INCREMENT primary key,
			办理日期 date,
			姓名 char(20),
			联系方式 char(20),
			营销员工 char(20),
			业务类型 char(20),
			推荐人工号 char(20)
			)
			"""

sql_insert_lich_creditCard = """ insert into lich_creditCard(
		办理日期,姓名,联系方式,营销员工,业务类型,推荐人工号)
		values
		(%s,%s,%s,%s,%s,%s)
		"""

select_lich_creditCrad =""" select 营销员工,业务类型,count(*) as 办理数量 from lich_creditcard
                          where 推荐人工号 = %s
                          and (办理日期 between %s and %s)
                          group by 营销员工,业务类型
                          order by 营销员工;

"""
select_lich_creditCrad_ct = """select 业务类型,count(*) from lich_creditcard
                          where 推荐人工号 = %s
                          and (办理日期 between %s and %s)
                          group by 业务类型;
"""

def readCreditCard(exclePath):
    lichxls = xlrd2.open_workbook(exclePath)
    shts_count = lichxls.nsheets
    ccards = []
    for sht_i in range(shts_count):

        #print (f'此处为第{sht_i}工作簿：{lichxls.sheet_by_index(sht_i).name}')
        sht = lichxls.sheet_by_index(sht_i)
        row_all = lichxls.sheet_by_index(sht_i).nrows
        col_all = lichxls.sheet_by_index(sht_i).ncols
        ccrad_sht = []
        for row_i in range(row_all):
            rows_value = sht.row_values(row_i,0,col_all)
            t1 =  sht.cell_value(row_i,0)
            t1str = str(t1)
            tt = t1str.split('.')
            #print("xxxx",tt)
            #print("xxx",tt[0],tt[1],tt[2])
            riqi = tt[0]+ '/' +tt[1] + '/' +tt[2]
            #date1 = xlrd2.xldate.xldate_as_datetime(t1,0)
            #riqi = date1.strftime("%Y/%m/%d")
            customer = rows_value[1]
            phoneNo = rows_value[2]
            staff = rows_value[3]
            type1 = rows_value[4]
            if "激活" in type1:
                type1 = "激活"
            if "办理" in type1:
                type1 = "办理"
            jobNostr = str(rows_value[5])
            jobNos = jobNostr.split('.')
            jobNo = jobNos[0]
            anyone = CreditCards(riqi, customer, phoneNo,staff, type1, jobNo)
            ccrad_sht.append(anyone)
        for ccd in ccrad_sht:
            ccards.append(ccd)
    return ccards




def creat_ccdsql(sql):

    cursor.execute("drop table if exists lich_creditCard")
    try:
        cursor.execute(sql_creat_creditCard)
    except:
        print("error to create_table ! ")

def inset_ccdsql(sql,ccds):
    try:
        for ccd in ccds:
            ccd.showdetiles()
            cursor.execute(sql_insert_lich_creditCard,(ccd.riqi,ccd.customer,ccd.phoneNo,ccd.staff,ccd.type1,ccd.jobNo))
        db.commit()
    except:
        db.rollback()
        print("error to insert1 fullback! ")



def ccd_pay(startdate,enddate):
    try:
        cursor.execute(select_lich_creditCrad,(WORK_ID,STARTDATE,ENDDATE));
        results = cursor.fetchall();
        print(f"在 {startdate} 到 {enddate} 期间：")
        for row in results:
            if row[1] =="办理":
                print(f"{row[0]}：{row[1]}信用卡{row[2]}张，奖励为{row[2]*30}元")
            if row[1] == "激活":
                print(f"{row[0]}：{row[1]}信用卡{row[2]}张，奖励为{row[2]*10}元")

    except:
        db.rollback()
        print("select  fullback! ")
    try:
        cursor.execute(select_lich_creditCrad_ct,(WORK_ID,STARTDATE,ENDDATE));
        results1 = cursor.fetchall();
        pay = 0
        for row in results1:
            if row[0] == "办理":
                banli = int(row[1])
                pay = pay + banli * 20
                print (f"共办理信用卡:{row[1]}张")
            if row[0] == "激活":
                pay = row[1]*30 + pay
                print(f"共激活信用卡:{row[1]}张")
        print(f"预计分配信用卡奖励共{pay}元" )

    except:
        db.rollback()
        print("select  fullback! ")

cursor = db.cursor()

ccds = readCreditCard(CCDS_PATH)
creat_ccdsql(sql_creat_creditCard)
inset_ccdsql(sql_insert_lich_creditCard,ccds)
ccd_pay(STARTDATE,ENDDATE)

db.close()
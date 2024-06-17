import pymysql
import xlrd2
import xlwt

'''
使用说明：
将Excel按格式复制到根目录下，多个sheet时，每个sheet模板保持一致，无其他废弃数据
'''
CCDS_PATH= "20220101_20230510etc.xls"
STARTDATE = '2023-01-01'
ENDDATE = '2023-01-31'
OUTPUTFILENAME = "资料整理.xls"

class Etc():
    def __init__(self, customerID,customer,OBU,arcNo,carNoColoer,carType,BusinessType,addtime,oubState,notes):
        self.customerID = customerID
        self.customer = customer
        self.OBU = OBU
        self.arcNo = arcNo
        self.carNoColoer = carNoColoer
        self.carType = carType
        self.BusinessType = BusinessType
        self.addtime = addtime
        self.oubState = oubState
        self.notes = notes


    def showdetiles(self):
        print(f' 客户号：{self.customerID}  客户：{self.customer}  电子标签号：{self.OBU}   车牌：{self.arcNo} '
              f' 车牌颜色：{self.carNoColoer}   车型：{self.carType}  业务类型：{self.BusinessType} '
              f' 时间：{self.addtime}  电子标签状态：{self.oubState} 备注：{self.notes}')

db = pymysql.connect(
    host='localhost',
    user='root',
    password='lichking',
    port=3306,
    db='test',
    charset='utf8')


sql_creat_etc = """ create table lich_etc(
			id int NOT NULL AUTO_INCREMENT primary key,
            客户号 char(20),
			客户 char(60),
			电子标签号 char(20),
			车牌 char(20),
			车牌颜色 char(20),
			车型 char(20),
			业务类型 char(20),
			时间 date,
			电子标签状态 char(20)
			)
			"""

sql_insert_lich_etc = """ insert into lich_etc(
		客户号,客户,电子标签号,车牌,车牌颜色,车型,业务类型,时间,电子标签状态)
		values
		(%s,%s,%s,%s,%s,%s,%s,%s,%s)
		"""

select_lich_creditCrad =""" select 营销员工,业务类型,count(*) as 办理数量 from lich_creditcard
                          where 推荐人工号 = "335776"
                          and (办理日期 between %s and %s)
                          group by 营销员工,业务类型
                          order by 营销员工;

"""
select_lich_creditCrad_ct = """select 业务类型,count(*) from lich_creditcard
                          where 推荐人工号 = "335776"
                          and (办理日期 between %s and %s)
                          group by 业务类型;
"""

select_lich_etc_old = """select * from lich_etc
                          where 业务类型 = "电子标签销售"
                          or 业务类型 = "电子标签维护"
                          or 业务类型 = "电子标签回收"
                          order by 时间;
"""
select_lich_etc = """select * from lich_etc
                          where 业务类型 = "电子标签销售"
                          or 业务类型 = "电子标签回收"
                          order by 时间;
"""



def readEtcAll(exclePath):
    lichxls = xlrd2.open_workbook(exclePath)
    shts_count = lichxls.nsheets
    etcs = []
    for sht_i in range(shts_count):

        #print (f'此处为第{sht_i}工作簿：{lichxls.sheet_by_index(sht_i).name}')
        sht = lichxls.sheet_by_index(sht_i)
        row_all = lichxls.sheet_by_index(sht_i).nrows
        #print("看看是啥3", row_all)
        #总行数
        col_all = lichxls.sheet_by_index(sht_i).ncols
        #print("看看是啥4", col_all)
        #总列数
        for row_i in range(row_all):
            #row_i行，0到col_all列的值的集合
            rows_value = sht.row_values(row_i,0,col_all)
            #print("看看是啥1" , rows_value)
            t1 =  sht.cell_value(row_i,6)
            #print("看看是啥2", t1)
            t1str = str(t1)
            tt = t1str.split(' ')
            #print("看看是啥5", tt)
            riqi = tt[0]
            #print(riqi)
            #date1 = xlrd2.xldate.xldate_as_datetime(t1,0)
            #riqi = date1.strftime("%Y/%m/%d")
            #customerID,customer,OBU,arcNo,carNoColoer,carType,BusinessType,addtime,oubState
            customerID = rows_value[0]
            customer = rows_value[1]
            OBU = ""
            arcNo = rows_value[2]
            carNoColoer = rows_value[3]
            carType = rows_value[4]
            BusinessType = rows_value[5]
            addtime = riqi
            oubState = ""
            notes = ""
            #jobNos = jobNostr.split('.')
            #jobNo = jobNos[0]
            anyone = Etc(customerID, customer,OBU,arcNo, carNoColoer, carType,BusinessType,addtime,oubState,notes)
            #anyone.showdetiles()
            etcs.append(anyone)
    return etcs




def creat_etcsql(sql):

    cursor.execute("drop table if exists lich_etc")
    try:
        cursor.execute(sql_creat_etc)
    except:
        print("error to create_table ! ")

def inset_etcsql(sql,etcs):
    try:
        for etc in etcs:
            cursor.execute(sql_insert_lich_etc,(etc.customerID,etc.customer,etc.OBU,etc.arcNo,etc.carNoColoer,etc.carType,etc.BusinessType,etc.addtime,etc.oubState))
        db.commit()
    except:
        db.rollback()
        print("error to insert data！ ")


#业务逻辑，单位、个人分类，注销业务备注，维护业务备注维修更换，
def etc_contents():
    cursor.execute(select_lich_etc);
    results= cursor.fetchall();
    gongsis = []
    gerens = []
    for row in results:
        # 单位
        if len(row[2]) > 3:
            customerID = row[1]
            customer = row[2]
            OBU = ""
            arcNo = row[4]
            carNoColoer = row[5]
            carType = row[6]
            BusinessType = row[7]
            addtime = row[8]
            oubState = ""
            notes = ""
            if BusinessType == "电子标签回收":
                notes = "注销"
            if BusinessType == "电子标签维护":
                notes = "维修更换"
            gongsi = Etc(customerID, customer, OBU, arcNo, carNoColoer, carType, BusinessType, addtime, oubState, notes)
            gongsis.append(gongsi)
        # 个人
        if len(row[2]) < 4:
            customerID = row[1]
            customer = row[2]
            OBU = ""
            arcNo = row[4]
            carNoColoer = row[5]
            carType = row[6]
            BusinessType = row[7]
            addtime = row[8]
            oubState = ""
            notes = ""
            if BusinessType == "电子标签回收":
                notes = "注销"
            if BusinessType == "电子标签维护":
                notes = "维修更换"
            geren = Etc(customerID, customer, OBU, arcNo, carNoColoer, carType, BusinessType, addtime, oubState, notes)
            gerens.append(geren)
    return  gongsis,gerens


def writeEtc(ziliaos,OUTPUTFILENAME):
    workbook = xlwt.Workbook(encoding="utf-8")
    ws_gs= workbook.add_sheet("单位etc")
    ws_gr = workbook.add_sheet("个人etc")
    title_data = ('序号','客户标识','客户名称','车牌号','办理日期','备注')
    #公司数据写入
    gs_row = len(ziliaos[0])
    gs_etc = ziliaos[0]
    for row in range(gs_row):
        ws_gs.write(row, 0, row+1)
        ws_gs.write(row,1,gs_etc[row].customerID)
        ws_gs.write(row, 2, gs_etc[row].customer)
        ws_gs.write(row, 3, gs_etc[row].arcNo)
        ws_gs.write(row, 4, str(gs_etc[row].addtime))
        ws_gs.write(row, 5, gs_etc[row].notes)
    #个人数据写入
    gr_row = len(ziliaos[1])
    gr_etc = ziliaos[1]
    for row in range(gr_row):
        ws_gr.write(row, 0, row+1)
        ws_gr.write(row,1,gr_etc[row].customerID)
        ws_gr.write(row, 2, gr_etc[row].customer)
        ws_gr.write(row, 3, gr_etc[row].arcNo)
        ws_gr.write(row, 4, str(gr_etc[row].addtime))
        ws_gr.write(row, 5, gr_etc[row].notes)
    workbook.save(OUTPUTFILENAME)



#获取游标 初始化
cursor = db.cursor()
'''
etcs = readEtcAll(CCDS_PATH)
creat_etcsql(creat_etcsql)
inset_etcsql(sql_insert_lich_etc,etcs)
'''
ziliaos = etc_contents()
writeEtc(ziliaos,OUTPUTFILENAME)

db.close()
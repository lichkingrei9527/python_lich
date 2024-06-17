import pymysql

class Jiaoyi():
	def __init__(self,jiaoyiriqi,jiaoyishijian,jiaoyileixing,jiaoyishouzhi,
		jiaoyifangshi,jiaoyijine,jiaoyiduifang,jiaoyiqudao):
		#self.jiaoyidanhao = jiaoyidanhao
		self.jiaoyiriqi = jiaoyiriqi
		self.jiaoyishijian = jiaoyishijian
		self.jiaoyileixing = jiaoyileixing
		self.jiaoyishouzhi =jiaoyishouzhi
		self.jiaoyifangshi = jiaoyifangshi
		self.jiaoyijine = jiaoyijine
		self.jiaoyiduifang = jiaoyiduifang
		self.jiaoyiqudao = jiaoyiqudao
		#self.shanghudanhao = shanghudanhao
	def showdetiles(self):
		print(f'交易日期：{self.jiaoyiriqi}   交易时间：{self.jiaoyishijian}   交易类型：{self.jiaoyileixing}   交易收支：{self.jiaoyishouzhi}  交易方式：{self.jiaoyifangshi}   交易金额：{self.jiaoyijine}  交易对方：{self.jiaoyiduifang}')
weixintxts = ['2020weixin.txt','2021weixin.txt','2022weixin.txt']


db = pymysql.connect(
	host='localhost' , 
	user='root' , 
	password='lichking' , 
	port=3306 ,
	db='test' ,
	charset='utf8')

# 微信账单
sql_creat_weixin =""" create table lich_weixin(
			id int NOT NULL AUTO_INCREMENT primary key,
			交易日期 date,
			交易时间 time,
			交易类型 char(50),
			交易收支 char(20),
			交易方式 char(20),
			交易金额 float,
			交易对方 char(80),
			交易渠道 char(10)
			)
			"""

sql_insert_lich_weixin ="""
		insert into lich_weixin(
		交易日期,交易时间,交易类型,交易收支,交易方式,交易金额,交易对方,交易渠道)
		values
		(%s,%s,%s,%s,%s,%s,%s,%s)
		"""

#建立游标
cursor = db.cursor()
#如果表存在则删掉表
cursor.execute("drop table if exists lich_weixin")

#执行sql 
try:
	cursor.execute(sql_creat_weixin)
except:
	print ("error to create_table ! ")

jiaoyi_all =[]
def readweixintxt(txts):
	for txt in txts:
		print (txt)
		Readdata = open (txt,encoding = 'utf-8')
		data_all = Readdata.read()
		data_m = data_all.split()		
		i = 0
		#print(len(data_m))
		while i < len(data_m):
			jiaoyiqudao = '微信'
			dateflag = 1
			while dateflag == 1:
				#print(data_m[i])
				if '2020-' in data_m[i]:
					jiaoyiriqi =data_m[i]
					dateflag = 0
				elif '2021-' in data_m[i]:
					jiaoyiriqi =data_m[i]
					dateflag = 0
				elif '2022-' in data_m[i]:
					jiaoyiriqi = data_m[i]
					dateflag = 0
				else:	
					i = i + 1
			i=i+1	

			jiaoyishijian = data_m[i]
			i=i+1
			jiaoyileixing = data_m[i]
			i = i+1
			while data_m[i] not in ['收入','支出','其他']:
				jiaoyileixing = jiaoyileixing + data_m[i]
				i = i+1
			jiaoyishouzhi = data_m[i]
			i=i+1
			jiaoyifangshi =data_m[i]
			i=i+1
			if jiaoyifangshi in ['山西农信(34','工商银行(21','山西农信(67','山西农信(96']:
				jiaoyifangshi = jiaoyifangshi + data_m[i]
				i = i+1
			jiaoyijine = data_m[i]
			i=i+1
			jiaoyiduifang =data_m[i]
			i=i+1
			for value in range(1,6):
				#\u4E00-\u9FFF 中文编码区
				if '\u4e00' <= data_m[i] <= '\u9fff':
					jiaoyiduifang = jiaoyiduifang +data_m[i]
					i = i+1
			anyone = Jiaoyi(jiaoyiriqi,jiaoyishijian,jiaoyileixing,jiaoyishouzhi,jiaoyifangshi,jiaoyijine,jiaoyiduifang,jiaoyiqudao)
			jiaoyi_all.append(anyone)
			#print(i)
			#anyone.showdetiles()
			if i> len(data_m)-5:
				i=i+5

		Readdata.close()

	return jiaoyi_all

jiaoyi_all = readweixintxt(weixintxts)
'''
for one in jiaoyi_all:
	print("日期：",one.jiaoyiriqi,"时间：",one.jiaoyishijian,"类型：",one.jiaoyileixing,"收支：",one.jiaoyishouzhi,"方式：",one.jiaoyifangshi,"金额：",one.jiaoyijine,"对方：",one.jiaoyiduifang)
'''



try:
	# insert sql
	for one in jiaoyi_all:
		#print("日期：",one.jiaoyiriqi,"时间：",one.jiaoyishijian,"类型：",one.jiaoyileixing,"收支：",one.jiaoyishouzhi,"方式：",one.jiaoyifangshi,"金额：",one.jiaoyijine,"对方：",one.jiaoyiduifang)
		cursor.execute(sql_insert_lich_weixin,(one.jiaoyiriqi,
			one.jiaoyishijian,one.jiaoyileixing,one.jiaoyishouzhi,one.jiaoyifangshi,one.jiaoyijine,one.jiaoyiduifang,one.jiaoyiqudao))
	db.commit()
except:
	#异常回滚
	db.rollback()
	print ("error to insert1 fullback! ")



db.close()
import xlrd
from random import randint
import time
'''
pip install pyexcel_xls
pip uninstall xlrd
pip install xlrd==1.2.0
'''
lichxls =  xlrd.open_workbook("山西农信.xlsx")
'''
print('所有sheets的名字：',lichxls.sheet_names())
print('sheets 数量：',lichxls.nsheets)
print('所有sheets对象：',lichxls.sheets())
print('名字获取sheet对象',lichxls.sheet_by_name('2021'))
print('索引获取sheet对象',lichxls.sheet_by_index(2))
print('sheet名:',lichxls.sheet_by_index(0).name)
print('行:',lichxls.sheet_by_index(0).nrows)
print('列:',lichxls.sheet_by_index(0).ncols)
'''
# 日期  x   x  交易类型  交易金额  账户余额  交易柜员  交易方式  
#2020/1/8	0		２０１９年值班费	1,330.00	2,567.24	301102	柜面
sheet1= lichxls.sheet_by_name('2022')
t1 = sheet1.cell_value(0, 0)
#xlrd.xldate.xldate_as_datetime(xldate,datemode)
date1 = xlrd.xldate.xldate_as_datetime(t1,0)
'''
%y	年份的后两位数字	
%Y	四位完整的年份	
%j	该日期是一年当中的第几天	范围在001-366之间
%m	月份	
%b	简写英文月份	
%B	完整英文月份	
%d	返回是该月的第几日	
%H	小时	24小时制
%I	小时	12小时制
%p	上午或下午	AM或者PM
%M	分钟	
%S	秒钟	
%x	日期	日/月/年（注意顺序与习惯相反）
%X	时间	时:分:秒
%c	详细日期时间	
date1 = xlrd.xldate.xldate_as_datetime(t1,0)
print(date1,date1.strftime("%Y/%m/%d"))

print(sheet1.row(0))
print(sheet1.row_types(0))
print(sheet1.row_values(0,3,6))#第一行  4-6列
print(sheet1.col_values(0,0,5))#第一列  1-5行
print(sheet1.row_slice(0,0,5))#第一行 1-5列 类型：值
print(sheet1.row_types(0,0,5))#第一行 1-5列 类型
#  空：0 ，字符串：1，  数字：2， 日期：3， 布尔：4，  error：5
#print (sheet1.row_values(0))
print (sheet1.cell_value(0,0)) #值
print (sheet1.cell(0,3).value) #值
print (sheet1.row(0)[0].value) # 值
print (sheet1.row(0)) #第一行  类型：值
print (sheet1.cell(0,0).ctype) # 类型
print (sheet1.cell_type(1,2)) #类型
print (sheet1.row(0)[1].ctype) #类型



'''
print('行:',lichxls.sheet_by_index(0).nrows)
print('列:',lichxls.sheet_by_index(0).ncols)
print(sheet1.nrows)#第一行  4-6列
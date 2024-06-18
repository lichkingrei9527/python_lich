"""
条件：
1、目前房价
2、将来房价
3、将来租金
4、目前租金
5、贷款利率
6、存款利率
7、工资收入
8、结余存款
9、房租
    租售比一般1:300为正常，即300个月回本_or_25年回本
    6000每平的售价，正常租金为20元每/平米*月
    120平，则2400元/月_28800元/年
10、现有存款
11、日常支出

本来是想自己算一下
可以做一个小程序，搞到微信或者抖音，“帮助”有需要的人
"""

lv_huoqi = 0.0035
lv_dingqi = 0.025
lv_daikuan_gjj = 0.0285
lv_daikuan_zgd = 0.036
lv_daikuan_sd = 0.4


# 房价，房屋面积，定期存款，活期存款，贷款，收入，支出
class Zichan:

    def __init__(self, fangjia, fang_mianji, dingqi, huoqi, daikuan, shouru, zhichu):
        self.fangjia = fangjia
        self.fang_mianji = fang_mianji
        self.dingqi = dingqi
        self.huoqi = huoqi
        self.daikuan = daikuan
        self.shouru = shouru
        self.zhichu = zhichu

    def showDetalis(self):
        fc = self.fangjia * self.fang_mianji
        zzc = self.fangjia * self.fang_mianji + self.huoqi + self.dingqi - self.daikuan
        print(f'当前持有资产： 房产价值：{fc} '
              f'  活期存款：{int(self.huoqi)}   定期存款(价值)：{int(self.dingqi)}   负债：{int(self.daikuan)}'
              f'  总资产 ：{int(zzc)},其中房产占比{int(fc / zzc * 100)}%  如果房价跌30%，资产为{int(self.fangjia * self.fang_mianji * 0.7 + self.huoqi + self.dingqi - self.daikuan)}')


# 每月月供额=〔贷款本金×月利率×(1+月利率)^还款月数〕÷〔(1+月利率)^还款月数-1〕
# 本金，月利率，贷款月份  return 月供 （等额本息）
def fangdaihuankuan(bj, ll, yf):
    yg = (bj * ll * (1 + ll) ** yf) / ((1 + ll) ** yf - 1)
    return yg


# 通过月供，当前本金，跑批下个月贷款剩余本金
def fd_benjin_yue(dkbj, yg):
    if dkbj <= 0:
        return 0
    lx = dkbj * lv_daikuan_gjj / 12
    ybj = yg - lx
    return dkbj - ybj


# 计算 按月还款12次，即一年后 贷款本金剩余
def fd_benjin_nian(dkbj, yg):
    if dkbj <= 0:
        # print("....")
        return 0
    # print("....xxx")
    for i in range(12):
        dkbj = fd_benjin_yue(dkbj, yg)
        # print(f'第 {i}个月，剩余本金{dkbj}')
    return dkbj


'''
房价，房屋面积，定期存款，活期存款，贷款，年收入，年支出
'''
# 20资产，买房首付20贷50，起始跑批0存50贷
fenghao_0_50 = Zichan(6200, 129, 0, 3000, 500000, 4500 * 12, 30000)
# 20资产，不买房，起始跑批20存0贷
fenghao_20_0 = Zichan(0, 0, 200000, 3000, 0, 4500 * 12, 30000)
# 40存款,买房首付20，贷50贷，起始跑批20存50贷
fenghao_20_50 = Zichan(6200, 129, 180000, 20000, 500000, 4500 * 12, 30000)


# 按年计算
def paopi(zichan, yg):
    # 年结余
    jieyu = zichan.shouru - zichan.zhichu
    if zichan.daikuan > 0:
        jieyu = jieyu - yg * 12
    # 活期跑批
    zichan.huoqi = (zichan.huoqi + jieyu) * (1 + lv_huoqi)
    if zichan.huoqi > 40000:
        zichan.dingqi = zichan.dingqi + 30000
        zichan.huoqi = zichan.huoqi - 30000
    if zichan.huoqi < 0:
        zichan.dingqi = zichan.dingqi - 20000
        zichan.huoqi = zichan.huoqi + 20000
    # 定期跑批
    if zichan.dingqi > 0:
        zichan.dingqi = zichan.dingqi * (1 + lv_dingqi)
    # 房贷跑批（年）剩余本金
    zichan.daikuan = fd_benjin_nian(zichan.daikuan, yg)
    # 房子价值
    jiazhi = zichan.fangjia * zichan.fang_mianji
    zichan.showDetalis()
    return zichan


yg_fh = fangdaihuankuan(490000, 0.0325 / 12, 240)
yg_hwm = fangdaihuankuan(500000, 0.0285 / 12, 240)

for i in range(20):
    print(f'第{i}年跑批结果：')
    print(f'20资产，买房首付20贷50，起始跑批0存50贷')
    fenghao_0_50 = paopi(fenghao_0_50, yg_fh)
    print(f'20资产，不买房，起始跑批20存0贷')
    fenghao_20_0 = paopi(fenghao_20_0, yg_fh)
    print(f'40资产,买房首付20，贷50贷，起始跑批20存50贷')
    fenghao_20_50 = paopi(fenghao_20_50, yg_fh)

'''
假设
借调结束2024.8   （31）
    处理各种杂事1个月
恋爱6个月(也可以短一点或者长一点) 2024.9-2025.5 (32)
    相处加深了解（可以的话旅游/同居(女主人心态)磨合能发现更多问题）
没大问题合适的话谈婚论嫁定日子，婚期可能在2025.5-2025.10 （32）
    准备婚纱照、嫁娶流程、婚宴、布置婚房（星辰or欣欣都行，如果是星辰那涉及装修、家具、家电、各种生活用品，装好还要通风散甲醛，
    想装一个心仪的屋子也会比较耗时间，各种选选选，我装的比较简单粗暴）、领证婚假蜜月
婚后半年到1年调养身体备孕2025.8-2026.7（33）
    身体状况好的话，孕期症状、产后恢复都很不一样的（不仅仅坐月子重要，孕前、孕期、孕后身体状况都很重要），当然也可以降低宝宝各种异常状况几率
孕期10个月2026.7-2027.4  （34 算大龄产妇吗= =）
    各种产检 
    （27年是羊年貌似不好呀= =据说容易被欺负，不过大家都这么想的话 同年出生人口少，竞争少也算好处吧
    晚一年猴宝宝挺好，可是你就35周岁36虚岁了啊= =高龄产妇伤身体）
婴儿期：月嫂+家长  带孩子 2027.5-2028 （35）
    婴儿时期_产假时期（我妈人蛮好~据我推测会比我认识的大部分人婆媳关系好很多= =））
学龄前：2028-2033（40了啊= =）
    双职工，只能家长带
幼儿园：2033-2036（43）   
    。。。。。。
孩子大学毕业 已退休（57）
'''

import shutil
import os
import time
import pymysql

'''
cmd 执行RePKG.exe extract 1scene.pkg 可以尝试不进行延时
1、先查询数据库 获取已操作 壁纸ID、复制后ID集合
2、获取最大ID
3、获取文件列表，遍历，不在数据库集合内文件进行copy操作，ID新增，记入新增列表      
4、新增列表写入数据库
5、新增列表执行cmd
突然不想改了。。。。。。。。
'''
db = pymysql.connect(
    host='localhost',
    user='root',
    password='lichking54321',
    port=3306,
    db='test',
    charset='utf8')

sql_creat_wallpaper = """ create table lich_wallpaper(
			id int NOT NULL AUTO_INCREMENT primary key,
			workshopID char(20),
			copyID char(20)
			)
			"""

sql_insert_lich_wallpaper = """ insert into lich_wallpaper(
		workshopID,copyID)
		values
		(%s,%s)
		"""

sql_select_wallpaper = """ select workshopID,copyID from lich_wallpaper;
"""

def creat_wallpaper_sql(creat_sql):

    cursor.execute("drop table if exists lich_wallpaper")
    try:
        cursor.execute(creat_sql)
    except:
        print("error to create_table ! ")

def inset_wallpaper(sql,wallpapers):
    try:
        for wallpaper in wallpapers:
            #print(wallpaper[0],wallpaper[1])
            cursor.execute(sql,(wallpaper[0],wallpaper[1]))
        db.commit()
    except:
        db.rollback()
        print("error to insert1 fullback! ")

def select_wallpaper(sql):
    try:
        cursor.execute(sql);
        results = cursor.fetchall();
    except:
        db.rollback()
        print("select  fullback! ")
    return  results

def make_wallpaper_list_scene(path):
    wallpaper_list = []
    files = os.listdir(path)
    i = 0
    #all_list
    for file in files:
        # print(path + '/' + file)
        path1 = path + '/' + file
        files1 = os.listdir(path1)
        for fle1 in files1:
            # print(path1 + '/' + fle1)
            if fle1 == "scene.pkg":
                i = i + 1
                path1 = path1 + '/' + fle1
                path3 = path2 + str(i) + 'scene.pkg'
                copyID = str(i) + 'scene.pkg'
                workshopID = file
                #print(workshopID,copyID)
                wpp = (workshopID,copyID)
                #print(i, path1, path3)
                # shutil.copy(path1, path3)
                wallpaper_list.append(wpp)


    return  wallpaper_list


def make_new_list(all_list,old_list):
    new_list = []
    if len(old_list)==0:
        print("空数据")
        new_list = all_list
    else:
        print("如果只看到我，说明没有新数据")
        #print(all_list[0])
        scene_all_list = []
        scene_old_list = []
        sceneID = len(old_list)
        print("当前已存在壁纸：-------" + str(sceneID))

        for all in all_list:
            scene_all_list.append(all[0])
        for old in old_list:
            scene_old_list.append(old[0])
        print("wallpaper已下载壁纸：",len(scene_all_list),scene_all_list)
        print("已解析壁纸",len(scene_old_list),scene_old_list)
        for all_sc in scene_all_list:
            if all_sc not in  scene_old_list:
                sceneID = sceneID + 1
                print("新增sceneID===" + str(sceneID))

                new_scene = (all_sc,str(sceneID)+"scene.pkg")
                print(new_scene)
                path1 = 'D:/tools/steam/steamapps/workshop/content/431960/' + new_scene[0] + "/scene.pkg"
                path2 = "D:/tools/wallpaperimgmaker/" + new_scene[1]
                print(path1,"复制到",path2)
                shutil.copy(path1,path2)
                new_list.append(new_scene)

    return new_list

def cmd_wallpaper(cmd_list):
    os.chdir("D:/tools/wallpaperimgmaker/")
    for c in cmd_list:
        print( "解析第+++++：",c)
        cmd = "RePKG.exe extract "+ c[1]
        os.system(cmd)
        #time.sleep(1)


# D:\tools\steam\steamapps\workshop\content\431960\2892998739\directories\customdirectory   目录下为直接图片 搜索了一下，改类型非常少
# D:\tools\steam\steamapps\workshop\content\431960\3003011737 为直接视频文件 搜索mp4即可筛选
path = 'D:/tools/steam/steamapps/workshop/content/431960'
path2 = "D:/tools/wallpaperimgmaker/"
cursor = db.cursor()

#获取当前全部壁纸
all_list = make_wallpaper_list_scene(path)
#第一次建表执行
#creat_wallpaper_sql(sql_creat_wallpaper)
#获取已操作列表
old_list = select_wallpaper(sql_select_wallpaper)
#遍历寻找未操作壁纸生成列表
new_list = make_new_list(all_list,old_list)
#执行cmd 拆分壁纸文件图片
cmd_wallpaper(new_list)
#将刚拆分壁纸写入数据库
inset_wallpaper(sql_insert_lich_wallpaper,new_list)



db.close()





#print(files)






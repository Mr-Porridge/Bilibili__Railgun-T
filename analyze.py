"""
    番剧数据统计 (data.py) 及数据绘制 (analyze.py)
    1.url 通过 F12 --> Network --> XHR --> stat?season_id=xxx 获取
    2.sleep time 可自定义
    3.使用挂在服务器端运行 数据保存为 txt 和 excel 两种格式方便基础用户使用
    4.客户端可以使用 analyze.py 自动通过 SFTP 下载表格使用 matplotlib 绘制图像

                                        --------- Mr.Porridge 2020.02.14
"""
import xlrd
import matplotlib.pyplot as plt
import paramiko
import time
import os
import shutil


# 打开表格
def open_excel():
    try:
        book = xlrd.open_workbook(today + ".xlsx")  # 文件名，把文件与py文件放在同一目录下
    except IOError as err1:
        print(">> Open excel file failed!", err1)
        book = None  # 找不到文件置空
    try:
        sheet = book.sheet_by_name("Sheet1")  # execl里面的worksheet1
        print(">> Open file successfully!")
        return sheet
    except IOError as err2:
        print(">> Locate worksheet in excel failed!", err2)


def get_data():
    # 第一行是标题名，对应表中的字段名所以应该从第二行开始，计算机以0开始计数，所以值row是1
    # 获取的数据类型为列表
    # 字典转列表 dict(zip(list_keys,list_values))
    sheet = open_excel()
    row_num = sheet.nrows
    # col_num = sheet.ncols
    # print(row_num, col_num)
    dic_key = {"number": [], "views": [], "danmu": [], "coins": [], "series_follow": [], "time": []}
    for row in range(1, row_num):
        row_data = sheet.row_values(row)
        dic_key["number"].append(eval(row_data[0]))
        dic_key["views"].append(eval(row_data[1]))
        dic_key["danmu"].append(eval(row_data[2]))
        dic_key["coins"].append(eval(row_data[3]))
        dic_key["series_follow"].append(eval(row_data[4]))
        dic_key["time"].append(row_data[5])
    # for key in dic_key:
    #     print(dic_key[key])
    return dic_key


def get_added(dic):
    dic_added = {"number": [], "views": [], "danmu": [], "coins": [], "series_follow": []}
    for sub in range(1, len(dic["number"])):
        dic_added["views"].append(dic["views"][sub] - dic["views"][sub - 1])
        dic_added["danmu"].append(dic["danmu"][sub] - dic["danmu"][sub - 1])
        dic_added["coins"].append(dic["coins"][sub] - dic["coins"][sub - 1])
        dic_added["series_follow"].append(dic["series_follow"][sub] - dic["series_follow"][sub - 1])
    dic_added["number"] = dic["number"][:-1]
    return dic_added


# Begin here
print()
today = time.strftime("%Y%m%d", time.localtime())

# make directory and change dir
try:
    os.mkdir(today)
except FileExistsError as err:
    print(">> Directory " + today + " has already been existed.")
    print(">> Deleting the existed %s......" % today)
    shutil.rmtree(today)
    print(">> Creating new %s......" % today)
    os.mkdir(today)
os.chdir(today)

# Connect the server
print(">> Connecting the server......")
trans = paramiko.Transport(('47.110.134.247', 22))
trans.connect(username='root', password='Sipras67905856')
sftp = paramiko.SFTPClient.from_transport(trans)

# Download files
print(">> Downloading the file......")
sftp.get('/usr/local/webserver/nginx/backend/bilibili/data.xlsx', today + '.xlsx')
sftp.close()
data = get_data()
data_added = get_added(data)

# Draw the picture
print(">> Drawing......")
fig = plt.figure(figsize=(32, 18))
info = {
    "x": "number",
    "y": ["views", "danmu", "coins", "series_follow", "views", "danmu"],
    "color": ["b", "r", "g", "c", "coral", "blueviolet"],
    "line": ["dashdot", "-", "dotted", "--", "-.", "-."],
}
for i in range(0, 6):
    plt.subplot(321 + i)
    if i < 4:
        plt.plot(data["number"], data[info["y"][i]], color=info["color"][i], linestyle=info["line"][i],
                 label=info["y"][i])
    else:
        plt.plot(data_added["number"], data_added[info["y"][i]], color=info["color"][i], linestyle=info["line"][i],
                 label=info["y"][i])
    plt.legend()
plt.savefig(today + '.png')
# plt.show()
print(">> Picture %s.png has already been saved!" % today)

# 复杂版本 已使用for循环进行优化
# plt.subplot(321)
# plt.plot(data["number"], data["views"], color='b', linestyle="dashdot", label="views")
# plt.legend()
# plt.subplot(322)
# plt.plot(data["number"], data["danmu"], color='r', linestyle="-", label="danmu")
# plt.legend()
# plt.subplot(323)
# plt.plot(data["number"], data["coins"], color='g', linestyle="dotted", label="coins")
# plt.legend()
# plt.subplot(324)
# plt.plot(data["number"], data["series_follow"], color='c', linestyle="--", label="series_follow")
# plt.legend()
# plt.subplot(325)
# plt.plot(data_added["number"], data_added["views"], color='coral', linestyle="-.", label="views_added")
# plt.legend()
# plt.subplot(326)
# plt.plot(data_added["number"], data_added["danmu"], color='blueviolet', linestyle="-.", label="danmu_added")
# plt.legend()
# plt.savefig(today + '.png')
# plt.show()
# print(">> Picture has already been saved!")

# plt.plot(data["number"][-24:], data[info["y"][0]][-24:])

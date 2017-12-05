# coding:utf-8

import MySQLdb
import time
import os
import glob

db = MySQLdb.connect("127.0.0.1", "root", "root", "test")
cur = db.cursor()

# each item of file_list is a file name, not absolute path!!
file_list = [item for item in os.listdir(r'C:\Users\Benny\PycharmProjects\mission-1') if 'csv' in item]

for i in range(len(file_list)):
    file1 = open(file_list[i], 'r')
    time_tuple = time.strptime(file1.name[22:40], '%b_%d_%Y_%H%M%S')
    fn = file1.name[11:21]
    dt = time.strftime('%Y-%m-%d %H:%M:%S', time_tuple)
    # read all lines
    temp = []
    while True:
        line = file1.readline()
        temp.append(line)
        if len(line) == 0:
            break

    for i in range(len(temp)):
        if 'Node' in temp[i]:
            node_name = temp[i][8:16]

        if '776' in temp[i]:
            # print temp[i - 1][31:34] + ' ' + temp[i].split()[1] + ' ' + temp[i].split()[3]
            sql_str = "insert into table1 VALUES (NULL ," + \
                      "'" + fn + "'," + \
                      "'" + temp[i].split()[1] + "'," + \
                      "'" + node_name + "'," + \
                      "'" + temp[i - 1][31:34] + "'," + \
                      "'" + temp[i].split()[3] + "','" + \
                      dt + "')"
            # execute sql command
            cur.execute(sql_str)

        elif '777' in temp[i]:
            # print temp[i - 2][31:34] + ' ' + temp[i].split()[1] + ' ' + temp[i].split()[3]
            sql_str = "insert into table1 VALUES (NULL ," + \
                      "'" + fn + "'," + \
                      "'" + temp[i].split()[1] + "'," + \
                      "'" + node_name + "'," + \
                      "'" + temp[i - 2][31:34] + "'," + \
                      "'" + temp[i].split()[3] + "','" + \
                      dt + "')"
            cur.execute(sql_str)
        elif '778' in temp[i]:
            # print temp[i - 3][31:34] + ' ' + temp[i].split()[1] + ' ' + temp[i].split()[3]
            sql_str = "insert into table1 VALUES (NULL ," + \
                      "'" + fn + "'," + \
                      "'" + temp[i].split()[1] + "'," + \
                      "'" + node_name + "'," + \
                      "'" + temp[i - 3][31:34] + "'," + \
                      "'" + temp[i].split()[3] + "','" + \
                      dt + "')"
            cur.execute(sql_str)
    file1.close()
db.commit()
db.close()

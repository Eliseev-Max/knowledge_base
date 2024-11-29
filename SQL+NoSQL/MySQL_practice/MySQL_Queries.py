#-*- coding: utf-8 -*-
import MySQLdb
con = MySQLdb.connect(user = "root", passwd = "123qaz", charset = "utf8", db = "shop")
con.autocommit(True)
cur = con.cursor()
#query_1 = """INSERT INTO `brands` (`id`,`brand`) VALUES ("1","Marc O\'Polo");"""
#query_2 = """INSERT INTO `brands` (`brand`) VALUES ("ALCOTT");"""
#query_3 = """INSERT INTO `brands` (`brand`) VALUES ("GUESS");"""
#query_4 = """INSERT INTO `brands` (`brand`) VALUES ("Calvin Klein");"""
query = """DELETE FROM `brands` WHERE `id` >1; """
try:
    cur.execute("SET NAMES utf8")
    cur.execute(query)
except MySQLdb.DatabaseError as err:
    print("Ошибка: ", err)
else:
    print("Запрос успешно выполнен")
cur.close()
con.close()
input()
    
    

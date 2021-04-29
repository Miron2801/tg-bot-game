import json
import staff_functions
import pymysql
import time

secrets = staff_functions.load_json("/secrets.json")
mysql_user                 = "miron_root"
mysql_pass				   = secrets["mysql_pass"]
class board:
        def __init__(self):
            pass
        def get_info(self, position):
                con = pymysql.connect('localhost', mysql_user, mysql_pass, 'tg_bot', autocommit=True)
                cur = con.cursor()
                cur.execute("SELECT * FROM `board` WHERE `position` = "+str(position))
                rows = cur.fetchall()
                return rows[0]
                
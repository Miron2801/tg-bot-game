import json
import staff_functions
import pymysql
import time

secrets = staff_functions.load_json("/secrets.json")
mysql_user                 = "miron_root"
mysql_pass				   = secrets["mysql_pass"]
class user:
        def __init__(self, chat_id, current_step, lives, last_time_write, payment, name, stage):
                self.stage          =       stage
                self.chat_id        =       chat_id
                self.current_step   =       current_step
                self.lives          =       lives
                self.payment        =       payment
                self.last_time_write=       last_time_write
                self.name           =       name
        def sync(self):
                con = pymysql.connect('localhost', mysql_user, mysql_pass, 'tg_bot', autocommit=True)
                cur = con.cursor()
                cur.execute("UPDATE `users` SET"+ 
                            "`chat_id` = '"              +str(self.chat_id)+"',"+
                            "`current_step` = "          +str(self.current_step )+","+
                            "`lives` = "                 +str(self.lives )+","+
                            "`last_time_write` = '"      +str(self.last_time_write)+"',"+
                            "`payment` = "               +str(self.payment)+","+
                            "`name` = '"                 +str(self.name )+"',"+
                            "`stage` = "                 +str(self.stage)+

                            " WHERE `users`.`chat_id` = "+str(self.chat_id)+";")
        def new_user(self):
                pass
        def echo_user(self):
                print("|", 
                           self.stage,          "|",
                           self.chat_id,        "|",
                           self.current_step,   "|", 
                           self.lives,          "|", 
                           self.payment,        "|", 
                           self.last_time_write,"|",
                           self.name,           "|"
                    )
        def get_user_query(self):
            try:
                return staff_functions.load_json("users/user_"+str(self.chat_id)+".json")["query"]   
            except FileNotFoundError:
                return
        def set_user_query(self, text):
            try:
                to_write = {
                            "user_id" : self.chat_id, 
                            "query"   : text,
                            }
                staff_functions.make_json("users/user_"+str(self.chat_id)+".json", to_write)
                return
            except FileExistsError:
                return
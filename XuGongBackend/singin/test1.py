
student_id = 20090102139
sing_id = 20221021001


from database import DataBase




db = DataBase.MySql()


import datetime
# aaa = str(datetime.datetime.now())[:19]
aaa = str(datetime.datetime.now())[:19]

sql_string = f"# update xugong.StudentSingInfo set SingTime='{aaa}' where SingID={sing_id} and ID={student_id}"
# sql_string = f"# select * from xugong.StudentSingInfo where SingID={sing_id} and ID={student_id}"

print(sql_string)
nihao = db.execute(sql_string)
print(nihao)


import pymysql

conn = pymysql.connect(host='localhost',
                     user='root',
                     password='dydyahd654!',
                     db='mydb',
                     charset='utf8')

cursor = conn.cursor()

# user update
#sql = "insert into user(email, name) values ('askjmyyyojqa@naver.com', '최현중')"
#cursor.execute(sql)
#sql = "insert into user(email, name) values ('ys.mun@wonderwall.kr', '문영선')"
#sql = "insert into user(email, name) values ('Jieun.yoo@wonderwall.kr', '유지은')"

sql = "ALTER TABLE `mydb`.`sunny` ADD COLUMN `interviewer` varchar(40) AFTER `record`"

cursor.execute(sql)
conn.commit()

conn.close()

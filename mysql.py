import pymysql

conn = pymysql.connect(host='localhost',
                     user='root',
                     password='dydyahd654!',
                     db='mydb',
                     charset='utf8')

cursor = conn.cursor()

# create table
user = {
    "email" : "varchar(40) not null primary key",
    "name"  : "varchar(40) not null"
}

variables = {
    # col : options
    "record" : "int not null primary key",
    "status" : "varchar(40) not null default 'incomplete'",
    "answerdate" : "varchar(40)",
    "pname": "varchar(40)",
    "position" : "int",
    "career" : "int",
    "gender" : "int",
    "age" : "int",
    "work": "int",
    "chk_point1" : "varchar(40)",
    "chk_point2" : "varchar(40)",
    "chk_point3" : "varchar(40)",
}
# for Q1 ~ Q3
for i in [1,2,3] :
    for j in [1,2,3,4,5] :
        qid = "Q%s_%s"%(i,j)
        variables[qid] = "int"

variables['total'] = 'int'
variables['comment'] = 'varchar(40)'
variables['pass'] = "varchar(40) default '보류'"

print(variables)

# sunny table
sets = ["%s %s"%(col, option) for col, option in variables.items()]

sql ="""create table sunny(
%s
);"""%(",\n".join(sets))

cursor.execute(sql)
conn.commit()

# user table
sets = ["%s %s"%(col, option) for col, option in user.items()]

sql ="""create table user(
%s
);"""%(",\n".join(sets))

cursor.execute(sql)
conn.commit()

# user update
sql = "insert into user(email, name) values ('dlcks17@naver.com', '이찬')"
cursor.execute(sql)
conn.commit()

conn.close()

from dbconn import Database

class CRUD(Database) :
    def insertDB(self, table, colum, data):
        sql = f"insert into {table}({colum}) values ('{data}') ;"
        try :
            self.execute(sql)
            self.commit()
        except Exception as e:
            print("Insert DB err", e)

    def readDB(self, table, colum):
        sql = f"select {colum} from {table};"
        try:
            self.execute(sql)
            result = self.fetchall()
        except Exception as e:
            result = ("read DB err", e)

        return result

    def updateDB(self,table,colum,value,condition):
        sql = f"update {table} set {colum}='{value}' where {condition}"
        try :
            self.execute(sql)
            self.commit()
        except Exception as e :
            print(" update DB err",e)

    def deleteDB(self,table,condition):
        sql = f"delete from {table} where {condition} ; "
        try :
            self.execute(sql)
            self.commit()
        except Exception as e:
            print( "delete DB err", e)
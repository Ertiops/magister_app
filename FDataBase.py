import sqlite3

class FDataBase:
    def __init__(self, db):
        self.__db = db
        self.__cur = db.cursor()



    def getTopicData(self, category_type):
        try:
            self.__cur.execute(f"SELECT text, category, datetime FROM texts WHERE category_type LIKE '{category_type}' ORDER BY datetime DESC")
            res = self.__cur.fetchall()
            if res:
                return res
            else:
                return None
        except sqlite3.Error as e:
            print("Ошибка получения текстов из БД" + str(e))
        return None
    
    def addData(self, text, category_type, category, datetime):
        try:
            self.__cur.execute("INSERT INTO texts VALUES (?, ?, ?, ?)", (text, category_type, category, datetime))
            self.__db.commit()
            return True
        except sqlite3.Error as e:
            print("Ошибка добавления текста в БД " + str(e))
            return False

    def deleteText(self, datetime):
        try:
            self.__cur.execute(f"DELETE FROM texts WHERE datetime = '{datetime}'")
            self.__db.commit()
            return True
        except sqlite3.Error as e:
            print("Ошибка удаления текста из БД " + str(e))
            return False
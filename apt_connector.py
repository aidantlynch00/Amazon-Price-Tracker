import mysql.connector
import datetime

class APT_Connector:

    def __init__(self, db_name):
        self.db_name = db_name

        config = {
            "user" : "root",
            "password" : "lego4atl",
            "host" : "localhost",
            "database" : "amazon_price_tracker",
            "raise_on_warnings" : True
        }

        try:
            self.db = mysql.connector.connect(**config)
            self.cursor = self.db.cursor()
        except mysql.connector.Error as err:
            print(err)

            

    def create_table(self, table_name):
        if self.table_exists(table_name):
            return

        query = (
            "CREATE TABLE `" + table_name + "` ("
            "   `date_pulled` DATE,"
            "   `price` double,"
            "   `available` boolean)" 
        )

        self.cursor.execute(query)



    def delete_table(self, table_name):
        if not self.table_exists(table_name):
            return

        query = (
            "DROP TABLE `" + table_name + "`"
        )

        self.cursor.execute(query)



    def add_data(self, table_name, price, available):
        if not self.table_exists(table_name):
            return

        query = (
            "INSERT INTO `" + table_name + "`"
            "(date_pulled, price, available)"
            "VALUES (%s, %s, %s)"
        )

        date = datetime.date.today()
        data = (date, price, available)

        self.cursor.execute(query, data)



    def get_data(self, table_name):
        query = (
            "SELECT * FROM `" + table_name + "`"
        )

        self.cursor.execute(query)
        result = self.cursor.fetchall()
        return result



    def table_exists(self, table_name):
        query = (
            "SHOW TABLES LIKE '%" + table_name + "%'"
        )

        self.cursor.execute(query)
        result = self.cursor.fetchone()
        return True if result else False

    def list_tables(self):
        query = (
            "SHOW TABLES"
        )

        self.cursor.execute(query)
        iterator = self.cursor.fetchall()

        table_list = [i[0] for i in iterator]
        return table_list



    def close(self):
        if self.db.is_connected():
            self.db.commit()
            self.cursor.close()
            self.db.close()
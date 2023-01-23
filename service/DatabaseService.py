import mysql.connector
import os

from entity.enums.TableEnum import TableEnum
from utility.debug import debug


class DatabaseService:
    def __init__(self):
        self.database = mysql.connector.connect(
            host=os.getenv("DATABASE_HOST"),
            user=os.getenv("DATABASE_USER"),
            password=os.getenv("DATABASE_PASSWORD"),
            database=os.getenv("DATABASE_NAME")
        )

        self.init_database()

    def init_database(self):
        cursor = self.database.cursor()

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS game (
                id INT AUTO_INCREMENT PRIMARY KEY,
                name VARCHAR(255) NOT NULL,
                UNIQUE (name)
            )
        """)

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS instant_gaming (
                id INT AUTO_INCREMENT PRIMARY KEY,
                game INT NOT NULL,
                default_price VARCHAR(15) NOT NULL,
                discount_price VARCHAR(15),
                in_stock VARCHAR(20),
                date_updated DATETIME,
                CONSTRAINT pk_game_ig FOREIGN KEY (game) REFERENCES game(id) ON DELETE CASCADE
            )
        """)

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS steam (
                id INT AUTO_INCREMENT PRIMARY KEY,
                game INT NOT NULL,
                default_price VARCHAR(15) NOT NULL,
                discount_price VARCHAR(15),
                date_updated DATETIME,
                CONSTRAINT pk_game_steam FOREIGN KEY (game) REFERENCES game(id) ON DELETE CASCADE
            )
        """)

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS user_alert_reduction_game (
                game INT NOT NULL,
                user VARCHAR(25) NOT NULL,
                
                CONSTRAINT pk_game_alert FOREIGN KEY (game) REFERENCES game(id) ON DELETE CASCADE
            )
        """)

    def insert_into(self, name_table, values):
        cursor = self.database.cursor()
        columns = list(values.keys())

        sql_request = "INSERT INTO {} ({}) VALUES ({})".format(
            name_table,
            ','.join(columns),
            ','.join(["%s" for _column in columns])
        )

        try:
            cursor.execute(sql_request, tuple(values.values()))

            id_game = cursor.lastrowid
            self.database.commit()

            cursor.close()
            return id_game
        except Exception:
            cursor.close()
            return -1

    def delete(self, name_table: TableEnum, conditions, is_unique_delete=True):
        cursor = self.database.cursor()
        sql_request = "DELETE FROM {}".format(name_table.value)

        try:
            conditions_list = []
            values = []

            for condition in conditions:
                column, operator, value = condition
                values.append(value)
                conditions_list.append("{} {} %s".format(column, operator))

            if len(conditions) != 0:
                sql_request += " WHERE {}".format(" AND ".join(conditions_list))
                cursor.execute(sql_request, tuple(values))
                debug("Demande de suppression, requête : {}.\nValeurs : {}".format(sql_request, values))
            else:
                cursor.execute(sql_request)
                debug("Demande de suppression, requête : {}".format(sql_request))

            self.database.commit()
            error = False
        except Exception:
            error = True

        cursor.close()

        return error

    def specific_select_request(self, request: str):
        cursor = self.database.cursor()
        cursor.execute(request)
        results = cursor.fetchall()
        cursor.close()

        return results

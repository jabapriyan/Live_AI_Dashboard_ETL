

import mysql.connector as sql
from mysql.connector import Error
from config import HOST,USER,PASSWORD,DATABASE
from utils.logger import logger
def get_connection():
    try:
        connection= sql.connect(host=HOST,
                     user=USER,
                     password=PASSWORD,
                     database=DATABASE)
        logger.info("database connected successfully")

        return connection
    except Error as e:
        logger.error(f"Database connected failed:{e}")

        return None
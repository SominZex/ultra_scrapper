import pymysql

def get_connection():
    connection = pymysql.connect(
        host='--hostname--',
        user='--put your username-',
        password='- your password-',
        database='web_scraping_db'
    )
    return connection

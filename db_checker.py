from sshtunnel import SSHTunnelForwarder
import pymysql

# Параметры SSH
SSH_HOST = "127.0.0.1"
SSH_PORT = 2222
SSH_USER = "vagrant"

# Параметры MySQL (как видно ИЗНУТРИ сервера, к которому подключаемся по SSH)
MYSQL_HOST = "127.0.0.1"        # обычно localhost на стороне сервера
MYSQL_PORT = 3306
MYSQL_USER = "root"
MYSQL_PASSWORD = "root"
MYSQL_DB = "cs_std131001"

def check_order(order_number):
    with SSHTunnelForwarder(
        (SSH_HOST, SSH_PORT),
        ssh_username=SSH_USER,
        remote_bind_address=(MYSQL_HOST, MYSQL_PORT),
        ssh_pkey="C:/PRO/box/.vagrant/machines/default/virtualbox/private_key"
    ) as tunnel:

        connection = pymysql.connect(
            host="127.0.0.1",
            port=tunnel.local_bind_port,   # локальный порт, который создал туннель
            user=MYSQL_USER,
            password=MYSQL_PASSWORD,
            database=MYSQL_DB,
            cursorclass=pymysql.cursors.DictCursor
        )

        try:
            with connection.cursor() as cursor:
                sql = "SELECT * FROM shopauftraege WHERE auftragsnr = %s"
                cursor.execute(sql, order_number)
                result = cursor.fetchone()
                print(result)
        finally:
            connection.close()

    return result


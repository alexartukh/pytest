import os
from sshtunnel import SSHTunnelForwarder
import pymysql

# Connection settings are read from environment variables (see README).
# No passwords or key paths are stored in the repository.
SSH_HOST = os.environ.get("SSH_HOST", "127.0.0.1")
SSH_PORT = int(os.environ.get("SSH_PORT", "2222"))
SSH_USER = os.environ.get("SSH_USER", "vagrant")
SSH_KEY_PATH = os.environ.get("SSH_KEY_PATH")        # path to the private key of the Vagrant VM

# MySQL as seen from inside the SSH server
MYSQL_HOST = os.environ.get("DB_HOST", "127.0.0.1")
MYSQL_PORT = int(os.environ.get("DB_PORT", "3306"))
MYSQL_USER = os.environ.get("DB_USER")
MYSQL_PASSWORD = os.environ.get("DB_PASSWORD")
MYSQL_DB = os.environ.get("DB_NAME")

def check_order(order_number):
    with SSHTunnelForwarder(
        (SSH_HOST, SSH_PORT),
        ssh_username=SSH_USER,
        remote_bind_address=(MYSQL_HOST, MYSQL_PORT),
        ssh_pkey=SSH_KEY_PATH
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


import os

mysql_host = os.environ.get('MYSQL_HOST', '127.0.0.1')
mysql_pwd = os.environ.get('MYSQL_PASSWORD', 'root')
mysql_user = os.environ.get('MYSQL_USER', 'root')
mysql_db = os.environ.get('MYSQL_DB', 'flask_test')
mysql_port = os.environ.get('MYSQL_PORT', 3306)

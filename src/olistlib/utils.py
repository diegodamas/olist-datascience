import os
import sqlalchemy
import dotenv
from tqdm import tqdm
import pandas as pd

BASE_DIR = os.path.dirname(os.path.dirname( os.path.abspath(__file__) ) )
DATA_DIR = os.path.join(BASE_DIR, 'data')

#Function connect db
def connect_db(db_name, dotenv_path = os.path.expanduser("~/.env"), **kwargs):

    dotenv.load_dotenv(dotenv_path)

    host = os.getenv("HOST_" + db_name.upper())
    port = os.getenv("PORT_" + db_name.upper())
    user = os.getenv("USER_" + db_name.upper())
    pswd = os.getenv("PSWD_" + db_name.upper())

    if(db_name == 'mariadb' or db_name == 'mysql'):
        str_connection = f"mysql+pymysql://{user}:{pswd}@{host}:{port}"

    elif db_name == 'oracle':
        str_connection = f"oracle://{user}:{pswd}@{host}:{port}"

    elif db_name == 'sqlite':
        str_connection = f"sqlite:///{kwargs['path']}"

    return sqlalchemy.create_engine(str_connection)

def import_query(path, **kwargs):
    with open(path, 'r', **kwargs) as file_query:
        query = file_query.read()
    return query

def execute_many_sql(sql, conn, verbose=False):
    if verbose:
        for i in tqdm(sql.split(";")[:-1]):
            conn.execute(i)
    else:
        for i in sql.split(";")[:-1]:
            conn.execute(i)

    



    



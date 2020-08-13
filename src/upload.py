import os
import pandas as pd
import sqlalchemy
import argparse

from olistlib import utils

parse = argparse.ArgumentParser()
parse.add_argument("--database", help='DB name', choices=['mariadb', 'mysql', 'oracle', 'sqlite'], default='mysql')
args = parse.parse_args()

#Folders path
BASE_DIR = os.path.dirname(os.path.dirname( os.path.abspath(__file__) ) )
DATA_DIR = os.path.join(BASE_DIR, 'data')
DOTENV_DIR = os.path.join(BASE_DIR, 'src')


#List comprehension data names
file_names = [val for val in os.listdir(DATA_DIR) if val.endswith('.csv')]

#Database connection from utils
con = utils.connect_db(args.database, dotenv_path = os.path.join(DOTENV_DIR, '.env'), path=os.path.join(DATA_DIR, 'olist.db'))

for i in file_names:
    print(i)
    df_temp = pd.read_csv(os.path.join(DATA_DIR, i))
    table_name = "tb_" + i.strip(".csv").replace("olist_", "").replace("_dataset", "")

    if(args.database == "sqlite"):

        df_temp.to_sql(table_name, con, if_exists='replace', index=False )

    else:

        df_temp.to_sql(table_name, con, schema='olist', if_exists='replace', index=False )




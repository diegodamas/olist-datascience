import pandas as pd
import os
from olistlib import utils
import sqlalchemy
import argparse
import datetime
from dateutil.relativedelta import relativedelta

parser = argparse.ArgumentParser()
parser.add_argument("--date_init", '-i', help='ABT start date')
parser.add_argument("--date_end", '-e', help='ABT end date')
parser.add_argument("--database", help='DB name', choices=['mariadb', 'mysql', 'oracle', 'sqlite'], default='mysql')
parser.add_argument("--save_db", '-d', help='Do you want to save the database?', action='store_true')
parser.add_argument("--save_file", '-f', help='Do you want to save to a file?', action='store_true')
args = parser.parse_args()

TRAIN_DIR = os.path.dirname(os.path.abspath( __file__ ))
DATA_PREP = os.path.join(os.path.dirname(TRAIN_DIR), 'data_prep')
SRC_DIR = os.path.dirname(os.path.dirname( os.path.abspath(__file__)))
BASE_DIR = os.path.dirname(SRC_DIR)
DATA_DIR = os.path.join(BASE_DIR, 'data')

OUT_DATA_DIR = os.path.join(BASE_DIR, "upload_olist")
DB_PATH = os.path.join( OUT_DATA_DIR, "olist.db")


date = datetime.datetime.strptime(args.date_init, "%Y-%m-%d")
date_end = datetime.datetime.strptime(args.date_end, "%Y-%m-%d")
dates = []
while  date <= date_end:
    dates.append(date.strftime( "%Y-%m-%d" ))
    date += relativedelta( months = 1 )

print("\n Connecting DB...")

con = utils.connect_db(args.database, dotenv_path = os.path.join(SRC_DIR, '.env'), path=DB_PATH)
print(" Ok.")

print("\n Extracting data...")

# Query features
query_etl_base = utils.import_query(os.path.join(DATA_PREP, 'etl.sql'))

# Query abt_base
query_abt_base = utils.import_query(os.path.join(DATA_PREP, 'abt.sql'))

dfs = []
for d in dates:

    query_etl = query_etl_base.format(date=d, stage="TRAIN")
    query_abt = query_abt_base.format(date=d)

    utils.execute_many_sql(query_etl, con)
    dfs.append(pd.read_sql_query(query_abt, con))

df = pd.concat(dfs, axis=0, ignore_index=True)
print("Ok")

if args.save_db:

    print("\n Saving data in DB...")

    table_name = 'tb_abt_{date_init}_{date_end}'.format(date_init = args.date_init.replace( "-", ""), date_end = args.date_end.replace( "-", ""))
    df.to_sql(table_name, con, index=False, if_exists='replace')
    print("Ok")

if args.save_file:

    print("\n Saving data in file...")

    table_name = 'tb_abt_{date_init}_{date_end}.csv'.format( date_init = args.date_init.replace( "-", ""), date_end = args.date_end.replace( "-", ""))
    df.to_csv(os.path.join( DATA_DIR, table_name), index=False)
    print("Ok")
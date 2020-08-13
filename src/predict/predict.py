import pandas as pd
import os
import shutil
from olistlib import utils
import argparse
import datetime
from dateutil.relativedelta import relativedelta
from sklearn import tree

parser = argparse.ArgumentParser()
parser.add_argument("--date", '-d', help='ABT start date')
parser.add_argument("--export", help="Export type", choices=['csv', 'sqlite'])
parser.add_argument("--database", help='DB Name', choices=['mariadb', 'mysql', 'oracle', 'sqlite'], default='mysql')
args = parser.parse_args()

SRC_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BASE_DIR = os.path.dirname(SRC_DIR)
DATA_PREP = os.path.join(SRC_DIR, 'data_prep')
TRAIN_DIR = os.path.join(SRC_DIR, 'train')
TRAIN_DIR = os.path.join(SRC_DIR, 'predict')
DATA_DIR = os.path.join(BASE_DIR, 'data')
MODELS_DIR = os.path.join(BASE_DIR, 'models')

#Dir sqlite
OUT_BASE_DIR = os.path.dirname(BASE_DIR)
OUT_DATA_DIR = os.path.join(OUT_BASE_DIR, "upload_olist", 'data')
DB_PATH = os.path.join(OUT_DATA_DIR, "olist.db")

model = pd.read_pickle( os.path.join(MODELS_DIR, 'model.pkl'))
print("Imported model")

query = utils.import_query(os.path.join(DATA_PREP, 'etl.sql'))
con = utils.connect_db(args.database, dotenv_path = os.path.join(SRC_DIR, '.env'), path=DB_PATH)
print("Ok")

query = query.format(date=args.date, stage='PREDICT')
utils.execute_many_sql(query, con)

df = pd.read_sql_table('PRE_ABT_PREDICT_CHURN', con)

print("\n Predicting...")
df['churn_prob'] = model['model'].predict_proba( df[ model['features'] ] )[:,1]


table = df[['seller_id','churn_prob']]

if args.export == 'sqlite':
    table.to_sql("tb_churn_score", con, index=False)

elif args.export == 'csv':
    table.to_csv(os.path.join(DATA_DIR, 'tb_churn_score.csv'), index=False)

print("Ok")

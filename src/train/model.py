import pandas as pd
import os
from olistlib import utils
import argparse
import datetime
from dateutil.relativedelta import relativedelta
from sklearn import tree

parser = argparse.ArgumentParser()
parser.add_argument("--date_init", '-i', help='ABT start date')
parser.add_argument("--date_end", '-e', help='ABT end date')
parser.add_argument("--file_type", help='Import location', choices=['csv', 'sql'])
parser.add_argument("--database", help='DB name', choices=['mariadb', 'mysql', 'oracle', 'sqlite'], default='mysql')
args = parser.parse_args()

SRC_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BASE_DIR = os.path.dirname(SRC_DIR)
TRAIN_DIR = os.path.join(SRC_DIR, 'train')
DATA_DIR = os.path.join(BASE_DIR, 'data')
MODELS_DIR = os.path.join(BASE_DIR, 'models')

#Dir sqlite
OUT_BASE_DIR = os.path.dirname(BASE_DIR)
OUT_DATA_DIR = os.path.join(OUT_BASE_DIR, "upload_olist", 'data')
DB_PATH = os.path.join(OUT_DATA_DIR, "olist.db")


if args.file_type == 'sql':

    con = utils.connect_db(args.database, dotenv_path = os.path.join(SRC_DIR, '.env'), path=DB_PATH)
    table_name = 'tb_abt_{date_init}_{date_end}'.format(date_init=args.date_init.replace("-",""), date_end=args.date_end.replace("-",""))
    df = pd.read_sql_table( table_name , con)
    print("Ok")

elif args.file_type == 'csv':
    table_name = 'tb_abt_{date_init}_{date_end}.csv'.format( date_init=args.date_init.replace("-",""), date_end=args.date_end.replace("-",""))
    df = pd.read_csv( os.path.join(DATA_DIR, table_name ))
    print("Ok")


print("\n Model...")

features = df.columns[3:-2]
target = 'flag_churn'

x = df[features]
y = df[target]

clf = tree.DecisionTreeClassifier(max_depth=8)
clf.fit(x, y)

print("\n Saving...")

model = pd.Series([features, clf], index = ['features', 'model'])
model.to_pickle(os.path.join(MODELS_DIR, 'model.pkl'))

print("\n Concluded")



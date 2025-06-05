import pandas as pd
from sqlalchemy import create_engine

df = pd.read_csv('./Dataset/data.csv', delimiter=';', index_col=False)

URL = "postgresql://postgres.eagqpykvzctmtucgodic:p1pds.dicoding@aws-0-ap-southeast-1.pooler.supabase.com:6543/postgres"
 
engine = create_engine(URL)
df.to_sql('students_performance', engine)
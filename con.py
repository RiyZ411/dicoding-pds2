from sqlalchemy import create_engine

DATABASE_URL = "postgresql://postgres.eagqpykvzctmtucgodic:p1pds.dicoding@aws-0-ap-southeast-1.pooler.supabase.com:6543/postgres"

try:
    engine = create_engine(DATABASE_URL)
    with engine.connect() as conn:
        print("Koneksi berhasil!")
except Exception as e:
    print("Gagal koneksi:", e)

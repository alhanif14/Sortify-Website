from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

DATABASE_URL = "postgresql://postgres:H140604:)@localhost:5432/sortify_db"

# ✅ Tambahkan pool settings untuk stability
engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True,
    pool_recycle=300
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# ✅ Context manager untuk database session
def get_db_session():
    """Context manager untuk database session"""
    db = SessionLocal()
    try:
        return db
    finally:
        db.close()
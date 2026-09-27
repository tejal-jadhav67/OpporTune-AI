from sqlalchemy import create_engine, inspect, text
from sqlalchemy.orm import DeclarativeBase, sessionmaker

DATABASE_URL = "sqlite:///./opportune.db"

engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False},
)

SessionLocal = sessionmaker(
    bind=engine,
    autocommit=False,
    autoflush=False,
)


class Base(DeclarativeBase):
    pass


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def create_tables():
    Base.metadata.create_all(bind=engine)

    inspector = inspect(engine)
    opportunity_columns = {
        column["name"] for column in inspector.get_columns("opportunities")
    }
    migrations = {
        "eligible_branches": "ALTER TABLE opportunities ADD COLUMN eligible_branches TEXT NOT NULL DEFAULT '[]'",
        "min_year": "ALTER TABLE opportunities ADD COLUMN min_year INTEGER",
        "max_year": "ALTER TABLE opportunities ADD COLUMN max_year INTEGER",
    }

    with engine.begin() as connection:
        for column_name, statement in migrations.items():
            if column_name not in opportunity_columns:
                connection.execute(text(statement))

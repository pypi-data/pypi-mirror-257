from sqlmodel import create_engine

SQLALCHEMY_DATABASE_URL = "sqlite:///./sql_app.db"

engine = create_engine("sqlite:///database.db")

from sqlmodel import create_engine, Session

DATABASE_URL = "sqlite:///./mem.db"
connect_args = {"check_same_thread": False}

engine = create_engine(DATABASE_URL, echo=True, connect_args=connect_args)

def get_session():
    with Session(engine) as session:
        yield session

from sqlalchemy import create_engine, Column, Integer, String, event
from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy.pool import StaticPool

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'
    __table_args__ = {'schema': 'dbo'}
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String)

engine = create_engine('sqlite:///:memory:', connect_args={'check_same_thread': False}, poolclass=StaticPool)

@event.listens_for(engine, 'connect')
def _attach_schemas(dbapi_conn, connection_record):
    cursor = dbapi_conn.cursor()
    cursor.execute("ATTACH DATABASE ':memory:' AS \"dbo\"")
    cursor.close()

Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()

u = User(name='test')
# Do not add or commit
try:
    session.refresh(u)
except Exception as e:
    print(f"Error: {type(e).__name__}: {e}")
